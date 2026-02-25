from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
import uuid
from typing import Any

import psycopg
from psycopg.types.json import Json

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


def _fetch_one_dict(conn: psycopg.Connection, sql: str, params: tuple[object, ...]) -> dict[str, Any] | None:
    with conn.cursor() as cur:
        cur.execute(sql, params)
        row = cur.fetchone()
        if row is None:
            return None
        cols = [d.name for d in cur.description or []]
        return {cols[i]: row[i] for i in range(len(cols))}


@register("rehearsal_chronicle_entries_envelope_backfill")
@register("rehearsal-chronicle-entries-envelope-backfill")
def run(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    database_url = str(payload.get("database_url") or "").strip()
    if not database_url:
        return DrillResult(ok=False, errors=["DATABASE_URL is required"], meta={}, summary={})

    now = dt.datetime.now(dt.timezone.utc)

    # Expected values are written ONLY in payload to ensure backfill logic does not
    # rely on chronicle_events envelope columns being populated.
    event_id = uuid.uuid4()
    expected = {
        "schema_version": 7,
        "provenance": "p2-c2",
        "source": "p2-c2",
        "actor_kind": "system",
        "correlation_id": f"p2-c2-{event_id}",
    }

    cs = _database_url_psycopg(database_url)
    try:
        with psycopg.connect(cs) as conn:
            # Validate target columns exist (migration prerequisite).
            entries_cols = _table_columns(conn, "chronicle_entries")
            required_entries_cols = {
                "schema_version",
                "provenance",
                "source",
                "actor_kind",
                "correlation_id",
            }
            missing = sorted(required_entries_cols - entries_cols)
            if missing:
                return DrillResult(
                    ok=False,
                    errors=[f"chronicle_entries missing envelope columns: {missing}"],
                    meta={"missing_columns": missing},
                    summary={},
                )

            library_id = uuid.uuid4()
            bookshelf_id = uuid.uuid4()
            book_id = uuid.uuid4()

            # Minimal FK chain.
            _insert_row(
                conn,
                table="libraries",
                values={
                    "id": library_id,
                    "user_id": uuid.uuid4(),
                    "name": "p2-c2 rehearsal library",
                    "description": "p2-c2 envelope backfill rehearsal",
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
                    "name": "p2-c2 rehearsal shelf",
                    "description": "p2-c2 envelope backfill rehearsal",
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
                    "title": "p2-c2 rehearsal book",
                    "summary": "p2-c2 envelope backfill rehearsal",
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

            # Insert chronicle_event with envelope values ONLY in payload.
            _insert_row(
                conn,
                table="chronicle_events",
                values={
                    "id": event_id,
                    "event_type": "p2-c2.envelope_backfill",
                    "book_id": book_id,
                    "block_id": None,
                    "actor_id": None,
                    "payload": Json(expected),
                    "occurred_at": now,
                    "created_at": now,
                    # Intentionally omit envelope columns.
                },
            )

            # Ensure the projection row does not exist prior to rehearsal.
            with conn.cursor() as cur:
                cur.execute("delete from chronicle_entries where id = %s", (event_id,))

            conn.commit()

    except Exception as exc:  # noqa: BLE001
        return DrillResult(ok=False, errors=[f"DB setup failed: {exc}"], meta={}, summary={})

    # Backfill / rebuild only this event.
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

    # Probe results.
    try:
        with psycopg.connect(_database_url_psycopg(database_url)) as conn:
            row = _fetch_one_dict(
                conn,
                """
                select schema_version, provenance, source, actor_kind, correlation_id
                from chronicle_entries
                where id = %s
                """,
                (event_id,),
            )
    except Exception as exc:  # noqa: BLE001
        return DrillResult(ok=False, errors=[f"probe failed: {exc}"], meta={"event_id": str(event_id)}, summary={})

    if row is None:
        return DrillResult(
            ok=False,
            errors=["chronicle_entries row not found after rebuild"],
            meta={"event_id": str(event_id)},
            summary={},
        )

    observed = {
        "schema_version": int(row.get("schema_version") or 0),
        "provenance": (row.get("provenance") or ""),
        "source": (row.get("source") or ""),
        "actor_kind": (row.get("actor_kind") or ""),
        "correlation_id": row.get("correlation_id"),
    }

    errors: list[str] = []
    for k, v in expected.items():
        if observed.get(k) != v:
            errors.append(f"mismatch {k}: expected={v!r} observed={observed.get(k)!r}")

    for k in ("provenance", "source", "actor_kind"):
        if str(observed.get(k) or "").strip().lower() == "unknown":
            errors.append(f"envelope field {k} is still 'unknown'")

    ok = not errors
    meta = {
        "ok": bool(ok),
        "errors": errors,
        "event_id": str(event_id),
        "expected": expected,
        "observed": observed,
        "rebuild_stdout": proc.stdout,
        "rebuild_stderr": proc.stderr,
    }
    summary = {
        "event_id": str(event_id),
        "ok": bool(ok),
        "errors": errors,
    }

    return DrillResult(ok=ok, errors=errors, meta=meta, summary=summary)
