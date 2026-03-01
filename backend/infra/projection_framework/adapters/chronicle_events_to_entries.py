from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Mapping

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from infra.database.models.chronicle_entries_models import ChronicleEntryModel
from infra.database.models.chronicle_models import ChronicleEventModel
from infra.database.models.outbox_event_models import OutboxEventModel
from infra.outbox_core.payload_contract import require_mapping, require_schema_version


PROJECTION_NAME = "chronicle_events_to_entries"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_str(value: Any) -> str | None:
    if value is None:
        return None
    s = str(value).strip()
    return s or None


def _extract_envelope(event: ChronicleEventModel) -> tuple[int, str, str, str, str | None]:
    payload: Mapping[str, Any] = require_mapping(event.payload, projection=PROJECTION_NAME, field_name="payload")
    schema_version = require_schema_version(payload, projection=PROJECTION_NAME, supported_versions={1})

    payload_provenance = _normalize_str(payload.get("provenance"))
    payload_source = _normalize_str(payload.get("source"))
    payload_actor_kind = _normalize_str(payload.get("actor_kind"))
    payload_correlation_id = _normalize_str(payload.get("correlation_id"))

    col_provenance = _normalize_str(getattr(event, "provenance", None))
    col_source = _normalize_str(getattr(event, "source", None))
    col_actor_kind = _normalize_str(getattr(event, "actor_kind", None))
    col_correlation_id = _normalize_str(getattr(event, "correlation_id", None))

    provenance = payload_provenance or col_provenance or "unknown"
    source = payload_source or col_source or "unknown"
    actor_kind = payload_actor_kind or col_actor_kind or "unknown"
    correlation_id = payload_correlation_id or col_correlation_id

    return (schema_version, provenance, source, actor_kind, correlation_id)


def _summarize(event: ChronicleEventModel) -> str:
    block_id = getattr(event, "block_id", None)
    if block_id:
        return f"{event.event_type} (book={event.book_id}, block={block_id})"
    return f"{event.event_type} (book={event.book_id})"


def _projection_version() -> int:
    # Preserve legacy behavior: default v1.
    raw = (os.getenv("CHRONICLE_PROJECTION_VERSION") or os.getenv("OUTBOX_PROJECTION_VERSION") or "").strip()
    if not raw:
        return 1
    return int(raw)


async def apply(*, ev: OutboxEventModel, session: AsyncSession) -> None:
    """Materialize chronicle_entries from chronicle_events.

    Contract:
    - Outbox entity_id points to chronicle_events.id
    - Only supports op=upsert (idempotent)
    """

    op = str(getattr(ev, "op", ""))
    if op != "upsert":
        raise ValueError(f"Unsupported outbox op for {PROJECTION_NAME}: {op!r}")

    event = (
        await session.execute(select(ChronicleEventModel).where(ChronicleEventModel.id == ev.entity_id))
    ).scalar_one_or_none()
    if event is None:
        raise ValueError(f"Missing chronicle_event: {ev.entity_id}")

    now = _utc_now()
    projection_version = _projection_version()
    (schema_version, provenance, source, actor_kind, correlation_id) = _extract_envelope(event)

    stmt = insert(ChronicleEntryModel).values(
        id=event.id,
        event_type=event.event_type,
        book_id=event.book_id,
        block_id=event.block_id,
        actor_id=event.actor_id,
        occurred_at=event.occurred_at,
        created_at=event.created_at,
        payload=event.payload or {},
        schema_version=schema_version,
        provenance=provenance,
        source=source,
        actor_kind=actor_kind,
        correlation_id=correlation_id,
        summary=_summarize(event),
        projection_version=projection_version,
        updated_at=now,
    )

    stmt = stmt.on_conflict_do_update(
        index_elements=[ChronicleEntryModel.id],
        set_={
            "event_type": event.event_type,
            "book_id": event.book_id,
            "block_id": event.block_id,
            "actor_id": event.actor_id,
            "occurred_at": event.occurred_at,
            "created_at": event.created_at,
            "payload": event.payload or {},
            "schema_version": schema_version,
            "provenance": provenance,
            "source": source,
            "actor_kind": actor_kind,
            "correlation_id": correlation_id,
            "summary": _summarize(event),
            "projection_version": projection_version,
            "updated_at": now,
        },
    )

    await session.execute(stmt)
