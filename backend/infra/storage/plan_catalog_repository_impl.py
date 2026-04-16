from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.app.modules.subscription_access.domain.models import Plan
from infra.database.models.plan_catalog_models import PlanCatalogModel


class SQLAlchemyPlanCatalogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_code(self, code: str) -> Plan | None:
        result = await self.session.execute(select(PlanCatalogModel).where(PlanCatalogModel.code == code))
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return Plan(code=model.code, display_name=model.display_name)


__all__ = ["SQLAlchemyPlanCatalogRepository"]