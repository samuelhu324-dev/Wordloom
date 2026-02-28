"""Unified outbox ORM model.

This table is intended to replace both:
- search_outbox_events
- chronicle_outbox_events

by multiplexing via `projection`.

Note: Migration ownership lives under infra/database/migrations.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import BigInteger, CheckConstraint, Column, DateTime, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID

from .base import Base


class OutboxEventModel(Base):
    __tablename__ = "outbox_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)

    # Queue / projection identifier (e.g. search_index_to_elastic).
    projection = Column(Text, nullable=False)

    entity_type = Column(String(50), nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=False)

    op = Column(String(20), nullable=False)

    event_version = Column(BigInteger, nullable=False, index=True, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    processed_at = Column(DateTime(timezone=True), nullable=True)

    status = Column(String(20), nullable=False, default="pending")
    owner = Column(String(120), nullable=True)
    lease_until = Column(DateTime(timezone=True), nullable=True)
    processing_started_at = Column(DateTime(timezone=True), nullable=True)

    attempts = Column(Integer, nullable=False, default=0)
    next_retry_at = Column(DateTime(timezone=True), nullable=True)

    error_reason = Column(String(80), nullable=True)
    error = Column(Text, nullable=True)

    traceparent = Column(String(512), nullable=True)
    tracestate = Column(Text, nullable=True)

    replay_count = Column(Integer, nullable=False, default=0)
    last_replayed_at = Column(DateTime(timezone=True), nullable=True)
    last_replayed_by = Column(String(120), nullable=True)
    last_replayed_reason = Column(Text, nullable=True)

    payload = Column(JSONB(astext_type=Text()), nullable=True)

    # Scope keys (optional; used for claim isolation).
    library_id = Column(UUID(as_uuid=True), nullable=True)
    book_id = Column(UUID(as_uuid=True), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "status in ('pending','processing','done','failed')",
            name="ck_outbox_events_status",
        ),
        CheckConstraint(
            "payload IS NULL OR jsonb_typeof(payload) = 'object'",
            name="ck_outbox_events_payload_object",
        ),
        Index("idx_outbox_entity", "projection", "entity_type", "entity_id"),
        Index("idx_outbox_processed", "projection", "processed_at"),
        Index("idx_outbox_claim", "projection", "status", "next_retry_at", "lease_until", "event_version"),
        Index("idx_outbox_processing_started", "projection", "status", "processing_started_at"),
        Index("idx_outbox_error_reason", "projection", "status", "error_reason"),
        Index(
            "idx_outbox_scope_library_claim",
            "projection",
            "library_id",
            "status",
            "next_retry_at",
            "lease_until",
            "event_version",
        ),
        Index(
            "idx_outbox_scope_book_claim",
            "projection",
            "book_id",
            "status",
            "next_retry_at",
            "lease_until",
            "event_version",
        ),
    )


__all__ = ["OutboxEventModel"]
