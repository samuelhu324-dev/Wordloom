"""add subscription access tables

Revision ID: 3f4b2c1d9e7a
Revises: 9f2c7d1a4b63
Create Date: 2026-04-16 16:55:00
"""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "3f4b2c1d9e7a"
down_revision: Union[str, Sequence[str], None] = "9f2c7d1a4b63"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "plan_catalog",
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("display_name", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("code"),
    )

    op.create_table(
        "subscriptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("library_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("plan_code", sa.String(length=50), nullable=False),
        sa.Column("state", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["library_id"], ["libraries.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["plan_code"], ["plan_catalog.code"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("library_id"),
    )
    op.create_index("ix_subscriptions_library_state", "subscriptions", ["library_id", "state"], unique=False)

    op.create_table(
        "payment_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("subscription_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("library_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("event_type", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["library_id"], ["libraries.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["subscription_id"], ["subscriptions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_payment_events_subscription_id"), "payment_events", ["subscription_id"], unique=False)
    op.create_index(op.f("ix_payment_events_library_id"), "payment_events", ["library_id"], unique=False)
    op.create_index("ix_payment_events_library_created", "payment_events", ["library_id", "created_at"], unique=False)

    op.create_table(
        "entitlement_snapshots",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("library_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("plan_code", sa.String(length=50), nullable=False),
        sa.Column("subscription_state", sa.String(length=30), nullable=False),
        sa.Column("entitlements", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["library_id"], ["libraries.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["plan_code"], ["plan_catalog.code"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("library_id"),
    )
    op.create_index(
        "ix_entitlement_snapshots_library_state",
        "entitlement_snapshots",
        ["library_id", "subscription_state"],
        unique=False,
    )

    op.execute(
        sa.text(
            """
            INSERT INTO plan_catalog (code, display_name, created_at, updated_at)
            VALUES
                ('trial', 'Trial', TIMEZONE('utc', NOW()), TIMEZONE('utc', NOW())),
                ('standard', 'Standard', TIMEZONE('utc', NOW()), TIMEZONE('utc', NOW())),
                ('vip', 'VIP', TIMEZONE('utc', NOW()), TIMEZONE('utc', NOW())),
                ('internal', 'Internal', TIMEZONE('utc', NOW()), TIMEZONE('utc', NOW()))
            """
        )
    )

    op.execute(
        sa.text(
            """
            INSERT INTO subscriptions (id, library_id, plan_code, state, created_at, updated_at)
            SELECT gen_random_uuid(), l.id, 'trial', 'trialing', TIMEZONE('utc', NOW()), TIMEZONE('utc', NOW())
            FROM libraries AS l
            WHERE NOT EXISTS (
                SELECT 1
                FROM subscriptions AS s
                WHERE s.library_id = l.id
            )
            """
        )
    )

    op.execute(
        sa.text(
            """
            INSERT INTO entitlement_snapshots (
                id,
                library_id,
                plan_code,
                subscription_state,
                entitlements,
                created_at,
                updated_at
            )
            SELECT gen_random_uuid(), s.library_id, s.plan_code, s.state, 'read_library', TIMEZONE('utc', NOW()), TIMEZONE('utc', NOW())
            FROM subscriptions AS s
            WHERE NOT EXISTS (
                SELECT 1
                FROM entitlement_snapshots AS es
                WHERE es.library_id = s.library_id
            )
            """
        )
    )


def downgrade() -> None:
    op.drop_index("ix_entitlement_snapshots_library_state", table_name="entitlement_snapshots")
    op.drop_table("entitlement_snapshots")

    op.drop_index("ix_payment_events_library_created", table_name="payment_events")
    op.drop_index(op.f("ix_payment_events_library_id"), table_name="payment_events")
    op.drop_index(op.f("ix_payment_events_subscription_id"), table_name="payment_events")
    op.drop_table("payment_events")

    op.drop_index("ix_subscriptions_library_state", table_name="subscriptions")
    op.drop_table("subscriptions")

    op.drop_table("plan_catalog")