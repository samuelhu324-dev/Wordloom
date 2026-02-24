from __future__ import annotations

import asyncio
import datetime as dt
import os
import subprocess
import sys
import uuid
from typing import Any

import psycopg
from psycopg.types.json import Json
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from api.app.config.setting import get_settings
from api.app.dependencies_real import DIContainerReal

from ..registry import register
from ..types import DrillInputs, DrillResult


def _database_url_psycopg(database_url: str) -> str:
    return database_url.replace("postgresql+psycopg://", "postgresql://")


def _table_columns(conn: psycopg.Connection, table_name: str) -> set[str]:
    sql = (
        "select column_name "
        "from information_schema.columns "
        "where table_schema = 'public' and table_name = %s"
    )
    with conn.cursor() as cur:
        cur.execute(sql, (table_name,))
        return {row[0] for row in cur.fetchall()}


def _insert_row(conn: psycopg.Connection, *, table: str, values: dict[str, object]) -> None:
    cols = _table_columns(conn, table)
    if not cols:
        raise RuntimeError(f"table not found: {table}")

    filtered = {k: v for k, v in values.items() if k in cols}
    if not filtered:
        raise RuntimeError(f"no matching columns to insert into {table}")

    columns = list(filtered.keys())
    placeholders = ",".join(["%s"] * len(columns))
    columns_sql = ", ".join(columns)
    sql = f"insert into {table} ({columns_sql}) values ({placeholders})"

    with conn.cursor() as cur:
        cur.execute(sql, tuple(filtered[c] for c in columns))


async def _probe_query_service(*, database_url: str, book_id: uuid.UUID, expected_event_id: uuid.UUID) -> dict[str, Any]:
    engine = create_async_engine(database_url)
    try:
        async with AsyncSession(engine) as session:
            di = DIContainerReal(session)

            # A) Default path: chronicle_events
            os.environ.pop("MERGED_READ_ENABLED", None)
            get_settings.cache_clear()
            service_a = di.get_chronicle_query_service()
            events_a, total_a = await service_a.list_book_events(book_id=book_id, limit=50, offset=0)
            found_a = any(str(e.id) == str(expected_event_id) for e in events_a)

            # B) Cutover path: chronicle_entries
            os.environ["MERGED_READ_ENABLED"] = "1"
            get_settings.cache_clear()
            service_b = di.get_chronicle_query_service()
            events_b, total_b = await service_b.list_book_events(book_id=book_id, limit=50, offset=0)
            found_b = any(str(e.id) == str(expected_event_id) for e in events_b)

            return {
                "events_repo_total": int(total_a),
                "events_repo_found": bool(found_a),
                "entries_repo_total": int(total_b),
                "entries_repo_found": bool(found_b),
                "events_repo_first_ids": [str(e.id) for e in events_a[:3]],
                "entries_repo_first_ids": [str(e.id) for e in events_b[:3]],
            }
    finally:
        await engine.dispose()


@register("rehearsal_chronicle_read_switch_smoke")
@register("rehearsal-chronicle-read-switch-smoke")
def run(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    database_url = str(payload.get("database_url") or "").strip()
    if not database_url:
        return DrillResult(ok=False, errors=["DATABASE_URL is required"], meta={}, summary={})

    now = dt.datetime.now(dt.timezone.utc)

    event_id = uuid.uuid4()

    cs = _database_url_psycopg(database_url)
    try:
        with psycopg.connect(cs) as conn:
            library_id = uuid.uuid4()
            bookshelf_id = uuid.uuid4()
            book_id = uuid.uuid4()

            _insert_row(
                conn,
                table="libraries",
                values={
                    "id": library_id,
                    "user_id": uuid.uuid4(),
                    "name": "p3 read switch rehearsal library",
                    "description": "p3 chronicle read switch smoke",
                    "created_at": now,
                    "updated_at": now,
                    "last_activity_at": now,
                    "views_count": 0,
                    "pinned": False,
                },
            )
            _insert_row(
                conn,
                table="bookshelves",
                values={
                    "id": bookshelf_id,
                    "library_id": library_id,
                    "name": "p3 read switch rehearsal shelf",
                    "description": "p3 chronicle read switch smoke",
                    "is_basement": False,
                    "is_pinned": False,
                    "is_favorite": False,
                    "status": "active",
                    "book_count": 0,
                    "created_at": now,
                    "updated_at": now,
                },
            )
            _insert_row(
                conn,
                table="books",
                values={
                    "id": book_id,
                    "bookshelf_id": bookshelf_id,
                    "library_id": library_id,
                    "title": "p3 read switch rehearsal book",
                    "summary": "p3 chronicle read switch smoke",
                    "status": "draft",
                    "maturity": "seed",
                    "is_pinned": False,
                    "block_count": 0,
                    "maturity_score": 0,
                    "legacy_flag": False,
                    "manual_maturity_override": False,
                    "visit_count_90d": 0,
                    "created_at": now,
                    "updated_at": now,
                },
            )

            _insert_row(
                conn,
                table="chronicle_events",
                values={
                    "id": event_id,
                    "event_type": "book_created",
                    "book_id": book_id,
                    "block_id": None,
                    "actor_id": None,
                    "payload": Json({"seed": "p3_read_switch_smoke", "event_id": str(event_id)}),
                    "occurred_at": now,
                    "created_at": now,
                },
            )

            with conn.cursor() as cur:
                cur.execute("delete from chronicle_entries where id = %s", (event_id,))

            conn.commit()

    except Exception as exc:  # noqa: BLE001
        return DrillResult(ok=False, errors=[f"DB setup failed: {exc}"], meta={}, summary={})

    proc = subprocess.run(  # noqa: S603
        [
            sys.executable,
            "backend/scripts/legacy/rebuild_chronicle_entries.py",
            "--event-id",
            str(event_id),
        ],
        text=True,
        capture_output=True,
        env={**os.environ, "DATABASE_URL": database_url},
    )

    if proc.returncode != 0:
        return DrillResult(
            ok=False,
            errors=["rebuild_chronicle_entries failed"],
            meta={
                "event_id": str(event_id),
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "returncode": int(proc.returncode),
            },
            summary={},
        )

    try:
        probe = asyncio.run(_probe_query_service(database_url=database_url, book_id=book_id, expected_event_id=event_id))
    except Exception as exc:  # noqa: BLE001
        return DrillResult(
            ok=False,
            errors=[f"probe failed: {exc}"],
            meta={"event_id": str(event_id), "rebuild_stdout": proc.stdout, "rebuild_stderr": proc.stderr},
            summary={},
        )

    errors: list[str] = []
    if not probe.get("events_repo_found"):
        errors.append("events repo did not return seeded event")
    if not probe.get("entries_repo_found"):
        errors.append("entries repo did not return seeded event (MERGED_READ_ENABLED=1)")

    ok = not errors

    meta = {
        "ok": bool(ok),
        "errors": errors,
        "event_id": str(event_id),
        "book_id": str(book_id),
        "probe": probe,
        "rebuild_stdout": proc.stdout,
        "rebuild_stderr": proc.stderr,
    }
    summary = {
        "event_id": str(event_id),
        "book_id": str(book_id),
        "ok": bool(ok),
        "errors": errors,
    }

    return DrillResult(ok=ok, errors=errors, meta=meta, summary=summary)
