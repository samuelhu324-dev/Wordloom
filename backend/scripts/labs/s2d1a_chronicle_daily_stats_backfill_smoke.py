"""S2D-1A/P2-C1-S1: chronicle_daily_stats backfill smoke (local, DB-only).

This lab exercises the generic backfill template for the
`chronicle_daily_stats` projection by:

- Creating (or reusing) a minimal Library/Bookshelf/Book FK chain
- Writing one Chronicle event via SQLAlchemyChronicleRepository (schema-aware)
- Running a DB-only backfill that emits a deterministic `outbox_events` row
  for `projection="chronicle_daily_stats"` from that event
- Re-running the same backfill to prove idempotence (2nd pass inserts 0)

Outputs:
- Writes `<outdir>/_result.json` as the evidence SoT for the round.

Notes:
- DB-only by design; harness is not invoked here.
- The env gate is satisfied explicitly for labs (`OUTBOX_BACKFILL_ENABLED=true`).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID

# Ensure `import infra.*` works when executed as a plain script.
_backend_dir = Path(__file__).resolve().parents[2]
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))

import psycopg
from sqlalchemy import select

from api.app.modules.chronicle.domain import ChronicleEvent, ChronicleEventType
from infra.database.session import get_session_factory
from infra.projection_framework.backfill_template import (
    BackfillEmitter,
    BackfillItem,
    BackfillStats,
    require_enabled_env,
    run_backfill,
)
from infra.storage.chronicle_repository_impl import SQLAlchemyChronicleRepository


PROJECTION_NAME = "chronicle_daily_stats"
LAB_ENTITY_TYPE = "chronicle_event"

LAB_LIBRARY_NAME = "LAB_S2D1A_DAILY_STATS_LIBRARY"
LAB_BOOKSHELF_NAME = "LAB_S2D1A_DAILY_STATS_SHELF"
LAB_BOOK_TITLE = "LAB_S2D1A_DAILY_STATS_BOOK"


def _utc_now_str() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def _database_url_psycopg(database_url: str) -> str:
    return database_url.replace("postgresql+psycopg://", "postgresql://")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _get_or_create_scaffold(conn: psycopg.Connection) -> dict[str, str]:
    """Create (or reuse) a minimal Library/Bookshelf/Book FK chain.

    Uses explicit columns to satisfy NOT NULL constraints.
    """

    now = _now()

    with conn.cursor() as cur:
        # Library
        cur.execute(
            "SELECT id FROM libraries WHERE name = %s ORDER BY created_at DESC LIMIT 1",
            (LAB_LIBRARY_NAME,),
        )
        row = cur.fetchone()
        if row is None:
            from uuid import uuid4

            library_id = str(uuid4())
            user_id = str(uuid4())
            cur.execute(
                """
                INSERT INTO libraries (
                    id, user_id, basement_bookshelf_id, name, description, cover_media_id,
                    theme_color, pinned, pinned_order, archived_at, last_activity_at,
                    views_count, last_viewed_at, created_at, updated_at, soft_deleted_at
                )
                VALUES (
                    %s, %s, NULL, %s, NULL, NULL,
                    NULL, FALSE, NULL, NULL, %s,
                    0, NULL, %s, %s, NULL
                )
                """,
                (library_id, user_id, LAB_LIBRARY_NAME, now, now, now),
            )
        else:
            (library_id,) = row
            library_id = str(library_id)

        # Bookshelf
        cur.execute(
            """
            SELECT id FROM bookshelves
            WHERE library_id = %s AND name = %s
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (library_id, LAB_BOOKSHELF_NAME),
        )
        row = cur.fetchone()
        if row is None:
            from uuid import uuid4

            bookshelf_id = str(uuid4())
            cur.execute(
                """
                INSERT INTO bookshelves (
                    id, library_id, name, description,
                    is_basement, is_pinned, pinned_at, is_favorite,
                    status, book_count, created_at, updated_at
                )
                VALUES (
                    %s, %s, %s, NULL,
                    FALSE, FALSE, NULL, FALSE,
                    'active', 0, %s, %s
                )
                """,
                (bookshelf_id, library_id, LAB_BOOKSHELF_NAME, now, now),
            )
        else:
            (bookshelf_id,) = row
            bookshelf_id = str(bookshelf_id)

        # Book
        cur.execute(
            """
            SELECT id FROM books
            WHERE library_id = %s AND bookshelf_id = %s AND title = %s
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (library_id, bookshelf_id, LAB_BOOK_TITLE),
        )
        row = cur.fetchone()
        if row is None:
            from uuid import uuid4

            book_id = str(uuid4())
            cur.execute(
                """
                INSERT INTO books (
                    id, bookshelf_id, library_id,
                    title, summary, cover_icon, cover_media_id,
                    is_pinned, due_at, status, maturity,
                    block_count, maturity_score, legacy_flag,
                    manual_maturity_override, manual_maturity_reason,
                    last_visited_at, visit_count_90d,
                    previous_bookshelf_id, moved_to_basement_at, soft_deleted_at,
                    created_at, updated_at
                )
                VALUES (
                    %s, %s, %s,
                    %s, NULL, NULL, NULL,
                    FALSE, NULL, 'draft', 'seed',
                    0, 0, FALSE,
                    FALSE, NULL,
                    NULL, 0,
                    NULL, NULL, NULL,
                    %s, %s
                )
                """,
                (book_id, bookshelf_id, library_id, LAB_BOOK_TITLE, now, now),
            )
        else:
            (book_id,) = row
            book_id = str(book_id)

    return {"library_id": library_id, "bookshelf_id": bookshelf_id, "book_id": book_id}


async def _create_chronicle_event(*, database_url: str) -> dict[str, str]:
    """Create one Chronicle event as backfill source.

    Returns a mapping with library_id, book_id, chronicle_event_id.
    """

    # Ensure SQLAlchemy engine sees the same DB URL.
    os.environ["DATABASE_URL"] = database_url

    cs = _database_url_psycopg(database_url)
    with psycopg.connect(cs) as conn:
        conn.execute("SET TIME ZONE 'UTC'")
        scaffold = _get_or_create_scaffold(conn)
        conn.commit()

    book_id = UUID(scaffold["book_id"])

    session_factory = await get_session_factory()
    async with session_factory() as session:
        repo = SQLAlchemyChronicleRepository(session)
        ev = ChronicleEvent.create(
            event_type=ChronicleEventType.BOOK_UPDATED,
            book_id=book_id,
            payload={"schema_version": 1, "provenance": "s2d1a_daily_stats_backfill_smoke"},
        )
        saved = await repo.save(ev)
        chronicle_event_id = saved.id

    return {
        "library_id": scaffold["library_id"],
        "book_id": str(book_id),
        "chronicle_event_id": str(chronicle_event_id),
    }


def _count_outbox_rows(*, database_url: str, entity_id: str, event_version: int) -> int:
    cs = _database_url_psycopg(database_url)
    with psycopg.connect(cs) as conn:
        conn.execute("SET TIME ZONE 'UTC'")
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT COUNT(*)
                FROM outbox_events
                WHERE projection = %s
                  AND entity_type = %s
                  AND entity_id = %s
                  AND op = 'upsert'
                  AND event_version = %s
                """,
                (PROJECTION_NAME, LAB_ENTITY_TYPE, entity_id, int(event_version)),
            )
            (n,) = cur.fetchone()
            return int(n or 0)


