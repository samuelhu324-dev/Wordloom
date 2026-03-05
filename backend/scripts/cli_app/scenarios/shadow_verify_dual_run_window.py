from __future__ import annotations

import json
import os
import re
import time
import uuid
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import bindparam, create_engine, text

from infra.outbox_unified.toggles import is_unified_outbox_read_enabled, is_unified_outbox_write_enabled

from ._pg_introspection import table_exists
from ._failure_drill_shared import spawn_search_outbox_worker, with_backend_pythonpath

from ..common import REPO_ROOT, write_json
from ..registry import register
from ..types import DrillInputs, DrillResult


SEARCH_OUTBOX_PROJECTION = "search_index_to_elastic"


def _http_json(
    method: str,
    url: str,
    *,
    body: dict[str, object] | None = None,
    timeout_s: float = 5.0,
) -> tuple[int, str]:
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url=url, data=data, method=method.upper(), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:  # noqa: S310
            payload = resp.read().decode("utf-8", errors="replace")
            return int(getattr(resp, "status", 0) or 0), payload
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace") if getattr(exc, "fp", None) else str(exc)
        return int(getattr(exc, "code", 0) or 0), payload
    except Exception as exc:
        return 0, f"{type(exc).__name__}: {exc}"


def _try_parse_json(payload: str) -> dict[str, object]:
    try:
        obj = json.loads(payload) if payload else {}
        return obj if isinstance(obj, dict) else {"_": obj}
    except Exception:
        return {"raw": payload}


def _sanitize_index_name(name: str) -> str:
    safe = re.sub(r"[^a-z0-9_\-]+", "-", name.lower()).strip("-_")
    safe = re.sub(r"-+", "-", safe)
    if not safe:
        safe = "wordloom-search-index"
    return safe[:80]


def _extract_last_claim_batch_id(worker_log_path: Path) -> str | None:
    try:
        text_content = worker_log_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None

    patterns = [
        r"last_claim_batch_id=([0-9a-f\-]{8,})",
        r"claim_batch_id=([0-9a-f\-]{8,})",
    ]
    for p in patterns:
        m = re.findall(p, text_content, flags=re.IGNORECASE)
        if m:
            return str(m[-1])
    return None


def _tail_file(path: Path, limit: int = 4000) -> str:
    try:
        t = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""
    if len(t) <= limit:
        return t
    return t[-limit:]


