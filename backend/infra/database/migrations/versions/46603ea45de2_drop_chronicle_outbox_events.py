"""Drop legacy chronicle_outbox_events.

Revision ID: 46603ea45de2
Revises: e0471c9d5da0
Create Date: 2026-02-28 11:55:14.438395

"""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "46603ea45de2"
down_revision: Union[str, Sequence[str], None] = "e0471c9d5da0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("DROP TABLE IF EXISTS chronicle_outbox_events")


def downgrade() -> None:
    op.create_table(
        "chronicle_outbox_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("op", sa.String(length=20), nullable=False),
        sa.Column("event_version", sa.BigInteger(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("owner", sa.String(length=120), nullable=True),
        sa.Column("lease_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("next_retry_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("processing_started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_reason", sa.String(length=80), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("traceparent", sa.String(length=512), nullable=True),
        sa.Column("tracestate", sa.Text(), nullable=True),
        sa.Column("replay_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_replayed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_replayed_by", sa.String(length=120), nullable=True),
        sa.Column("last_replayed_reason", sa.Text(), nullable=True),
    )

    # Keep model-level defaults; drop server defaults where appropriate.
    op.alter_column("chronicle_outbox_events", "event_version", server_default=None)
    op.alter_column("chronicle_outbox_events", "attempts", server_default=None)
    op.alter_column("chronicle_outbox_events", "replay_count", server_default=None)

    op.create_index(
        "idx_chronicle_outbox_entity",
        "chronicle_outbox_events",
        ["entity_type", "entity_id"],
        unique=False,
    )
    op.create_index(
        "idx_chronicle_outbox_processed",
        "chronicle_outbox_events",
        ["processed_at"],
        unique=False,
    )
    op.create_index(
        "idx_chronicle_outbox_claim",
        "chronicle_outbox_events",
        ["status", "next_retry_at", "lease_until", "event_version"],
        unique=False,
    )
    op.create_index(
        "idx_chronicle_outbox_processing_started",
        "chronicle_outbox_events",
        ["status", "processing_started_at"],
        unique=False,
    )
    op.create_index(
        "idx_chronicle_outbox_error_reason",
        "chronicle_outbox_events",
        ["status", "error_reason"],
        unique=False,
    )