async def _work(*, session: Any, emit: BackfillEmitter, entity_id: UUID, event_version: int) -> None:
    from infra.database.models.chronicle_models import ChronicleEventModel

    stmt = select(ChronicleEventModel).where(ChronicleEventModel.id == entity_id)
    row = (await session.execute(stmt)).scalars().first()
    if row is None:
        raise RuntimeError(f"chronicle_event not found for id={entity_id}")

    await emit.emit(
        BackfillItem(
            projection=PROJECTION_NAME,
            entity_type=LAB_ENTITY_TYPE,
            entity_id=row.id,
            op="upsert",
            event_version=int(event_version),
            library_id=None,
            book_id=row.book_id,
            payload=row.payload or {},
        )
    )

    await emit.flush()


@dataclass(frozen=True)
class EvidenceResult:
    lab_id: str
    scenario: str
    run_id: str
    created_at: str
    ok: bool
    database_url: str
    chronicle: dict[str, Any]
    pass1: dict[str, Any]
    pass2: dict[str, Any]


def _stats_jsonable(stats: BackfillStats) -> dict[str, Any]:
    raw = asdict(stats)
    raw["started_at"] = stats.started_at.isoformat()
    raw["finished_at"] = stats.finished_at.isoformat()
    return raw


async def _run(*, database_url: str, run_id: str, outdir: Path) -> EvidenceResult:
    outdir.mkdir(parents=True, exist_ok=True)

    # Align DB access layers (SQLAlchemy engine reads env at import time).
    os.environ["DATABASE_URL"] = database_url

    # Labs: satisfy the gate explicitly, then enforce it.
    os.environ.setdefault("OUTBOX_BACKFILL_ENABLED", "true")
    require_enabled_env()

    chronicle = await _create_chronicle_event(database_url=database_url)

    entity_id = UUID(chronicle["chronicle_event_id"])
    # For this smoke test we pin event_version=0 (same as writer template).
    event_version = 0

    before0 = _count_outbox_rows(
        database_url=database_url,
        entity_id=str(entity_id),
        event_version=event_version,
    )

    from infra.database.session import get_session_factory as _get_session_factory

    session_factory = await _get_session_factory()

    # Pass 1
    _, stats1 = await run_backfill(
        projection_name=PROJECTION_NAME,
        session_factory=session_factory,
        work=lambda session, emit: _work(
            session=session,
            emit=emit,
            entity_id=entity_id,
            event_version=event_version,
        ),
        run_id=run_id,
        worker_id=f"s2d1a_daily_stats_backfill_smoke:{run_id}",
        dry_run=False,
        batch_size=100,
    )

    after1 = _count_outbox_rows(
        database_url=database_url,
        entity_id=str(entity_id),
        event_version=event_version,
    )

    # Pass 2 (idempotence)
    _, stats2 = await run_backfill(
        projection_name=PROJECTION_NAME,
        session_factory=session_factory,
        work=lambda session, emit: _work(
            session=session,
            emit=emit,
            entity_id=entity_id,
            event_version=event_version,
        ),
        run_id=run_id,
        worker_id=f"s2d1a_daily_stats_backfill_smoke:{run_id}",
        dry_run=False,
        batch_size=100,
    )

    after2 = _count_outbox_rows(
        database_url=database_url,
        entity_id=str(entity_id),
        event_version=event_version,
    )

    pass1 = {
        "before": int(before0),
        "after": int(after1),
        "inserted": int(after1 - before0),
        "stats": _stats_jsonable(stats1),
    }
    pass2 = {
        "before": int(after1),
        "after": int(after2),
        "inserted": int(after2 - after1),
        "stats": _stats_jsonable(stats2),
    }

    ok = pass1["inserted"] == 1 and pass2["inserted"] == 0 and after2 == 1

    result = EvidenceResult(
        lab_id="s2d1a_chronicle_daily_stats_backfill_smoke",
        scenario="verify/chronicle_daily_stats/backfill_outbox_smoke",
        run_id=run_id,
        created_at=_utc_now_str(),
        ok=bool(ok),
        database_url=database_url,
        chronicle=chronicle,
        pass1=pass1,
        pass2=pass2,
    )

    (outdir / "_result.json").write_text(
        json.dumps(asdict(result), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--outdir", required=True)

    args = parser.parse_args()

    database_url = str(args.database_url).strip()
    run_id = str(args.run_id).strip()
    outdir = Path(str(args.outdir).strip())

    # psycopg async is incompatible with ProactorEventLoop on Windows.
    if sys.platform.startswith("win"):
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except Exception:
            pass

    result = asyncio.run(_run(database_url=database_url, run_id=run_id, outdir=outdir))

    if not result.ok:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
