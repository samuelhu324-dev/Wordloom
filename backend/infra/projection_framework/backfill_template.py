from __future__ import annotations

"""Backfill runner template.

This module centralizes the common operational contract for backfill tools:
- deterministic, idempotent outbox event emission (ON CONFLICT DO NOTHING)
- payload contract safety (payload defaults to `{}`; must be a JSON object)
- structured logs with run_id / worker_id (without polluting metrics labels)

Backfill definition (v1): emit outbox events from a projection's source-of-truth.
Consumption is handled separately by the projection harness / worker.

Individual backfill scripts should provide the projection-specific scan logic and
call `emit.emit(...)` for each item to enqueue.
"""

import logging
import os
import socket
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable, Mapping, MutableMapping, Optional, TypeVar

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from infra.database.models.outbox_event_models import OutboxEventModel


logger = logging.getLogger(__name__)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _default_run_id() -> str:
    run_id = (os.getenv("RUN_ID") or "").strip()
    if run_id:
        return run_id
    return "local"


def _default_worker_id() -> str:
    worker_id = (os.getenv("OUTBOX_WORKER_ID") or "").strip()
    if worker_id:
        return worker_id
    return f"{socket.gethostname()}:{os.getpid()}"


_BACKFILL_ID_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, "wordloom.backfill.outbox_id.v1")


def compute_backfill_outbox_id(
    *, projection: str, entity_type: str, entity_id: uuid.UUID, op: str, event_version: int
) -> uuid.UUID:
    """Compute a deterministic outbox event id for backfill.

    This provides v1 idempotence: backfill may be re-run safely without creating
    duplicate outbox rows.
    """

    key = f"{projection}:{entity_type}:{entity_id}:{op}:{int(event_version)}"
    return uuid.uuid5(_BACKFILL_ID_NAMESPACE, key)


def require_enabled_env(*, env_name: str = "OUTBOX_BACKFILL_ENABLED") -> None:
    """Guardrail: require an explicit enable flag for backfill tools."""

    raw = (os.getenv(env_name) or "").strip().lower()
    if raw != "true":
        raise RuntimeError(f"{env_name} must be 'true' to run backfill")


@dataclass(frozen=True)
class BackfillItem:
    projection: str
    entity_type: str
    entity_id: uuid.UUID
    op: str
    event_version: int
    library_id: uuid.UUID | None = None
    book_id: uuid.UUID | None = None
    payload: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class BackfillStats:
    projection: str
    dry_run: bool
    scanned: int
    enqueued: int
    skipped_existing: int
    batches: int
    started_at: datetime
    finished_at: datetime
    run_id: str
    worker_id: str


