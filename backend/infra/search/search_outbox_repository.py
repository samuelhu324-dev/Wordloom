"""Search outbox repository.

This is an infra-only helper to encapsulate writes into `outbox_events`.
The worker/daemon can remain script-driven; this repo is mainly used by
projection writers to enqueue events within the same DB transaction.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from infra.outbox_unified.writer import OutboxWriter


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
        await OutboxWriter(self._db).enqueue(
            projection=SEARCH_PROJECTION,
            entity_type=entity_type,
            entity_id=entity_id,
            library_id=library_id,
            op=op,
            event_version=event_version,
        )


__all__ = ["SearchOutboxRepository"]
