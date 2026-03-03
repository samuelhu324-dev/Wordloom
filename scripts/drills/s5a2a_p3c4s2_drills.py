"""S5A-2A P3-C4-S2 drills runner.

Scenarios (read-path 404 contract + audit not_found):
1) book.list non-member -> 404 + audit not_found (reason=not_member)
2) book.list tenant_mismatch (library_id query != header tenant) -> 404 + audit not_found (reason=tenant_mismatch)
3) book.list tenant_mismatch (bookshelf_id belongs to other tenant) -> 404 + audit not_found (reason=tenant_mismatch)
4) book.get non-member -> 404 + audit not_found (reason=not_member)
5) book.get tenant_mismatch (book belongs to other tenant) -> 404 + audit not_found (reason=tenant_mismatch)

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
import sys
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import httpx
import jwt
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


# psycopg async on Windows requires SelectorEventLoop (Proactor is incompatible).
if sys.platform.startswith("win"):
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass


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
    out_dir = os.path.join("artifacts", "_tmp_s5a2a_p3c4s2")
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, f"drills_{int(time.time())}.json")


def _try_json(resp: httpx.Response) -> Any:
    if resp.headers.get("content-type", "").startswith("application/json"):
        try:
            return resp.json()
        except Exception:
            return None
    return None


def _id_from_json(resp: httpx.Response, key: str) -> Optional[str]:
    payload = _try_json(resp) or {}
    raw = payload.get(key)
    return str(raw) if raw else None


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

    user_member = uuid.uuid4()
    user_non_member = uuid.uuid4()

    token_member = _make_token(user_id=user_member, secret_key=cfg.jwt_secret_key, algorithm=cfg.jwt_algorithm)
    token_non_member = _make_token(user_id=user_non_member, secret_key=cfg.jwt_secret_key, algorithm=cfg.jwt_algorithm)

    async with httpx.AsyncClient(base_url=cfg.api_base_url, timeout=30.0) as client:
        # Setup: create two libraries (owner = DEV_USER_ID implicit)
        lib_a_name = f"drill-lib-a-s5a2a-p3c4-{run_id[:8]}"
        r_lib_a = await client.post("/api/v1/libraries", json={"name": lib_a_name, "description": "drill"})
        lib_a_id = _id_from_json(r_lib_a, "id")

        lib_b_name = f"drill-lib-b-s5a2a-p3c4-{run_id[:8]}"
        r_lib_b = await client.post("/api/v1/libraries", json={"name": lib_b_name, "description": "drill"})
        lib_b_id = _id_from_json(r_lib_b, "id")

        # Setup: grant member role to user_member in BOTH libraries
        r_grant_member_a = await client.post(
            f"/api/v1/libraries/{lib_a_id}/memberships",
            json={"user_id": str(user_member), "role": "member"},
            headers={"X-Library-Id": str(lib_a_id)},
        )
        grant_member_a_req_id = r_grant_member_a.headers.get("X-Request-Id")

        r_grant_member_b = await client.post(
            f"/api/v1/libraries/{lib_b_id}/memberships",
            json={"user_id": str(user_member), "role": "member"},
            headers={"X-Library-Id": str(lib_b_id)},
        )
        grant_member_b_req_id = r_grant_member_b.headers.get("X-Request-Id")

        # Setup: create one bookshelf + one book in library A (as owner implicit)
        shelf_name = f"drill-shelf-a-{run_id[:8]}"
        r_shelf = await client.post(
            "/api/v1/bookshelves",
            json={"library_id": str(lib_a_id), "name": shelf_name, "description": "drill"},
            headers={"X-Library-Id": str(lib_a_id)},
        )
        shelf_id = _id_from_json(r_shelf, "id")

        book_title = f"drill-book-a-{run_id[:8]}"
        r_book = await client.post(
            "/api/v1/books",
            json={
                "bookshelf_id": str(shelf_id),
                "library_id": str(lib_a_id),
                "title": book_title,
                "summary": "drill",
                "cover_icon": None,
                "actor_user_id": None,
                "enforce_owner_check": True,
            },
            headers={"X-Library-Id": str(lib_a_id)},
        )
        book_id = _id_from_json(r_book, "id")

        # Drill #1: non-member list -> 404 not_member
        r_list_non_member = await client.get(
            "/api/v1/books",
            params={"library_id": str(lib_a_id), "skip": 0, "limit": 10},
            headers={
                "X-Library-Id": str(lib_a_id),
                "Authorization": f"Bearer {token_non_member}",
            },
        )
        list_non_member_req_id = r_list_non_member.headers.get("X-Request-Id")

        # Drill #2: tenant mismatch list (library_id query mismatches header) -> 404 tenant_mismatch
        r_list_tenant_mismatch_query = await client.get(
            "/api/v1/books",
            params={"library_id": str(lib_b_id), "skip": 0, "limit": 10},
            headers={
                "X-Library-Id": str(lib_a_id),
                "Authorization": f"Bearer {token_member}",
            },
        )
        list_tenant_mismatch_query_req_id = r_list_tenant_mismatch_query.headers.get("X-Request-Id")

        # Drill #3: tenant mismatch list (bookshelf_id belongs to other tenant) -> 404 tenant_mismatch
        r_list_tenant_mismatch_shelf = await client.get(
            "/api/v1/books",
            params={"bookshelf_id": str(shelf_id), "skip": 0, "limit": 10},
            headers={
                "X-Library-Id": str(lib_b_id),
                "Authorization": f"Bearer {token_member}",
            },
        )
        list_tenant_mismatch_shelf_req_id = r_list_tenant_mismatch_shelf.headers.get("X-Request-Id")

        # Drill #4: non-member get -> 404 not_member
        r_get_non_member = await client.get(
            f"/api/v1/books/{book_id}",
            headers={
                "X-Library-Id": str(lib_a_id),
                "Authorization": f"Bearer {token_non_member}",
            },
        )
        get_non_member_req_id = r_get_non_member.headers.get("X-Request-Id")

        # Drill #5: tenant mismatch get (book belongs to A, ctx tenant is B) -> 404 tenant_mismatch
        r_get_tenant_mismatch = await client.get(
            f"/api/v1/books/{book_id}",
            headers={
                "X-Library-Id": str(lib_b_id),
                "Authorization": f"Bearer {token_member}",
            },
        )
        get_tenant_mismatch_req_id = r_get_tenant_mismatch.headers.get("X-Request-Id")

    audit_grant_member_a = await _fetch_audit_rows(engine=engine, request_id=grant_member_a_req_id) if grant_member_a_req_id else []
    audit_grant_member_b = await _fetch_audit_rows(engine=engine, request_id=grant_member_b_req_id) if grant_member_b_req_id else []

    audit_list_non_member = await _fetch_audit_rows(engine=engine, request_id=list_non_member_req_id) if list_non_member_req_id else []
    audit_list_tenant_mismatch_query = (
        await _fetch_audit_rows(engine=engine, request_id=list_tenant_mismatch_query_req_id)
        if list_tenant_mismatch_query_req_id
        else []
    )
    audit_list_tenant_mismatch_shelf = (
        await _fetch_audit_rows(engine=engine, request_id=list_tenant_mismatch_shelf_req_id)
        if list_tenant_mismatch_shelf_req_id
        else []
    )
    audit_get_non_member = await _fetch_audit_rows(engine=engine, request_id=get_non_member_req_id) if get_non_member_req_id else []
    audit_get_tenant_mismatch = (
        await _fetch_audit_rows(engine=engine, request_id=get_tenant_mismatch_req_id)
        if get_tenant_mismatch_req_id
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
            "library_a": {"name": lib_a_name, "id": lib_a_id, "status": r_lib_a.status_code, "response": _try_json(r_lib_a)},
            "library_b": {"name": lib_b_name, "id": lib_b_id, "status": r_lib_b.status_code, "response": _try_json(r_lib_b)},
            "users": {"member": str(user_member), "non_member": str(user_non_member)},
            "grant_member_a": {"status": r_grant_member_a.status_code, "request_id": grant_member_a_req_id, "response": _try_json(r_grant_member_a)},
            "grant_member_b": {"status": r_grant_member_b.status_code, "request_id": grant_member_b_req_id, "response": _try_json(r_grant_member_b)},
            "bookshelf_create": {"status": r_shelf.status_code, "request_id": r_shelf.headers.get("X-Request-Id"), "response": _try_json(r_shelf)},
            "book_create": {"status": r_book.status_code, "request_id": r_book.headers.get("X-Request-Id"), "response": _try_json(r_book)},
        },
        "drills": {
            "book_list_non_member": {"status": r_list_non_member.status_code, "request_id": list_non_member_req_id, "response": _try_json(r_list_non_member)},
            "book_list_tenant_mismatch_query": {"status": r_list_tenant_mismatch_query.status_code, "request_id": list_tenant_mismatch_query_req_id, "response": _try_json(r_list_tenant_mismatch_query)},
            "book_list_tenant_mismatch_bookshelf": {"status": r_list_tenant_mismatch_shelf.status_code, "request_id": list_tenant_mismatch_shelf_req_id, "response": _try_json(r_list_tenant_mismatch_shelf)},
            "book_get_non_member": {"status": r_get_non_member.status_code, "request_id": get_non_member_req_id, "response": _try_json(r_get_non_member)},
            "book_get_tenant_mismatch": {"status": r_get_tenant_mismatch.status_code, "request_id": get_tenant_mismatch_req_id, "response": _try_json(r_get_tenant_mismatch)},
        },
        "audit": {
            "grant_member_a": audit_grant_member_a,
            "grant_member_b": audit_grant_member_b,
            "book_list_non_member": audit_list_non_member,
            "book_list_tenant_mismatch_query": audit_list_tenant_mismatch_query,
            "book_list_tenant_mismatch_bookshelf": audit_list_tenant_mismatch_shelf,
            "book_get_non_member": audit_get_non_member,
            "book_get_tenant_mismatch": audit_get_tenant_mismatch,
        },
    }


async def main() -> None:
    result = await run()
    path = _artifact_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(path)


if __name__ == "__main__":
    asyncio.run(main())
