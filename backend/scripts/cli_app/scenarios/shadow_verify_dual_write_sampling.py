from __future__ import annotations

import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import bindparam, create_engine, text

from infra.outbox_unified.toggles import is_unified_outbox_read_enabled, is_unified_outbox_write_enabled

from ._failure_drill_shared import (
    insert_search_outbox_supply_rows_sql_v1,
    resolve_search_outbox_supply_sql_target_v1,
    verify_supply_rows_v1,
)
from ._search_index_seed import ensure_search_index_min_rows
from ..common import write_json
from ..registry import register
from ..types import DrillInputs, DrillResult


SEARCH_OUTBOX_PROJECTION = "search_index_to_elastic"


def _parse_csv_list(value: str | None) -> list[str]:
    if not value:
        return []
    parts = [p.strip() for p in str(value).split(",")]
    return [p for p in parts if p]


@register("shadow_verify_dual_write_sampling")
@register("shadow-verify-dual-write-sampling")
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

    entity_types_raw = payload.get("entity_types")
    entity_types: list[str]
    if isinstance(entity_types_raw, str) or entity_types_raw is None:
        entity_types = _parse_csv_list(entity_types_raw)
    elif isinstance(entity_types_raw, list):
        entity_types = [str(x).strip() for x in entity_types_raw if str(x).strip()]
    else:
        entity_types = []

    ensure_min_rows = int(payload.get("ensure_min_rows") or 0)
    sample_size = int(payload.get("sample_size") or 0)
    duration_seconds = int(payload.get("duration_seconds") or 0)
    interval_seconds = float(payload.get("interval_seconds") or 0.0)
    max_total_events = int(payload.get("max_total_events") or 0)
    strategy = str(payload.get("strategy") or "").strip().lower() or "soft"
    inject_failed_rate = float(payload.get("inject_failed_rate") or 0.0)
    replay_failed = bool(payload.get("replay_failed"))
    replay_by = str(payload.get("replay_by") or "labs")[:120]
    replay_reason = str(payload.get("replay_reason") or "labs shadow dual-write sampling replay")
    cleanup = bool(payload.get("cleanup"))

    if ensure_min_rows < 0:
        return DrillResult(ok=False, errors=["ensure_min_rows must be >= 0"], meta={}, summary={})
    if sample_size <= 0:
        return DrillResult(ok=False, errors=["sample_size must be > 0"], meta={}, summary={})
    if duration_seconds < 0:
        return DrillResult(ok=False, errors=["duration_seconds must be >= 0"], meta={}, summary={})
    if interval_seconds <= 0:
        return DrillResult(ok=False, errors=["interval_seconds must be > 0"], meta={}, summary={})
    if max_total_events <= 0:
        return DrillResult(ok=False, errors=["max_total_events must be > 0"], meta={}, summary={})
    if strategy not in {"soft", "strict"}:
        return DrillResult(ok=False, errors=["strategy must be one of: soft, strict"], meta={}, summary={})
    if inject_failed_rate < 0.0 or inject_failed_rate > 1.0:
        return DrillResult(ok=False, errors=["inject_failed_rate must be in [0.0, 1.0]"], meta={}, summary={})

    scope = "all" if library_id is None else f"library:{library_id}"
    engine = create_engine(database_url)

    unified_write_enabled = is_unified_outbox_write_enabled(SEARCH_OUTBOX_PROJECTION)

    now = datetime.now(timezone.utc)
    stop_at = now.timestamp() + float(duration_seconds)

    inserted_outbox_ids: list[str] = []
    inserted_total = 0
    dlq_failed_total = 0
    replayed_total = 0
    seed_rows_inserted = 0
    loops = 0
    primary_outbox_table = "search_outbox_events"
    primary_outbox_projection: str | None = None
    supply: dict[str, object] | None = None
    supply_db_check: dict[str, object] | None = None

    def _select_candidates(conn, limit: int) -> list[tuple[str, str, int, str | None]]:
        where_parts: list[str] = []
        params: dict[str, object] = {"limit": int(limit)}

        if library_id is not None:
            where_parts.append("library_id = :library_id")
            params["library_id"] = library_id

        if entity_types:
            where_parts.append("entity_type IN :entity_types")
            params["entity_types"] = entity_types

        where_sql = ("WHERE " + " AND ".join(where_parts)) if where_parts else ""
        stmt = text(
            f"""
            SELECT entity_type, entity_id::text, event_version, library_id::text AS library_id
            FROM search_index
            {where_sql}
            ORDER BY updated_at DESC, entity_type, entity_id
            LIMIT :limit
            """
        )
        if entity_types:
            stmt = stmt.bindparams(bindparam("entity_types", expanding=True))

        rows = conn.execute(stmt, params).fetchall()
        return [
            (
                str(r[0]),
                str(r[1]),
                int(r[2] or 0),
                (str(r[3]) if (len(r) > 3 and r[3] is not None) else None),
            )
            for r in rows
        ]

    with engine.connect() as conn:
        supply_target = resolve_search_outbox_supply_sql_target_v1(conn=conn, projection=SEARCH_OUTBOX_PROJECTION)
        primary_outbox_table = str(supply_target.table_name)
        primary_outbox_projection = supply_target.projection

        if ensure_min_rows > 0:
            seed_rows_inserted = ensure_search_index_min_rows(
                conn=conn,
                ensure_min_rows=ensure_min_rows,
                library_id=library_id,
                seed_entity_type="seed_sampling",
            )

        use_unified_read = is_unified_outbox_read_enabled(SEARCH_OUTBOX_PROJECTION)

        while True:
            loops += 1
            remaining_budget = max_total_events - inserted_total
            if remaining_budget <= 0:
                break

            batch_limit = min(int(sample_size), int(remaining_budget))
            candidates = _select_candidates(conn, limit=batch_limit)
            if not candidates:
                break

            batch_now = datetime.now(timezone.utc)
            by_entity_type: dict[str, list[dict[str, object]]] = {}
            for (et, entity_id, event_version, candidate_library_id) in candidates:
                by_entity_type.setdefault(str(et), []).append(
                    {
                        "entity_id": entity_id,
                        "event_version": int(event_version),
                        "library_id": candidate_library_id,
                    }
                )

            batch_ids: list[str] = []
            batch_entity_types = list(by_entity_type.keys())
            for et, batch_candidates in by_entity_type.items():
                batch_supply = insert_search_outbox_supply_rows_sql_v1(
                    conn=conn,
                    target=supply_target,
                    projection=SEARCH_OUTBOX_PROJECTION,
                    candidates=batch_candidates,
                    entity_type=str(et),
                    op="upsert",
                    status="pending",
                )
                ids = [str(x).strip() for x in (batch_supply.get("outbox_event_ids") or []) if str(x).strip()]
                batch_ids.extend(ids)

                if supply is None:
                    supply = dict(batch_supply)
                    supply["entity_type"] = "mixed" if len(batch_entity_types) > 1 else str(et)
                    supply["entity_types"] = list(batch_entity_types)
                else:
                    prev_count = int(supply.get("insert_count") or 0)
                    supply["insert_count"] = int(prev_count + int(batch_supply.get("insert_count") or 0))
                    prev_ids = supply.get("outbox_event_ids")
                    if not isinstance(prev_ids, list):
                        prev_ids = []
                    supply["outbox_event_ids"] = list(prev_ids) + list(ids)
                    supply["entity_type"] = "mixed"
                    supply["entity_types"] = sorted(
                        {str(x) for x in (supply.get("entity_types") or []) if str(x).strip()} | set(batch_entity_types)
                    )

            conn.commit()

            inserted_outbox_ids.extend(batch_ids)
            inserted_total += len(batch_ids)

            # DLQ simulation: mark a subset as failed.
            fail_n = int(round(float(inject_failed_rate) * float(len(batch_ids))))
            fail_ids = batch_ids[: max(0, min(fail_n, len(batch_ids)))]
            if fail_ids:
                now_fail = datetime.now(timezone.utc)
                legacy_fail_sql = (
                    text(
                        """
                        UPDATE search_outbox_events
                        SET status='failed',
                            error_reason='simulated_new_side_failure',
                            error='simulated by labs shadow-verify-dual-write-sampling',
                            updated_at=:now
                        WHERE id IN :ids
                        """
                    ).bindparams(bindparam("ids", expanding=True))
                )
                unified_fail_sql = (
                    text(
                        """
                        UPDATE outbox_events
                        SET status='failed',
                            error_reason='simulated_new_side_failure',
                            error='simulated by labs shadow-verify-dual-write-sampling',
                            updated_at=:now
                        WHERE projection = :projection
                          AND id IN :ids
                        """
                    ).bindparams(bindparam("ids", expanding=True))
                )

                if primary_outbox_table == "search_outbox_events":
                    conn.execute(legacy_fail_sql, {"now": now_fail, "ids": fail_ids})
                else:
                    conn.execute(
                        unified_fail_sql,
                        {"now": now_fail, "projection": SEARCH_OUTBOX_PROJECTION, "ids": fail_ids},
                    )
                conn.commit()
                dlq_failed_total += len(fail_ids)

            # Replay evidence (failed -> pending with audit fields).
            if replay_failed and fail_ids:
                replay_now = datetime.now(timezone.utc)
                legacy_replay_sql = (
                    text(
                        """
                        UPDATE search_outbox_events
                        SET status='pending',
                            owner=NULL,
                            lease_until=NULL,
                            processing_started_at=NULL,
                            attempts=0,
                            next_retry_at=NULL,
                            error_reason=NULL,
                            error=NULL,
                            replay_count=(replay_count + 1),
                            last_replayed_at=:now,
                            last_replayed_by=:by,
                            last_replayed_reason=:reason,
                            updated_at=:now
                        WHERE id IN :ids
                          AND status='failed'
                        """
                    ).bindparams(bindparam("ids", expanding=True))
                )
                unified_replay_sql = (
                    text(
                        """
                        UPDATE outbox_events
                        SET status='pending',
                            owner=NULL,
                            lease_until=NULL,
                            processing_started_at=NULL,
                            attempts=0,
                            next_retry_at=NULL,
                            error_reason=NULL,
                            error=NULL,
                            replay_count=(replay_count + 1),
                            last_replayed_at=:now,
                            last_replayed_by=:by,
                            last_replayed_reason=:reason,
                            updated_at=:now
                        WHERE projection = :projection
                          AND id IN :ids
                          AND status='failed'
                        """
                    ).bindparams(bindparam("ids", expanding=True))
                )

                params = {"now": replay_now, "by": replay_by, "reason": replay_reason, "ids": fail_ids}
                if primary_outbox_table == "search_outbox_events":
                    conn.execute(legacy_replay_sql, params)
                else:
                    conn.execute(unified_replay_sql, {**params, "projection": SEARCH_OUTBOX_PROJECTION})
                conn.commit()
                replayed_total += len(fail_ids)

            if duration_seconds <= 0:
                break

            if datetime.now(timezone.utc).timestamp() >= stop_at:
                break

            time.sleep(interval_seconds)

        # Verify status distribution for inserted rows.
        pending_count = 0
        failed_count = 0
        if inserted_outbox_ids:
            if primary_outbox_table == "search_outbox_events":
                rows = conn.execute(
                    text(
                        """
                        SELECT status, COUNT(*)
                        FROM search_outbox_events
                        WHERE id IN :ids
                        GROUP BY status
                        """
                    ).bindparams(bindparam("ids", expanding=True)),
                    {"ids": inserted_outbox_ids},
                ).fetchall()
            else:
                rows = conn.execute(
                    text(
                        """
                        SELECT status, COUNT(*)
                        FROM outbox_events
                        WHERE projection = :projection
                          AND id IN :ids
                        GROUP BY status
                        """
                    ).bindparams(bindparam("ids", expanding=True)),
                    {"projection": SEARCH_OUTBOX_PROJECTION, "ids": inserted_outbox_ids},
                ).fetchall()
            for status, cnt in rows:
                if str(status) == "pending":
                    pending_count = int(cnt)
                elif str(status) == "failed":
                    failed_count = int(cnt)

        remaining_outbox = None
        remaining_legacy_outbox = None

        if supply is not None:
            try:
                write_json(outdir / "_supply.json", supply)
            except Exception:
                pass
            try:
                supply_db_check = verify_supply_rows_v1(database_url=database_url, supply=supply)
            except Exception:
                supply_db_check = None
        if cleanup and inserted_outbox_ids:
            legacy_delete_sql = text("DELETE FROM search_outbox_events WHERE id IN :ids").bindparams(
                bindparam("ids", expanding=True)
            )
            unified_delete_sql = text(
                "DELETE FROM outbox_events WHERE projection = :projection AND id IN :ids"
            ).bindparams(bindparam("ids", expanding=True))

            if primary_outbox_table == "search_outbox_events":
                conn.execute(legacy_delete_sql, {"ids": inserted_outbox_ids})
            else:
                conn.execute(
                    unified_delete_sql,
                    {"projection": SEARCH_OUTBOX_PROJECTION, "ids": inserted_outbox_ids},
                )
            conn.commit()
            if primary_outbox_table == "search_outbox_events":
                remaining_outbox = int(
                    conn.execute(
                        text("SELECT COUNT(*) FROM search_outbox_events WHERE id IN :ids").bindparams(
                            bindparam("ids", expanding=True)
                        ),
                        {"ids": inserted_outbox_ids},
                    ).scalar()
                    or 0
                )
            else:
                remaining_outbox = int(
                    conn.execute(
                        text(
                            "SELECT COUNT(*) FROM outbox_events WHERE projection = :projection AND id IN :ids"
                        ).bindparams(bindparam("ids", expanding=True)),
                        {"projection": SEARCH_OUTBOX_PROJECTION, "ids": inserted_outbox_ids},
                    ).scalar()
                    or 0
                )
                remaining_legacy_outbox = None

    strict_failed = failed_count > 0
    ok = True
    if strategy == "strict" and strict_failed:
        ok = False
    if cleanup and inserted_outbox_ids and remaining_outbox not in (0, None):
        ok = False
    # supply_db_check is best-effort evidence; do not hard-fail ok when skipped.
    if supply_db_check is not None and (not bool(supply_db_check.get("skipped"))):
        ok = bool(ok) and bool(supply_db_check.get("ok"))

    result: dict[str, object] = {
        "lab_id": inputs.scope_id,
        "scenario": "shadow_verify_dual_write_sampling",
        "run_id": inputs.run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "scope": scope,
        "dry_run": False,
        "artifacts_contract_hint": "success uploads summary.json only; failure uploads artifacts.zip; _result.json is single source of truth",
        "targets": {
            "projection_table": "search_index",
            "outbox_table": str(primary_outbox_table),
            "outbox_projection": primary_outbox_projection,
            "unified_outbox_write_enabled": bool(unified_write_enabled),
            "use_unified_outbox_read": bool(use_unified_read),
            "enqueue_entrypoint": "backend/infra/search/search_outbox_repository.py::SearchOutboxRepository.enqueue",
            "producer_entrypoint": "backend/infra/search/search_indexer.py::PostgresSearchIndexer",
            "replay_tool_hint": "backend/scripts/ops/search_outbox_replay_failed.py (stable shim)",
        },
        "config": {
            "library_id": library_id,
            "entity_types": entity_types,
            "ensure_min_rows": int(ensure_min_rows),
            "sample_size": int(sample_size),
            "duration_seconds": int(duration_seconds),
            "interval_seconds": float(interval_seconds),
            "max_total_events": int(max_total_events),
            "strategy": strategy,
            "inject_failed_rate": float(inject_failed_rate),
            "replay_failed": bool(replay_failed),
            "cleanup": bool(cleanup),
        },
        "observed": {
            "loops": int(loops),
            "seed_rows_inserted": int(seed_rows_inserted),
            "outbox_inserted_total": int(inserted_total),
            "dlq_failed_simulated_total": int(dlq_failed_total),
            "replayed_total": int(replayed_total),
            "pending_after": int(pending_count),
            "failed_after": int(failed_count),
        },
        "rollback": {
            "cleanup_enabled": bool(cleanup),
            "remaining_outbox_rows": remaining_outbox,
            "remaining_legacy_outbox_rows": remaining_legacy_outbox,
        },
        "supply": supply,
        "supply_db_check": supply_db_check,
        "policy": {
            "strategy": strategy,
            "strict_fails_on_failed": True,
            "soft_allows_failed": True,
            "dlq_definition": "status=failed rows are treated as terminal by worker; ops can replay to pending with audit fields",
            "replay_audit_fields": [
                "replay_count",
                "last_replayed_at",
                "last_replayed_by",
                "last_replayed_reason",
            ],
        },
        "ok": bool(ok),
    }

    return DrillResult(
        ok=bool(ok),
        meta=result,
        summary={
            "scope": scope,
            "strategy": strategy,
            "outbox_inserted_total": int(inserted_total),
            "pending_after": int(pending_count),
            "failed_after": int(failed_count),
            "dlq_failed_simulated_total": int(dlq_failed_total),
            "replayed_total": int(replayed_total),
            "cleanup_enabled": bool(cleanup),
        },
        errors=[],
    )
