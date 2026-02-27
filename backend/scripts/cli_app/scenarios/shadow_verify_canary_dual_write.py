from __future__ import annotations

import time
import uuid
from datetime import datetime, timezone

from sqlalchemy import bindparam, create_engine, text

from infra.outbox_unified.toggles import is_unified_outbox_write_enabled

from ..registry import register
from ..types import DrillInputs, DrillResult


SEARCH_OUTBOX_PROJECTION = "search_index_to_elastic"


@register("shadow_verify_canary_dual_write")
@register("shadow-verify-canary-dual-write")
def run(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    database_url = str(payload.get("database_url") or "").strip()
    if not database_url:
        return DrillResult(ok=False, errors=["DATABASE_URL is required"], meta={}, summary={})

    library_id = (str(payload.get("library_id") or "").strip() or None)
    if library_id is not None:
        try:
            uuid.UUID(library_id)
        except ValueError:
            return DrillResult(ok=False, errors=[f"invalid library_id: {library_id}"], meta={}, summary={})

    max_writes = int(payload.get("max_writes") or 0)
    if max_writes <= 0:
        return DrillResult(ok=False, errors=["max_writes must be > 0"], meta={}, summary={})

    cleanup = bool(payload.get("cleanup"))
    scope = "all" if library_id is None else f"library:{library_id}"
    entity_type = "canary"

    now = datetime.now(timezone.utc)
    entity_ids: list[str] = [str(uuid.uuid4()) for _ in range(max_writes)]
    search_index_ids: list[str] = [str(uuid.uuid4()) for _ in range(max_writes)]
    outbox_ids: list[str] = [str(uuid.uuid4()) for _ in range(max_writes)]

    search_rows: list[dict[str, object]] = []
    outbox_rows: list[dict[str, object]] = []
    for i in range(max_writes):
        search_rows.append(
            {
                "id": search_index_ids[i],
                "entity_type": entity_type,
                "library_id": library_id,
                "entity_id": entity_ids[i],
                "text": f"canary:{inputs.run_id}:{i}",
                "snippet": None,
                "rank_score": 0.0,
                "created_at": now,
                "updated_at": now,
                "event_version": int(i + 1),
            }
        )
        outbox_rows.append(
            {
                "id": outbox_ids[i],
                "entity_type": entity_type,
                "library_id": library_id,
                "entity_id": entity_ids[i],
                "op": "upsert",
                "event_version": int(i + 1),
                "created_at": now,
                "status": "pending",
                "attempts": 0,
                "updated_at": now,
                "replay_count": 0,
            }
        )

    engine = create_engine(database_url)
    inserted_search = 0
    inserted_outbox = 0
    inserted_unified_outbox = 0
    verify_search_count = 0
    verify_outbox_count = 0
    verify_unified_outbox_count = 0
    cleanup_deleted_search = 0
    cleanup_deleted_outbox = 0
    cleanup_deleted_unified_outbox = 0
    cleanup_remaining_search: int | None = None
    cleanup_remaining_outbox: int | None = None
    cleanup_remaining_unified_outbox: int | None = None
    dup_extra = 0

    with engine.connect() as conn:
        # 1) insert projection rows
        conn.execute(
            text(
                """
                INSERT INTO search_index
                  (id, entity_type, library_id, entity_id, text, snippet, rank_score, created_at, updated_at, event_version)
                VALUES
                  (:id, :entity_type, :library_id, :entity_id, :text, :snippet, :rank_score, :created_at, :updated_at, :event_version)
                """
            ),
            search_rows,
        )
        inserted_search = max_writes

        # 2) enqueue outbox rows
        conn.execute(
            text(
                """
                INSERT INTO search_outbox_events
                                    (id, entity_type, library_id, entity_id, op, event_version, created_at, status, attempts, updated_at, replay_count)
                VALUES
                                    (:id, :entity_type, :library_id, :entity_id, :op, :event_version, :created_at, :status, :attempts, :updated_at, :replay_count)
                """
            ),
            outbox_rows,
        )
        inserted_outbox = max_writes

        if is_unified_outbox_write_enabled(SEARCH_OUTBOX_PROJECTION):
            unified_rows = [{**r, "projection": SEARCH_OUTBOX_PROJECTION} for r in outbox_rows]
            conn.execute(
                text(
                    """
                    INSERT INTO outbox_events
                                    (id, projection, entity_type, library_id, entity_id, op, event_version, created_at, status, attempts, updated_at, replay_count)
                    VALUES
                                    (:id, :projection, :entity_type, :library_id, :entity_id, :op, :event_version, :created_at, :status, :attempts, :updated_at, :replay_count)
                    """
                ),
                unified_rows,
            )
            inserted_unified_outbox = max_writes

        conn.commit()

        # 3) verify presence
        verify_search_count = int(
            conn.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM search_index
                    WHERE entity_type = :entity_type
                      AND entity_id IN :entity_ids
                    """
                ).bindparams(bindparam("entity_ids", expanding=True)),
                {"entity_type": entity_type, "entity_ids": entity_ids},
            ).scalar()
            or 0
        )
        verify_outbox_count = int(
            conn.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM search_outbox_events
                    WHERE entity_type = :entity_type
                      AND entity_id IN :entity_ids
                    """
                ).bindparams(bindparam("entity_ids", expanding=True)),
                {"entity_type": entity_type, "entity_ids": entity_ids},
            ).scalar()
            or 0
        )

        if is_unified_outbox_write_enabled(SEARCH_OUTBOX_PROJECTION):
            verify_unified_outbox_count = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM outbox_events
                        WHERE projection = :projection
                          AND entity_type = :entity_type
                          AND entity_id IN :entity_ids
                        """
                    ).bindparams(bindparam("entity_ids", expanding=True)),
                    {
                        "projection": SEARCH_OUTBOX_PROJECTION,
                        "entity_type": entity_type,
                        "entity_ids": entity_ids,
                    },
                ).scalar()
                or 0
            )

        # 4) verify write-gate uniqueness still holds
        dup_extra = int(
            conn.execute(
                text(
                    """
                    SELECT COALESCE(SUM(cnt - 1), 0)
                    FROM (
                      SELECT COUNT(*) AS cnt
                      FROM search_index
                      GROUP BY entity_type, entity_id
                      HAVING COUNT(*) > 1
                    ) t
                    """
                )
            ).scalar()
            or 0
        )

        # 5) cleanup (rollback evidence)
        if cleanup:
            conn.execute(
                text(
                    """
                    DELETE FROM search_outbox_events
                    WHERE entity_type = :entity_type
                      AND entity_id IN :entity_ids
                    """
                ).bindparams(bindparam("entity_ids", expanding=True)),
                {"entity_type": entity_type, "entity_ids": entity_ids},
            )
            if is_unified_outbox_write_enabled(SEARCH_OUTBOX_PROJECTION):
                conn.execute(
                    text(
                        """
                        DELETE FROM outbox_events
                        WHERE projection = :projection
                          AND entity_type = :entity_type
                          AND entity_id IN :entity_ids
                        """
                    ).bindparams(bindparam("entity_ids", expanding=True)),
                    {
                        "projection": SEARCH_OUTBOX_PROJECTION,
                        "entity_type": entity_type,
                        "entity_ids": entity_ids,
                    },
                )
            conn.execute(
                text(
                    """
                    DELETE FROM search_index
                    WHERE entity_type = :entity_type
                      AND entity_id IN :entity_ids
                    """
                ).bindparams(bindparam("entity_ids", expanding=True)),
                {"entity_type": entity_type, "entity_ids": entity_ids},
            )
            conn.commit()

            cleanup_remaining_search = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM search_index
                        WHERE entity_type = :entity_type
                          AND entity_id IN :entity_ids
                        """
                    ).bindparams(bindparam("entity_ids", expanding=True)),
                    {"entity_type": entity_type, "entity_ids": entity_ids},
                ).scalar()
                or 0
            )
            cleanup_remaining_outbox = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM search_outbox_events
                        WHERE entity_type = :entity_type
                          AND entity_id IN :entity_ids
                        """
                    ).bindparams(bindparam("entity_ids", expanding=True)),
                    {"entity_type": entity_type, "entity_ids": entity_ids},
                ).scalar()
                or 0
            )

            if is_unified_outbox_write_enabled(SEARCH_OUTBOX_PROJECTION):
                cleanup_remaining_unified_outbox = int(
                    conn.execute(
                        text(
                            """
                            SELECT COUNT(*)
                            FROM outbox_events
                            WHERE projection = :projection
                              AND entity_type = :entity_type
                              AND entity_id IN :entity_ids
                            """
                        ).bindparams(bindparam("entity_ids", expanding=True)),
                        {
                            "projection": SEARCH_OUTBOX_PROJECTION,
                            "entity_type": entity_type,
                            "entity_ids": entity_ids,
                        },
                    ).scalar()
                    or 0
                )

            cleanup_deleted_search = verify_search_count - cleanup_remaining_search
            cleanup_deleted_outbox = verify_outbox_count - cleanup_remaining_outbox
            if is_unified_outbox_write_enabled(SEARCH_OUTBOX_PROJECTION):
                cleanup_deleted_unified_outbox = verify_unified_outbox_count - (cleanup_remaining_unified_outbox or 0)

    ok = (
        inserted_search == max_writes
        and inserted_outbox == max_writes
        and (
            (not is_unified_outbox_write_enabled(SEARCH_OUTBOX_PROJECTION))
            or (inserted_unified_outbox == max_writes)
        )
        and verify_search_count == max_writes
        and verify_outbox_count == max_writes
        and (
            (not is_unified_outbox_write_enabled(SEARCH_OUTBOX_PROJECTION))
            or (verify_unified_outbox_count == max_writes)
        )
        and dup_extra == 0
        and (
            (not cleanup)
            or (
                cleanup_remaining_search == 0
                and cleanup_remaining_outbox == 0
                and (
                    (not is_unified_outbox_write_enabled(SEARCH_OUTBOX_PROJECTION))
                    or (cleanup_remaining_unified_outbox == 0)
                )
            )
        )
    )

    result: dict[str, object] = {
        "lab_id": inputs.scope_id,
        "scenario": "shadow_verify_canary_dual_write",
        "run_id": inputs.run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "scope": scope,
        "dry_run": False,
        "targets": {
            "projection_table": "search_index",
            "outbox_table": "search_outbox_events",
            "unified_outbox_table": ("outbox_events" if is_unified_outbox_write_enabled(SEARCH_OUTBOX_PROJECTION) else None),
            "entrypoint_hint": "backend/infra/search/search_indexer.py::PostgresSearchIndexer (writes search_index + enqueues search_outbox_events)",
        },
        "canary": {
            "entity_type": entity_type,
            "max_writes": max_writes,
            "entity_ids": entity_ids,
            "search_index_ids": search_index_ids,
            "outbox_event_ids": outbox_ids,
        },
        "verify": {
            "search_index_rows_found": int(verify_search_count),
            "search_outbox_rows_found": int(verify_outbox_count),
            "unified_outbox_rows_found": (
                int(verify_unified_outbox_count) if is_unified_outbox_write_enabled(SEARCH_OUTBOX_PROJECTION) else None
            ),
            "duplicates_extra_rows_total": int(dup_extra),
        },
        "rollback": {
            "cleanup_enabled": bool(cleanup),
            "deleted_search_index": int(cleanup_deleted_search),
            "deleted_search_outbox_events": int(cleanup_deleted_outbox),
            "deleted_unified_outbox_events": (
                int(cleanup_deleted_unified_outbox) if is_unified_outbox_write_enabled(SEARCH_OUTBOX_PROJECTION) else None
            ),
            "remaining_search_index": cleanup_remaining_search,
            "remaining_search_outbox_events": cleanup_remaining_outbox,
            "remaining_unified_outbox_events": cleanup_remaining_unified_outbox,
            "note": "Cleanup is executed by default to keep CI/devtest DB clean.",
        },
        "ok": bool(ok),
    }

    return DrillResult(
        ok=bool(ok),
        meta=result,
        summary={
            "scope": scope,
            "max_writes": int(max_writes),
            "verify_search_index_rows_found": int(verify_search_count),
            "verify_search_outbox_rows_found": int(verify_outbox_count),
            "verify_unified_outbox_rows_found": (
                int(verify_unified_outbox_count) if is_unified_outbox_write_enabled(SEARCH_OUTBOX_PROJECTION) else None
            ),
            "duplicates_extra_rows_total": int(dup_extra),
            "cleanup_enabled": bool(cleanup),
        },
        errors=[],
    )
