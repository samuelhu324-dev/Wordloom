from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.app.modules.subscription_access.domain.models import Subscription
from infra.database.models.subscription_models import SubscriptionModel


class SQLAlchemySubscriptionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_library_id(self, library_id: UUID) -> Subscription | None:
        result = await self.session.execute(
            select(SubscriptionModel).where(SubscriptionModel.library_id == library_id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return Subscription(
            id=model.id,
            library_id=model.library_id,
            plan_code=model.plan_code,
            state=model.state,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def save(self, subscription: Subscription) -> Subscription:
        result = await self.session.execute(
            select(SubscriptionModel).where(SubscriptionModel.id == subscription.id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            model = SubscriptionModel(
                id=subscription.id,
                library_id=subscription.library_id,
                plan_code=subscription.plan_code,
                state=subscription.state,
                created_at=subscription.created_at,
                updated_at=subscription.updated_at,
            )
            self.session.add(model)
        else:
            model.plan_code = subscription.plan_code
            model.state = subscription.state
            model.updated_at = subscription.updated_at
        await self.session.flush()
        return subscription


__all__ = ["SQLAlchemySubscriptionRepository"]