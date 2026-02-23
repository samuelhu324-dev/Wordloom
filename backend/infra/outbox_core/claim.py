from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any, Iterable

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from infra.outbox_core.lease import lease_until


async def claim_pending_batch(
    session: AsyncSession,
    model: Any,
    *,
    now: datetime,
    batch_size: int,
    worker_id: Any,
    lease_seconds: float,
    scope_predicates: Iterable[Any] = (),
    order_by: Iterable[Any] = (),
    break_claim_atomicity: bool = False,
    break_claim_sleep_seconds: float = 0.0,
) -> list[Any]:
    """Claim a batch of pending outbox rows.

    This helper is projection-agnostic and expects `model` to expose:
    - id, processed_at, status, next_retry_at
    - owner, lease_until, processing_started_at, updated_at
    - error_reason, error

    Semantics are intentionally aligned with the existing Search worker:
    - default: SELECT ... FOR UPDATE SKIP LOCKED
    - experiment mode: run the locked SELECT first, then re-run without locking
      (to match current behavior), optionally sleep before UPDATE.
    - on success: update rows to {status=processing, owner=worker_id, lease_until, processing_started_at}
      and clear error fields; commit within this function.
    """

    processed_at = getattr(model, "processed_at")
    status = getattr(model, "status")
    next_retry_at = getattr(model, "next_retry_at")

    base_stmt = (
        select(model)
        .where(
            processed_at.is_(None),
            status == "pending",
            (next_retry_at.is_(None) | (next_retry_at <= now)),
            *list(scope_predicates),
        )
        .order_by(*list(order_by))
        .limit(int(batch_size))
    )

    # Normal behavior: row locking to avoid blocking between concurrent workers.
    claimable = (await session.execute(base_stmt.with_for_update(skip_locked=True))).scalars().all()

    if break_claim_atomicity:
        # Match current Search worker behavior: re-run without row locking.
        claimable = (await session.execute(base_stmt)).scalars().all()

    if not claimable:
        return []

    if break_claim_atomicity and break_claim_sleep_seconds and float(break_claim_sleep_seconds) > 0:
        await asyncio.sleep(float(break_claim_sleep_seconds))

    ids = [getattr(row, "id") for row in claimable]
    await session.execute(
        update(model)
        .where(getattr(model, "id").in_(ids))
        .values(
            status="processing",
            owner=worker_id,
            lease_until=lease_until(now=now, lease_seconds=lease_seconds),
            processing_started_at=now,
            updated_at=now,
            error_reason=None,
            error=None,
        )
    )
    await session.commit()

    return list(claimable)
