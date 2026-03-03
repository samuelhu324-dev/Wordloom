"""Add library_memberships table.

Revision ID: 9f2c7d1a4b63
Revises: 511e785a43fb
Create Date: 2026-03-02

"""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "9f2c7d1a4b63"
down_revision: Union[str, Sequence[str], None] = "511e785a43fb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "library_memberships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "library_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("libraries.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.CheckConstraint(
            "role in ('owner','admin','member')",
            name="ck_library_memberships_role",
        ),
        sa.UniqueConstraint(
            "library_id",
            "user_id",
            name="uq_library_memberships_library_user",
        ),
    )

    op.create_index(
        "ix_library_memberships_library_id",
        "library_memberships",
        ["library_id"],
        unique=False,
    )
    op.create_index(
        "ix_library_memberships_user_id",
        "library_memberships",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_library_memberships_library_user",
        "library_memberships",
        ["library_id", "user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_library_memberships_library_user", table_name="library_memberships")
    op.drop_index("ix_library_memberships_user_id", table_name="library_memberships")
    op.drop_index("ix_library_memberships_library_id", table_name="library_memberships")
    op.drop_table("library_memberships")