class BackfillEmitter:
    def __init__(
        self,
        session: AsyncSession,
        *,
        projection_name: str,
        run_id: str,
        worker_id: str,
        dry_run: bool,
        batch_size: int,
    ) -> None:
        if not projection_name.strip():
            raise ValueError("projection_name must be non-empty")
        if batch_size <= 0:
            raise ValueError("batch_size must be > 0")

        self._session = session
        self._projection_name = projection_name
        self._run_id = run_id
        self._worker_id = worker_id
        self._dry_run = bool(dry_run)
        self._batch_size = int(batch_size)

        self._pending: list[BackfillItem] = []
        self._scanned = 0
        self._enqueued = 0
        self._batches = 0

    @property
    def scanned(self) -> int:
        return int(self._scanned)

    @property
    def enqueued(self) -> int:
        return int(self._enqueued)

    @property
    def batches(self) -> int:
        return int(self._batches)

    async def emit(self, item: BackfillItem) -> None:
        if item.projection != self._projection_name:
            raise ValueError(
                f"BackfillItem.projection mismatch: expected={self._projection_name!r} got={item.projection!r}"
            )
        self._scanned += 1

        self._pending.append(item)
        if len(self._pending) >= self._batch_size:
            await self.flush()

    async def flush(self) -> int:
        if not self._pending:
            return 0

        now = utc_now()
        values: list[MutableMapping[str, Any]] = []

        for it in self._pending:
            payload_obj: Mapping[str, Any] | None = it.payload
            if payload_obj is None:
                payload_obj = {}
            if not isinstance(payload_obj, Mapping):
                raise TypeError(f"payload must be a mapping (JSON object), got: {type(payload_obj).__name__}")

            outbox_id = compute_backfill_outbox_id(
                projection=it.projection,
                entity_type=it.entity_type,
                entity_id=it.entity_id,
                op=it.op,
                event_version=int(it.event_version),
            )

            values.append(
                {
                    "id": outbox_id,
                    "projection": str(it.projection),
                    "entity_type": str(it.entity_type),
                    "entity_id": it.entity_id,
                    "op": str(it.op),
                    "event_version": int(it.event_version),
                    "payload": dict(payload_obj),
                    "library_id": it.library_id,
                    "book_id": it.book_id,
                    "created_at": now,
                    "updated_at": now,
                    "status": "pending",
                    "attempts": 0,
                    "replay_count": 0,
                }
            )

        scanned = len(self._pending)
        self._pending = []

        if self._dry_run:
            self._batches += 1
            return 0

        stmt = pg_insert(OutboxEventModel).values(values)
        stmt = stmt.on_conflict_do_nothing(index_elements=[OutboxEventModel.id]).returning(OutboxEventModel.id)
        result = await self._session.execute(stmt)

        # `rowcount` is not reliable for psycopg with ON CONFLICT DO NOTHING.
        inserted_ids = list(result.scalars().all())
        inserted = int(len(inserted_ids))
        self._enqueued += inserted
        self._batches += 1

        skipped = max(0, scanned - inserted)

        logger.info(
            {
                "event": "projection.backfill.flush",
                "layer": "backfill",
                "projection": self._projection_name,
                "run_id": self._run_id,
                "worker_id": self._worker_id,
                "scanned": int(scanned),
                "inserted": int(inserted),
                "skipped_existing": int(skipped),
            }
        )

        return inserted


T = TypeVar("T")


async def run_backfill(
    *,
    projection_name: str,
    session_factory: Any,
    work: Callable[[AsyncSession, BackfillEmitter], Awaitable[T]],
    run_id: Optional[str] = None,
    worker_id: Optional[str] = None,
    dry_run: bool = False,
    batch_size: int = 1000,
) -> tuple[T, BackfillStats]:
    """Run backfill work with standardized idempotent outbox emission.

    - `work(session, emit)` should scan SoT and call `emit.emit(...)`.
    - This function commits on success (unless dry_run).

    Note: backfill does not update `projection_status` (that table is rebuild bookkeeping).
    """

    started_at = utc_now()
    if run_id is None:
        run_id = _default_run_id()
    if worker_id is None:
        worker_id = _default_worker_id()

    logger.info(
        {
            "event": "projection.backfill.start",
            "layer": "backfill",
            "projection": projection_name,
            "run_id": run_id,
            "worker_id": worker_id,
            "dry_run": bool(dry_run),
            "batch_size": int(batch_size),
        }
    )

    async with session_factory() as session:
        emit = BackfillEmitter(
            session,
            projection_name=projection_name,
            run_id=run_id,
            worker_id=worker_id,
            dry_run=bool(dry_run),
            batch_size=int(batch_size),
        )

        result = await work(session, emit)
        await emit.flush()

        if not dry_run:
            await session.commit()

    finished_at = utc_now()

    stats = BackfillStats(
        projection=projection_name,
        dry_run=bool(dry_run),
        scanned=int(emit.scanned),
        enqueued=int(emit.enqueued),
        skipped_existing=max(0, int(emit.scanned) - int(emit.enqueued)),
        batches=int(emit.batches),
        started_at=started_at,
        finished_at=finished_at,
        run_id=str(run_id),
        worker_id=str(worker_id),
    )

    logger.info(
        {
            "event": "projection.backfill.finish",
            "layer": "backfill",
            "projection": projection_name,
            "run_id": run_id,
            "worker_id": worker_id,
            "ok": True,
            "scanned": int(stats.scanned),
            "enqueued": int(stats.enqueued),
            "skipped_existing": int(stats.skipped_existing),
            "batches": int(stats.batches),
            "duration_s": float((finished_at - started_at).total_seconds()),
        }
    )

    return result, stats
