from __future__ import annotations

import time
from typing import Any

from sqlalchemy import create_engine, text

from ..registry import register
from ..types import DrillInputs, DrillResult


@register("shadow_verify_chronicle_entries")
@register("shadow-verify-chronicle-entries")
def run(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    database_url = str(payload.get("database_url") or "").strip()
    book_id = (str(payload.get("book_id") or "").strip() or None)

    # Validation is expected to be handled by the shim (legacy CLI) to preserve behavior.
    if not database_url:
        return DrillResult(ok=False, errors=["DATABASE_URL is required"], meta={}, summary={})

    engine = create_engine(database_url)
    with engine.connect() as conn:
        if book_id is None:
            events_total = int(conn.execute(text("SELECT COUNT(*) FROM chronicle_events")).scalar() or 0)
            entries_total = int(conn.execute(text("SELECT COUNT(*) FROM chronicle_entries")).scalar() or 0)
            missing_entries = int(
                conn.execute(
                    text(
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
                    text(
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
                    text(
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
                    text("SELECT COUNT(*) FROM chronicle_events WHERE book_id = :book_id"),
                    {"book_id": book_id},
                ).scalar()
                or 0
            )
            entries_total = int(
                conn.execute(
                    text("SELECT COUNT(*) FROM chronicle_entries WHERE book_id = :book_id"),
                    {"book_id": book_id},
                ).scalar()
                or 0
            )
            missing_entries = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM chronicle_events e
                        LEFT JOIN chronicle_entries p ON p.id = e.id
                        WHERE e.book_id = :book_id AND p.id IS NULL
                        """
                    ),
                    {"book_id": book_id},
                ).scalar()
                or 0
            )
            extra_entries = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM chronicle_entries p
                        LEFT JOIN chronicle_events e ON e.id = p.id
                        WHERE p.book_id = :book_id AND e.id IS NULL
                        """
                    ),
                    {"book_id": book_id},
                ).scalar()
                or 0
            )
            mismatched_book_id = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM chronicle_events e
                        JOIN chronicle_entries p ON p.id = e.id
                        WHERE e.book_id = :book_id AND p.book_id <> e.book_id
                        """
                    ),
                    {"book_id": book_id},
                ).scalar()
                or 0
            )
            scope = f"book:{book_id}"

    ok = (missing_entries == 0) and (extra_entries == 0) and (mismatched_book_id == 0)

    result: dict[str, Any] = {
        "lab_id": inputs.scope_id,
        "scenario": "shadow_verify_chronicle_entries",
        "run_id": inputs.run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "scope": scope,
        "events_total": int(events_total),
        "entries_total": int(entries_total),
        "missing_entries": int(missing_entries),
        "extra_entries": int(extra_entries),
        "mismatched_book_id": int(mismatched_book_id),
        "ok": bool(ok),
    }

    return DrillResult(
        ok=bool(ok),
        meta=result,
        summary={
            "scope": scope,
            "missing_entries": int(missing_entries),
            "extra_entries": int(extra_entries),
            "mismatched_book_id": int(mismatched_book_id),
        },
        errors=[],
    )
