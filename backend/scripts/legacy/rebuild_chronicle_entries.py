"""Rebuild chronicle_entries from chronicle_events.

This is the Chronicle analogue to rebuild_search_index.py, but DB->DB.

Usage (WSL2/bash or PowerShell):
  export DATABASE_URL='postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_test'
  python backend/scripts/rebuild_chronicle_entries.py --truncate

Options:
- --truncate: clears chronicle_entries before rebuild
- --emit-outbox: enqueue chronicle_outbox_events instead of writing entries directly
  (useful to validate the worker path)
"""

from __future__ import annotations

import argparse
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert

_HERE = Path(__file__).resolve()
_BACKEND_ROOT = _HERE.parents[2]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from infra.database.session import get_session_factory
from infra.database.models.chronicle_models import ChronicleEventModel
from infra.database.models.chronicle_entries_models import ChronicleEntryModel
from infra.database.models.outbox_event_models import OutboxEventModel
from infra.projection_framework.rebuild_template import run_rebuild, utc_now


PROJECTION_NAME = "chronicle_events_to_entries"


def _utc_now() -> datetime:
    # Preserve legacy naming for minimal diffs.
    return utc_now()


def _normalize_str(v: Any) -> Optional[str]:
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def _normalize_int(v: Any) -> Optional[int]:
    if v is None:
        return None
    if isinstance(v, int):
        return v
    s = str(v).strip()
    if not s:
        return None
    try:
        return int(s)
    except ValueError:
        return None


def _extract_envelope(event: ChronicleEventModel) -> tuple[int, str, str, str, Optional[str]]:
    # Payload is the source of truth. Columns may be present but defaulted
    # (e.g. schema_version=1, provenance/source/actor_kind='unknown') for older
    # rows or direct SQL inserts.
    payload = event.payload or {}
    if not isinstance(payload, dict):
        payload = {}

    payload_schema_version = _normalize_int(payload.get("schema_version"))
    payload_provenance = _normalize_str(payload.get("provenance"))
    payload_source = _normalize_str(payload.get("source"))
    payload_actor_kind = _normalize_str(payload.get("actor_kind"))
    payload_correlation_id = _normalize_str(payload.get("correlation_id"))

    col_schema_version = _normalize_int(getattr(event, "schema_version", None))
    col_provenance = _normalize_str(getattr(event, "provenance", None))
    col_source = _normalize_str(getattr(event, "source", None))
    col_actor_kind = _normalize_str(getattr(event, "actor_kind", None))
    col_correlation_id = _normalize_str(getattr(event, "correlation_id", None))

    schema_version = payload_schema_version or col_schema_version or 1
    provenance = payload_provenance or col_provenance or "unknown"
    source = payload_source or col_source or "unknown"
    actor_kind = payload_actor_kind or col_actor_kind or "unknown"
    correlation_id = payload_correlation_id or col_correlation_id

    return (schema_version, provenance, source, actor_kind, correlation_id)


def _summarize(event: ChronicleEventModel) -> str:
    # Minimal deterministic summary. Intentionally conservative; evolve later.
    if event.block_id:
        return f"{event.event_type} (book={event.book_id}, block={event.block_id})"
    return f"{event.event_type} (book={event.book_id})"


def _get_int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise RuntimeError(f"Invalid int env {name}={raw!r}") from exc


def _get_projection_version() -> int:
    # Default to v1 to match current behavior.
    return _get_int_env("CHRONICLE_PROJECTION_VERSION", _get_int_env("OUTBOX_PROJECTION_VERSION", 1))


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Rebuild chronicle_entries from chronicle_events")
    p.add_argument("--truncate", action="store_true", help="Delete all rows in chronicle_entries first")
    p.add_argument("--emit-outbox", action="store_true", help="Enqueue outbox_events (projection=chronicle_events_to_entries) instead of writing entries")
    p.add_argument("--limit", type=int, default=0, help="Optional limit (0 means no limit)")
    p.add_argument(
        "--event-id",
        type=str,
        default="",
        help="Optional: rebuild only a single chronicle_event id (UUID).",
    )
    return p.parse_args()


