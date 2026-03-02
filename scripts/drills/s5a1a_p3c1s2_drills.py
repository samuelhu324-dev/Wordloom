"""S5A-1A P3-C1-S2 drills runner.

Scenarios (v1):
1) tenant 越权读：同一 bookshelf_id，用错误的 X-Library-Id 读取 → 404 + audit_log.not_found
2) role/owner 不足写/读：非 owner 读取同 tenant → 403 + audit_log.denied
3) 审计完整性：一次成功写入（create bookshelf）必须产生 audit_log.success

This script is designed to be repeatable and to output artifacts as JSON.

Prereqs:
- API is running (default http://localhost:30001)
- DB is reachable via DATABASE_URL (same DB as API)
- (Optional) For scenario #2, set ALLOW_DEV_LIBRARY_OWNER_OVERRIDE=0 on the API process.
"""

from __future__ import annotations

import asyncio
import json
import os
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

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
    # JSON-serializable
    out: list[dict[str, Any]] = []
    for r in rows:
        d = dict(r)
        for k in ("occurred_at",):
            if d.get(k) is not None:
                d[k] = d[k].isoformat()
        for k in ("tenant_id", "actor_user_id", "resource_id"):
            if d.get(k) is not None:
                d[k] = str(d[k])
        out.append(d)
    return out


async def _post_json(client: httpx.AsyncClient, url: str, body: dict[str, Any], headers: dict[str, str] | None = None) -> httpx.Response:
    return await client.post(url, json=body, headers=headers)


async def _get(client: httpx.AsyncClient, url: str, headers: dict[str, str] | None = None) -> httpx.Response:
    return await client.get(url, headers=headers)


def _artifact_path() -> str:
    out_dir = os.path.join("artifacts", "_tmp_s5a1a_p3c1s2")
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

    async with httpx.AsyncClient(base_url=cfg.api_base_url, timeout=30.0) as client:
        # Setup: create 2 libraries + 1 bookshelf in lib_a
        lib_a_name = f"drill-lib-a-{run_id[:8]}"
        lib_b_name = f"drill-lib-b-{run_id[:8]}"

        r_lib_a = await _post_json(client, "/api/v1/libraries", {"name": lib_a_name, "description": "drill"})
        r_lib_b = await _post_json(client, "/api/v1/libraries", {"name": lib_b_name, "description": "drill"})

        lib_a = (r_lib_a.json() if r_lib_a.headers.get("content-type", "").startswith("application/json") else None) or {}
        lib_b = (r_lib_b.json() if r_lib_b.headers.get("content-type", "").startswith("application/json") else None) or {}

        lib_a_id = lib_a.get("id")
        lib_b_id = lib_b.get("id")

        # Create bookshelf (write success audit)
        shelf_name = f"drill-shelf-{run_id[:8]}"
        r_create_shelf = await _post_json(
            client,
            "/api/v1/bookshelves",
            {"library_id": lib_a_id, "name": shelf_name, "description": "drill"},
        )
        create_req_id = r_create_shelf.headers.get("X-Request-Id")
        shelf = (r_create_shelf.json() if r_create_shelf.headers.get("content-type", "").startswith("application/json") else None) or {}
        shelf_id = shelf.get("id")

        # Drill #1: tenant cross read -> 404
        r_cross = await _get(
            client,
            f"/api/v1/bookshelves/{shelf_id}",
            headers={"X-Library-Id": str(lib_b_id)},
        )
        cross_req_id = r_cross.headers.get("X-Request-Id")

        # Drill #2: non-owner read in same tenant -> 403 (requires owner-check enabled)
        user_b = uuid.uuid4()
        token_b = _make_token(user_id=user_b, secret_key=cfg.jwt_secret_key, algorithm=cfg.jwt_algorithm)
        r_non_owner = await _get(
            client,
            f"/api/v1/bookshelves/{shelf_id}",
            headers={
                "X-Library-Id": str(lib_a_id),
                "Authorization": f"Bearer {token_b}",
            },
        )
        non_owner_req_id = r_non_owner.headers.get("X-Request-Id")

    # Query audit rows for request_ids
    audit_create = await _fetch_audit_rows(engine=engine, request_id=create_req_id) if create_req_id else []
    audit_cross = await _fetch_audit_rows(engine=engine, request_id=cross_req_id) if cross_req_id else []
    audit_non_owner = await _fetch_audit_rows(engine=engine, request_id=non_owner_req_id) if non_owner_req_id else []

    await engine.dispose()

    return {
        "meta": {
            "run_id": run_id,
            "started_at": t0,
            "finished_at": _now_iso(),
            "config": asdict(cfg),
            "notes": {
                "scenario_2_requires": "ALLOW_DEV_LIBRARY_OWNER_OVERRIDE=0 on API",
            },
        },
        "setup": {
            "library_a": {"name": lib_a_name, "id": lib_a_id, "status": r_lib_a.status_code},
            "library_b": {"name": lib_b_name, "id": lib_b_id, "status": r_lib_b.status_code},
            "bookshelf": {"name": shelf_name, "id": shelf_id, "status": r_create_shelf.status_code},
        },
        "drills": {
            "audit_integrity_write_success": {
                "request_id": create_req_id,
                "http_status": r_create_shelf.status_code,
                "audit_rows": audit_create,
                "expected": {"action": "bookshelf.create", "result": "success"},
            },
            "tenant_cross_read_404": {
                "request_id": cross_req_id,
                "http_status": r_cross.status_code,
                "audit_rows": audit_cross,
                "expected": {"action": "bookshelf.get", "result": "not_found", "http_status": 404},
            },
            "non_owner_read_403": {
                "request_id": non_owner_req_id,
                "http_status": r_non_owner.status_code,
                "audit_rows": audit_non_owner,
                "expected": {"action": "bookshelf.get", "result": "denied", "http_status": 403},
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
