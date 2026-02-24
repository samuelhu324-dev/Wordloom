from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Iterable

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from infra.outbox_core.sanitize import terminal_clear_values


@dataclass(frozen=True)
class ReplayFailedResult:
    total_matched: int
    will_replay: int
    changed: int


async def replay_failed_rows(
    session: AsyncSession,
    model: Any,
    *,
    now: datetime,
    by: Any,
    reason: str,
    limit: int,
    entity_type: str | None = None,
    since_hours: float | None = None,
    ids: Iterable[Any] | None = None,
    dry_run: bool = False,
) -> ReplayFailedResult:
    """Replay terminal failed outbox rows back to pending.

    This helper is projection-agnostic and expects `model` to expose:
    - status, owner, lease_until, processing_started_at
    - attempts, next_retry_at, error_reason, error
    - replay_count, last_replayed_at, last_replayed_by, last_replayed_reason
    - updated_at

    Notes:
    - Intentionally mirrors current legacy replay tools semantics.
    - `limit` currently affects the reported will_replay only (the legacy tools
      update all matched rows). We preserve that behavior here.
    """

    status = getattr(model, "status")
    updated_at = getattr(model, "updated_at")

    where = [status == "failed"]
    if ids:
        where.append(getattr(model, "id").in_(list(ids)))
    if entity_type is not None:
        where.append(getattr(model, "entity_type") == entity_type)
    if since_hours is not None:
        where.append(updated_at >= (now - timedelta(hours=float(since_hours))))

    total = (
        await session.execute(select(func.count()).select_from(model).where(*where))
    ).scalar_one()
    total_i = int(total or 0)

    will_replay = min(total_i, max(0, int(limit)))
    if dry_run or will_replay <= 0:
        return ReplayFailedResult(total_matched=total_i, will_replay=will_replay, changed=0)

    terminal_clear = terminal_clear_values(now=now, clear_next_retry_at=True)

    result = await session.execute(
        update(model)
        .where(*where)
        .values(
            status="pending",
            attempts=0,
            error_reason=None,
            error=None,
            **terminal_clear,
            replay_count=(getattr(model, "replay_count") + 1),
            last_replayed_at=now,
            last_replayed_by=str(by)[:120],
            last_replayed_reason=str(reason),
        )
    )
    await session.commit()

    changed = int(getattr(result, "rowcount", 0) or 0)
    return ReplayFailedResult(total_matched=total_i, will_replay=will_replay, changed=changed)
