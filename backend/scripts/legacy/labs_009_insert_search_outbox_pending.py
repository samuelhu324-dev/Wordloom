"""Insert a deterministic pending row into a Search outbox table.

Prefers the unified table `outbox_events` when present (projection=search_index_to_elastic),
and falls back to legacy `search_outbox_events` for older schemas.

This helper exists to avoid shell quoting issues when triggering Labs-009 experiments.

Usage:
  # Windows PowerShell or WSL2 bash
  # (DATABASE_URL must be set)
    python backend/scripts/labs/labs_009_insert_search_outbox_pending.py

Optional env vars:
  OUTBOX_ENTITY_TYPE (default: book)
  OUTBOX_ENTITY_ID_PREFIX (default: labs-009)
  OUTBOX_OP (default: upsert)
  OUTBOX_PAYLOAD_JSON (default: {})
    OUTBOX_CREATE_SEARCH_INDEX_ROW (default: 0)  # if 1, upsert a matching row into `search_index`
    OUTBOX_SEARCH_INDEX_TEXT (default: labs-009 <outbox_event_id>)
    OUTBOX_LIBRARY_ID (optional UUID)
"""

from __future__ import annotations

import datetime as dt
import os
import uuid
import json

import psycopg
SEARCH_PROJECTION = "search_index_to_elastic"


SUPPLY_EVIDENCE_PREFIX = "SUPPLY_EVIDENCE_JSON:"


def _truthy(raw: str | None) -> bool:
    v = (raw or "").strip().lower()
    return v in {"1", "true", "yes", "y", "on"}


def _adapt_param(value: object) -> object:
    """Adapt Python objects to types psycopg can send.

    psycopg3 doesn't automatically adapt `dict`/`list` to JSON.
    """

    if isinstance(value, (dict, list)):
        try:
            from psycopg.types.json import Json  # type: ignore

            return Json(value)
        except Exception:
            return json.dumps(value)
    return value



def _database_url_psycopg(database_url: str) -> str:
    # Allow reuse of SQLAlchemy-style URL.
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


def _table_column_types(conn: psycopg.Connection, table_name: str) -> dict[str, str]:
    """Return a best-effort mapping of column -> type identifier.

    Prefer `udt_name` when available (e.g., 'uuid').
    """

    sql = (
        "select column_name, udt_name "
        "from information_schema.columns "
        "where table_schema = 'public' and table_name = %s"
    )
    with conn.cursor() as cur:
        cur.execute(sql, (table_name,))
        return {row[0]: row[1] for row in cur.fetchall()}


def _table_exists(conn: psycopg.Connection, table_name: str) -> bool:
    return bool(_table_columns(conn, table_name))


def _insert_pending(conn: psycopg.Connection, table_name: str, values: dict[str, object]) -> None:
    cols = _table_columns(conn, table_name)
    filtered = {k: v for k, v in values.items() if k in cols}
    if "id" not in filtered:
        raise RuntimeError(f"{table_name}.id column not found")
    if "status" not in filtered:
        raise RuntimeError(f"{table_name}.status column not found")

    columns = list(filtered.keys())
    placeholders = ",".join(["%s"] * len(columns))
    columns_sql = ", ".join(columns)
    sql = f"insert into {table_name} ({columns_sql}) values ({placeholders})"

    with conn.cursor() as cur:
        cur.execute(sql, tuple(_adapt_param(filtered[c]) for c in columns))


def _upsert_search_index(conn: psycopg.Connection, values: dict[str, object]) -> None:
    cols = _table_columns(conn, "search_index")
    if not cols:
        raise RuntimeError("search_index table not found")

    filtered = {k: v for k, v in values.items() if k in cols}
    required = {"entity_type", "entity_id", "text"}
    missing = [k for k in required if k not in filtered]
    if missing:
        raise RuntimeError(f"search_index missing required columns: {missing}")

    # Ensure we provide an id if the column exists and the DB has no default.
    if "id" in cols and "id" not in filtered:
        filtered["id"] = uuid.uuid4()

    columns = list(filtered.keys())
    placeholders = ",".join(["%s"] * len(columns))
    columns_sql = ", ".join(columns)

    # Conflict target matches the model's unique constraint.
    conflict_target = "(entity_type, entity_id)" if {"entity_type", "entity_id"}.issubset(cols) else None
    if conflict_target is None:
        raise RuntimeError("search_index missing conflict target columns")

    # Update everything except identity / conflict key columns.
    non_updatable = {"id", "entity_type", "entity_id"}
    update_cols = [c for c in columns if c not in non_updatable]
    if update_cols:
        set_sql = ", ".join([f"{c} = EXCLUDED.{c}" for c in update_cols])
        sql = (
            f"insert into search_index ({columns_sql}) values ({placeholders}) "
            f"on conflict {conflict_target} do update set {set_sql}"
        )
    else:
        sql = (
            f"insert into search_index ({columns_sql}) values ({placeholders}) "
            f"on conflict {conflict_target} do nothing"
        )

    with conn.cursor() as cur:
        cur.execute(sql, tuple(_adapt_param(filtered[c]) for c in columns))


