"""S5B-1A P1-C1-S1 minimal drills runner.

Goal (v1): provide a repeatable runner that:
- calls API with AuthContext (JWT) + tenant header
- captures request_id from responses
- queries audit_log by request_id
- writes machine-verifiable artifacts in the S5B-1A contract layout

This script intentionally starts with ONE minimal case to validate end-to-end wiring.
More scenarios will be added in P2/P3.

Prereqs:
- API is running (WORDLOOM_API_BASE_URL)
- DB is reachable (DATABASE_URL)
- JWT secret/alg are configured (WORDLOOM_JWT_SECRET_KEY/WORDLOOM_JWT_ALG)

Run:
  python scripts/drills/s5b1a_p1c1s1_drills_runner.py

Windows note:
- psycopg async cannot run on ProactorEventLoop (Windows default).
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import subprocess
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from urllib.parse import urlsplit, urlunsplit

import httpx
import jwt
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


@dataclass(frozen=True)
class RunnerConfig:
    api_base_url: str
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str
    suite_id: str


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _convert_to_psycopg(url: str) -> str:
    if url.startswith("postgresql+psycopg://"):
        return url
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql+asyncpg://"):
        return url.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql+"):
        parts = url.split("://", 1)
        if len(parts) == 2:
            return f"postgresql+psycopg://{parts[1]}"
    return url


def _redact_url_password(url: str) -> str:
    try:
        parts = urlsplit(url)
        if not parts.username or parts.password is None:
            return url
        netloc = parts.netloc
        # Replace :password@ with :***@
        netloc = re.sub(r":([^@]+)@", r":***@", netloc, count=1)
        return urlunsplit((parts.scheme, netloc, parts.path, parts.query, parts.fragment))
    except Exception:
        return url


def _get_git_sha() -> Optional[str]:
    sha = os.getenv("GITHUB_SHA")
    if sha and sha.strip():
        return sha.strip()
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL)
        return out.decode("utf-8").strip()
    except Exception:
        return None


def _make_token(*, user_id: uuid.UUID, secret_key: str, algorithm: str) -> str:
    payload = {
        "user_id": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    return jwt.encode(payload, secret_key, algorithm=algorithm)


async def _fetch_audit_rows(*, engine, request_id: str) -> list[dict[str, Any]]:
    sql = text(
        """
        SELECT
          occurred_at,
          tenant_id,
          actor_user_id,
          request_id,
          action,
          resource_type,
          resource_id,
          result,
          reason,
          meta_json
        FROM audit_log
        WHERE request_id = :request_id
        ORDER BY occurred_at ASC
        """
    )
    async with engine.connect() as conn:
        rows = (await conn.execute(sql, {"request_id": request_id})).mappings().all()

    out: list[dict[str, Any]] = []
    for r in rows:
        d = dict(r)
        if d.get("occurred_at") is not None:
            d["occurred_at"] = d["occurred_at"].isoformat()
        for k in ("tenant_id", "actor_user_id", "resource_id"):
            if d.get(k) is not None:
                d[k] = str(d[k])
        out.append(d)
    return out


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _write_json(path: str, obj: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _write_text(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _try_json(r: httpx.Response) -> Any:
    try:
        if (r.headers.get("content-type") or "").startswith("application/json"):
            return r.json()
    except Exception:
        return None
    return None


def _require_status(r: httpx.Response, *, ok_statuses: set[int], label: str, log_lines: list[str]) -> None:
    if r.status_code in ok_statuses:
        return
    body = _try_json(r)
    if body is None:
        body = (r.text or "").strip()
    log_lines.append(f"http_error:{label}:status={r.status_code}")
    log_lines.append(f"http_error:{label}:body={body}")
    raise RuntimeError(f"http_error:{label}:{r.status_code}")


def _require_id(obj: Any, *, label: str, log_lines: list[str]) -> str:
    if isinstance(obj, dict) and isinstance(obj.get("id"), str) and obj.get("id"):
        return obj["id"]
    log_lines.append(f"schema_error:{label}:missing_id")
    log_lines.append(f"schema_error:{label}:body={obj}")
    raise RuntimeError(f"schema_error:{label}:missing_id")


def _pick_failure_reason(*, expected: dict[str, Any], observed: dict[str, Any]) -> str:
    if expected.get("http_status") != observed.get("http_status"):
        return "http_status_mismatch"

    exp_audit = expected.get("audit") or {}
    obs_audit_rows = ((observed.get("audit_rows") or {}).get("rows") or [])

    if expected.get("audit_expected") is True and len(obs_audit_rows) == 0:
        return "audit_missing"

    if expected.get("audit_expected") is True:
        row = None
        for r in obs_audit_rows:
            if r.get("action") == exp_audit.get("action"):
                row = r
                break
        if row is None:
            return "audit_action_mismatch"
        if row.get("result") != exp_audit.get("result"):
            return "audit_result_mismatch"
        if exp_audit.get("reason") is not None and row.get("reason") != exp_audit.get("reason"):
            return "audit_reason_mismatch"

    return "unexpected_error"


def _build_case_result(*, case_id: str, title: str, inputs: dict[str, Any], expected: dict[str, Any], observed: dict[str, Any]) -> dict[str, Any]:
    ok = True

    if expected.get("http_status") != observed.get("http_status"):
        ok = False

    if expected.get("audit_expected") is True:
        rows = ((observed.get("audit_rows") or {}).get("rows") or [])
        if len(rows) == 0:
            ok = False
        else:
            exp_audit = expected.get("audit") or {}
            matched = None
            for r in rows:
                if r.get("action") == exp_audit.get("action") and r.get("result") == exp_audit.get("result"):
                    matched = r
                    break
            if matched is None:
                ok = False
            else:
                exp_reason = exp_audit.get("reason")
                if exp_reason is not None and matched.get("reason") != exp_reason:
                    ok = False

    failure_reason: Optional[str] = None
    if not ok:
        failure_reason = _pick_failure_reason(expected=expected, observed=observed)

    return {
        "case_id": case_id,
        "title": title,
        "inputs": inputs,
        "expected": expected,
        "observed": observed,
        "verdict": {"ok": ok, "failure_reason": failure_reason},
    }


def _artifact_run_dir(*, suite_id: str, run_id: str) -> str:
    return os.path.join("docs", "labs", "_snapshot", "auto", "S5B-1A", suite_id, run_id)


async def run() -> tuple[str, dict[str, Any]]:
    cfg = RunnerConfig(
        api_base_url=os.getenv("WORDLOOM_API_BASE_URL", "http://localhost:30001").rstrip("/"),
        database_url=os.getenv("DATABASE_URL", "postgresql://postgres:pgpass@localhost:5432/wordloom"),
        jwt_secret_key=os.getenv("WORDLOOM_JWT_SECRET_KEY", "dev-secret-key-change-in-production"),
        jwt_algorithm=os.getenv("WORDLOOM_JWT_ALG", "HS256"),
        suite_id=os.getenv("S5B_1A_SUITE_ID", "tenant_escape_read"),
    )

    git_sha = _get_git_sha()
    run_id = str(uuid.uuid4())

    run_dir = _artifact_run_dir(suite_id=cfg.suite_id, run_id=run_id)
    logs_dir = os.path.join(run_dir, "_logs")
    metrics_dir = os.path.join(run_dir, "_metrics")
    _ensure_dir(logs_dir)
    _ensure_dir(metrics_dir)

    t0 = time.time()
    started_at = _now_iso()

    log_lines: list[str] = []
    log_lines.append(f"started_at={started_at}")
    log_lines.append(f"run_id={run_id}")
    log_lines.append(f"suite_id={cfg.suite_id}")
    log_lines.append(f"api_base_url={cfg.api_base_url}")
    log_lines.append(f"database_url={_redact_url_password(cfg.database_url)}")
    if git_sha:
        log_lines.append(f"git_sha={git_sha}")

    recipe = {
        "schema_version": "s5b-1a.recipe.v1",
        "meta": {
            "run_id": run_id,
            "suite_id": cfg.suite_id,
            "started_at": started_at,
            "git_sha": git_sha,
        },
        "config": {
            "api_base_url": cfg.api_base_url,
            "database_url_redacted": _redact_url_password(cfg.database_url),
            "jwt_algorithm": cfg.jwt_algorithm,
        },
        "cases": [
            {
                "case_id": "tenant_cross_read_404",
                "title": "cross-tenant read is rejected (404 + audit not_found + reason=tenant_mismatch)",
                "endpoint": {"method": "GET", "path_template": "/api/v1/bookshelves/{bookshelf_id}"},
            }
        ],
    }

    engine = create_async_engine(_convert_to_psycopg(cfg.database_url), echo=False)

    case_results: list[dict[str, Any]] = []

    try:
        # NOTE: Current backend dev mode uses a fixed user id in some flows.
        # Keep actor stable and configurable so drills are repeatable.
        user_id = uuid.UUID(os.getenv("S5B_1A_ACTOR_USER_ID", "550e8400-e29b-41d4-a716-446655440000"))
        token = _make_token(user_id=user_id, secret_key=cfg.jwt_secret_key, algorithm=cfg.jwt_algorithm)

        async with httpx.AsyncClient(base_url=cfg.api_base_url, timeout=30.0) as client:
            auth_headers = {"Authorization": f"Bearer {token}"}

            # Setup: create 2 libraries + 1 bookshelf in lib_a
            lib_a_name = f"s5b1a-lib-a-{run_id[:8]}"
            lib_b_name = f"s5b1a-lib-b-{run_id[:8]}"

            r_lib_a = await client.post("/api/v1/libraries", json={"name": lib_a_name, "description": "drill"}, headers=auth_headers)
            r_lib_b = await client.post("/api/v1/libraries", json={"name": lib_b_name, "description": "drill"}, headers=auth_headers)

            _require_status(r_lib_a, ok_statuses={200, 201}, label="create_library_a", log_lines=log_lines)
            _require_status(r_lib_b, ok_statuses={200, 201}, label="create_library_b", log_lines=log_lines)

            lib_a = _try_json(r_lib_a) or {}
            lib_b = _try_json(r_lib_b) or {}

            lib_a_id = _require_id(lib_a, label="create_library_a", log_lines=log_lines)
            lib_b_id = _require_id(lib_b, label="create_library_b", log_lines=log_lines)

            shelf_name = f"s5b1a-shelf-{run_id[:8]}"
            r_create = await client.post(
                "/api/v1/bookshelves",
                json={"library_id": lib_a_id, "name": shelf_name, "description": "drill"},
                headers={
                    **auth_headers,
                    "X-Library-Id": str(lib_a_id),
                },
            )
            _require_status(r_create, ok_statuses={200, 201}, label="create_bookshelf", log_lines=log_lines)
            shelf = _try_json(r_create) or {}
            shelf_id = _require_id(shelf, label="create_bookshelf", log_lines=log_lines)

            # Case: cross-tenant read
            path = f"/api/v1/bookshelves/{shelf_id}"
            r_cross = await client.get(
                path,
                headers={
                    **auth_headers,
                    "X-Library-Id": str(lib_b_id),
                },
            )
            request_id = r_cross.headers.get("X-Request-Id")

        audit_rows = await _fetch_audit_rows(engine=engine, request_id=request_id) if request_id else []

        inputs = {
            "request_id": request_id,
            "tenant_id": str(lib_b_id) if lib_b_id else None,
            "actor_user_id": str(user_id),
            "roles": ["member"],
            "http": {
                "method": "GET",
                "path": path,
                "path_template": "/api/v1/bookshelves/{bookshelf_id}",
            },
        }
        expected = {
            "http_status": 404,
            "audit_expected": True,
            "audit": {"action": "bookshelf.get", "result": "not_found", "reason": "tenant_mismatch"},
        }
        observed = {
            "http_status": int(r_cross.status_code),
            "audit_rows": {"count": len(audit_rows), "rows": audit_rows[:10]},
        }

        case_results.append(
            _build_case_result(
                case_id="tenant_cross_read_404",
                title="cross-tenant read is rejected",
                inputs=inputs,
                expected=expected,
                observed=observed,
            )
        )

    except Exception as e:
        # Keep _result.json low-cardinality; put details in logs.
        log_lines.append(f"error_type={type(e).__name__}")
        case_results.append(
            {
                "case_id": "tenant_cross_read_404",
                "title": "cross-tenant read is rejected",
                "inputs": {},
                "expected": {},
                "observed": {},
                "verdict": {"ok": False, "failure_reason": "unexpected_error"},
            }
        )

    finally:
        await engine.dispose()

    passed = sum(1 for c in case_results if (c.get("verdict") or {}).get("ok") is True)
    failed = len(case_results) - passed
    ok = failed == 0

    finished_at = _now_iso()
    duration_s = time.time() - t0

    result = {
        "schema_version": "s5b-1a.result.v1",
        "ok": ok,
        "meta": {
            "run_id": run_id,
            "suite_id": cfg.suite_id,
            "started_at": started_at,
            "finished_at": finished_at,
            "git_sha": git_sha,
        },
        "summary": {
            "total": len(case_results),
            "passed": passed,
            "failed": failed,
        },
        "cases": case_results,
    }

    # Ensure we always write non-empty artifacts.
    _write_json(os.path.join(run_dir, "_recipe.json"), recipe)
    _write_json(os.path.join(run_dir, "_result.json"), result)

    _write_text(os.path.join(logs_dir, "run.log"), "\n".join(log_lines) + "\n")

    metrics = {
        "schema_version": "s5b-1a.metrics.v1",
        "run_id": run_id,
        "suite_id": cfg.suite_id,
        "ok": ok,
        "duration_s": duration_s,
        "cases_total": len(case_results),
        "cases_passed": passed,
        "cases_failed": failed,
    }
    _write_json(os.path.join(metrics_dir, "summary.json"), metrics)

    return run_dir, result


def main() -> None:
    if os.name == "nt":
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except Exception:
            pass

    run_dir, result = asyncio.run(run())
    ok = bool(result.get("ok"))
    print(f"[{'OK' if ok else 'FAIL'}] Wrote artifacts: {run_dir}")


if __name__ == "__main__":
    main()
