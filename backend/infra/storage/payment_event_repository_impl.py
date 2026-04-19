from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.app.modules.subscription_access.domain import PaymentEvent, PaymentEventType
from infra.database.models.payment_event_models import PaymentEventModel


class SQLAlchemyPaymentEventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def append(self, event: PaymentEvent) -> PaymentEvent:
        self.session.add(
            PaymentEventModel(
                id=event.id,
                subscription_id=event.subscription_id,
                library_id=event.library_id,
                event_type=event.event_type.value,
                created_at=event.created_at,
            )
        )
        await self.session.flush()
        return event

    async def list_by_library_id(self, library_id: UUID) -> list[PaymentEvent]:
        result = await self.session.execute(
            select(PaymentEventModel)
            .where(PaymentEventModel.library_id == library_id)
            .order_by(PaymentEventModel.created_at.asc())
        )
        items = result.scalars().all()
        return [
            PaymentEvent(
                id=item.id,
                subscription_id=item.subscription_id,
                library_id=item.library_id,
                event_type=PaymentEventType(item.event_type),
                created_at=item.created_at,
            )
            for item in items
        ]


__all__ = ["SQLAlchemyPaymentEventRepository"]