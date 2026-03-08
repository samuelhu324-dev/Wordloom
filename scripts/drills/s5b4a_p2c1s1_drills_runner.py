"""S5B-4A P2-C1-S1 drills runner.

Goal (v1): exercise search query authorization & tenant isolation for
`search.blocks.two_stage` with audit coverage:
- Same-tenant authorized search → success
- Cross-tenant library_id (query) mismatch → denied/tenant_mismatch
- Non-member search → denied/not_member
- Invalid query → error/invalid_query

Artifacts contract:
- Writes S5B-1A-compatible recipe/result/metrics schemas so we can reuse the
  existing verifier.
- Output: docs/labs/_snapshot/auto/S5B-4A/<suite_id>/<run_id>/

Prereqs:
- API is running (WORDLOOM_API_BASE_URL)
- DB is reachable (DATABASE_URL)
- JWT secret/alg are configured (WORDLOOM_JWT_SECRET_KEY/WORDLOOM_JWT_ALG)

Run:
  python scripts/drills/s5b4a_p2c1s1_drills_runner.py

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
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from urllib.parse import urlencode, urlsplit, urlunsplit

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


def _artifact_run_dir(*, suite_id: str, run_id: str) -> str:
    return os.path.join("docs", "labs", "_snapshot", "auto", "S5B-4A", suite_id, run_id)


async def run() -> tuple[str, dict[str, Any]]:
    cfg = RunnerConfig(
        api_base_url=os.getenv("WORDLOOM_API_BASE_URL", "http://127.0.0.1:31001").rstrip("/"),
        database_url=os.getenv("DATABASE_URL", "postgresql://wordloom:wordloom@127.0.0.1:5435/wordloom_test"),
        jwt_secret_key=os.getenv("WORDLOOM_JWT_SECRET_KEY", "dev-secret-key-change-in-production"),
        jwt_algorithm=os.getenv("WORDLOOM_JWT_ALG", "HS256"),
        suite_id=os.getenv("S5B_4A_SUITE_ID", "search_query_authorization"),
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
                "case_id": "same_tenant_success",
                "title": "same-tenant search → success/audit success",
                "endpoint": {"method": "GET", "path_template": "/api/v1/search/blocks/two-stage"},
            },
            {
                "case_id": "cross_tenant_query_param_denied",
                "title": "cross-tenant library_id (query) → denied/tenant_mismatch",
                "endpoint": {"method": "GET", "path_template": "/api/v1/search/blocks/two-stage"},
            },
            {
                "case_id": "non_member_denied",
                "title": "non-member search → denied/not_member",
                "endpoint": {"method": "GET", "path_template": "/api/v1/search/blocks/two-stage"},
            },
            {
                "case_id": "invalid_query_error",
                "title": "invalid query → error/invalid_query",
                "endpoint": {"method": "GET", "path_template": "/api/v1/search/blocks/two-stage"},
            },
        ],
    }

    engine = create_async_engine(_convert_to_psycopg(cfg.database_url), echo=False)

    case_results: list[dict[str, Any]] = []

    # Setup actors
    user_member = uuid.uuid4()
    user_other = uuid.uuid4()

    token_member = _make_token(user_id=user_member, secret_key=cfg.jwt_secret_key, algorithm=cfg.jwt_algorithm)
    token_other = _make_token(user_id=user_other, secret_key=cfg.jwt_secret_key, algorithm=cfg.jwt_algorithm)

    lib_id: Optional[str] = None
    other_lib_id: Optional[str] = None

    try:
        async with httpx.AsyncClient(base_url=cfg.api_base_url, timeout=30.0) as client:
            # Setup: create two libraries and grant member role on the first for user_member.
            lib_name = f"s5b4a-lib-{run_id[:8]}"
            r_lib1 = await client.post("/api/v1/libraries", json={"name": lib_name, "description": "s5b4a drills lib1"})
            r_lib1.raise_for_status()
            lib1 = _try_json(r_lib1) or {}
            lib_id = (lib1 or {}).get("id")

            lib_name2 = f"s5b4a-lib-{run_id[:8]}-other"
            r_lib2 = await client.post("/api/v1/libraries", json={"name": lib_name2, "description": "s5b4a drills lib2"})
            r_lib2.raise_for_status()
            lib2 = _try_json(r_lib2) or {}
            other_lib_id = (lib2 or {}).get("id")

            # grant member on first library for user_member
            if lib_id:
                await client.post(
                    f"/api/v1/libraries/{lib_id}/memberships",
                    json={"user_id": str(user_member), "role": "member"},
                    headers={"X-Library-Id": str(lib_id)},
                )

            # Case 1: same-tenant success
            params = {"q": "test", "limit": 5}
            q_string = urlencode(params)
            path = f"/api/v1/search/blocks/two-stage?{q_string}"
            r1 = await client.get(
                path,
                headers={
                    "X-Library-Id": str(lib_id),
                    "Authorization": f"Bearer {token_member}",
                },
            )
            req_id1 = r1.headers.get("X-Request-Id")
            audit_rows1 = await _fetch_audit_rows(engine=engine, request_id=req_id1) if req_id1 else []
            case_results.append(
                {
                    "case_id": "same_tenant_success",
                    "title": "same-tenant search → success/audit success",
                    "inputs": {
                        "request_id": req_id1,
                        "tenant_id": str(lib_id) if lib_id else None,
                        "actor_user_id": str(user_member),
                        "http": {
                            "method": "GET",
                            "path": path,
                            "path_template": "/api/v1/search/blocks/two-stage",
                        },
                    },
                    "expected": {
                        "http_status": 200,
                        "audit_expected": True,
                        "audit": {"action": "search.blocks.two_stage", "result": "success", "reason": None},
                        "audit_required_fields": [
                            "tenant_id",
                            "actor_user_id",
                            "request_id",
                            "action",
                            "result",
                        ],
                    },
                    "observed": {
                        "http_status": int(r1.status_code),
                        "audit_rows": {"count": len(audit_rows1), "rows": audit_rows1[:10]},
                    },
                    "verdict": {"ok": None, "failure_reason": None},
                }
            )

            # Case 2: cross-tenant query param denied (library_id != ctx.tenant_id)
            params2 = {"q": "test", "limit": 5, "library_id": other_lib_id}
            q_string2 = urlencode(params2)
            path2 = f"/api/v1/search/blocks/two-stage?{q_string2}"
            r2 = await client.get(
                path2,
                headers={
                    "X-Library-Id": str(lib_id),
                    "Authorization": f"Bearer {token_member}",
                },
            )
            req_id2 = r2.headers.get("X-Request-Id")
            audit_rows2 = await _fetch_audit_rows(engine=engine, request_id=req_id2) if req_id2 else []
            case_results.append(
                {
                    "case_id": "cross_tenant_query_param_denied",
                    "title": "cross-tenant library_id (query) → denied/tenant_mismatch",
                    "inputs": {
                        "request_id": req_id2,
                        "tenant_id": str(lib_id) if lib_id else None,
                        "actor_user_id": str(user_member),
                        "http": {
                            "method": "GET",
                            "path": path2,
                            "path_template": "/api/v1/search/blocks/two-stage",
                        },
                    },
                    "expected": {
                        "http_status": 403,
                        "audit_expected": True,
                        "audit": {
                            "action": "search.blocks.two_stage",
                            "result": "denied",
                            "reason": "tenant_mismatch",
                        },
                        "audit_required_fields": [
                            "tenant_id",
                            "actor_user_id",
                            "request_id",
                            "action",
                            "result",
                            "reason",
                        ],
                    },
                    "observed": {
                        "http_status": int(r2.status_code),
                        "audit_rows": {"count": len(audit_rows2), "rows": audit_rows2[:10]},
                    },
                    "verdict": {"ok": None, "failure_reason": None},
                }
            )

            # Case 3: non-member denied (no membership for user_other)
            params3 = {"q": "test", "limit": 5}
            q_string3 = urlencode(params3)
            path3 = f"/api/v1/search/blocks/two-stage?{q_string3}"
            r3 = await client.get(
                path3,
                headers={
                    "X-Library-Id": str(lib_id),
                    "Authorization": f"Bearer {token_other}",
                },
            )
            req_id3 = r3.headers.get("X-Request-Id")
            audit_rows3 = await _fetch_audit_rows(engine=engine, request_id=req_id3) if req_id3 else []
            case_results.append(
                {
                    "case_id": "non_member_denied",
                    "title": "non-member search → denied/not_member",
                    "inputs": {
                        "request_id": req_id3,
                        "tenant_id": str(lib_id) if lib_id else None,
                        "actor_user_id": str(user_other),
                        "http": {
                            "method": "GET",
                            "path": path3,
                            "path_template": "/api/v1/search/blocks/two-stage",
                        },
                    },
                    "expected": {
                        "http_status": 403,
                        "audit_expected": True,
                        "audit": {
                            "action": "search.blocks.two_stage",
                            "result": "denied",
                            "reason": "not_member",
                        },
                        "audit_required_fields": [
                            "tenant_id",
                            "actor_user_id",
                            "request_id",
                            "action",
                            "result",
                            "reason",
                        ],
                    },
                    "observed": {
                        "http_status": int(r3.status_code),
                        "audit_rows": {"count": len(audit_rows3), "rows": audit_rows3[:10]},
                    },
                    "verdict": {"ok": None, "failure_reason": None},
                }
            )

            # Case 4: invalid query error (too long q to trigger ValueError)
            invalid_q = "x" * 2000
            params4 = {"q": invalid_q, "limit": 5}
            q_string4 = urlencode(params4)
            path4 = f"/api/v1/search/blocks/two-stage?{q_string4}"
            r4 = await client.get(
                path4,
                headers={
                    "X-Library-Id": str(lib_id),
                    "Authorization": f"Bearer {token_member}",
                },
            )
            req_id4 = r4.headers.get("X-Request-Id")
            audit_rows4 = await _fetch_audit_rows(engine=engine, request_id=req_id4) if req_id4 else []
            case_results.append(
                {
                    "case_id": "invalid_query_error",
                    "title": "invalid query → error/invalid_query",
                    "inputs": {
                        "request_id": req_id4,
                        "tenant_id": str(lib_id) if lib_id else None,
                        "actor_user_id": str(user_member),
                        "http": {
                            "method": "GET",
                            "path": path4,
                            "path_template": "/api/v1/search/blocks/two-stage",
                        },
                    },
                    "expected": {
                        "http_status": 422,
                        "audit_expected": True,
                        "audit": {
                            "action": "search.blocks.two_stage",
                            "result": "error",
                            "reason": "invalid_query",
                        },
                        "audit_required_fields": [
                            "tenant_id",
                            "actor_user_id",
                            "request_id",
                            "action",
                            "result",
                            "reason",
                        ],
                    },
                    "observed": {
                        "http_status": int(r4.status_code),
                        "audit_rows": {"count": len(audit_rows4), "rows": audit_rows4[:10]},
                    },
                    "verdict": {"ok": None, "failure_reason": None},
                }
            )

    finally:
        await engine.dispose()

    # Evaluate verdicts
    passed = 0
    failed = 0
    for c in case_results:
        exp = c.get("expected") or {}
        obs = c.get("observed") or {}
        ok = True
        if exp.get("http_status") != obs.get("http_status"):
            ok = False
        if exp.get("audit_expected") is True:
            rows = ((obs.get("audit_rows") or {}).get("rows") or [])
            if not rows:
                ok = False
            else:
                exp_audit = exp.get("audit") or {}
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

        c["verdict"] = {"ok": ok, "failure_reason": None if ok else "unexpected_error"}
        if ok:
            passed += 1
        else:
            failed += 1

    overall_ok = failed == 0

    finished_at = _now_iso()
    duration_s = time.time() - t0

    result = {
        "schema_version": "s5b-1a.result.v1",
        "ok": overall_ok,
        "meta": {
            "run_id": run_id,
            "suite_id": cfg.suite_id,
            "started_at": started_at,
            "finished_at": finished_at,
            "git_sha": git_sha,
        },
        "summary": {"total": len(case_results), "passed": passed, "failed": failed},
        "cases": case_results,
    }

    _write_json(os.path.join(run_dir, "_recipe.json"), recipe)
    _write_json(os.path.join(run_dir, "_result.json"), result)
    _write_text(os.path.join(logs_dir, "run.log"), "\n".join(log_lines) + "\n")

    metrics = {
        "schema_version": "s5b-1a.metrics.v1",
        "run_id": run_id,
        "suite_id": cfg.suite_id,
        "ok": overall_ok,
        "duration_s": duration_s,
        "cases_total": len(case_results),
        "cases_passed": passed,
        "cases_failed": failed,
    }
    _write_json(os.path.join(metrics_dir, "summary.json"), metrics)

    return run_dir, result


def main() -> None:
    if os.name == "nt":
        from asyncio import WindowsSelectorEventLoopPolicy

        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    run_dir, result = asyncio.run(run())

    print(f"[OK] Wrote artifacts to {run_dir}")
    print(json.dumps(result["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
