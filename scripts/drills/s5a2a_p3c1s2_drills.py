"""S5A-2A P3-C1-S2 drills runner.

Scenarios (v2):
1) not_member executes admin action (bookshelf.create) -> 403 + audit denied (reason=not_member)
2) member executes admin action (bookshelf.create) -> 403 + audit denied (reason=not_admin)
3) admin executes admin action (bookshelf.create) -> 201 + audit success

Also validates membership grant auditing:
- membership.grant -> audit success (action=membership.grant)

Prereqs:
- API is running (default http://localhost:30001)
- DB is reachable via DATABASE_URL (same DB as API)
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
    out_dir = os.path.join("artifacts", "_tmp_s5a2a_p3c1s2")
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, f"drills_{int(time.time())}.json")


async def run() -> dict[str, Any]:
    cfg = DrillConfig(
        api_base_url=os.getenv("WORDLOOM_API_BASE_URL", "http://localhost:30001").rstrip("/"),
        database_url=os.getenv("DATABASE_URL", "postgresql://postgres:pgpass@localhost:5432/wordloom"),
        jwt_secret_key=os.getenv("WORDLOOM_JWT_SECRET_KEY", "dev-secret-key-change-in-production"),
        jwt_algorithm=os.getenv("WORDLOOM_JWT_ALG", "HS256"),
    )

    engine = create_async_engine(_convert_to_psycopg(cfg.database_url), echo=False)

    run_id = str(uuid.uuid4())
    t0 = _now_iso()

    user_admin = uuid.uuid4()
    user_member = uuid.uuid4()
    user_stranger = uuid.uuid4()

    token_admin = _make_token(user_id=user_admin, secret_key=cfg.jwt_secret_key, algorithm=cfg.jwt_algorithm)
    token_member = _make_token(user_id=user_member, secret_key=cfg.jwt_secret_key, algorithm=cfg.jwt_algorithm)
    token_stranger = _make_token(user_id=user_stranger, secret_key=cfg.jwt_secret_key, algorithm=cfg.jwt_algorithm)

    async with httpx.AsyncClient(base_url=cfg.api_base_url, timeout=30.0) as client:
        # Setup: create library (owned by dev user_id on API side)
        lib_name = f"drill-lib-s5a2a-{run_id[:8]}"
        r_lib = await client.post("/api/v1/libraries", json={"name": lib_name, "description": "drill"})
        lib = (r_lib.json() if r_lib.headers.get("content-type", "").startswith("application/json") else None) or {}
        lib_id = lib.get("id")

        # Setup: grant admin/member (as owner/dev user on API side)
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

        # Drill #1: not_member -> 403 not_member
        shelf_name_1 = f"drill-shelf-nm-{run_id[:8]}"
        r_not_member = await client.post(
            "/api/v1/bookshelves",
            json={"library_id": str(lib_id), "name": shelf_name_1, "description": "drill"},
            headers={
                "X-Library-Id": str(lib_id),
                "Authorization": f"Bearer {token_stranger}",
            },
        )
        not_member_req_id = r_not_member.headers.get("X-Request-Id")

        # Drill #2: member -> 403 not_admin
        shelf_name_2 = f"drill-shelf-m-{run_id[:8]}"
        r_member = await client.post(
            "/api/v1/bookshelves",
            json={"library_id": str(lib_id), "name": shelf_name_2, "description": "drill"},
            headers={
                "X-Library-Id": str(lib_id),
                "Authorization": f"Bearer {token_member}",
            },
        )
        member_req_id = r_member.headers.get("X-Request-Id")

        # Drill #3: admin -> 201 success
        shelf_name_3 = f"drill-shelf-a-{run_id[:8]}"
        r_admin = await client.post(
            "/api/v1/bookshelves",
            json={"library_id": str(lib_id), "name": shelf_name_3, "description": "drill"},
            headers={
                "X-Library-Id": str(lib_id),
                "Authorization": f"Bearer {token_admin}",
            },
        )
        admin_req_id = r_admin.headers.get("X-Request-Id")

    # Query audit rows for request_ids
    audit_grant_admin = await _fetch_audit_rows(engine=engine, request_id=grant_admin_req_id) if grant_admin_req_id else []
    audit_grant_member = await _fetch_audit_rows(engine=engine, request_id=grant_member_req_id) if grant_member_req_id else []
    audit_not_member = await _fetch_audit_rows(engine=engine, request_id=not_member_req_id) if not_member_req_id else []
    audit_member = await _fetch_audit_rows(engine=engine, request_id=member_req_id) if member_req_id else []
    audit_admin = await _fetch_audit_rows(engine=engine, request_id=admin_req_id) if admin_req_id else []

    await engine.dispose()

    def _try_json(resp: httpx.Response) -> Any:
        if (resp.headers.get("content-type", "").startswith("application/json")):
            try:
                return resp.json()
            except Exception:
                return None
        return None

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
                "stranger": str(user_stranger),
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
            "bookshelf_create_not_member_denied": {
                "request_id": not_member_req_id,
                "http_status": r_not_member.status_code,
                "response": _try_json(r_not_member),
                "audit_rows": audit_not_member,
                "expected": {"action": "bookshelf.create", "result": "denied", "reason": "not_member", "http_status": 403},
            },
            "bookshelf_create_member_denied": {
                "request_id": member_req_id,
                "http_status": r_member.status_code,
                "response": _try_json(r_member),
                "audit_rows": audit_member,
                "expected": {"action": "bookshelf.create", "result": "denied", "reason": "not_admin", "http_status": 403},
            },
            "bookshelf_create_admin_success": {
                "request_id": admin_req_id,
                "http_status": r_admin.status_code,
                "response": _try_json(r_admin),
                "audit_rows": audit_admin,
                "expected": {"action": "bookshelf.create", "result": "success", "http_status": 201},
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
