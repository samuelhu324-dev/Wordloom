"""Merge heads: outbox trace context + search outbox library id

Revision ID: f0b1c2d3e4f5
Revises: a4f1c2d7e9b0, 7b3a1c9f2d4e
Create Date: 2026-02-20

"""

from typing import Sequence, Union

from alembic import op  # noqa: F401


# revision identifiers, used by Alembic.
revision: str = "f0b1c2d3e4f5"
down_revision: Union[str, Sequence[str], None] = ("a4f1c2d7e9b0", "7b3a1c9f2d4e")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Merge revision (no-op).
    pass


def downgrade() -> None:
    # Merge revision (no-op).
    pass
