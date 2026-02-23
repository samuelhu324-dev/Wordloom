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
    clear_next_retry_at: bool = False,
) -> int:
    """Clear owner/lease fields for terminal rows.

    Matches the invariant used by existing workers:
    - processed_at IS NOT NULL OR status in {done, failed}
      => owner/lease_until/processing_started_at must be NULL.

    Optional: if clear_next_retry_at is True, also clears next_retry_at.

    Returns affected row count (best-effort).
    """

    processed_at = getattr(model, "processed_at")
    status = getattr(model, "status")
    owner = getattr(model, "owner")
    lease_until = getattr(model, "lease_until")
    processing_started_at = getattr(model, "processing_started_at")
    next_retry_at = getattr(model, "next_retry_at", None)

    values: dict[str, Any] = {
        "owner": None,
        "lease_until": None,
        "processing_started_at": None,
        "updated_at": now,
    }
    if clear_next_retry_at and next_retry_at is not None:
        values["next_retry_at"] = None

    dirty_fields = owner.is_not(None) | lease_until.is_not(None) | processing_started_at.is_not(None)
    if clear_next_retry_at and next_retry_at is not None:
        dirty_fields = dirty_fields | next_retry_at.is_not(None)

    result = await session.execute(
        update(model)
        .where(
            processed_at.is_not(None) | status.in_(list(terminal_statuses)),
            dirty_fields,
        )
        .values(**values)
    )

    return int(getattr(result, "rowcount", 0) or 0)
