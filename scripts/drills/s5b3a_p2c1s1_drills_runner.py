"""S5B-3A P2-C1-S1 drills runner.

Goal (v1): exercise membership audit coverage for:
- membership.grant success
- membership.revoke success
- membership.revoke not_found (idempotent delete)
- membership.grant deny (403 not_admin)
- membership.revoke error (simulated domain/unexpected error via invalid input)

Artifacts contract:
- Writes S5B-1A-compatible recipe/result/metrics schemas so we can reuse the existing verifier.
- Output: docs/labs/_snapshot/auto/S5B-3A/<suite_id>/<run_id>/

Prereqs:
- API is running (WORDLOOM_API_BASE_URL)
- DB is reachable (DATABASE_URL)
- JWT secret/alg are configured (WORDLOOM_JWT_SECRET_KEY/WORDLOOM_JWT_ALG)

Run:
  python scripts/drills/s5b3a_p2c1s1_drills_runner.py

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

        required_fields = expected.get("audit_required_fields") or []
        if required_fields:
            missing = [k for k in required_fields if not row.get(k)]
            if missing:
                return "schema_violation"

    return "unexpected_error"


def _build_case_result(
    *,
    case_id: str,
    title: str,
    inputs: dict[str, Any],
    expected: dict[str, Any],
    observed: dict[str, Any],
) -> dict[str, Any]:
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

                required_fields = expected.get("audit_required_fields") or []
                if required_fields:
                    for k in required_fields:
                        if not matched.get(k):
                            ok = False
                            break

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
    return os.path.join("docs", "labs", "_snapshot", "auto", "S5B-3A", suite_id, run_id)


async def run() -> tuple[str, dict[str, Any]]:
    cfg = RunnerConfig(
        api_base_url=os.getenv("WORDLOOM_API_BASE_URL", "http://127.0.0.1:31001").rstrip("/"),
        database_url=os.getenv("DATABASE_URL", "postgresql://wordloom:wordloom@127.0.0.1:5435/wordloom_test"),
        jwt_secret_key=os.getenv("WORDLOOM_JWT_SECRET_KEY", "dev-secret-key-change-in-production"),
        jwt_algorithm=os.getenv("WORDLOOM_JWT_ALG", "HS256"),
        suite_id=os.getenv("S5B_3A_SUITE_ID", "membership_audit_coverage"),
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
                "case_id": "grant_success",
                "title": "grant membership success → audit success",
                "endpoint": {"method": "POST", "path_template": "/api/v1/libraries/{library_id}/memberships"},
            },
            {
                "case_id": "revoke_success",
                "title": "revoke membership success → audit success",
                "endpoint": {"method": "DELETE", "path_template": "/api/v1/libraries/{library_id}/memberships/{user_id}"},
            },
            {
                "case_id": "revoke_not_found",
                "title": "revoke non-existing membership → audit not_found",
                "endpoint": {"method": "DELETE", "path_template": "/api/v1/libraries/{library_id}/memberships/{user_id}"},
            },
            {
                "case_id": "grant_not_admin_403",
                "title": "member cannot manage memberships (403 not_admin)",
                "endpoint": {"method": "POST", "path_template": "/api/v1/libraries/{library_id}/memberships"},
            },
            {
                "case_id": "revoke_domain_error",
                "title": "revoke membership tenant_mismatch deny → audit denied/tenant_mismatch",
                "endpoint": {"method": "DELETE", "path_template": "/api/v1/libraries/{library_id}/memberships/{user_id}"},
            },
        ],
    }

    engine = create_async_engine(_convert_to_psycopg(cfg.database_url), echo=False)

    case_results: list[dict[str, Any]] = []

    # Setup actors
    user_admin = uuid.uuid4()
    user_member = uuid.uuid4()
    user_target = uuid.uuid4()

    token_admin = _make_token(user_id=user_admin, secret_key=cfg.jwt_secret_key, algorithm=cfg.jwt_algorithm)
    token_member = _make_token(user_id=user_member, secret_key=cfg.jwt_secret_key, algorithm=cfg.jwt_algorithm)

    lib_id: Optional[str] = None
    membership_user_id: Optional[str] = None

    try:
        async with httpx.AsyncClient(base_url=cfg.api_base_url, timeout=30.0) as client:
            # Setup: create one library and grant admin/member roles
            lib_name = f"s5b3a-lib-{run_id[:8]}"
            r_lib = await client.post("/api/v1/libraries", json={"name": lib_name, "description": "s5b3a drills"})
            _require_status(r_lib, ok_statuses={200, 201}, label="create_library", log_lines=log_lines)
            lib = _try_json(r_lib) or {}
            lib_id = _require_id(lib, label="create_library", log_lines=log_lines)

            # grant admin on this library
            r_grant_admin = await client.post(
                f"/api/v1/libraries/{lib_id}/memberships",
                json={"user_id": str(user_admin), "role": "admin"},
                headers={"X-Library-Id": str(lib_id)},
            )
            _require_status(r_grant_admin, ok_statuses={200, 201, 204}, label="grant_admin", log_lines=log_lines)

            # grant member on this library
            r_grant_member = await client.post(
                f"/api/v1/libraries/{lib_id}/memberships",
                json={"user_id": str(user_member), "role": "member"},
                headers={"X-Library-Id": str(lib_id)},
            )
            _require_status(r_grant_member, ok_statuses={200, 201, 204}, label="grant_member", log_lines=log_lines)

            # Case 1: grant success (admin grants target user)
            membership_user_id = str(user_target)
            grant_path = f"/api/v1/libraries/{lib_id}/memberships"
            r_grant = await client.post(
                grant_path,
                json={"user_id": membership_user_id, "role": "member"},
                headers={
                    "X-Library-Id": str(lib_id),
                    "Authorization": f"Bearer {token_admin}",
                },
            )
            grant_req_id = r_grant.headers.get("X-Request-Id")
            grant_audit_rows = await _fetch_audit_rows(engine=engine, request_id=grant_req_id) if grant_req_id else []
            case_results.append(
                _build_case_result(
                    case_id="grant_success",
                    title="grant membership success → audit success",
                    inputs={
                        "request_id": grant_req_id,
                        "tenant_id": str(lib_id) if lib_id else None,
                        "actor_user_id": str(user_admin),
                        "http": {
                            "method": "POST",
                            "path": grant_path,
                            "path_template": "/api/v1/libraries/{library_id}/memberships",
                        },
                    },
                    expected={
                        "http_status": 204,
                        "audit_expected": True,
                        "audit": {"action": "membership.grant", "result": "success", "reason": None},
                        "audit_required_fields": [
                            "tenant_id",
                            "actor_user_id",
                            "request_id",
                            "action",
                            "result",
                        ],
                    },
                    observed={
                        "http_status": int(r_grant.status_code),
                        "audit_rows": {"count": len(grant_audit_rows), "rows": grant_audit_rows[:10]},
                    },
                )
            )

            # Case 2: revoke success (admin revokes the membership we just granted)
            revoke_path = f"/api/v1/libraries/{lib_id}/memberships/{membership_user_id}"
            r_revoke_success = await client.delete(
                revoke_path,
                headers={
                    "X-Library-Id": str(lib_id),
                    "Authorization": f"Bearer {token_admin}",
                },
            )
            revoke_success_req_id = r_revoke_success.headers.get("X-Request-Id")
            revoke_success_rows = (
                await _fetch_audit_rows(engine=engine, request_id=revoke_success_req_id)
                if revoke_success_req_id
                else []
            )
            case_results.append(
                _build_case_result(
                    case_id="revoke_success",
                    title="revoke membership success → audit success",
                    inputs={
                        "request_id": revoke_success_req_id,
                        "tenant_id": str(lib_id) if lib_id else None,
                        "actor_user_id": str(user_admin),
                        "http": {
                            "method": "DELETE",
                            "path": revoke_path,
                            "path_template": "/api/v1/libraries/{library_id}/memberships/{user_id}",
                        },
                    },
                    expected={
                        "http_status": 204,
                        "audit_expected": True,
                        "audit": {"action": "membership.revoke", "result": "success", "reason": None},
                        "audit_required_fields": [
                            "tenant_id",
                            "actor_user_id",
                            "request_id",
                            "action",
                            "result",
                        ],
                    },
                    observed={
                        "http_status": int(r_revoke_success.status_code),
                        "audit_rows": {
                            "count": len(revoke_success_rows),
                            "rows": revoke_success_rows[:10],
                        },
                    },
                )
            )

            # Case 3: revoke not_found (idempotent second revoke)
            r_revoke_not_found = await client.delete(
                revoke_path,
                headers={
                    "X-Library-Id": str(lib_id),
                    "Authorization": f"Bearer {token_admin}",
                },
            )
            revoke_not_found_req_id = r_revoke_not_found.headers.get("X-Request-Id")
            revoke_not_found_rows = (
                await _fetch_audit_rows(engine=engine, request_id=revoke_not_found_req_id)
                if revoke_not_found_req_id
                else []
            )
            case_results.append(
                _build_case_result(
                    case_id="revoke_not_found",
                    title="revoke non-existing membership → audit not_found",
                    inputs={
                        "request_id": revoke_not_found_req_id,
                        "tenant_id": str(lib_id) if lib_id else None,
                        "actor_user_id": str(user_admin),
                        "http": {
                            "method": "DELETE",
                            "path": revoke_path,
                            "path_template": "/api/v1/libraries/{library_id}/memberships/{user_id}",
                        },
                    },
                    expected={
                        "http_status": 204,
                        "audit_expected": True,
                        "audit": {"action": "membership.revoke", "result": "not_found", "reason": None},
                        "audit_required_fields": [
                            "tenant_id",
                            "actor_user_id",
                            "request_id",
                            "action",
                            "result",
                        ],
                    },
                    observed={
                        "http_status": int(r_revoke_not_found.status_code),
                        "audit_rows": {
                            "count": len(revoke_not_found_rows),
                            "rows": revoke_not_found_rows[:10],
                        },
                    },
                )
            )

            # Case 4: member cannot manage memberships (403 not_admin)
            r_grant_member_denied = await client.post(
                grant_path,
                json={"user_id": str(uuid.uuid4()), "role": "member"},
                headers={
                    "X-Library-Id": str(lib_id),
                    "Authorization": f"Bearer {token_member}",
                },
            )
            grant_denied_req_id = r_grant_member_denied.headers.get("X-Request-Id")
            grant_denied_rows = (
                await _fetch_audit_rows(engine=engine, request_id=grant_denied_req_id)
                if grant_denied_req_id
                else []
            )
            case_results.append(
                _build_case_result(
                    case_id="grant_not_admin_403",
                    title="member cannot manage memberships (403 not_admin)",
                    inputs={
                        "request_id": grant_denied_req_id,
                        "tenant_id": str(lib_id) if lib_id else None,
                        "actor_user_id": str(user_member),
                        "http": {
                            "method": "POST",
                            "path": grant_path,
                            "path_template": "/api/v1/libraries/{library_id}/memberships",
                        },
                    },
                    expected={
                        "http_status": 403,
                        "audit_expected": True,
                        "audit": {"action": "membership.grant", "result": "denied", "reason": "not_admin"},
                        "audit_required_fields": [
                            "tenant_id",
                            "actor_user_id",
                            "request_id",
                            "action",
                            "result",
                            "reason",
                        ],
                    },
                    observed={
                        "http_status": int(r_grant_member_denied.status_code),
                        "audit_rows": {
                            "count": len(grant_denied_rows),
                            "rows": grant_denied_rows[:10],
                        },
                    },
                )
            )

            # Case 5: revoke deny (simulate tenant_mismatch via invalid header tenant)
            r_revoke_error = await client.delete(
                revoke_path,
                headers={
                    # deliberately mismatched tenant header to trigger 403 tenant_mismatch
                    "X-Library-Id": str(uuid.uuid4()),
                    "Authorization": f"Bearer {token_admin}",
                },
            )
            revoke_error_req_id = r_revoke_error.headers.get("X-Request-Id")
            revoke_error_rows = (
                await _fetch_audit_rows(engine=engine, request_id=revoke_error_req_id)
                if revoke_error_req_id
                else []
            )
            case_results.append(
                _build_case_result(
                    case_id="revoke_domain_error",
                    title="revoke membership domain/unexpected error → audit error",
                    inputs={
                        "request_id": revoke_error_req_id,
                        "tenant_id": str(lib_id) if lib_id else None,
                        "actor_user_id": str(user_admin),
                        "http": {
                            "method": "DELETE",
                            "path": revoke_path,
                            "path_template": "/api/v1/libraries/{library_id}/memberships/{user_id}",
                        },
                    },
                    expected={
                        "http_status": int(r_revoke_error.status_code),
                        "audit_expected": True,
                        "audit": {
                            "action": "membership.revoke",
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
                    observed={
                        "http_status": int(r_revoke_error.status_code),
                        "audit_rows": {
                            "count": len(revoke_error_rows),
                            "rows": revoke_error_rows[:10],
                        },
                    },
                )
            )

    except Exception as e:  # noqa: BLE001
        log_lines.append(f"error_type={type(e).__name__}")
        log_lines.append(f"setup_state:lib_id={lib_id}")
        log_lines.append(f"setup_state:membership_user_id={membership_user_id}")

        for case in [
            ("grant_success", "grant membership success → audit success"),
            ("revoke_success", "revoke membership success → audit success"),
            ("revoke_not_found", "revoke non-existing membership → audit not_found"),
            ("grant_not_admin_403", "member cannot manage memberships (403 not_admin)"),
            ("revoke_domain_error", "revoke membership domain/unexpected error → audit error"),
        ]:
            cid, title = case
            if not any(r.get("case_id") == cid for r in case_results):
                case_results.append(
                    {
                        "case_id": cid,
                        "title": title,
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
        from asyncio import WindowsSelectorEventLoopPolicy

        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    run_dir, result = asyncio.run(run())

    print(f"[OK] Wrote artifacts to {run_dir}")
    print(json.dumps(result["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
