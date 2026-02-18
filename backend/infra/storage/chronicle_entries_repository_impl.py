"""Chronicle Entries Repository Implementation

Read-side adapter backed by the chronicle_entries projection table.

This repository exists to support a safe read-switch (shadow/dual-run):
- Default (MERGED_READ_ENABLED=0): read from chronicle_events (source of truth)
- Enabled (MERGED_READ_ENABLED=1): read from chronicle_entries (projection)

Write operations are intentionally unsupported here.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, Sequence, Tuple, List
from uuid import UUID

from sqlalchemy import and_, asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.app.modules.chronicle.domain import ChronicleEvent, ChronicleEventType, ChronicleRepositoryPort
from api.app.modules.chronicle.exceptions import ChronicleRepositoryError
from infra.database.models import ChronicleEntryModel


class SQLAlchemyChronicleEntriesRepository(ChronicleRepositoryPort):
    """Read-only Chronicle repository backed by chronicle_entries."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, event: ChronicleEvent) -> ChronicleEvent:
        raise ChronicleRepositoryError("chronicle_entries is read-only; use chronicle_events repository for writes")

    async def list_by_book(
        self,
        book_id: UUID,
        event_types: Optional[Sequence[ChronicleEventType]] = None,
        limit: int = 50,
        offset: int = 0,
        order_desc: bool = True,
    ) -> Tuple[List[ChronicleEvent], int]:
        try:
            filters = [ChronicleEntryModel.book_id == book_id]
            if event_types:
                filters.append(
                    ChronicleEntryModel.event_type.in_([et.value for et in event_types])
                )

            order_by = (
                (desc(ChronicleEntryModel.occurred_at), desc(ChronicleEntryModel.id))
                if order_desc
                else (asc(ChronicleEntryModel.occurred_at), asc(ChronicleEntryModel.id))
            )

            count_stmt = select(func.count(ChronicleEntryModel.id)).where(and_(*filters))
            total_result = await self._session.execute(count_stmt)
            total = int(total_result.scalar() or 0)

            stmt = (
                select(ChronicleEntryModel)
                .where(and_(*filters))
                .order_by(*order_by)
                .offset(offset)
                .limit(limit)
            )
            result = await self._session.execute(stmt)
            models = result.scalars().all()
            return [self._to_domain(model) for model in models], total
        except Exception as exc:
            raise ChronicleRepositoryError(str(exc)) from exc

    async def list_by_time_range(
        self,
        start: datetime,
        end: datetime,
        event_types: Optional[Sequence[ChronicleEventType]] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Tuple[List[ChronicleEvent], int]:
        try:
            filters = [ChronicleEntryModel.occurred_at.between(start, end)]
            if event_types:
                filters.append(
                    ChronicleEntryModel.event_type.in_([et.value for et in event_types])
                )

            count_stmt = select(func.count(ChronicleEntryModel.id)).where(and_(*filters))
            total_result = await self._session.execute(count_stmt)
            total = int(total_result.scalar() or 0)

            stmt = (
                select(ChronicleEntryModel)
                .where(and_(*filters))
                .order_by(desc(ChronicleEntryModel.occurred_at), desc(ChronicleEntryModel.id))
                .offset(offset)
                .limit(limit)
            )
            result = await self._session.execute(stmt)
            models = result.scalars().all()
            return [self._to_domain(model) for model in models], total
        except Exception as exc:
            raise ChronicleRepositoryError(str(exc)) from exc

    def _to_domain(self, model: ChronicleEntryModel) -> ChronicleEvent:
        return ChronicleEvent(
            id=model.id,
            event_type=ChronicleEventType(model.event_type),
            book_id=model.book_id,
            block_id=model.block_id,
            actor_id=model.actor_id,
            payload=model.payload or {},
            occurred_at=model.occurred_at,
            created_at=model.created_at,
        )
