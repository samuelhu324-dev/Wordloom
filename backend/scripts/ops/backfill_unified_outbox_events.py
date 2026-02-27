"""Backfill unified outbox_events from legacy outbox tables.

Copies rows from:
- search_outbox_events   -> outbox_events (projection=search_index_to_elastic)
- chronicle_outbox_events -> outbox_events (projection=chronicle_events_to_entries)

Properties:
- Idempotent via ON CONFLICT (id) DO NOTHING
- Batch-oriented keyset pagination to avoid huge transactions

Usage (PowerShell):
  $env:DATABASE_URL='postgresql://wordloom:wordloom@localhost:5435/wordloom_test'
  $env:OUTBOX_UNIFIED_BACKFILL_ENABLED='true'
  c:/python314/python.exe backend/scripts/ops/backfill_unified_outbox_events.py --search --chronicle

Notes:
- book_id backfill is intentionally left NULL for Chronicle in v1.
- payload is NULL for both projections in v1.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import text

_HERE = Path(__file__).resolve()
_BACKEND_ROOT = _HERE.parents[2]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))


# psycopg async cannot run on ProactorEventLoop. Force Selector policy on Windows.
if sys.platform.startswith("win"):
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass


from infra.database.session import get_session_factory


SEARCH_PROJECTION = "search_index_to_elastic"
CHRONICLE_PROJECTION = "chronicle_events_to_entries"


@dataclass(frozen=True)
class _BackfillResult:
    projection: str
    inserted: int
    batches: int
    started_at: datetime
    finished_at: datetime


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Backfill unified outbox_events from legacy outbox tables")
    p.add_argument("--search", action="store_true", help="Backfill from search_outbox_events")
    p.add_argument("--chronicle", action="store_true", help="Backfill from chronicle_outbox_events")
    p.add_argument("--batch-size", type=int, default=5000, help="Batch size (default: 5000)")
    p.add_argument("--max-batches", type=int, default=0, help="Stop after N batches (0 means no limit)")
    p.add_argument(
        "--require-enabled-env",
        action="store_true",
        default=True,
        help="Require OUTBOX_UNIFIED_BACKFILL_ENABLED=true (default: true)",
    )
    p.add_argument(
        "--no-require-enabled-env",
        action="store_false",
        dest="require_enabled_env",
        help="Disable OUTBOX_UNIFIED_BACKFILL_ENABLED guard",
    )
    return p.parse_args()


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _require_env_ok(require: bool) -> None:
    if not os.getenv("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL must be set")

    if not require:
        return

    if os.getenv("OUTBOX_UNIFIED_BACKFILL_ENABLED", "").strip().lower() != "true":
        raise RuntimeError(
            "OUTBOX_UNIFIED_BACKFILL_ENABLED must be 'true' to run backfill (or pass --no-require-enabled-env)"
        )


async def _backfill_search(*, batch_size: int, max_batches: int) -> _BackfillResult:
    session_factory = await get_session_factory()

    started_at = _utc_now()
    inserted_total = 0
    batches = 0

    last_created_at: datetime | None = None
    last_id = None

    async with session_factory() as session:
        while True:
            if max_batches and batches >= max_batches:
                break

            where = "WHERE processed_at IS NULL OR status in ('pending','processing')"
            params: dict[str, object] = {"limit": batch_size}

            if last_created_at is not None and last_id is not None:
                where = (
                    where
                    + " AND (created_at, id) > (:last_created_at, :last_id)"
                )
                params["last_created_at"] = last_created_at
                params["last_id"] = last_id

            page = await session.execute(
                text(
                    f"""
                    SELECT id, created_at
                    FROM search_outbox_events
                    {where}
                    ORDER BY created_at ASC, id ASC
                    LIMIT :limit
                    """
                ),
                params,
            )
            rows = page.all()
            if not rows:
                break

            last_id, last_created_at = rows[-1][0], rows[-1][1]
            ids = [r[0] for r in rows]

            result = await session.execute(
                text(
                    """
                    INSERT INTO outbox_events (
                        id, projection, entity_type, entity_id, op, event_version,
                        created_at, updated_at, processed_at,
                        status, owner, lease_until, processing_started_at,
                        attempts, next_retry_at,
                        error_reason, error,
                        traceparent, tracestate,
                        replay_count, last_replayed_at, last_replayed_by, last_replayed_reason,
                        payload, library_id, book_id
                    )
                    SELECT
                        s.id,
                        :projection,
                        s.entity_type,
                        s.entity_id,
                        s.op,
                        s.event_version,
                        s.created_at,
                        s.updated_at,
                        s.processed_at,
                        s.status,
                        s.owner,
                        s.lease_until,
                        s.processing_started_at,
                        s.attempts,
                        s.next_retry_at,
                        s.error_reason,
                        s.error,
                        s.traceparent,
                        s.tracestate,
                        s.replay_count,
                        s.last_replayed_at,
                        s.last_replayed_by,
                        s.last_replayed_reason,
                        NULL::jsonb,
                        s.library_id,
                        NULL::uuid
                    FROM search_outbox_events s
                    WHERE s.id = ANY(:ids)
                    ON CONFLICT (id) DO NOTHING
                    """
                ),
                {"projection": SEARCH_PROJECTION, "ids": ids},
            )

            inserted = int(getattr(result, "rowcount", 0) or 0)
            inserted_total += inserted
            batches += 1

            await session.commit()

    finished_at = _utc_now()
    return _BackfillResult(
        projection=SEARCH_PROJECTION,
        inserted=inserted_total,
        batches=batches,
        started_at=started_at,
        finished_at=finished_at,
    )


async def _backfill_chronicle(*, batch_size: int, max_batches: int) -> _BackfillResult:
    session_factory = await get_session_factory()

    started_at = _utc_now()
    inserted_total = 0
    batches = 0

    last_created_at: datetime | None = None
    last_id = None

    async with session_factory() as session:
        while True:
            if max_batches and batches >= max_batches:
                break

            where = "WHERE processed_at IS NULL OR status in ('pending','processing')"
            params: dict[str, object] = {"limit": batch_size}

            if last_created_at is not None and last_id is not None:
                where = (
                    where
                    + " AND (created_at, id) > (:last_created_at, :last_id)"
                )
                params["last_created_at"] = last_created_at
                params["last_id"] = last_id

            page = await session.execute(
                text(
                    f"""
                    SELECT id, created_at
                    FROM chronicle_outbox_events
                    {where}
                    ORDER BY created_at ASC, id ASC
                    LIMIT :limit
                    """
                ),
                params,
            )
            rows = page.all()
            if not rows:
                break

            last_id, last_created_at = rows[-1][0], rows[-1][1]
            ids = [r[0] for r in rows]

            result = await session.execute(
                text(
                    """
                    INSERT INTO outbox_events (
                        id, projection, entity_type, entity_id, op, event_version,
                        created_at, updated_at, processed_at,
                        status, owner, lease_until, processing_started_at,
                        attempts, next_retry_at,
                        error_reason, error,
                        traceparent, tracestate,
                        replay_count, last_replayed_at, last_replayed_by, last_replayed_reason,
                        payload, library_id, book_id
                    )
                    SELECT
                        c.id,
                        :projection,
                        c.entity_type,
                        c.entity_id,
                        c.op,
                        c.event_version,
                        c.created_at,
                        c.updated_at,
                        c.processed_at,
                        c.status,
                        c.owner,
                        c.lease_until,
                        c.processing_started_at,
                        c.attempts,
                        c.next_retry_at,
                        c.error_reason,
                        c.error,
                        c.traceparent,
                        c.tracestate,
                        c.replay_count,
                        c.last_replayed_at,
                        c.last_replayed_by,
                        c.last_replayed_reason,
                        NULL::jsonb,
                        NULL::uuid,
                        NULL::uuid
                    FROM chronicle_outbox_events c
                    WHERE c.id = ANY(:ids)
                    ON CONFLICT (id) DO NOTHING
                    """
                ),
                {"projection": CHRONICLE_PROJECTION, "ids": ids},
            )

            inserted = int(getattr(result, "rowcount", 0) or 0)
            inserted_total += inserted
            batches += 1

            await session.commit()

    finished_at = _utc_now()
    return _BackfillResult(
        projection=CHRONICLE_PROJECTION,
        inserted=inserted_total,
        batches=batches,
        started_at=started_at,
        finished_at=finished_at,
    )


async def main_async() -> int:
    args = _parse_args()
    _require_env_ok(bool(args.require_enabled_env))

    if not args.search and not args.chronicle:
        raise RuntimeError("At least one of --search/--chronicle must be set")

    batch_size = int(args.batch_size or 0)
    if batch_size <= 0:
        raise RuntimeError("--batch-size must be > 0")

    max_batches = int(args.max_batches or 0)
    if max_batches < 0:
        raise RuntimeError("--max-batches must be >= 0")

    results: list[_BackfillResult] = []

    if args.search:
        results.append(await _backfill_search(batch_size=batch_size, max_batches=max_batches))

    if args.chronicle:
        results.append(await _backfill_chronicle(batch_size=batch_size, max_batches=max_batches))

    for r in results:
        duration_s = max(0.0, (r.finished_at - r.started_at).total_seconds())
        print(f"[OK] projection={r.projection} inserted={r.inserted} batches={r.batches} duration_s={duration_s:.2f}")

    return 0


def main() -> int:
    return asyncio.run(main_async())


if __name__ == "__main__":
    raise SystemExit(main())
