from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession


async def sanitize_terminal_rows(
    session: AsyncSession,
    model: Any,
    *,
    now: datetime,
    terminal_statuses: tuple[str, ...] = ("done", "failed"),
) -> int:
    """Clear owner/lease fields for terminal rows.

    Matches the invariant used by existing workers:
    - processed_at IS NOT NULL OR status in {done, failed}
      => owner/lease_until/processing_started_at must be NULL.

    Returns affected row count (best-effort).
    """

    processed_at = getattr(model, "processed_at")
    status = getattr(model, "status")
    owner = getattr(model, "owner")
    lease_until = getattr(model, "lease_until")
    processing_started_at = getattr(model, "processing_started_at")

    result = await session.execute(
        update(model)
        .where(
            processed_at.is_not(None) | status.in_(list(terminal_statuses)),
            owner.is_not(None) | lease_until.is_not(None) | processing_started_at.is_not(None),
        )
        .values(
            owner=None,
            lease_until=None,
            processing_started_at=None,
            updated_at=now,
        )
    )

    return int(getattr(result, "rowcount", 0) or 0)
