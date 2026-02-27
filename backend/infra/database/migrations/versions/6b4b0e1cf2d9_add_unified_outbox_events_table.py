"""Add unified outbox_events table.

Revision ID: 6b4b0e1cf2d9
Revises: 2efcb7462da4
Create Date: 2026-02-27

"""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "6b4b0e1cf2d9"
down_revision: Union[str, Sequence[str], None] = "2efcb7462da4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "outbox_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("projection", sa.Text(), nullable=False),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("op", sa.String(length=20), nullable=False),
        sa.Column("event_version", sa.BigInteger(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("owner", sa.String(length=120), nullable=True),
        sa.Column("lease_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("processing_started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("next_retry_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_reason", sa.String(length=80), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("traceparent", sa.String(length=512), nullable=True),
        sa.Column("tracestate", sa.Text(), nullable=True),
        sa.Column("replay_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_replayed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_replayed_by", sa.String(length=120), nullable=True),
        sa.Column("last_replayed_reason", sa.Text(), nullable=True),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("library_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("book_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.CheckConstraint(
            "status in ('pending','processing','done','failed')",
            name="ck_outbox_events_status",
        ),
        sa.CheckConstraint(
            "payload IS NULL OR jsonb_typeof(payload) = 'object'",
            name="ck_outbox_events_payload_object",
        ),
    )

    # Keep model-level defaults; drop server defaults where appropriate.
    op.alter_column("outbox_events", "event_version", server_default=None)
    op.alter_column("outbox_events", "attempts", server_default=None)
    op.alter_column("outbox_events", "replay_count", server_default=None)

    op.create_index(
        "idx_outbox_entity",
        "outbox_events",
        ["projection", "entity_type", "entity_id"],
        unique=False,
    )
    op.create_index(
        "idx_outbox_processed",
        "outbox_events",
        ["projection", "processed_at"],
        unique=False,
    )
    op.create_index(
        "idx_outbox_claim",
        "outbox_events",
        ["projection", "status", "next_retry_at", "lease_until", "event_version"],
        unique=False,
    )
    op.create_index(
        "idx_outbox_processing_started",
        "outbox_events",
        ["projection", "status", "processing_started_at"],
        unique=False,
    )
    op.create_index(
        "idx_outbox_error_reason",
        "outbox_events",
        ["projection", "status", "error_reason"],
        unique=False,
    )
    op.create_index(
        "idx_outbox_scope_library_claim",
        "outbox_events",
        ["projection", "library_id", "status", "next_retry_at", "lease_until", "event_version"],
        unique=False,
    )
    op.create_index(
        "idx_outbox_scope_book_claim",
        "outbox_events",
        ["projection", "book_id", "status", "next_retry_at", "lease_until", "event_version"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("idx_outbox_scope_book_claim", table_name="outbox_events")
    op.drop_index("idx_outbox_scope_library_claim", table_name="outbox_events")
    op.drop_index("idx_outbox_error_reason", table_name="outbox_events")
    op.drop_index("idx_outbox_processing_started", table_name="outbox_events")
    op.drop_index("idx_outbox_claim", table_name="outbox_events")
    op.drop_index("idx_outbox_processed", table_name="outbox_events")
    op.drop_index("idx_outbox_entity", table_name="outbox_events")

    op.drop_table("outbox_events")
