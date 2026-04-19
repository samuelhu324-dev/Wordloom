from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class EntitlementSnapshotModel(Base):
    __tablename__ = "entitlement_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    library_id = Column(UUID(as_uuid=True), ForeignKey("libraries.id", ondelete="CASCADE"), nullable=False, unique=True)
    plan_code = Column(String(50), ForeignKey("plan_catalog.code"), nullable=False)
    subscription_state = Column(String(30), nullable=False)
    entitlements = Column(Text, nullable=False, default="")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (Index("ix_entitlement_snapshots_library_state", "library_id", "subscription_state"),)


__all__ = ["EntitlementSnapshotModel"]