async def main_async() -> int:
    args = _parse_args()

    event_id: uuid.UUID | None = None
    if str(getattr(args, "event_id", "") or "").strip():
        try:
            event_id = uuid.UUID(str(args.event_id).strip())
        except Exception as exc:  # noqa: BLE001
            raise SystemExit(f"Invalid --event-id: {args.event_id!r}") from exc

    if not os.getenv("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL must be set")

    session_factory = await get_session_factory()

    async def _work(session) -> int:
        if args.truncate and not args.emit_outbox:
            await session.execute(delete(ChronicleEntryModel))

        if args.truncate and args.emit_outbox:
            await session.execute(delete(OutboxEventModel).where(OutboxEventModel.projection == PROJECTION_NAME))

        limit = int(args.limit or 0)
        stmt = select(ChronicleEventModel)
        if event_id is not None:
            stmt = stmt.where(ChronicleEventModel.id == event_id)
        stmt = stmt.order_by(ChronicleEventModel.occurred_at.asc(), ChronicleEventModel.id.asc())
        if limit > 0:
            stmt = stmt.limit(limit)

        result = await session.execute(stmt)
        events = list(result.scalars().all())

        now = _utc_now()
        projection_version = _get_projection_version()

        if args.emit_outbox:
            # Enqueue pending outbox rows. Worker will materialize chronicle_entries.
            for ev in events:
                session.add(
                    OutboxEventModel(
                        id=uuid.uuid4(),
                        projection=PROJECTION_NAME,
                        entity_type="chronicle_event",
                        entity_id=ev.id,
                        op="upsert",
                        event_version=0,
                        status="pending",
                        attempts=0,
                        replay_count=0,
                        created_at=now,
                        updated_at=now,
                        book_id=ev.book_id,
                    )
                )
        else:
            for ev in events:
                (schema_version, provenance, source, actor_kind, correlation_id) = _extract_envelope(ev)
                stmt2 = insert(ChronicleEntryModel).values(
                    id=ev.id,
                    event_type=ev.event_type,
                    book_id=ev.book_id,
                    block_id=ev.block_id,
                    actor_id=ev.actor_id,
                    occurred_at=ev.occurred_at,
                    created_at=ev.created_at,
                    payload=ev.payload or {},
                    schema_version=schema_version,
                    provenance=provenance,
                    source=source,
                    actor_kind=actor_kind,
                    correlation_id=correlation_id,
                    summary=_summarize(ev),
                    projection_version=projection_version,
                    updated_at=now,
                )
                stmt2 = stmt2.on_conflict_do_update(
                    index_elements=[ChronicleEntryModel.id],
                    set_={
                        "event_type": ev.event_type,
                        "book_id": ev.book_id,
                        "block_id": ev.block_id,
                        "actor_id": ev.actor_id,
                        "occurred_at": ev.occurred_at,
                        "created_at": ev.created_at,
                        "payload": ev.payload or {},
                        "schema_version": schema_version,
                        "provenance": provenance,
                        "source": source,
                        "actor_kind": actor_kind,
                        "correlation_id": correlation_id,
                        "summary": _summarize(ev),
                        "projection_version": projection_version,
                        "updated_at": now,
                    },
                )
                await session.execute(stmt2)

        return len(events)

    events_count = await run_rebuild(
        projection_name=PROJECTION_NAME,
        session_factory=session_factory,
        work=_work,
    )

    print(
        f"Rebuild OK: events={events_count} truncate={bool(args.truncate)} emit_outbox={bool(args.emit_outbox)}"
    )
    return 0


def main() -> None:
    import asyncio

    if sys.platform == "win32":
        # psycopg async is incompatible with ProactorEventLoop.
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    raise SystemExit(asyncio.run(main_async()))


if __name__ == "__main__":  # pragma: no cover
    main()
