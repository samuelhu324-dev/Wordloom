from __future__ import annotations

import time
from typing import Any

from sqlalchemy import create_engine, text

from infra.outbox_unified.toggles import is_unified_outbox_read_enabled

from ._pg_introspection import table_exists

from ..registry import register
from ..types import DrillInputs, DrillResult


SEARCH_OUTBOX_PROJECTION = "search_index_to_elastic"


@register("shadow_verify_search_index")
@register("shadow-verify-search-index")
def run(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    database_url = str(payload.get("database_url") or "").strip()
    library_id = (str(payload.get("library_id") or "").strip() or None)

    # Validation is expected to be handled by the shim (legacy CLI) to preserve behavior.
    if not database_url:
        return DrillResult(ok=False, errors=["DATABASE_URL is required"], meta={}, summary={})

    engine = create_engine(database_url)
    with engine.connect() as conn:
        if library_id is None:
            scope = "all"
            blocks_total = int(
                conn.execute(
                    text(
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
            blocks_index_total = int(
                conn.execute(text("SELECT COUNT(*) FROM search_index WHERE entity_type = 'block' ")).scalar() or 0
            )
            blocks_missing = int(
                conn.execute(
                    text(
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
                    text(
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
                    text(
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

            books_total = int(conn.execute(text("SELECT COUNT(*) FROM books WHERE soft_deleted_at IS NULL")).scalar() or 0)
            books_index_total = int(
                conn.execute(text("SELECT COUNT(*) FROM search_index WHERE entity_type = 'book'")).scalar() or 0
            )
            books_missing = int(
                conn.execute(
                    text(
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
                    text(
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
                    text(
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
            params = {"library_id": library_id}

            blocks_total = int(
                conn.execute(
                    text(
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
                    text(
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
                    text(
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
                    text(
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
                    text(
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
                    text(
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
                    text(
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
                    text(
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
                    text(
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
                    text(
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

        tags_total = int(conn.execute(text("SELECT COUNT(*) FROM tags WHERE deleted_at IS NULL")).scalar() or 0)
        tags_index_total = int(conn.execute(text("SELECT COUNT(*) FROM search_index WHERE entity_type = 'tag'")).scalar() or 0)
        tags_missing = int(
            conn.execute(
                text(
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
                text(
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
                text(
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

        legacy_outbox_available = table_exists(conn, "search_outbox_events")
        use_unified = is_unified_outbox_read_enabled(SEARCH_OUTBOX_PROJECTION) or (not legacy_outbox_available)
        if use_unified:
            outbox_total = int(
                conn.execute(
                    text("SELECT COUNT(*) FROM outbox_events WHERE projection = :projection"),
                    {"projection": SEARCH_OUTBOX_PROJECTION},
                ).scalar()
                or 0
            )
            outbox_pending = int(
                conn.execute(
                    text(
                        "SELECT COUNT(*) FROM outbox_events WHERE projection = :projection AND status = 'pending'"
                    ),
                    {"projection": SEARCH_OUTBOX_PROJECTION},
                ).scalar()
                or 0
            )
            outbox_processing = int(
                conn.execute(
                    text(
                        "SELECT COUNT(*) FROM outbox_events WHERE projection = :projection AND status = 'processing'"
                    ),
                    {"projection": SEARCH_OUTBOX_PROJECTION},
                ).scalar()
                or 0
            )
            outbox_done = int(
                conn.execute(
                    text("SELECT COUNT(*) FROM outbox_events WHERE projection = :projection AND status = 'done'"),
                    {"projection": SEARCH_OUTBOX_PROJECTION},
                ).scalar()
                or 0
            )
            outbox_failed = int(
                conn.execute(
                    text(
                        "SELECT COUNT(*) FROM outbox_events WHERE projection = :projection AND status = 'failed'"
                    ),
                    {"projection": SEARCH_OUTBOX_PROJECTION},
                ).scalar()
                or 0
            )
        else:
            outbox_total = int(conn.execute(text("SELECT COUNT(*) FROM search_outbox_events")).scalar() or 0)
            outbox_pending = int(
                conn.execute(text("SELECT COUNT(*) FROM search_outbox_events WHERE status = 'pending'")).scalar()
                or 0
            )
            outbox_processing = int(
                conn.execute(text("SELECT COUNT(*) FROM search_outbox_events WHERE status = 'processing'")).scalar()
                or 0
            )
            outbox_done = int(conn.execute(text("SELECT COUNT(*) FROM search_outbox_events WHERE status = 'done'")).scalar() or 0)
            outbox_failed = int(
                conn.execute(text("SELECT COUNT(*) FROM search_outbox_events WHERE status = 'failed'")).scalar()
                or 0
            )

    ok = (
        (blocks_missing == 0)
        and (blocks_extra == 0)
        and (blocks_mismatched_library_id == 0)
        and (books_missing == 0)
        and (books_extra == 0)
        and (books_mismatched_library_id == 0)
        and (tags_missing == 0)
        and (tags_extra == 0)
        and (tags_invalid_library_id == 0)
    )

    result: dict[str, Any] = {
        "lab_id": inputs.scope_id,
        "scenario": "shadow_verify_search_index",
        "run_id": inputs.run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "scope": scope,
        "blocks_total": int(blocks_total),
        "blocks_index_total": int(blocks_index_total),
        "blocks_missing": int(blocks_missing),
        "blocks_extra": int(blocks_extra),
        "blocks_mismatched_library_id": int(blocks_mismatched_library_id),
        "books_total": int(books_total),
        "books_index_total": int(books_index_total),
        "books_missing": int(books_missing),
        "books_extra": int(books_extra),
        "books_mismatched_library_id": int(books_mismatched_library_id),
        "tags_total": int(tags_total),
        "tags_index_total": int(tags_index_total),
        "tags_missing": int(tags_missing),
        "tags_extra": int(tags_extra),
        "tags_invalid_library_id": int(tags_invalid_library_id),
        "outbox_total": int(outbox_total),
        "outbox_pending": int(outbox_pending),
        "outbox_processing": int(outbox_processing),
        "outbox_done": int(outbox_done),
        "outbox_failed": int(outbox_failed),
        "ok": bool(ok),
    }

    return DrillResult(
        ok=bool(ok),
        meta=result,
        summary={
            "scope": scope,
            "blocks_missing": int(blocks_missing),
            "blocks_extra": int(blocks_extra),
            "books_missing": int(books_missing),
            "books_extra": int(books_extra),
            "tags_missing": int(tags_missing),
            "tags_extra": int(tags_extra),
        },
        errors=[],
    )
