from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession


def lease_until(*, now: datetime, lease_seconds: float) -> datetime:
    return now + timedelta(seconds=float(lease_seconds))


async def renew_lease(
    session: AsyncSession,
    model: Any,
    ids: list[Any],
    *,
    worker_id: Any,
    lease_seconds: float,
    now: datetime,
) -> int:
    """Extend lease for in-flight rows owned by this worker.

    The model is expected to expose attributes used below
    (id/processed_at/status/owner/lease_until/updated_at).

    Returns the affected row count (best-effort; may be 0 on some dialects).
    """

    if not ids:
        return 0

    result = await session.execute(
        update(model)
        .where(
            getattr(model, "id").in_(ids),
            getattr(model, "processed_at").is_(None),
            getattr(model, "status") == "processing",
            getattr(model, "owner") == worker_id,
        )
        .values(
            lease_until=lease_until(now=now, lease_seconds=lease_seconds),
            updated_at=now,
        )
    )
    return int(getattr(result, "rowcount", 0) or 0)
