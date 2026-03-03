"""S5A-2A P3-C3-S2 drills runner.

Scenarios (read-path 404 contract + audit not_found):
1) bookshelf.list non-member -> 404 + audit not_found (reason=not_member)
2) bookshelf.list tenant_mismatch -> 404 + audit not_found (reason=tenant_mismatch)
3) bookshelf.dashboard non-member -> 404 + audit not_found (reason=not_member)
4) bookshelf.basement.get non-member -> 404 + audit not_found (reason=not_member)

Prereqs:
- API is running (default http://localhost:31001)
- DB is reachable via DATABASE_URL (same DB as API)

Notes:
- Uses JWT tokens with user_id only (dev auth).
- Uses X-Library-Id header as tenant selector.
"""

from __future__ import annotations

import asyncio
import json
import os
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx
import jwt
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


@dataclass(frozen=True)
class DrillConfig:
    api_base_url: str
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str


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


def _artifact_path() -> str:
    out_dir = os.path.join("artifacts", "_tmp_s5a2a_p3c3s2")
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, f"drills_{int(time.time())}.json")


def _try_json(resp: httpx.Response) -> Any:
    if resp.headers.get("content-type", "").startswith("application/json"):
        try:
            return resp.json()
        except Exception:
            return None
    return None


async def run() -> dict[str, Any]:
    cfg = DrillConfig(
        api_base_url=os.getenv("WORDLOOM_API_BASE_URL", "http://localhost:31001").rstrip("/"),
        database_url=os.getenv("DATABASE_URL", "postgresql://postgres:pgpass@localhost:5432/wordloom"),
        jwt_secret_key=os.getenv("WORDLOOM_JWT_SECRET_KEY", "dev-secret-key-change-in-production"),
        jwt_algorithm=os.getenv("WORDLOOM_JWT_ALG", "HS256"),
    )

    engine = create_async_engine(_convert_to_psycopg(cfg.database_url), echo=False)

    run_id = str(uuid.uuid4())
    t0 = _now_iso()

    user_admin = uuid.uuid4()
    user_member = uuid.uuid4()
    user_non_member = uuid.uuid4()

    token_admin = _make_token(user_id=user_admin, secret_key=cfg.jwt_secret_key, algorithm=cfg.jwt_algorithm)
    token_member = _make_token(user_id=user_member, secret_key=cfg.jwt_secret_key, algorithm=cfg.jwt_algorithm)
    token_non_member = _make_token(user_id=user_non_member, secret_key=cfg.jwt_secret_key, algorithm=cfg.jwt_algorithm)

    async with httpx.AsyncClient(base_url=cfg.api_base_url, timeout=30.0) as client:
        # Setup: create library (dev endpoint)
        lib_name = f"drill-lib-s5a2a-p3c3-{run_id[:8]}"
        r_lib = await client.post("/api/v1/libraries", json={"name": lib_name, "description": "drill"})
        lib = (r_lib.json() if r_lib.headers.get("content-type", "").startswith("application/json") else None) or {}
        lib_id = lib.get("id")

        # Setup: grant admin/member
        r_grant_admin = await client.post(
            f"/api/v1/libraries/{lib_id}/memberships",
            json={"user_id": str(user_admin), "role": "admin"},
            headers={"X-Library-Id": str(lib_id)},
        )
        grant_admin_req_id = r_grant_admin.headers.get("X-Request-Id")

        r_grant_member = await client.post(
            f"/api/v1/libraries/{lib_id}/memberships",
            json={"user_id": str(user_member), "role": "member"},
            headers={"X-Library-Id": str(lib_id)},
        )
        grant_member_req_id = r_grant_member.headers.get("X-Request-Id")

        # Setup: create one bookshelf as admin (so list isn't empty)
        shelf_name = f"drill-shelf-a-{run_id[:8]}"
        r_admin_create = await client.post(
            "/api/v1/bookshelves",
            json={"library_id": str(lib_id), "name": shelf_name, "description": "drill"},
            headers={
                "X-Library-Id": str(lib_id),
                "Authorization": f"Bearer {token_admin}",
            },
        )
        admin_create_req_id = r_admin_create.headers.get("X-Request-Id")

        # Drill #1: non-member list -> 404 not_member
        r_list_non_member = await client.get(
            "/api/v1/bookshelves",
            params={"library_id": str(lib_id), "skip": 0, "limit": 10},
            headers={
                "X-Library-Id": str(lib_id),
                "Authorization": f"Bearer {token_non_member}",
            },
        )
        list_non_member_req_id = r_list_non_member.headers.get("X-Request-Id")

        # Drill #2: tenant mismatch list -> 404 tenant_mismatch
        other_lib_id = str(uuid.uuid4())
        r_list_tenant_mismatch = await client.get(
            "/api/v1/bookshelves",
            params={"library_id": other_lib_id, "skip": 0, "limit": 10},
            headers={
                "X-Library-Id": str(lib_id),
                "Authorization": f"Bearer {token_member}",
            },
        )
        list_tenant_mismatch_req_id = r_list_tenant_mismatch.headers.get("X-Request-Id")

        # Drill #3: non-member dashboard -> 404 not_member
        r_dashboard_non_member = await client.get(
            "/api/v1/bookshelves/dashboard",
            params={"library_id": str(lib_id), "page": 1, "size": 5},
            headers={
                "X-Library-Id": str(lib_id),
                "Authorization": f"Bearer {token_non_member}",
            },
        )
        dashboard_non_member_req_id = r_dashboard_non_member.headers.get("X-Request-Id")

        # Drill #4: non-member basement -> 404 not_member
        r_basement_non_member = await client.get(
            "/api/v1/bookshelves/basement",
            params={"library_id": str(lib_id)},
            headers={
                "X-Library-Id": str(lib_id),
                "Authorization": f"Bearer {token_non_member}",
            },
        )
        basement_non_member_req_id = r_basement_non_member.headers.get("X-Request-Id")

    audit_grant_admin = await _fetch_audit_rows(engine=engine, request_id=grant_admin_req_id) if grant_admin_req_id else []
    audit_grant_member = await _fetch_audit_rows(engine=engine, request_id=grant_member_req_id) if grant_member_req_id else []
    audit_admin_create = await _fetch_audit_rows(engine=engine, request_id=admin_create_req_id) if admin_create_req_id else []

    audit_list_non_member = (
        await _fetch_audit_rows(engine=engine, request_id=list_non_member_req_id) if list_non_member_req_id else []
    )
    audit_list_tenant_mismatch = (
        await _fetch_audit_rows(engine=engine, request_id=list_tenant_mismatch_req_id)
        if list_tenant_mismatch_req_id
        else []
    )
    audit_dashboard_non_member = (
        await _fetch_audit_rows(engine=engine, request_id=dashboard_non_member_req_id)
        if dashboard_non_member_req_id
        else []
    )
    audit_basement_non_member = (
        await _fetch_audit_rows(engine=engine, request_id=basement_non_member_req_id)
        if basement_non_member_req_id
        else []
    )

    await engine.dispose()

    return {
        "meta": {
            "run_id": run_id,
            "started_at": t0,
            "finished_at": _now_iso(),
            "config": asdict(cfg),
        },
        "setup": {
            "library": {"name": lib_name, "id": lib_id, "status": r_lib.status_code},
            "users": {
                "admin": str(user_admin),
                "member": str(user_member),
                "non_member": str(user_non_member),
            },
            "bookshelf_create": {
                "status": r_admin_create.status_code,
                "request_id": admin_create_req_id,
                "response": _try_json(r_admin_create),
                "audit_rows": audit_admin_create,
            },
        },
        "drills": {
            "membership_grant_admin": {
                "request_id": grant_admin_req_id,
                "http_status": r_grant_admin.status_code,
                "audit_rows": audit_grant_admin,
                "expected": {"action": "membership.grant", "result": "success"},
            },
            "membership_grant_member": {
                "request_id": grant_member_req_id,
                "http_status": r_grant_member.status_code,
                "audit_rows": audit_grant_member,
                "expected": {"action": "membership.grant", "result": "success"},
            },
            "bookshelf_list_non_member_not_found": {
                "request_id": list_non_member_req_id,
                "http_status": r_list_non_member.status_code,
                "response": _try_json(r_list_non_member),
                "audit_rows": audit_list_non_member,
                "expected": {"action": "bookshelf.list", "result": "not_found", "reason": "not_member", "http_status": 404},
            },
            "bookshelf_list_tenant_mismatch_not_found": {
                "request_id": list_tenant_mismatch_req_id,
                "http_status": r_list_tenant_mismatch.status_code,
                "response": _try_json(r_list_tenant_mismatch),
                "audit_rows": audit_list_tenant_mismatch,
                "expected": {
                    "action": "bookshelf.list",
                    "result": "not_found",
                    "reason": "tenant_mismatch",
                    "http_status": 404,
                },
            },
            "bookshelf_dashboard_non_member_not_found": {
                "request_id": dashboard_non_member_req_id,
                "http_status": r_dashboard_non_member.status_code,
                "response": _try_json(r_dashboard_non_member),
                "audit_rows": audit_dashboard_non_member,
                "expected": {
                    "action": "bookshelf.dashboard",
                    "result": "not_found",
                    "reason": "not_member",
                    "http_status": 404,
                },
            },
            "bookshelf_basement_get_non_member_not_found": {
                "request_id": basement_non_member_req_id,
                "http_status": r_basement_non_member.status_code,
                "response": _try_json(r_basement_non_member),
                "audit_rows": audit_basement_non_member,
                "expected": {
                    "action": "bookshelf.basement.get",
                    "result": "not_found",
                    "reason": "not_member",
                    "http_status": 404,
                },
            },
        },
    }


def main() -> None:
    # psycopg async cannot run on ProactorEventLoop (Windows default).
    if os.name == "nt":
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except Exception:
            pass

    result = asyncio.run(run())
    out_path = _artifact_path()
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"[OK] Wrote artifact: {out_path}")


if __name__ == "__main__":
    main()
