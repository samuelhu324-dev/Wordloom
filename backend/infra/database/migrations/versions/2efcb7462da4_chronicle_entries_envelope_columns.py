"""Add envelope columns to chronicle_entries.

Chronicle Phase C promoted durable envelope fields to columns on chronicle_events.
Phase 2 (table merge migration) needs the same low-cardinality fields on the
projection table (chronicle_entries) so filtering/auditing can be served from
the projection table without losing observability.

Revision ID: 2efcb7462da4
Revises: f0b1c2d3e4f5
Create Date: 2026-02-24

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2efcb7462da4"
down_revision: Union[str, Sequence[str], None] = "f0b1c2d3e4f5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add envelope columns (nullable; defaults set after backfill).
    op.add_column("chronicle_entries", sa.Column("schema_version", sa.Integer(), nullable=True))
    op.add_column("chronicle_entries", sa.Column("provenance", sa.String(length=32), nullable=True))
    op.add_column("chronicle_entries", sa.Column("source", sa.String(length=64), nullable=True))
    op.add_column("chronicle_entries", sa.Column("actor_kind", sa.String(length=32), nullable=True))
    op.add_column("chronicle_entries", sa.Column("correlation_id", sa.String(length=128), nullable=True))

    # Backfill from payload envelope (safe for JSON/JSONB).
    op.execute(
        """
        UPDATE chronicle_entries
        SET
            schema_version = COALESCE(schema_version, NULLIF(payload->>'schema_version', '')::int, 1),
            provenance     = COALESCE(provenance, NULLIF(payload->>'provenance', ''), 'unknown'),
            source         = COALESCE(source, NULLIF(payload->>'source', ''), 'unknown'),
            actor_kind     = COALESCE(actor_kind, NULLIF(payload->>'actor_kind', ''), 'unknown'),
            correlation_id = COALESCE(correlation_id, NULLIF(payload->>'correlation_id', ''))
        WHERE
            schema_version IS NULL
            OR provenance IS NULL
            OR source IS NULL
            OR actor_kind IS NULL
            OR correlation_id IS NULL
        """
    )

    op.create_index(
        "ix_chronicle_entries_correlation_id",
        "chronicle_entries",
        ["correlation_id"],
        unique=False,
    )
    op.create_index(
        "ix_chronicle_entries_source_time",
        "chronicle_entries",
        ["source", "occurred_at"],
        unique=False,
    )

    # Server defaults (without NOT NULL): keep new writes from producing NULLs.
    op.alter_column(
        "chronicle_entries",
        "schema_version",
        existing_type=sa.Integer(),
        server_default=sa.text("1"),
    )
    op.alter_column(
        "chronicle_entries",
        "provenance",
        existing_type=sa.String(length=32),
        server_default=sa.text("'unknown'"),
    )
    op.alter_column(
        "chronicle_entries",
        "source",
        existing_type=sa.String(length=64),
        server_default=sa.text("'unknown'"),
    )
    op.alter_column(
        "chronicle_entries",
        "actor_kind",
        existing_type=sa.String(length=32),
        server_default=sa.text("'unknown'"),
    )


def downgrade() -> None:
    op.alter_column(
        "chronicle_entries",
        "actor_kind",
        existing_type=sa.String(length=32),
        server_default=None,
    )
    op.alter_column(
        "chronicle_entries",
        "source",
        existing_type=sa.String(length=64),
        server_default=None,
    )
    op.alter_column(
        "chronicle_entries",
        "provenance",
        existing_type=sa.String(length=32),
        server_default=None,
    )
    op.alter_column(
        "chronicle_entries",
        "schema_version",
        existing_type=sa.Integer(),
        server_default=None,
    )

    op.drop_index("ix_chronicle_entries_source_time", table_name="chronicle_entries")
    op.drop_index("ix_chronicle_entries_correlation_id", table_name="chronicle_entries")

    op.drop_column("chronicle_entries", "correlation_id")
    op.drop_column("chronicle_entries", "actor_kind")
    op.drop_column("chronicle_entries", "source")
    op.drop_column("chronicle_entries", "provenance")
    op.drop_column("chronicle_entries", "schema_version")
