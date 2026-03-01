"""Unified outbox writer template.

A dependency-light helper to enqueue rows into `outbox_events` in the same DB
transaction as the source-of-truth write.

This is the "writer template" counterpart to outbox_core (consumer/runtime).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import UUID, uuid4

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from infra.database.models.outbox_event_models import OutboxEventModel


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _inject_trace_context() -> tuple[str | None, str | None]:
    try:
        from infra.observability.tracing import inject_trace_context

        return inject_trace_context()
    except Exception:
        return (None, None)


class OutboxWriter:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def enqueue(
        self,
        *,
        projection: str,
        entity_type: str,
        entity_id: UUID,
        op: str,
        event_version: int,
        library_id: UUID | None = None,
        book_id: UUID | None = None,
        payload: Mapping[str, Any] | None = None,
    ) -> UUID:
        now = _utc_now()
        outbox_id = uuid4()
        traceparent, tracestate = _inject_trace_context()

        await self._db.execute(
            pg_insert(OutboxEventModel).values(
                id=outbox_id,
                projection=str(projection),
                entity_type=str(entity_type),
                entity_id=entity_id,
                op=str(op),
                event_version=int(event_version),
                payload=(dict(payload) if payload is not None else None),
                library_id=library_id,
                book_id=book_id,
                traceparent=traceparent,
                tracestate=tracestate,
                created_at=now,
                updated_at=now,
                status="pending",
                attempts=0,
                replay_count=0,
            )
        )

        return outbox_id


__all__ = ["OutboxWriter"]
