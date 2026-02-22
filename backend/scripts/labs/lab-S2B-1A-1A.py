"""Lab-S2B-1A-1A: Shadow verify chronicle_entries vs chronicle_events.

Goal: provide a cheap, repeatable "shadow verification" artifact before read-switch.

Environment:
- DATABASE_URL: Postgres DSN
- BOOK_ID (optional): scope checks to a single book
- OUTDIR (optional): if provided, writes JSON artifact to OUTDIR/_result.json
- RUN_ID (optional): included in JSON artifact when OUTDIR is provided

Checks:
- counts: events vs entries
- missing entries: chronicle_events without a corresponding chronicle_entries row

Usage (PowerShell):
- $env:DATABASE_URL='postgresql://...'
- python backend/scripts/labs/lab-S2B-1A-1A.py

Artifact usage (optional):
- $env:OUTDIR='docs/labs/_snapshot/manual/lab-S2B-1A-1A/<run_id>'
- $env:RUN_ID='20260218T120000'
- python backend/scripts/labs/lab-S2B-1A-1A.py
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


LAB_ID = "S2B-1A-1A"
SCENARIO = "shadow_verify_chronicle_entries"


@dataclass(frozen=True)
class VerifyResult:
    scope: str
    events_total: int
    entries_total: int
    missing_entries: int
    extra_entries: int
    mismatched_book_id: int


def _parse_book_id(raw: str) -> Optional[UUID]:
    raw = (raw or "").strip()
    if not raw:
        return None
    return UUID(raw)


def _write_artifact(*, outdir: Path, run_id: str | None, result: VerifyResult) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    ok = (result.missing_entries == 0) and (result.extra_entries == 0) and (result.mismatched_book_id == 0)
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

    book_id = _parse_book_id(os.getenv("BOOK_ID") or "")

    outdir_raw = (os.getenv("OUTDIR") or "").strip()
    outdir = Path(outdir_raw) if outdir_raw else None
    run_id = (os.getenv("RUN_ID") or "").strip() or None

    engine = sa.create_engine(database_url)

    with engine.connect() as conn:
        if book_id is None:
            events_total = int(conn.execute(sa.text("SELECT COUNT(*) FROM chronicle_events")).scalar() or 0)
            entries_total = int(conn.execute(sa.text("SELECT COUNT(*) FROM chronicle_entries")).scalar() or 0)
            missing_entries = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM chronicle_events e
                        LEFT JOIN chronicle_entries p ON p.id = e.id
                        WHERE p.id IS NULL
                        """
                    )
                ).scalar()
                or 0
            )
            extra_entries = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM chronicle_entries p
                        LEFT JOIN chronicle_events e ON e.id = p.id
                        WHERE e.id IS NULL
                        """
                    )
                ).scalar()
                or 0
            )
            mismatched_book_id = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM chronicle_events e
                        JOIN chronicle_entries p ON p.id = e.id
                        WHERE p.book_id <> e.book_id
                        """
                    )
                ).scalar()
                or 0
            )
            scope = "all"
        else:
            events_total = int(
                conn.execute(
                    sa.text("SELECT COUNT(*) FROM chronicle_events WHERE book_id = :book_id"),
                    {"book_id": str(book_id)},
                ).scalar()
                or 0
            )
            entries_total = int(
                conn.execute(
                    sa.text("SELECT COUNT(*) FROM chronicle_entries WHERE book_id = :book_id"),
                    {"book_id": str(book_id)},
                ).scalar()
                or 0
            )
            missing_entries = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM chronicle_events e
                        LEFT JOIN chronicle_entries p ON p.id = e.id
                        WHERE e.book_id = :book_id AND p.id IS NULL
                        """
                    ),
                    {"book_id": str(book_id)},
                ).scalar()
                or 0
            )
            extra_entries = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM chronicle_entries p
                        LEFT JOIN chronicle_events e ON e.id = p.id
                        WHERE p.book_id = :book_id AND e.id IS NULL
                        """
                    ),
                    {"book_id": str(book_id)},
                ).scalar()
                or 0
            )
            mismatched_book_id = int(
                conn.execute(
                    sa.text(
                        """
                        SELECT COUNT(*)
                        FROM chronicle_events e
                        JOIN chronicle_entries p ON p.id = e.id
                        WHERE e.book_id = :book_id AND p.book_id <> e.book_id
                        """
                    ),
                    {"book_id": str(book_id)},
                ).scalar()
                or 0
            )
            scope = f"book:{book_id}"

    result = VerifyResult(
        scope=scope,
        events_total=events_total,
        entries_total=entries_total,
        missing_entries=missing_entries,
        extra_entries=extra_entries,
        mismatched_book_id=mismatched_book_id,
    )

    print("lab-S2B-1A-1A.shadow_verify_chronicle_entries")
    print(f"scope={result.scope}")
    print(f"events_total={result.events_total}")
    print(f"entries_total={result.entries_total}")
    print(f"missing_entries={result.missing_entries}")
    print(f"extra_entries={result.extra_entries}")
    print(f"mismatched_book_id={result.mismatched_book_id}")

    if outdir is not None:
        _write_artifact(outdir=outdir, run_id=run_id, result=result)
        print(f"outputs: {outdir}")

    # Exit non-zero if verification fails.
    if (result.missing_entries != 0) or (result.extra_entries != 0) or (result.mismatched_book_id != 0):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
