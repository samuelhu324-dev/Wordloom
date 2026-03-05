from __future__ import annotations

import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import bindparam, create_engine, text

from infra.outbox_unified.toggles import is_unified_outbox_write_enabled

from ._failure_drill_shared import (
    insert_search_outbox_supply_rows_sql_v1,
    resolve_search_outbox_supply_sql_target_v1,
    verify_supply_rows_v1,
)

from ..common import write_json
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

    outdir_raw = payload.get("outdir")
    outdir = Path(str(outdir_raw)) if outdir_raw else None
    if outdir is None:
        return DrillResult(ok=False, errors=["outdir is required"], meta={}, summary={})

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
    outbox_event_ids: list[str] = []

    search_rows: list[dict[str, object]] = []
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

    engine = create_engine(database_url)
    unified_write_enabled = is_unified_outbox_write_enabled(SEARCH_OUTBOX_PROJECTION)
    primary_outbox_table = "search_outbox_events"
    primary_outbox_projection: str | None = None
    supply: dict[str, object] | None = None
    supply_db_check: dict[str, object] | None = None
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
        supply_target = resolve_search_outbox_supply_sql_target_v1(conn=conn, projection=SEARCH_OUTBOX_PROJECTION)
        primary_outbox_table = str(supply_target.table_name)
        primary_outbox_projection = supply_target.projection

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
        supply = insert_search_outbox_supply_rows_sql_v1(
            conn=conn,
            target=supply_target,
            projection=SEARCH_OUTBOX_PROJECTION,
            candidates=[
                {"entity_id": entity_ids[i], "event_version": int(i + 1), "library_id": library_id}
                for i in range(max_writes)
            ],
            entity_type=entity_type,
            op="upsert",
            status="pending",
        )
        outbox_event_ids = [str(x).strip() for x in (supply.get("outbox_event_ids") or []) if str(x).strip()]

        if primary_outbox_table == "outbox_events":
            inserted_unified_outbox = max_writes
        else:
            inserted_outbox = max_writes

        conn.commit()

        # Persist supply evidence before optional cleanup deletes the rows.
        try:
            if supply is not None:
                write_json(outdir / "_supply.json", supply)
        except Exception:
            pass
        try:
            if supply is not None:
                supply_db_check = verify_supply_rows_v1(database_url=database_url, supply=supply)
        except Exception:
            supply_db_check = None

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
        if primary_outbox_table == "search_outbox_events":
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
        else:
            verify_outbox_count = 0

        if primary_outbox_table == "outbox_events":
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
            if primary_outbox_table == "outbox_events":
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
            else:
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
                0
                if primary_outbox_table != "search_outbox_events"
                else (
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
            )

            if primary_outbox_table == "outbox_events":
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
            if primary_outbox_table == "outbox_events":
                cleanup_deleted_unified_outbox = verify_unified_outbox_count - (cleanup_remaining_unified_outbox or 0)

    ok = (
        inserted_search == max_writes
        and (
            (
                primary_outbox_table == "outbox_events"
                and inserted_outbox == 0
                and inserted_unified_outbox == max_writes
            )
            or (
                primary_outbox_table == "search_outbox_events"
                and inserted_outbox == max_writes
                and inserted_unified_outbox == 0
            )
        )
        and verify_search_count == max_writes
        and (
            (
                primary_outbox_table == "outbox_events"
                and verify_outbox_count == 0
                and verify_unified_outbox_count == max_writes
            )
            or (
                primary_outbox_table == "search_outbox_events"
                and verify_outbox_count == max_writes
                and verify_unified_outbox_count == 0
            )
        )
        and dup_extra == 0
        and (
            (not cleanup)
            or (
                cleanup_remaining_search == 0
                and cleanup_remaining_outbox == 0
                and (
                    (primary_outbox_table != "outbox_events")
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
            "outbox_table": str(primary_outbox_table),
            "outbox_projection": primary_outbox_projection,
            "unified_outbox_table": ("outbox_events" if primary_outbox_table == "outbox_events" else None),
            "unified_outbox_write_enabled": bool(unified_write_enabled),
            "entrypoint_hint": "backend/infra/search/search_indexer.py::PostgresSearchIndexer (writes search_index + enqueues unified outbox when enabled)",
        },
        "canary": {
            "entity_type": entity_type,
            "max_writes": max_writes,
            "entity_ids": entity_ids,
            "search_index_ids": search_index_ids,
            "outbox_event_ids": outbox_event_ids,
        },
        "supply": supply,
        "supply_db_check": supply_db_check,
        "verify": {
            "search_index_rows_found": int(verify_search_count),
            "search_outbox_rows_found": int(verify_outbox_count),
            "unified_outbox_rows_found": (
                int(verify_unified_outbox_count) if primary_outbox_table == "outbox_events" else None
            ),
            "duplicates_extra_rows_total": int(dup_extra),
        },
        "rollback": {
            "cleanup_enabled": bool(cleanup),
            "deleted_search_index": int(cleanup_deleted_search),
            "deleted_search_outbox_events": int(cleanup_deleted_outbox),
            "deleted_unified_outbox_events": (
                int(cleanup_deleted_unified_outbox) if primary_outbox_table == "outbox_events" else None
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
                int(verify_unified_outbox_count) if primary_outbox_table == "outbox_events" else None
            ),
            "duplicates_extra_rows_total": int(dup_extra),
            "cleanup_enabled": bool(cleanup),
        },
        errors=[],
    )
