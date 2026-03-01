"""S2C-3A/P2 rebuild smoke (local, DB-only).

Goal:
- Provide a minimal, catalog-driven "rebuild smoke" scenario that exercises the
  Chronicle rebuild path (DB -> DB) and produces a stable `_result.json`.

What it does:
- Creates (or reuses) a minimal Library/Bookshelf/Book FK chain
- Inserts one Chronicle event via SQLAlchemy repository (schema-aware)
- Invokes the stable rebuild shim with `--event-id` for determinism
- Verifies chronicle_entries was materialized and projection_status bookkeeping updated

Outputs:
- Writes `<outdir>/_result.json` as the evidence SoT for this run.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import psycopg

from api.app.modules.chronicle.domain import ChronicleEvent, ChronicleEventType
from infra.database.session import get_session_factory
from infra.storage.chronicle_repository_impl import SQLAlchemyChronicleRepository


def _utc_now_str() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def _database_url_psycopg(database_url: str) -> str:
    return database_url.replace("postgresql+psycopg://", "postgresql://")


LAB_LIBRARY_NAME = "LAB_S2C3A_REBUILD_SMOKE_LIBRARY"
LAB_BOOKSHELF_NAME = "LAB_S2C3A_REBUILD_SMOKE_SHELF"
LAB_BOOK_TITLE = "LAB_S2C3A_REBUILD_SMOKE_BOOK"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _get_or_create_scaffold(conn: psycopg.Connection) -> dict[str, str]:
    """Create (or reuse) a minimal Library/Bookshelf/Book FK chain."""

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
class SmokeResult:
    lab_id: str
    scenario: str
    run_id: str
    created_at: str
    ok: bool
    database_url: str
    chronicle: dict[str, Any]
    rebuild: dict[str, Any]


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="S2C-3A Chronicle rebuild smoke (DB-only)")
    p.add_argument("--database-url", required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--outdir", required=True)
    return p.parse_args()


async def _create_event(*, database_url: str) -> dict[str, str]:
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
            payload={"schema_version": 1, "provenance": "s2c3a_rebuild_smoke"},
        )
        saved = await repo.save(ev)
        chronicle_event_id = saved.id

    return {
        "library_id": str(scaffold["library_id"]),
        "book_id": str(book_id),
        "chronicle_event_id": str(chronicle_event_id),
    }


def _invoke_rebuild(*, event_id: str, run_id: str) -> int:
    # Run rebuild in a separate process to avoid nested asyncio.run() errors.
    script = Path("backend/scripts/ops/rebuild_chronicle_entries.py")
    if not script.exists():
        raise SystemExit(f"rebuild shim not found: {script}")

    env = dict(os.environ)
    env["RUN_ID"] = run_id

    completed = subprocess.run(
        [sys.executable, str(script), "--event-id", str(event_id)],
        env=env,
        cwd=str(Path.cwd()),
        capture_output=True,
        text=True,
    )

    if completed.stdout:
        print(completed.stdout.rstrip())
    if completed.stderr:
        # Keep stderr for visibility but avoid failing the parent run by printing.
        print(completed.stderr.rstrip(), file=sys.stderr)

    return int(completed.returncode)


def _verify(*, database_url: str, event_id: str) -> dict[str, Any]:
    cs = _database_url_psycopg(database_url)
    with psycopg.connect(cs) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "select count(*) from chronicle_entries where id = %s",
                (str(event_id),),
            )
            entries_for_event = int(cur.fetchone()[0] or 0)

            cur.execute(
                """
                select last_rebuild_success, last_rebuild_finished_at
                from projection_status
                where projection_name = %s
                """,
                ("chronicle_events_to_entries",),
            )
            row = cur.fetchone()
            if row is None:
                status_success = None
                status_finished_at = None
            else:
                (status_success, status_finished_at) = row

    return {
        "entries_for_event": entries_for_event,
        "projection_status": {
            "last_rebuild_success": status_success,
            "last_rebuild_finished_at": str(status_finished_at) if status_finished_at else None,
        },
    }


async def main_async() -> int:
    args = _parse_args()
    database_url = str(args.database_url)
    run_id = str(args.run_id)
    outdir = Path(str(args.outdir))

    outdir.mkdir(parents=True, exist_ok=True)

    created = await _create_event(database_url=database_url)
    event_id = created["chronicle_event_id"]

    rebuild_exit_code = _invoke_rebuild(event_id=event_id, run_id=run_id)
    verified = _verify(database_url=database_url, event_id=event_id)

    ok = (
        rebuild_exit_code == 0
        and int(verified.get("entries_for_event") or 0) == 1
        and verified.get("projection_status", {}).get("last_rebuild_success") in (True, 1)
    )

    result = SmokeResult(
        lab_id="S2C-3A",
        scenario="verify/chronicle/rebuild_entries_smoke",
        run_id=run_id,
        created_at=_utc_now_str(),
        ok=bool(ok),
        database_url=database_url,
        chronicle=created,
        rebuild={"exit_code": int(rebuild_exit_code), **verified},
    )

    (outdir / "_result.json").write_text(json.dumps(asdict(result), indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not ok:
        return 2
    return 0


def main() -> None:
    import asyncio

    if sys.platform == "win32":
        # psycopg async is incompatible with ProactorEventLoop.
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    raise SystemExit(asyncio.run(main_async()))


if __name__ == "__main__":  # pragma: no cover
    main()
