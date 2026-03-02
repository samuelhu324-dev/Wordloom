"""Library membership repository implementation (Infrastructure Adapter).

RBAC-lite v1 (S5A-2A): read membership role for (library_id, user_id).
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infra.database.models.library_membership_models import LibraryMembershipModel


class SQLAlchemyLibraryMembershipRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_role(self, *, library_id: UUID, user_id: UUID) -> Optional[str]:
        result = await self.session.execute(
            select(LibraryMembershipModel.role).where(
                LibraryMembershipModel.library_id == library_id,
                LibraryMembershipModel.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()


__all__ = ["SQLAlchemyLibraryMembershipRepository"]
