from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession


async def mark_done(
    session: AsyncSession,
    model: Any,
    *,
    ev_id: Any,
    worker_id: Any,
    now: datetime,
) -> int:
    """Mark an in-flight outbox event as done.

    Preserves the common invariants:
    - terminal rows must not keep owner/lease/processing_started_at
    - next_retry_at/error fields cleared on success

    The model is expected to expose attributes used below
    (id/processed_at/status/owner/lease_until/processing_started_at/next_retry_at/
    error_reason/error/updated_at).

    Returns affected rowcount (best-effort; may be 0 on some dialects).
    """

    result = await session.execute(
        update(model)
        .where(
            getattr(model, "id") == ev_id,
            getattr(model, "owner") == worker_id,
            getattr(model, "status") == "processing",
            getattr(model, "lease_until") > now,
        )
        .values(
            status="done",
            processed_at=now,
            owner=None,
            lease_until=None,
            processing_started_at=None,
            next_retry_at=None,
            error_reason=None,
            error=None,
            updated_at=now,
        )
    )
    return int(getattr(result, "rowcount", 0) or 0)


async def mark_retry(
    session: AsyncSession,
    model: Any,
    *,
    ev_id: Any,
    reason: str,
    error: str,
    attempts: int,
    next_retry_at: datetime,
    now: datetime,
    error_max_len: int = 8000,
) -> int:
    """Return an event back to pending and schedule a retry."""

    result = await session.execute(
        update(model)
        .where(getattr(model, "id") == ev_id)
        .values(
            status="pending",
            owner=None,
            lease_until=None,
            processing_started_at=None,
            attempts=int(attempts),
            next_retry_at=next_retry_at,
            error_reason=str(reason),
            error=(error or "")[: int(error_max_len)],
            updated_at=now,
        )
    )
    return int(getattr(result, "rowcount", 0) or 0)


async def mark_failed(
    session: AsyncSession,
    model: Any,
    *,
    ev_id: Any,
    reason: str,
    error: str,
    attempts: int,
    now: datetime,
    error_max_len: int = 8000,
) -> int:
    """Mark an event as terminal failed."""

    result = await session.execute(
        update(model)
        .where(getattr(model, "id") == ev_id)
        .values(
            status="failed",
            owner=None,
            lease_until=None,
            processing_started_at=None,
            attempts=int(attempts),
            next_retry_at=None,
            error_reason=str(reason),
            error=(error or "")[: int(error_max_len)],
            updated_at=now,
        )
    )
    return int(getattr(result, "rowcount", 0) or 0)
