"""S2C-2A/P3 evidence runner (local, DB-only).

This script produces a stable `_result.json` artifact for the writer-template
migration by:

- Creating a minimal library/bookshelf/book FK chain (best-effort, schema-aware)
- Writing one Chronicle event via `SQLAlchemyChronicleRepository.save()` which
  enqueues a unified `outbox_events` row via `OutboxWriter`
- Running the projection framework harness for `chronicle_events_to_entries`
  until idle (so the row is consumed)
- Enqueuing one Search outbox event via `SearchOutboxRepository.enqueue()`
  (writer-template path) and verifying the row exists (no ES/worker required)

Outputs:
- Writes `<outdir>/_result.json` as the evidence SoT for the round.

Notes:
- DB-only by design; Search apply/harness is intentionally not wired in S2C yet.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import psycopg

from api.app.modules.chronicle.domain import ChronicleEvent, ChronicleEventType
from infra.database.session import get_session_factory
from infra.projection_framework.harness import HarnessConfig, run_harness
from infra.search.search_outbox_repository import SearchOutboxRepository
from infra.storage.chronicle_repository_impl import SQLAlchemyChronicleRepository


def _utc_now_str() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def _database_url_psycopg(database_url: str) -> str:
    return database_url.replace("postgresql+psycopg://", "postgresql://")


LAB_LIBRARY_NAME = "LAB_S2C2A_EVIDENCE_LIBRARY"
LAB_BOOKSHELF_NAME = "LAB_S2C2A_EVIDENCE_SHELF"
LAB_BOOK_TITLE = "LAB_S2C2A_EVIDENCE_BOOK"


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


@dataclass(frozen=True)
class EvidenceResult:
    lab_id: str
    scenario: str
    run_id: str
    created_at: str
    ok: bool
    database_url: str
    chronicle: dict[str, Any]
    search_outbox: dict[str, Any]


async def _enqueue_chronicle_and_process(*, database_url: str) -> dict[str, Any]:
    # Ensure Alembic env resolves the same DB.
    os.environ["DATABASE_URL"] = database_url

    # Create a minimal FK chain for chronicle_events.book_id.
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
            payload={"schema_version": 1, "provenance": "s2c2a_evidence"},
        )
        saved = await repo.save(ev)
        chronicle_event_id = saved.id

    # Process the unified outbox row using the harness (DB-only projection).
    cfg = HarnessConfig(
        batch_size=50,
        lease_seconds=15.0,
        max_processing_seconds=300,
        max_attempts=3,
        base_backoff_seconds=0.2,
        max_backoff_seconds=2.0,
        poll_interval_seconds=0.2,
        reclaim_interval_seconds=1.0,
        exit_when_idle=True,
    )
    harness_exit_code = await run_harness(projection_name="chronicle_events_to_entries", config=cfg)

    # Verify: the entry exists for this event + book.
    cs = _database_url_psycopg(database_url)
    with psycopg.connect(cs) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "select count(*) from chronicle_entries where id = %s and book_id = %s",
                (str(chronicle_event_id), str(book_id)),
            )
            entries_for_event = int(cur.fetchone()[0] or 0)

            cur.execute(
                "select count(*) from outbox_events where projection = %s and entity_id = %s",
                ("chronicle_events_to_entries", str(chronicle_event_id)),
            )
            outbox_rows_for_event = int(cur.fetchone()[0] or 0)

    return {
        "book_id": str(book_id),
        "library_id": str(scaffold["library_id"]),
        "chronicle_event_id": str(chronicle_event_id),
        "entries_for_event": int(entries_for_event),
        "outbox_rows_for_event": int(outbox_rows_for_event),
        "harness_exit_code": int(harness_exit_code),
    }


async def _enqueue_search_outbox_only(*, database_url: str) -> dict[str, Any]:
    os.environ["DATABASE_URL"] = database_url

    entity_id = uuid4()
    session_factory = await get_session_factory()
    async with session_factory() as session:
        repo = SearchOutboxRepository(session)
        await repo.enqueue(
            entity_type="book",
            entity_id=entity_id,
            library_id=None,
            op="upsert",
            event_version=int(datetime.now(timezone.utc).timestamp() * 1_000_000),
        )
        await session.commit()

    cs = _database_url_psycopg(database_url)
    with psycopg.connect(cs) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "select id, status from outbox_events where projection = %s and entity_id = %s order by created_at desc limit 1",
                ("search_index_to_elastic", str(entity_id)),
            )
            row = cur.fetchone()

    outbox_id: str | None
    status: str | None
    if row:
        outbox_id = str(row[0])
        status = str(row[1])
    else:
        outbox_id = None
        status = None

    return {
        "entity_type": "book",
        "entity_id": str(entity_id),
        "outbox_id": outbox_id,
        "status": status,
    }


async def _run(*, database_url: str, run_id: str, outdir: Path) -> EvidenceResult:
    outdir.mkdir(parents=True, exist_ok=True)

    chronicle = await _enqueue_chronicle_and_process(database_url=database_url)
    search_outbox = await _enqueue_search_outbox_only(database_url=database_url)

    ok = (
        chronicle.get("harness_exit_code") == 0
        and int(chronicle.get("entries_for_event") or 0) == 1
        and int(chronicle.get("outbox_rows_for_event") or 0) >= 1
        and bool(search_outbox.get("outbox_id"))
        and str(search_outbox.get("status")) == "pending"
    )

    return EvidenceResult(
        lab_id="S2C-2A",
        scenario="s2c2a_writer_template_harness_evidence",
        run_id=run_id,
        created_at=_utc_now_str(),
        ok=bool(ok),
        database_url=database_url,
        chronicle=chronicle,
        search_outbox=search_outbox,
    )


def main(argv: list[str] | None = None) -> int:
    # psycopg async cannot run on ProactorEventLoop. Force Selector policy on Windows.
    import sys

    if sys.platform.startswith("win"):
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except Exception:
            pass

    p = argparse.ArgumentParser(description="S2C-2A/P3 harness evidence runner (DB-only)")
    p.add_argument("--database-url", required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--outdir", required=True)
    args = p.parse_args(argv)

    database_url = str(args.database_url).strip()
    run_id = str(args.run_id).strip()
    outdir = Path(str(args.outdir)).resolve()

    result = asyncio.run(_run(database_url=database_url, run_id=run_id, outdir=outdir))
    (outdir / "_result.json").write_text(json.dumps(asdict(result), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"ok={result.ok}")
    print(f"outputs: {outdir}")
    return 0 if result.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
