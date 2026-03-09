from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infra.database.models.chronicle_models import ChronicleEventModel
from infra.database.models.outbox_event_models import OutboxEventModel
from infra.outbox_core.payload_contract import require_mapping, require_schema_version


PROJECTION_NAME = "chronicle_daily_stats"


def _utc_today(dt: datetime) -> datetime:
    # Normalize to UTC date boundary for aggregation.
    return datetime(dt.year, dt.month, dt.day, tzinfo=timezone.utc)


async def apply(*, ev: OutboxEventModel, session: AsyncSession) -> None:
    """Sample projection: chronicle daily stats (v0 skeleton).

    Current behavior (v0):
    - Validate outbox op and source chronicle_event payload contract.
    - Load the source chronicle_event as SoT.
    - Compute the (tenant, date, event_type) identity in memory.
    - No DB writes yet; later phases will materialize into a dedicated table.
    """

    op = str(getattr(ev, "op", ""))
    if op != "upsert":
        # Deterministic programming error; do not retry.
        raise ValueError(f"Unsupported outbox op for {PROJECTION_NAME}: {op!r}")

    event = (
        await session.execute(select(ChronicleEventModel).where(ChronicleEventModel.id == ev.entity_id))
    ).scalar_one_or_none()
    if event is None:
        raise ValueError(f"Missing chronicle_event for {PROJECTION_NAME}: {ev.entity_id}")

    payload: Mapping[str, Any] = require_mapping(event.payload, projection=PROJECTION_NAME, field_name="payload")
    # Reuse the same schema_version contract as entries projection for now.
    require_schema_version(payload, projection=PROJECTION_NAME, supported_versions={1}, allow_missing=False)

    # Derive the aggregation key in-memory (tenant ~= book, day, event_type).
    occurred_at = getattr(event, "occurred_at", None) or datetime.now(timezone.utc)
    day_bucket = _utc_today(occurred_at)
    tenant_id = getattr(event, "book_id", None)
    event_type = getattr(event, "event_type", None)

    # v0 implementation intentionally does not persist stats.
    # This ensures the projection is harness-compatible while leaving
    # the physical stats table design to a later phase.
    _ = (tenant_id, day_bucket, event_type)