@register("shadow_verify_dual_run_window")
@register("shadow-verify-dual-run-window")
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

    ensure_min_rows = int(payload.get("ensure_min_rows") or 0)
    candidate_limit = int(payload.get("candidate_limit") or 0)
    strategy = str(payload.get("strategy") or "").strip() or "soft"
    duration_seconds = float(payload.get("duration_seconds") or 0.0)
    interval_seconds = float(payload.get("interval_seconds") or 0.0)
    enqueue_batch_size = int(payload.get("enqueue_batch_size") or 0)
    max_total_events = int(payload.get("max_total_events") or 0)
    drain_timeout_seconds = float(payload.get("drain_timeout_seconds") or 0.0)

    max_outbox_failed = int(payload.get("max_outbox_failed") or 0)
    max_outbox_pending = int(payload.get("max_outbox_pending") or 0)
    max_outbox_processing = int(payload.get("max_outbox_processing") or 0)
    require_outbox_done_eq_enqueued = bool(payload.get("require_outbox_done_eq_enqueued"))

    worker_batch_size = int(payload.get("worker_batch_size") or 0)
    worker_concurrency = int(payload.get("worker_concurrency") or 0)
    worker_poll_interval_seconds = float(payload.get("worker_poll_interval_seconds") or 0.0)
    worker_max_runtime_seconds = float(payload.get("worker_max_runtime_seconds") or 0.0)

    if ensure_min_rows < 0:
        return DrillResult(ok=False, errors=["ensure_min_rows must be >= 0"], meta={}, summary={})
    if candidate_limit <= 0:
        return DrillResult(ok=False, errors=["candidate_limit must be > 0"], meta={}, summary={})
    if strategy not in {"soft", "strict"}:
        return DrillResult(ok=False, errors=["strategy must be one of: soft, strict"], meta={}, summary={})
    if duration_seconds <= 0:
        return DrillResult(ok=False, errors=["duration_seconds must be > 0"], meta={}, summary={})
    if interval_seconds <= 0:
        return DrillResult(ok=False, errors=["interval_seconds must be > 0"], meta={}, summary={})
    if enqueue_batch_size <= 0:
        return DrillResult(ok=False, errors=["enqueue_batch_size must be > 0"], meta={}, summary={})
    if max_total_events <= 0:
        return DrillResult(ok=False, errors=["max_total_events must be > 0"], meta={}, summary={})
    if drain_timeout_seconds <= 0:
        return DrillResult(ok=False, errors=["drain_timeout_seconds must be > 0"], meta={}, summary={})
    if max_outbox_failed < 0:
        return DrillResult(ok=False, errors=["max_outbox_failed must be >= 0"], meta={}, summary={})
    if max_outbox_pending < 0:
        return DrillResult(ok=False, errors=["max_outbox_pending must be >= 0"], meta={}, summary={})
    if max_outbox_processing < 0:
        return DrillResult(ok=False, errors=["max_outbox_processing must be >= 0"], meta={}, summary={})
    if worker_batch_size <= 0:
        return DrillResult(ok=False, errors=["worker_batch_size must be > 0"], meta={}, summary={})
    if worker_concurrency <= 0:
        return DrillResult(ok=False, errors=["worker_concurrency must be > 0"], meta={}, summary={})
    if worker_poll_interval_seconds < 0:
        return DrillResult(ok=False, errors=["worker_poll_interval_seconds must be >= 0"], meta={}, summary={})
    if worker_max_runtime_seconds <= 0:
        return DrillResult(ok=False, errors=["worker_max_runtime_seconds must be > 0"], meta={}, summary={})

    env_payload = payload.get("env")
    env: dict[str, str] = os.environ.copy()
    if isinstance(env_payload, dict):
        env.update({str(k): str(v) for k, v in env_payload.items()})

    outdir_raw = payload.get("outdir")
    outdir = Path(str(outdir_raw)) if outdir_raw else None
    if outdir is None:
        return DrillResult(ok=False, errors=["outdir is required"], meta={}, summary={})

    scope = "all" if library_id is None else f"library:{library_id}"

    es_url = str(payload.get("es_url") or env.get("ELASTIC_URL") or "http://127.0.0.1:19200").strip().rstrip("/")
    token = str(payload.get("token") or "").strip()
    if not token:
        token = "dualrun" + re.sub(r"[^0-9A-Za-z]+", "", inputs.run_id)

    es_index = str(
        payload.get("es_index")
        or env.get("ELASTIC_INDEX")
        or _sanitize_index_name(f"wordloom-search-index-dualrun-{token}")
    ).strip()
    es_index = _sanitize_index_name(es_index)
    recreate_index = bool(payload.get("recreate_index"))

    seed_text_prefix = f"{token} "
    seed_entity_type = "block"

    where_parts: list[str] = ["entity_type = :entity_type", "text ILIKE :pattern"]
    base_params: dict[str, object] = {
        "entity_type": seed_entity_type,
        "pattern": f"{seed_text_prefix}%",
    }
    if library_id is not None:
        where_parts.append("library_id = :library_id")
        base_params["library_id"] = library_id
    where_sql = " AND ".join(where_parts)

    engine = create_engine(database_url)
    inserted_rows = 0
    pg_candidates: list[dict[str, object]] = []

    use_unified_read = False
    dual_write_enabled = False
    primary_outbox_table = "search_outbox_events"
    primary_outbox_projection: str | None = None

    def _table_columns(conn, table_name: str) -> set[str]:
        rows = conn.execute(
            text(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = :t
                """
            ),
            {"t": table_name},
        ).all()
        return {str(r[0]) for r in rows if r and r[0]}

    outbox_cols: set[str] = set()
    with engine.connect() as conn:
        existing_for_token = int(
            conn.execute(text(f"SELECT COUNT(*) FROM search_index WHERE {where_sql}"), base_params).scalar() or 0
        )
        need = int(ensure_min_rows) - int(existing_for_token)
        if need > 0:
            now = datetime.now(timezone.utc)
            max_ev = int(conn.execute(text("SELECT COALESCE(MAX(event_version), 0) FROM search_index")).scalar() or 0)
            rows = []
            for i in range(int(need)):
                rows.append(
                    {
                        "id": uuid.uuid4(),
                        "entity_type": seed_entity_type,
                        "library_id": (uuid.UUID(library_id) if library_id else None),
                        "entity_id": uuid.uuid4(),
                        "text": f"{seed_text_prefix}{i}",
                        "snippet": None,
                        "rank_score": 0.0,
                        "created_at": now,
                        "updated_at": now,
                        "event_version": int(max_ev + i + 1),
                    }
                )

            conn.execute(
                text(
                    """
                    INSERT INTO search_index
                      (id, entity_type, library_id, entity_id, text, snippet, rank_score, created_at, updated_at, event_version)
                    VALUES
                      (:id, :entity_type, :library_id, :entity_id, :text, :snippet, :rank_score, :created_at, :updated_at, :event_version)
                    """
                ),
                rows,
            )
            conn.commit()
            inserted_rows = int(need)

        pg_sql = f"""
            SELECT entity_id::text AS entity_id,
                   COALESCE(event_version, 0) AS event_version,
                   library_id::text AS library_id
            FROM search_index
            WHERE {where_sql}
            ORDER BY COALESCE(event_version, 0) ASC, entity_id::text ASC
            LIMIT :limit
        """
        pg_params = dict(base_params)
        pg_params["limit"] = candidate_limit
        pg_rows = conn.execute(text(pg_sql), pg_params).all()
        pg_candidates = [
            {
                "entity_id": str(r[0]),
                "event_version": int(r[1] or 0),
                "library_id": (str(r[2]) if (len(r) > 2 and r[2] is not None) else None),
            }
            for r in pg_rows
        ]
        if not pg_candidates:
            return DrillResult(ok=False, errors=["no pg candidates; increase ensure_min_rows"], meta={}, summary={})

        use_unified_read = is_unified_outbox_read_enabled(SEARCH_OUTBOX_PROJECTION)
        dual_write_enabled = is_unified_outbox_write_enabled(SEARCH_OUTBOX_PROJECTION)
        primary_outbox_table = "outbox_events" if use_unified_read else "search_outbox_events"
        if primary_outbox_table == "search_outbox_events" and (not table_exists(conn, "search_outbox_events")):
            # Slice C drops legacy table; unified outbox is now the only valid source.
            use_unified_read = True
            primary_outbox_table = "outbox_events"
        primary_outbox_projection = SEARCH_OUTBOX_PROJECTION if primary_outbox_table == "outbox_events" else None

        outbox_cols = _table_columns(conn, primary_outbox_table)
        if not outbox_cols:
            return DrillResult(ok=False, errors=[f"table {primary_outbox_table} not found"], meta={}, summary={})

        required_cols = {"id", "entity_type", "entity_id", "op", "event_version", "status"}
        if primary_outbox_table == "outbox_events":
            required_cols.add("projection")
        missing_required = sorted([c for c in required_cols if c not in outbox_cols])
        if missing_required:
            return DrillResult(
                ok=False,
                errors=[f"{primary_outbox_table} missing required columns: {missing_required}"],
                meta={},
                summary={},
            )

    if enqueue_batch_size > len(pg_candidates):
        return DrillResult(
            ok=False,
            errors=[
                f"enqueue_batch_size ({enqueue_batch_size}) exceeds pg_candidates_total ({len(pg_candidates)})"
            ],
            meta={},
            summary={},
        )

    probe: dict[str, object] = {
        "event": "labs.dual_run.window.probe",
        "lab_id": inputs.scope_id,
        "scenario": "shadow_verify_dual_run_window",
        "run_id": inputs.run_id,
        "scope": scope,
        "library_id": library_id,
        "token": token,
        "pg_candidates_total": len(pg_candidates),
        "duration_seconds": duration_seconds,
        "interval_seconds": interval_seconds,
        "enqueue_batch_size": enqueue_batch_size,
        "max_total_events": max_total_events,
        "es_url": es_url,
        "es_index": es_index,
        "outbox_table": primary_outbox_table,
        "outbox_projection": primary_outbox_projection,
        "use_unified_outbox_read": bool(use_unified_read),
        "unified_outbox_write_enabled": bool(dual_write_enabled),
    }
    print(json.dumps(probe, ensure_ascii=False, separators=(",", ":")))

    es_health_status, es_health_payload = _http_json("GET", f"{es_url}", body=None, timeout_s=5.0)
    es_health_ok = bool(es_health_status == 200)

    if recreate_index:
        _http_json("DELETE", f"{es_url}/{es_index}", body=None, timeout_s=10.0)

    mapping = {
        "mappings": {
            "properties": {
                "entity_type": {"type": "keyword"},
                "library_id": {"type": "keyword"},
                "entity_id": {"type": "keyword"},
                "text": {"type": "text"},
                "snippet": {"type": "text", "index": False},
                "rank_score": {"type": "float"},
                "event_version": {"type": "long"},
                "updated_at": {"type": "date"},
            }
        }
    }
    es_index_status, es_index_payload = _http_json(
        "PUT",
        f"{es_url}/{es_index}",
        body=mapping,
        timeout_s=10.0,
    )
    es_index_ok = bool(es_index_status in {200, 201} or es_index_status == 400)

    worker_env = env.copy()
    worker_env["DATABASE_URL"] = database_url
    worker_env["ELASTIC_URL"] = es_url
    worker_env["ELASTIC_INDEX"] = es_index

    explicit_allowlist = str(worker_env.get("SEARCH_OUTBOX_LIBRARY_ALLOWLIST") or "").strip()
    if explicit_allowlist:
        worker_env["SEARCH_OUTBOX_LIBRARY_ALLOWLIST"] = explicit_allowlist
    elif library_id is not None:
        worker_env["SEARCH_OUTBOX_LIBRARY_ALLOWLIST"] = str(library_id)
    else:
        worker_env.pop("SEARCH_OUTBOX_LIBRARY_ALLOWLIST", None)

    worker_env = with_backend_pythonpath(worker_env)

    worker_env["OUTBOX_EXIT_WHEN_IDLE"] = "0"
    worker_env["OUTBOX_MAX_RUNTIME_SECONDS"] = str(float(worker_max_runtime_seconds))
    worker_env["OUTBOX_POLL_INTERVAL_SECONDS"] = str(float(worker_poll_interval_seconds))
    worker_env["OUTBOX_BULK_SIZE"] = str(int(worker_batch_size))
    worker_env["OUTBOX_CONCURRENCY"] = str(int(worker_concurrency))
    worker_env["OUTBOX_REQUIRE_ES_READY"] = "1"
    worker_env["OUTBOX_SHUTDOWN_GRACE_SECONDS"] = "5"

    worker_log_path = outdir / "worker.log"
    worker_started_at = time.time()
    worker_exit_code: int | None = None
    worker_runtime_s: float | None = None
    worker_ok = False
    worker_stop_requested = False
    worker_stop_kind: str | None = None

    worker_handle = spawn_search_outbox_worker(
        env=worker_env,
        logs_dir=outdir,
        run_id=inputs.run_id,
        log_name="worker.log",
        evidence_env_keys=[
            "DATABASE_URL",
            "ELASTIC_URL",
            "ELASTIC_INDEX",
            "SEARCH_OUTBOX_LIBRARY_ALLOWLIST",
            "OUTBOX_EXIT_WHEN_IDLE",
            "OUTBOX_MAX_RUNTIME_SECONDS",
            "OUTBOX_POLL_INTERVAL_SECONDS",
            "OUTBOX_BULK_SIZE",
            "OUTBOX_CONCURRENCY",
            "OUTBOX_REQUIRE_ES_READY",
            "OUTBOX_SHUTDOWN_GRACE_SECONDS",
        ],
    )
    write_json(outdir / "_worker_start.json", worker_handle.evidence_summary())

    outbox_event_ids: list[str] = []
    enqueued_entity_ids: list[str] = []
    window_samples: list[dict[str, object]] = []

    def _outbox_status_counts_for_ids(ids: list[str]) -> dict[str, int]:
        if not ids:
            return {}
        where_parts = ["id IN :ids"]
        params: dict[str, object] = {"ids": [uuid.UUID(x) for x in ids]}
        if primary_outbox_projection is not None:
            where_parts.append("projection = :projection")
            params["projection"] = str(primary_outbox_projection)

        outbox_sql = text(
            f"""
            SELECT status, COUNT(*) AS n
            FROM {primary_outbox_table}
            WHERE {' AND '.join(where_parts)}
            GROUP BY status
            """
        ).bindparams(bindparam("ids", expanding=True))
        counts: dict[str, int] = {}
        with engine.connect() as conn:
            rows = conn.execute(outbox_sql, params).all()
            for st, n in rows:
                counts[str(st)] = int(n or 0)
        return counts

    now = datetime.now(timezone.utc)
    base_event: dict[str, object] = {
        "projection": primary_outbox_projection,
        "entity_type": seed_entity_type,
        "op": "upsert",
        "status": "pending",
        "attempts": 0,
        "replay_count": 0,
        "created_at": now,
        "updated_at": now,
        "traceparent": None,
        "tracestate": None,
    }
    chosen_cols = [
        c
        for c in (
            "id",
            "projection",
            "entity_type",
            "library_id",
            "entity_id",
            "op",
            "event_version",
            "status",
            "attempts",
            "replay_count",
            "created_at",
            "updated_at",
            "traceparent",
            "tracestate",
        )
        if c in outbox_cols
    ]
    cols_sql = ", ".join(chosen_cols)
    placeholders = ", ".join([f":{c}" for c in chosen_cols])
    outbox_insert_sql = text(f"INSERT INTO {primary_outbox_table} ({cols_sql}) VALUES ({placeholders})")

    enqueue_finished_at = None
    final_status_counts: dict[str, int] = {}

    t_start = time.monotonic()
    t_end = t_start + float(duration_seconds)
    cursor = 0
    while True:
        t_now = time.monotonic()
        if t_now >= t_end:
            break
        if len(outbox_event_ids) >= int(max_total_events):
            break
        if worker_handle.proc.poll() is not None:
            break

        batch: list[dict[str, object]] = []
        for _ in range(enqueue_batch_size):
            if len(outbox_event_ids) >= int(max_total_events):
                break
            c = pg_candidates[cursor]
            cursor = (cursor + 1) % len(pg_candidates)
            ev_uuid = uuid.uuid4()
            outbox_event_ids.append(str(ev_uuid))
            enqueued_entity_ids.append(str(c["entity_id"]))
            row = {
                **{k: v for k, v in base_event.items() if k in chosen_cols},
                "id": ev_uuid,
                "entity_id": uuid.UUID(str(c["entity_id"])),
                "event_version": int(c["event_version"] or 0),
            }
            if "library_id" in chosen_cols:
                lib = c.get("library_id") or library_id
                row["library_id"] = (uuid.UUID(str(lib)) if lib else None)
            batch.append(row)

        if batch:
            with engine.connect() as conn:
                conn.execute(outbox_insert_sql, batch)
                conn.commit()

        counts = _outbox_status_counts_for_ids(outbox_event_ids)
        window_samples.append(
            {
                "t_seconds": float(time.monotonic() - t_start),
                "enqueued_total": int(len(outbox_event_ids)),
                "status_counts": counts,
            }
        )

        sleep_s = float(interval_seconds)
        if sleep_s > 0:
            time.sleep(sleep_s)

    enqueue_finished_at = time.time()

    drain_t0 = time.monotonic()
    while True:
        if worker_handle.proc.poll() is not None:
            break
        final_status_counts = _outbox_status_counts_for_ids(outbox_event_ids)
        pending = int(final_status_counts.get("pending", 0))
        processing = int(final_status_counts.get("processing", 0))
        if pending == 0 and processing == 0:
            break
        if (time.monotonic() - drain_t0) >= float(drain_timeout_seconds):
            break
        time.sleep(0.25)

    if worker_handle.proc.poll() is None:
        worker_stop_requested = True
        worker_stop_kind = "terminate"
        try:
            worker_handle.terminate_and_wait(timeout_s=10.0)
        except Exception:
            worker_stop_kind = "kill"
            try:
                worker_handle.terminate_and_wait(timeout_s=2.0)
            except Exception:
                pass
    else:
        try:
            worker_handle.wait(timeout_s=1.0)
        except Exception:
            pass

    worker_exit_code = int(worker_handle.proc.returncode) if worker_handle.proc.returncode is not None else None
    worker_runtime_s = float(time.time() - worker_started_at)
    worker_ok = bool((worker_exit_code == 0) or worker_stop_requested)

    try:
        with worker_log_path.open("a", encoding="utf-8") as wf:
            wf.write("\n--- labs window metadata ---\n")
            wf.write(
                json.dumps(
                    {
                        "event": "labs.dual_run.window.meta",
                        "scenario": "shadow_verify_dual_run_window",
                        "run_id": inputs.run_id,
                        "enqueue_finished_at": enqueue_finished_at,
                        "total_events": int(len(outbox_event_ids)),
                    },
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
                + "\n"
            )
    except Exception:
        pass

    last_claim_batch_id = _extract_last_claim_batch_id(worker_log_path)

    es_refresh_status, _es_refresh_payload = _http_json(
        "POST",
        f"{es_url}/{es_index}/_refresh",
        body=None,
        timeout_s=10.0,
    )
    es_refresh_ok = bool(es_refresh_status < 400)

    es_query_filters: list[dict[str, object]] = [{"term": {"entity_type": seed_entity_type}}]
    if library_id is not None:
        es_query_filters.append({"term": {"library_id": library_id}})

    es_search_body: dict[str, object] = {
        "query": {
            "bool": {
                "must": [{"match": {"text": token}}],
                "filter": es_query_filters,
            }
        },
        "sort": [{"event_version": "asc"}, {"entity_id": "asc"}],
        "_source": ["entity_id", "event_version", "entity_type", "library_id"],
        "size": candidate_limit,
    }

    es_search_status, es_search_payload = _http_json(
        "POST",
        f"{es_url}/{es_index}/_search",
        body=es_search_body,
        timeout_s=10.0,
    )
    es_search_ok = bool(es_search_status < 400)
    es_search_obj = _try_parse_json(es_search_payload)
    hits = (((es_search_obj.get("hits") or {}) if isinstance(es_search_obj, dict) else {}).get("hits") or [])
    if not isinstance(hits, list):
        hits = []

    es_candidates: list[dict[str, object]] = []
    for h in hits:
        if not isinstance(h, dict):
            continue
        src = h.get("_source")
        if not isinstance(src, dict):
            continue
        entity_id = src.get("entity_id")
        event_version = src.get("event_version")
        if entity_id is None:
            continue
        try:
            ev = int(event_version or 0)
        except Exception:
            ev = 0
        es_candidates.append({"entity_id": str(entity_id), "event_version": ev})

    es_count_status, es_count_payload = _http_json(
        "POST",
        f"{es_url}/{es_index}/_count",
        body={"query": es_search_body.get("query")},
        timeout_s=10.0,
    )
    es_count_obj = _try_parse_json(es_count_payload)
    es_count = None
    if isinstance(es_count_obj, dict) and isinstance(es_count_obj.get("count"), int):
        es_count = int(es_count_obj["count"])

    outbox_status_counts = _outbox_status_counts_for_ids(outbox_event_ids)
    outbox_done = int(outbox_status_counts.get("done", 0))
    outbox_pending = int(outbox_status_counts.get("pending", 0))
    outbox_processing = int(outbox_status_counts.get("processing", 0))
    outbox_failed = int(outbox_status_counts.get("failed", 0))

    expected_id_set = set(enqueued_entity_ids)
    expected_pg_candidates = [c for c in pg_candidates if str(c["entity_id"]) in expected_id_set]
    expected_pg_ids = [str(c["entity_id"]) for c in expected_pg_candidates]
    es_ids = [str(c["entity_id"]) for c in es_candidates]

    if strategy == "strict":
        parity_ok = bool(expected_pg_ids == es_ids[: len(expected_pg_ids)])
    else:
        parity_ok = bool(set(expected_pg_ids) & set(es_ids))

    ok = bool(
        len(outbox_event_ids) > 0
        and es_health_ok
        and es_index_ok
        and worker_ok
        and es_refresh_ok
        and es_search_ok
        and outbox_failed <= max_outbox_failed
        and outbox_pending <= max_outbox_pending
        and outbox_processing <= max_outbox_processing
        and ((not require_outbox_done_eq_enqueued) or (outbox_done == len(outbox_event_ids)))
        and parity_ok
    )

    def _rel_repo(path: Path) -> str:
        try:
            return str(path.resolve().relative_to(REPO_ROOT).as_posix())
        except Exception:
            return str(path.as_posix())

    result: dict[str, object] = {
        "lab_id": inputs.scope_id,
        "scenario": "shadow_verify_dual_run_window",
        "run_id": inputs.run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "scope": scope,
        "targets": {
            "projection_table": "search_index",
            "outbox_table": str(primary_outbox_table),
            "outbox_projection": primary_outbox_projection,
            "use_unified_outbox_read": bool(use_unified_read),
            "unified_outbox_write_enabled": bool(dual_write_enabled),
            "worker_entrypoint": worker_handle.entry_id,
        },
        "inputs": {
            "token": token,
            "ensure_min_rows": ensure_min_rows,
            "seed_entity_type": seed_entity_type,
            "candidate_limit": candidate_limit,
            "strategy": strategy,
            "duration_seconds": duration_seconds,
            "interval_seconds": interval_seconds,
            "enqueue_batch_size": enqueue_batch_size,
            "max_total_events": max_total_events,
            "drain_timeout_seconds": drain_timeout_seconds,
            "max_outbox_failed": max_outbox_failed,
            "max_outbox_pending": max_outbox_pending,
            "max_outbox_processing": max_outbox_processing,
            "require_outbox_done_eq_enqueued": bool(require_outbox_done_eq_enqueued),
            "es_url": es_url,
            "es_index": es_index,
            "recreate_index": bool(recreate_index),
            "worker_batch_size": worker_batch_size,
            "worker_concurrency": worker_concurrency,
            "worker_poll_interval_seconds": worker_poll_interval_seconds,
            "worker_max_runtime_seconds": worker_max_runtime_seconds,
        },
        "seed_rows_inserted": int(inserted_rows),
        "postgres": {
            "candidates": pg_candidates,
        },
        "window": {
            "enqueued_total": int(len(outbox_event_ids)),
            "samples": window_samples,
        },
        "outbox": {
            "enqueued_total": int(len(outbox_event_ids)),
            "event_ids": outbox_event_ids,
            "status_counts": outbox_status_counts,
        },
        "elasticsearch": {
            "health": {"status": int(es_health_status), "ok": bool(es_health_ok), "payload": es_health_payload},
            "index": {"status": int(es_index_status), "ok": bool(es_index_ok), "payload": es_index_payload},
            "refresh": {"status": int(es_refresh_status), "ok": bool(es_refresh_ok)},
            "search": {
                "status": int(es_search_status),
                "ok": bool(es_search_ok),
                "request": es_search_body,
                "response_excerpt": {
                    "hits_total": ((es_search_obj.get("hits") or {}).get("total") if isinstance(es_search_obj, dict) else None),
                },
                "candidates": es_candidates,
            },
            "count": {"status": int(es_count_status), "count": es_count, "payload": es_count_obj},
        },
        "worker": {
            "entry_id": worker_handle.entry_id,
            "exit_code": worker_exit_code,
            "ok": bool(worker_ok),
            "runtime_seconds": worker_runtime_s,
            "log_path": _rel_repo(worker_log_path),
            "last_claim_batch_id": last_claim_batch_id,
            "stop_requested": bool(worker_stop_requested),
            "stop_kind": worker_stop_kind,
            "stdout_stderr_tail": _tail_file(worker_log_path),
        },
        "compare": {
            "expected_pg_ids": expected_pg_ids,
            "es_ids": es_ids,
            "parity_ok": bool(parity_ok),
        },
        "ok": bool(ok),
    }

    return DrillResult(
        ok=bool(ok),
        meta=result,
        summary={
            "scope": scope,
            "token": token,
            "seed_rows_inserted": int(inserted_rows),
            "pg_candidates_total": len(pg_candidates),
            "outbox_enqueued_total": int(len(outbox_event_ids)),
            "outbox_done": int(outbox_done),
            "outbox_failed": int(outbox_failed),
            "worker_ok": bool(worker_ok),
            "es_health_ok": bool(es_health_ok),
            "es_index_ok": bool(es_index_ok),
            "es_refresh_ok": bool(es_refresh_ok),
            "es_search_ok": bool(es_search_ok),
            "es_candidates_total": len(es_candidates),
            "parity_ok": bool(parity_ok),
            "strategy": strategy,
        },
        errors=[],
    )
