"""Audit log ORM model (append-only).

v1 contract (S5A-1A):
- append-only (only INSERT)
- structured fields for tenant/actor/request correlation
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Column, DateTime, Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID

from .base import Base


class AuditLogModel(Base):
    __tablename__ = "audit_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)

    occurred_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    actor_user_id = Column(UUID(as_uuid=True), nullable=False)

    request_id = Column(String(64), nullable=False)

    action = Column(String(80), nullable=False)

    resource_type = Column(String(80), nullable=True)
    resource_id = Column(UUID(as_uuid=True), nullable=True)

    result = Column(String(32), nullable=False)
    reason = Column(String(80), nullable=True)

    meta_json = Column(JSONB(astext_type=Text()), nullable=True)

    __table_args__ = (
        Index("ix_audit_log_tenant_occurred_at", "tenant_id", "occurred_at"),
        Index("ix_audit_log_request_id", "request_id"),
        Index("ix_audit_log_actor_user_id", "actor_user_id"),
        Index("ix_audit_log_action", "action"),
        Index("ix_audit_log_resource", "resource_type", "resource_id"),
    )


__all__ = ["AuditLogModel"]
