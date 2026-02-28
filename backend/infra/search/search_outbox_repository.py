"""Search outbox repository.

This is an infra-only helper to encapsulate writes into `outbox_events`.
The worker/daemon can remain script-driven; this repo is mainly used by
projection writers to enqueue events within the same DB transaction.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID
from uuid import uuid4

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from infra.database.models.outbox_event_models import OutboxEventModel
from infra.observability.tracing import inject_trace_context


SEARCH_PROJECTION = "search_index_to_elastic"


class SearchOutboxRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def enqueue(
        self,
        *,
        entity_type: str,
        entity_id: UUID,
        library_id: UUID | None = None,
        op: str,
        event_version: int,
    ) -> None:
        now = datetime.now(timezone.utc)
        outbox_id = uuid4()
        traceparent, tracestate = inject_trace_context()
        await self._db.execute(
            pg_insert(OutboxEventModel).values(
                id=outbox_id,
                projection=SEARCH_PROJECTION,
                entity_type=entity_type,
                entity_id=entity_id,
                library_id=library_id,
                op=op,
                event_version=event_version,
                traceparent=traceparent,
                tracestate=tracestate,
                created_at=now,
                updated_at=now,
                status="pending",
                attempts=0,
                replay_count=0,
            )
        )


__all__ = ["SearchOutboxRepository"]
