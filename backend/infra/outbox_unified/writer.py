"""Unified outbox writer template.

A dependency-light helper to enqueue rows into `outbox_events` in the same DB
transaction as the source-of-truth write.

This is the "writer template" counterpart to outbox_core (consumer/runtime).
"""

from __future__ import annotations

import logging
import os
import socket
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import UUID, uuid4

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from infra.database.models.outbox_event_models import OutboxEventModel
from infra.observability.outbox_metrics import outbox_enqueued_total


logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _default_run_id() -> str:
    run_id = (os.getenv("RUN_ID") or "").strip()
    return run_id or "local"


def _default_worker_id() -> str | None:
    worker_id = (os.getenv("OUTBOX_WORKER_ID") or "").strip()
    if worker_id:
        return worker_id
    # Writer calls are not necessarily worker processes; keep this optional.
    return None


def _default_writer_id() -> str:
    return f"{socket.gethostname()}:{os.getpid()}"


def _inject_trace_context() -> tuple[str | None, str | None]:
    try:
        from infra.observability.tracing import inject_trace_context

        return inject_trace_context()
    except Exception:
        return (None, None)


class OutboxWriter:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def enqueue(
        self,
        *,
        projection: str,
        entity_type: str,
        entity_id: UUID,
        op: str,
        event_version: int,
        library_id: UUID | None = None,
        book_id: UUID | None = None,
        payload: Mapping[str, Any] | None = None,
    ) -> UUID:
        now = _utc_now()
        outbox_id = uuid4()
        traceparent, tracestate = _inject_trace_context()

        run_id = _default_run_id()
        worker_id = _default_worker_id()
        writer_id = _default_writer_id()

        await self._db.execute(
            pg_insert(OutboxEventModel).values(
                id=outbox_id,
                projection=str(projection),
                entity_type=str(entity_type),
                entity_id=entity_id,
                op=str(op),
                event_version=int(event_version),
                payload=(dict(payload) if payload is not None else {}),
                library_id=library_id,
                book_id=book_id,
                traceparent=traceparent,
                tracestate=tracestate,
                created_at=now,
                updated_at=now,
                status="pending",
                attempts=0,
                replay_count=0,
            )
        )

        outbox_enqueued_total.labels(projection=str(projection), op=str(op)).inc()
        logger.info(
            {
                "event": "outbox.enqueue",
                "layer": "writer",
                "projection": str(projection),
                "op": str(op),
                "run_id": run_id,
                "worker_id": worker_id,
                "writer_id": writer_id,
                "outbox_id": str(outbox_id),
                "entity_type": str(entity_type),
                "entity_id": str(entity_id),
                "event_version": int(event_version),
                "library_id": (str(library_id) if library_id else None),
                "book_id": (str(book_id) if book_id else None),
            }
        )

        return outbox_id


__all__ = ["OutboxWriter"]
