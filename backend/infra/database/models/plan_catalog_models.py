from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, String

from .base import Base


class PlanCatalogModel(Base):
    __tablename__ = "plan_catalog"

    code = Column(String(50), primary_key=True, nullable=False)
    display_name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


__all__ = ["PlanCatalogModel"]