"""Library membership ORM model.

RBAC-lite v1 (S5A-2A): owner/admin/member per (library_id, user_id).
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class LibraryMembershipModel(Base):
    __tablename__ = "library_memberships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)

    library_id = Column(
        UUID(as_uuid=True),
        ForeignKey("libraries.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)

    role = Column(String(20), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "library_id",
            "user_id",
            name="uq_library_memberships_library_user",
        ),
        CheckConstraint(
            "role in ('owner','admin','member')",
            name="ck_library_memberships_role",
        ),
        Index("ix_library_memberships_library_user", "library_id", "user_id"),
    )


__all__ = ["LibraryMembershipModel"]
