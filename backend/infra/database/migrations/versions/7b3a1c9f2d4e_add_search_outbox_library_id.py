"""Add library_id to search_outbox_events for scoped workers.

Revision ID: 7b3a1c9f2d4e
Revises: 0f3c2a7d9b41
Create Date: 2026-02-20

Purpose:
- Allow the Search outbox worker to restrict claim/processing to a subset of
  libraries (canary / dual-run isolation) without joining to search_index.

Notes:
- Column is nullable; older rows or global entity types may remain NULL.
- Includes a best-effort backfill from search_index for rows where a matching
  search_index row exists.
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "7b3a1c9f2d4e"
down_revision = "0f3c2a7d9b41"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "search_outbox_events",
        sa.Column("library_id", postgresql.UUID(as_uuid=True), nullable=True),
    )

    # Best-effort backfill when the corresponding search_index row still exists.
    # (For deletes, search_index may already be removed, so library_id may stay NULL.)
    op.execute(
        """
        UPDATE search_outbox_events oe
        SET library_id = si.library_id
        FROM search_index si
        WHERE oe.library_id IS NULL
          AND oe.entity_type = si.entity_type
          AND oe.entity_id = si.entity_id
          AND si.library_id IS NOT NULL
        """
    )

    op.create_index(
        "idx_search_outbox_library_claim",
        "search_outbox_events",
        ["library_id", "status", "next_retry_at", "lease_until", "event_version"],
    )


def downgrade() -> None:
    op.drop_index("idx_search_outbox_library_claim", table_name="search_outbox_events")
    op.drop_column("search_outbox_events", "library_id")