def main() -> None:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL is required")

    raw_insert_count = (os.environ.get("OUTBOX_INSERT_COUNT") or "1").strip()
    try:
        insert_count = int(raw_insert_count)
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"Invalid OUTBOX_INSERT_COUNT={raw_insert_count!r}") from exc
    if insert_count <= 0:
        raise SystemExit("OUTBOX_INSERT_COUNT must be >= 1")

    entity_type = os.environ.get("OUTBOX_ENTITY_TYPE", "book")
    entity_id_prefix = os.environ.get("OUTBOX_ENTITY_ID_PREFIX", "labs-009")
    entity_id_raw = os.environ.get("OUTBOX_ENTITY_ID")
    op = os.environ.get("OUTBOX_OP", "upsert")
    payload_json = os.environ.get("OUTBOX_PAYLOAD_JSON", "{}")
    create_search_index_row = (os.environ.get("OUTBOX_CREATE_SEARCH_INDEX_ROW", "0") or "0").strip().lower() in {
        "1",
        "true",
        "yes",
        "y",
        "on",
    }
    search_index_text = os.environ.get("OUTBOX_SEARCH_INDEX_TEXT")
    library_id_raw = os.environ.get("OUTBOX_LIBRARY_ID")
    traceparent = os.environ.get("OUTBOX_TRACEPARENT")
    tracestate = os.environ.get("OUTBOX_TRACESTATE")
    emit_supply_evidence = _truthy(os.environ.get("OUTBOX_SUPPLY_EVIDENCE_JSON"))

    cs = _database_url_psycopg(database_url)
    with psycopg.connect(cs) as conn:
        table_name = "outbox_events" if _table_exists(conn, "outbox_events") else "search_outbox_events"
        col_types = _table_column_types(conn, table_name)

        if emit_supply_evidence:
            evidence_obj = {
                "target_table": table_name,
                "projection": (SEARCH_PROJECTION if table_name == "outbox_events" else None),
                "insert_count": int(insert_count),
                "entity_type": str(entity_type),
                "op": str(op),
                "create_search_index_row": bool(create_search_index_row),
                "fallback": {
                    "used": bool(table_name != "outbox_events"),
                    "reason": ("outbox_events_table_missing" if table_name != "outbox_events" else None),
                },
            }
            print(SUPPLY_EVIDENCE_PREFIX + json.dumps(evidence_obj, ensure_ascii=False, sort_keys=True))

        raw_event_version = (os.environ.get("OUTBOX_EVENT_VERSION") or "").strip()
        ids: list[str] = []

        for _i in range(insert_count):
            outbox_event_uuid = uuid.uuid4()
            outbox_event_id = str(outbox_event_uuid)
            now = dt.datetime.now(dt.timezone.utc)

            if raw_event_version:
                event_version = int(raw_event_version)
            else:
                # Default to a monotonic-ish microsecond timestamp so the row orders sensibly.
                event_version = int(now.timestamp() * 1_000_000)

            entity_id_value: object
            if "entity_id" in col_types and col_types["entity_id"] == "uuid":
                if entity_id_raw:
                    entity_id_value = uuid.UUID(entity_id_raw)
                else:
                    entity_id_value = uuid.uuid4()
            else:
                if entity_id_raw:
                    entity_id_value = entity_id_raw
                else:
                    entity_id_value = f"{entity_id_prefix}-entity-{outbox_event_id[:8]}"

            # Parse payload once per insert to support json/jsonb columns.
            try:
                payload_obj: object = json.loads(payload_json)
            except Exception:
                payload_obj = {}

            values: dict[str, object] = {
                "id": outbox_event_id,
                "projection": SEARCH_PROJECTION,
                "entity_type": entity_type,
                "entity_id": entity_id_value,
                "op": op,
                "event_version": event_version,
                "status": "pending",
                "attempts": 0,
                "replay_count": 0,
                "created_at": now,
                "updated_at": now,
                # Some schemas include payload-like columns; we only insert if present.
                "payload": payload_obj,
                "payload_json": payload_json,
                "data": payload_json,
                # Trace context (optional).
                "traceparent": traceparent,
                "tracestate": tracestate,
            }

            # If inserting into unified outbox, ensure required projection is present.
            if table_name != "outbox_events":
                values.pop("projection", None)

            if create_search_index_row:
                lib_id_val = None
                if library_id_raw:
                    try:
                        lib_id_val = uuid.UUID(library_id_raw)
                    except Exception as exc:  # noqa: BLE001
                        raise SystemExit(f"Invalid OUTBOX_LIBRARY_ID={library_id_raw!r}") from exc

                text_val = search_index_text or f"labs-009 {outbox_event_id}"
                search_values: dict[str, object] = {
                    "entity_type": entity_type,
                    "entity_id": entity_id_value,
                    "library_id": lib_id_val,
                    "text": text_val,
                    "snippet": text_val[:200],
                    "rank_score": 0.0,
                    "created_at": now,
                    "updated_at": now,
                    "event_version": event_version,
                }
                _upsert_search_index(conn, search_values)

            _insert_pending(conn, table_name, values)
            ids.append(outbox_event_id)

        conn.commit()

    for outbox_event_id in ids:
        print(outbox_event_id)


if __name__ == "__main__":
    main()
