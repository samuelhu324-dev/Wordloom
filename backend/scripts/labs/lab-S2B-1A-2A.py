"""Lab-S2B-1A-2A: Shadow verify search_index vs source-of-truth tables.

Goal: provide a cheap, repeatable "shadow verification" artifact for Search before
any read switch / index provider switch.

Environment:
- DATABASE_URL: Postgres DSN (required)
- LIBRARY_ID (optional): scope block/book checks to a single library
- OUTDIR (optional): if provided, writes JSON artifact to OUTDIR/_result.json
- RUN_ID (optional): included in JSON artifact when OUTDIR is provided

Checks (v0):
- counts: SoT tables vs search_index (by entity type)
- missing: SoT entity exists but search_index row missing
- extra: search_index row exists but SoT entity missing or soft-deleted
- key consistency: search_index.library_id matches books.library_id for block/book
  (tags are not library-scoped; their search_index.library_id should be NULL)

Usage (PowerShell):
- $env:DATABASE_URL='postgresql://...'
- python backend/scripts/labs/lab-S2B-1A-2A.py

Optional (scope to a single library):
- $env:LIBRARY_ID='<uuid>'
- python backend/scripts/labs/lab-S2B-1A-2A.py
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional
from uuid import UUID

import sqlalchemy as sa


_SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from cli_app.common import write_json


LAB_ID = "S2B-1A-2A"
SCENARIO = "shadow_verify_search_index"


@dataclass(frozen=True)
class VerifyResult:
    scope: str

    blocks_total: int
    blocks_index_total: int
    blocks_missing: int
    blocks_extra: int
    blocks_mismatched_library_id: int

    books_total: int
    books_index_total: int
    books_missing: int
    books_extra: int
    books_mismatched_library_id: int

    tags_total: int
    tags_index_total: int
    tags_missing: int
    tags_extra: int
    tags_invalid_library_id: int

    outbox_total: int
    outbox_pending: int
    outbox_processing: int
    outbox_done: int
    outbox_failed: int


def _parse_uuid(raw: str) -> Optional[UUID]:
    raw = (raw or "").strip()
    if not raw:
        return None
    return UUID(raw)


def _write_artifact(*, outdir: Path, run_id: str | None, result: VerifyResult) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    ok = (
        (result.blocks_missing == 0)
        and (result.blocks_extra == 0)
        and (result.blocks_mismatched_library_id == 0)
        and (result.books_missing == 0)
        and (result.books_extra == 0)
        and (result.books_mismatched_library_id == 0)
        and (result.tags_missing == 0)
        and (result.tags_extra == 0)
        and (result.tags_invalid_library_id == 0)
    )

    payload: dict[str, object] = {
        "lab_id": LAB_ID,
        "scenario": SCENARIO,
        "run_id": run_id,
        "scope": result.scope,
        "ok": bool(ok),
        **asdict(result),
    }
    write_json(outdir / "_result.json", payload)


def main() -> None:
    database_url = (os.getenv("DATABASE_URL") or "").strip()
    if not database_url:
        raise SystemExit("DATABASE_URL is required")

    library_id = _parse_uuid(os.getenv("LIBRARY_ID") or "")

    outdir_raw = (os.getenv("OUTDIR") or "").strip()
    outdir = Path(outdir_raw) if outdir_raw else None
    run_id = (os.getenv("RUN_ID") or "").strip() or None

    engine = sa.create_engine(database_url)

    with engine.connect() as conn:
        if library_id is None:
            scope = "all"
            blocks_total = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM blocks bl
                        JOIN books bo ON bo.id = bl.book_id
                        WHERE bl.soft_deleted_at IS NULL
                          AND bo.soft_deleted_at IS NULL
                        """
                    )
                ).scalar()
                or 0
            )
            blocks_index_total = int(conn.execute(sa.text("SELECT COUNT(*) FROM search_index WHERE entity_type = 'block' ")).scalar() or 0)
            blocks_missing = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM blocks bl
                        JOIN books bo ON bo.id = bl.book_id
                        LEFT JOIN search_index si
                          ON si.entity_type = 'block'
                         AND si.entity_id = bl.id
                        WHERE bl.soft_deleted_at IS NULL
                          AND bo.soft_deleted_at IS NULL
                          AND si.entity_id IS NULL
                        """
                    )
                ).scalar()
                or 0
            )
            blocks_extra = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM search_index si
                        LEFT JOIN blocks bl ON bl.id = si.entity_id
                        LEFT JOIN books bo ON bo.id = bl.book_id
                        WHERE si.entity_type = 'block'
                          AND (
                            bl.id IS NULL
                            OR bl.soft_deleted_at IS NOT NULL
                            OR bo.id IS NULL
                            OR bo.soft_deleted_at IS NOT NULL
                          )
                        """
                    )
                ).scalar()
                or 0
            )
            blocks_mismatched_library_id = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM search_index si
                        JOIN blocks bl ON bl.id = si.entity_id
                        JOIN books bo ON bo.id = bl.book_id
                        WHERE si.entity_type = 'block'
                          AND bo.soft_deleted_at IS NULL
                          AND bl.soft_deleted_at IS NULL
                          AND (si.library_id IS DISTINCT FROM bo.library_id)
                        """
                    )
                ).scalar()
                or 0
            )

            books_total = int(conn.execute(sa.text("SELECT COUNT(*) FROM books WHERE soft_deleted_at IS NULL")).scalar() or 0)
            books_index_total = int(conn.execute(sa.text("SELECT COUNT(*) FROM search_index WHERE entity_type = 'book'")).scalar() or 0)
            books_missing = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM books bo
                        LEFT JOIN search_index si
                          ON si.entity_type = 'book'
                         AND si.entity_id = bo.id
                        WHERE bo.soft_deleted_at IS NULL
                          AND si.entity_id IS NULL
                        """
                    )
                ).scalar()
                or 0
            )
            books_extra = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM search_index si
                        LEFT JOIN books bo ON bo.id = si.entity_id
                        WHERE si.entity_type = 'book'
                          AND (bo.id IS NULL OR bo.soft_deleted_at IS NOT NULL)
                        """
                    )
                ).scalar()
                or 0
            )
            books_mismatched_library_id = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM search_index si
                        JOIN books bo ON bo.id = si.entity_id
                        WHERE si.entity_type = 'book'
                          AND bo.soft_deleted_at IS NULL
                          AND (si.library_id IS DISTINCT FROM bo.library_id)
                        """
                    )
                ).scalar()
                or 0
            )
        else:
            scope = f"library:{library_id}"
            params = {"library_id": str(library_id)}

            blocks_total = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM blocks bl
                        JOIN books bo ON bo.id = bl.book_id
                        WHERE bl.soft_deleted_at IS NULL
                          AND bo.soft_deleted_at IS NULL
                          AND bo.library_id = :library_id
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )
            blocks_index_total = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM search_index
                        WHERE entity_type = 'block'
                          AND library_id = :library_id
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )
            blocks_missing = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM blocks bl
                        JOIN books bo ON bo.id = bl.book_id
                        LEFT JOIN search_index si
                          ON si.entity_type = 'block'
                         AND si.entity_id = bl.id
                        WHERE bl.soft_deleted_at IS NULL
                          AND bo.soft_deleted_at IS NULL
                          AND bo.library_id = :library_id
                          AND si.entity_id IS NULL
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )
            blocks_extra = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM search_index si
                        LEFT JOIN blocks bl ON bl.id = si.entity_id
                        LEFT JOIN books bo ON bo.id = bl.book_id
                        WHERE si.entity_type = 'block'
                          AND si.library_id = :library_id
                          AND (
                            bl.id IS NULL
                            OR bl.soft_deleted_at IS NOT NULL
                            OR bo.id IS NULL
                            OR bo.soft_deleted_at IS NOT NULL
                            OR bo.library_id <> :library_id
                          )
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )
            blocks_mismatched_library_id = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM search_index si
                        JOIN blocks bl ON bl.id = si.entity_id
                        JOIN books bo ON bo.id = bl.book_id
                        WHERE si.entity_type = 'block'
                          AND bo.library_id = :library_id
                          AND bo.soft_deleted_at IS NULL
                          AND bl.soft_deleted_at IS NULL
                          AND (si.library_id IS DISTINCT FROM bo.library_id)
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )

            books_total = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM books
                        WHERE soft_deleted_at IS NULL
                          AND library_id = :library_id
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )
            books_index_total = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM search_index
                        WHERE entity_type = 'book'
                          AND library_id = :library_id
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )
            books_missing = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM books bo
                        LEFT JOIN search_index si
                          ON si.entity_type = 'book'
                         AND si.entity_id = bo.id
                        WHERE bo.soft_deleted_at IS NULL
                          AND bo.library_id = :library_id
                          AND si.entity_id IS NULL
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )
            books_extra = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM search_index si
                        LEFT JOIN books bo ON bo.id = si.entity_id
                        WHERE si.entity_type = 'book'
                          AND si.library_id = :library_id
                          AND (
                            bo.id IS NULL
                            OR bo.soft_deleted_at IS NOT NULL
                            OR bo.library_id <> :library_id
                          )
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )
            books_mismatched_library_id = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM search_index si
                        JOIN books bo ON bo.id = si.entity_id
                        WHERE si.entity_type = 'book'
                          AND bo.library_id = :library_id
                          AND bo.soft_deleted_at IS NULL
                          AND (si.library_id IS DISTINCT FROM bo.library_id)
                        """
                    ),
                    params,
                ).scalar()
                or 0
            )

        # Tags are global (not library-scoped in search_indexer).
        tags_total = int(conn.execute(sa.text("SELECT COUNT(*) FROM tags WHERE deleted_at IS NULL")).scalar() or 0)
        tags_index_total = int(conn.execute(sa.text("SELECT COUNT(*) FROM search_index WHERE entity_type = 'tag'")).scalar() or 0)
        tags_missing = int(
            conn.execute(
                sa.text(
                    """
                    SELECT COUNT(*)
                    FROM tags t
                    LEFT JOIN search_index si
                      ON si.entity_type = 'tag'
                     AND si.entity_id = t.id
                    WHERE t.deleted_at IS NULL
                      AND si.entity_id IS NULL
                    """
                )
            ).scalar()
            or 0
        )
        tags_extra = int(
            conn.execute(
                sa.text(
                    """
                    SELECT COUNT(*)
                    FROM search_index si
                    LEFT JOIN tags t ON t.id = si.entity_id
                    WHERE si.entity_type = 'tag'
                      AND (t.id IS NULL OR t.deleted_at IS NOT NULL)
                    """
                )
            ).scalar()
            or 0
        )
        tags_invalid_library_id = int(
            conn.execute(
                sa.text(
                    """
                    SELECT COUNT(*)
                    FROM search_index
                    WHERE entity_type = 'tag'
                      AND library_id IS NOT NULL
                    """
                )
            ).scalar()
            or 0
        )

        outbox_total = int(conn.execute(sa.text("SELECT COUNT(*) FROM search_outbox_events")).scalar() or 0)
        outbox_pending = int(
            conn.execute(sa.text("SELECT COUNT(*) FROM search_outbox_events WHERE status = 'pending'")).scalar() or 0
        )
        outbox_processing = int(
            conn.execute(sa.text("SELECT COUNT(*) FROM search_outbox_events WHERE status = 'processing'")).scalar() or 0
        )
        outbox_done = int(conn.execute(sa.text("SELECT COUNT(*) FROM search_outbox_events WHERE status = 'done'")).scalar() or 0)
        outbox_failed = int(
            conn.execute(sa.text("SELECT COUNT(*) FROM search_outbox_events WHERE status = 'failed'")).scalar() or 0
        )

    result = VerifyResult(
        scope=scope,
        blocks_total=blocks_total,
        blocks_index_total=blocks_index_total,
        blocks_missing=blocks_missing,
        blocks_extra=blocks_extra,
        blocks_mismatched_library_id=blocks_mismatched_library_id,
        books_total=books_total,
        books_index_total=books_index_total,
        books_missing=books_missing,
        books_extra=books_extra,
        books_mismatched_library_id=books_mismatched_library_id,
        tags_total=tags_total,
        tags_index_total=tags_index_total,
        tags_missing=tags_missing,
        tags_extra=tags_extra,
        tags_invalid_library_id=tags_invalid_library_id,
        outbox_total=outbox_total,
        outbox_pending=outbox_pending,
        outbox_processing=outbox_processing,
        outbox_done=outbox_done,
        outbox_failed=outbox_failed,
    )

    print("lab-S2B-1A-2A.shadow_verify_search_index")
    print(f"scope={result.scope}")
    print(f"blocks_total={result.blocks_total}")
    print(f"blocks_index_total={result.blocks_index_total}")
    print(f"blocks_missing={result.blocks_missing}")
    print(f"blocks_extra={result.blocks_extra}")
    print(f"blocks_mismatched_library_id={result.blocks_mismatched_library_id}")
    print(f"books_total={result.books_total}")
    print(f"books_index_total={result.books_index_total}")
    print(f"books_missing={result.books_missing}")
    print(f"books_extra={result.books_extra}")
    print(f"books_mismatched_library_id={result.books_mismatched_library_id}")
    print(f"tags_total={result.tags_total}")
    print(f"tags_index_total={result.tags_index_total}")
    print(f"tags_missing={result.tags_missing}")
    print(f"tags_extra={result.tags_extra}")
    print(f"tags_invalid_library_id={result.tags_invalid_library_id}")
    print(f"outbox_total={result.outbox_total}")
    print(f"outbox_pending={result.outbox_pending}")
    print(f"outbox_processing={result.outbox_processing}")
    print(f"outbox_done={result.outbox_done}")
    print(f"outbox_failed={result.outbox_failed}")

    if outdir is not None:
        _write_artifact(outdir=outdir, run_id=run_id, result=result)
        print(f"outputs: {outdir}")

    if (
        (result.blocks_missing != 0)
        or (result.blocks_extra != 0)
        or (result.blocks_mismatched_library_id != 0)
        or (result.books_missing != 0)
        or (result.books_extra != 0)
        or (result.books_mismatched_library_id != 0)
        or (result.tags_missing != 0)
        or (result.tags_extra != 0)
        or (result.tags_invalid_library_id != 0)
    ):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
