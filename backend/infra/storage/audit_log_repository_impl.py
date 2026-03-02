"""Audit log repository implementation (Infrastructure Adapter).

Append-only v1: provide a minimal insert API and avoid exposing update/delete.
"""

from __future__ import annotations

import logging
from typing import Any, Mapping, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from infra.database.models.audit_log_models import AuditLogModel

logger = logging.getLogger(__name__)


class SQLAlchemyAuditLogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def append(
        self,
        *,
        tenant_id: UUID,
        actor_user_id: UUID,
        request_id: str,
        action: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[UUID] = None,
        result: str,
        reason: Optional[str] = None,
        meta_json: Optional[Mapping[str, Any]] = None,
    ) -> UUID:
        model = AuditLogModel(
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            request_id=request_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            result=result,
            reason=reason,
            meta_json=dict(meta_json) if meta_json is not None else None,
        )
        self.session.add(model)

        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        return model.id


__all__ = ["SQLAlchemyAuditLogRepository"]
