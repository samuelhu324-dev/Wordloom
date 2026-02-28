"""Manual replay tool for Search outbox events.

Policy (v2):
- Automatic worker treats `failed` as terminal (won't claim again).
- Ops can explicitly replay failed rows back to pending, with audit fields.

This tool targets the unified outbox table (`outbox_events`) and filters by
projection (`search_index_to_elastic`).

Usage (PowerShell):
  $env:DATABASE_URL = "postgresql+psycopg://wordloom:wordloom@localhost:5435/wordloom_dev"
  python backend/scripts/search_outbox_replay_failed.py --by alice --reason "fixed mapping" --limit 100 --dry-run
  python backend/scripts/search_outbox_replay_failed.py --by alice --reason "fixed mapping" --limit 100
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure backend root is on sys.path (same pattern as worker).
_HERE = Path(__file__).resolve()
_BACKEND_ROOT = _HERE.parents[1]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from infra.database.session import get_session_factory
from infra.database.models.outbox_event_models import OutboxEventModel
from infra.outbox_core.replay import replay_failed_rows


SEARCH_OUTBOX_PROJECTION = "search_index_to_elastic"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Replay terminal failed outbox_events (search projection) back to pending")
    p.add_argument("--by", required=True, help="Operator identifier (for audit)")
    p.add_argument("--reason", required=True, help="Why this replay is being done (for audit)")
    p.add_argument("--limit", type=int, default=1000, help="Max rows to replay")
    p.add_argument("--entity-type", default=None, help="Filter by entity_type")
    p.add_argument("--since-hours", type=float, default=None, help="Only replay rows updated within last N hours")
    p.add_argument("--dry-run", action="store_true", help="Print count but do not modify")
    return p.parse_args()


async def main_async() -> int:
    args = _parse_args()

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL must be set")

    now = _utc_now()
    session_factory = await get_session_factory()

    async with session_factory() as session:
        result = await replay_failed_rows(
            session,
            OutboxEventModel,
            now=now,
            by=args.by,
            reason=str(args.reason),
            limit=int(args.limit),
            projection=SEARCH_OUTBOX_PROJECTION,
            entity_type=(str(args.entity_type) if args.entity_type else None),
            since_hours=(float(args.since_hours) if args.since_hours is not None else None),
            ids=None,
            dry_run=bool(args.dry_run),
        )

        print(
            f"Matched failed rows: {int(result.total_matched)}; "
            f"will replay: {int(result.will_replay)} (limit={args.limit})"
        )
        if not args.dry_run and result.will_replay > 0:
            print(f"Replayed rows: {int(result.changed)}")

    return 0


def main() -> None:
    import asyncio

    if sys.platform == "win32":
        # psycopg async is incompatible with ProactorEventLoop.
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    raise SystemExit(asyncio.run(main_async()))


if __name__ == "__main__":  # pragma: no cover
    main()
