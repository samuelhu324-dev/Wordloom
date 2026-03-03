"""Library membership repository implementation (Infrastructure Adapter).

RBAC-lite v1 (S5A-2A):
- read membership role for (library_id, user_id)
- write (grant/revoke) helpers for drills/admin endpoints
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import delete, select
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

    async def grant_role(self, *, library_id: UUID, user_id: UUID, role: str) -> UUID:
        normalized = str(role).strip().lower()
        if normalized not in {"owner", "admin", "member"}:
            raise ValueError("invalid role")

        result = await self.session.execute(
            select(LibraryMembershipModel).where(
                LibraryMembershipModel.library_id == library_id,
                LibraryMembershipModel.user_id == user_id,
            )
        )
        model = result.scalar_one_or_none()
        if model is None:
            model = LibraryMembershipModel(
                library_id=library_id,
                user_id=user_id,
                role=normalized,
            )
            self.session.add(model)
        else:
            model.role = normalized

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return model.id

    async def revoke(self, *, library_id: UUID, user_id: UUID) -> bool:
        result = await self.session.execute(
            delete(LibraryMembershipModel).where(
                LibraryMembershipModel.library_id == library_id,
                LibraryMembershipModel.user_id == user_id,
            )
        )
        deleted = bool(getattr(result, "rowcount", 0))
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        return deleted


__all__ = ["SQLAlchemyLibraryMembershipRepository"]
