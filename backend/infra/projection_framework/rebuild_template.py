from __future__ import annotations

"""Rebuild/backfill runner template.

This module centralizes the common operational contract for rebuild tools:
- projection_status bookkeeping (low-cardinality, one row per projection)
- best-effort rebuild metrics (no-op if observability deps are unavailable)

Individual rebuild scripts should provide the projection-specific "work" function.
"""

from datetime import datetime, timezone
import os
import socket
import uuid
from typing import Any, Awaitable, Callable, Optional, TypeVar

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from infra.database.models.projection_status_models import ProjectionStatusModel


class _NoopMetric:
    def labels(self, **_kwargs):  # noqa: ANN003
        return self

    def set(self, *_args, **_kwargs):  # noqa: ANN003
        return None


def get_rebuild_metrics():
    """Best-effort metrics.

    Rebuild tools must remain runnable in minimal environments.
    """

    try:
        from infra.observability.outbox_metrics import (
            projection_rebuild_duration_seconds,
            projection_rebuild_last_finished_timestamp_seconds,
            projection_rebuild_last_success,
        )

        return (
            projection_rebuild_duration_seconds,
            projection_rebuild_last_finished_timestamp_seconds,
            projection_rebuild_last_success,
        )
    except Exception:
        noop = _NoopMetric()
        return (noop, noop, noop)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


async def set_projection_status(
    session: AsyncSession,
    *,
    projection_name: str,
    success: bool,
    error: Optional[str],
    started_at: datetime,
    finished_at: datetime,
) -> None:
    duration_s = max(0.0, (finished_at - started_at).total_seconds())

    stmt = pg_insert(ProjectionStatusModel).values(
        projection_name=projection_name,
        last_rebuild_started_at=started_at,
        last_rebuild_finished_at=finished_at,
        last_rebuild_duration_seconds=duration_s,
        last_rebuild_success=bool(success),
        last_rebuild_error=error,
        updated_at=finished_at,
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=[ProjectionStatusModel.projection_name],
        set_={
            "last_rebuild_started_at": started_at,
            "last_rebuild_finished_at": finished_at,
            "last_rebuild_duration_seconds": duration_s,
            "last_rebuild_success": bool(success),
            "last_rebuild_error": error,
            "updated_at": finished_at,
        },
    )
    await session.execute(stmt)


T = TypeVar("T")


async def run_rebuild(
    *,
    projection_name: str,
    session_factory: Any,
    work: Callable[[AsyncSession], Awaitable[T]],
    run_id: str | None = None,
    worker_id: str | None = None,
) -> T:
    """Run rebuild work with standardized bookkeeping + metrics.

    - `work(session)` should do the projection-specific rebuild and return a result.
    - This function commits on success after writing projection_status.
    - On failure, it best-effort writes projection_status in a fresh session.
    """

    (
        projection_rebuild_duration_seconds,
        projection_rebuild_last_finished_timestamp_seconds,
        projection_rebuild_last_success,
    ) = get_rebuild_metrics()

    started_at = utc_now()
    if run_id is None:
        run_id = str(os.getenv("RUN_ID") or "").strip() or f"manual-{uuid.uuid4()}"
    if worker_id is None:
        worker_id = str(os.getenv("WORKER_ID") or "").strip() or socket.gethostname()

    print(f"[rebuild] start projection={projection_name} run_id={run_id} worker_id={worker_id}")

    try:
        async with session_factory() as session:
            result = await work(session)

            finished_at = utc_now()
            await set_projection_status(
                session,
                projection_name=projection_name,
                success=True,
                error=None,
                started_at=started_at,
                finished_at=finished_at,
            )
            await session.commit()

        projection_rebuild_duration_seconds.labels(projection=projection_name).set(
            (finished_at - started_at).total_seconds()
        )
        projection_rebuild_last_finished_timestamp_seconds.labels(projection=projection_name).set(
            finished_at.timestamp()
        )
        projection_rebuild_last_success.labels(projection=projection_name).set(1)

        print(
            "[rebuild] ok projection=%s run_id=%s worker_id=%s duration_s=%.3f"
            % (projection_name, run_id, worker_id, (finished_at - started_at).total_seconds())
        )

        return result

    except Exception as exc:
        error = str(exc)
        finished_at = utc_now()

        try:
            async with session_factory() as session:
                await set_projection_status(
                    session,
                    projection_name=projection_name,
                    success=False,
                    error=error,
                    started_at=started_at,
                    finished_at=finished_at,
                )
                await session.commit()
        except Exception:
            pass

        projection_rebuild_last_finished_timestamp_seconds.labels(projection=projection_name).set(
            finished_at.timestamp()
        )
        projection_rebuild_last_success.labels(projection=projection_name).set(0)

        print(
            "[rebuild] fail projection=%s run_id=%s worker_id=%s duration_s=%.3f error=%s"
            % (projection_name, run_id, worker_id, (finished_at - started_at).total_seconds(), error)
        )

        raise
