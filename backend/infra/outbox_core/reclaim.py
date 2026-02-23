from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from infra.outbox_core.stuck import stuck_processing_predicate


async def reclaim_stuck_processing(
    session: AsyncSession,
    model: Any,
    *,
    now: datetime,
    max_processing_seconds: int,
) -> int:
    """Best-effort stuck reclaim.

    Uses the shared predicate (lease expiry OR max processing duration exceeded)
    and resets rows back to pending.

    Returns affected row count (best-effort).
    """

    result = await session.execute(
        update(model)
        .where(stuck_processing_predicate(model, now=now, max_processing_seconds=max_processing_seconds))
        .values(
            status="pending",
            owner=None,
            lease_until=None,
            processing_started_at=None,
            updated_at=now,
        )
    )

    return int(getattr(result, "rowcount", 0) or 0)
