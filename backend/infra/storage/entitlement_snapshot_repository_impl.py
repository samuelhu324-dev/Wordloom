from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.app.modules.subscription_access.domain.models import EntitlementSnapshot
from infra.database.models.entitlement_snapshot_models import EntitlementSnapshotModel


def _encode_entitlements(entitlements: tuple[str, ...]) -> str:
    return ",".join(entitlements)


def _decode_entitlements(payload: str) -> tuple[str, ...]:
    if not payload:
        return tuple()
    return tuple(item for item in payload.split(",") if item)


class SQLAlchemyEntitlementSnapshotRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_library_id(self, library_id: UUID) -> EntitlementSnapshot | None:
        result = await self.session.execute(
            select(EntitlementSnapshotModel).where(EntitlementSnapshotModel.library_id == library_id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return EntitlementSnapshot(
            id=model.id,
            library_id=model.library_id,
            plan_code=model.plan_code,
            subscription_state=model.subscription_state,
            entitlements=_decode_entitlements(model.entitlements),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def create(
        self,
        *,
        library_id: UUID,
        plan_code: str,
        subscription_state: str,
        entitlements: tuple[str, ...],
    ) -> EntitlementSnapshot:
        snapshot = EntitlementSnapshot(
            library_id=library_id,
            plan_code=plan_code,
            subscription_state=subscription_state,
            entitlements=entitlements,
        )
        self.session.add(
            EntitlementSnapshotModel(
                id=snapshot.id,
                library_id=snapshot.library_id,
                plan_code=snapshot.plan_code,
                subscription_state=snapshot.subscription_state,
                entitlements=_encode_entitlements(snapshot.entitlements),
                created_at=snapshot.created_at,
                updated_at=snapshot.updated_at,
            )
        )
        await self.session.flush()
        return snapshot

    async def save(self, snapshot: EntitlementSnapshot) -> EntitlementSnapshot:
        result = await self.session.execute(
            select(EntitlementSnapshotModel).where(EntitlementSnapshotModel.id == snapshot.id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            model = EntitlementSnapshotModel(
                id=snapshot.id,
                library_id=snapshot.library_id,
                plan_code=snapshot.plan_code,
                subscription_state=snapshot.subscription_state,
                entitlements=_encode_entitlements(snapshot.entitlements),
                created_at=snapshot.created_at,
                updated_at=snapshot.updated_at,
            )
            self.session.add(model)
        else:
            model.plan_code = snapshot.plan_code
            model.subscription_state = snapshot.subscription_state
            model.entitlements = _encode_entitlements(snapshot.entitlements)
            model.updated_at = snapshot.updated_at
        await self.session.flush()
        return snapshot


__all__ = ["SQLAlchemyEntitlementSnapshotRepository"]