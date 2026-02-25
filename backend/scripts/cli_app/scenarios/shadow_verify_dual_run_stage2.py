from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
import uuid
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import bindparam, create_engine, text

from ..common import REPO_ROOT, write_json, write_text
from ..registry import register
from ..types import DrillInputs, DrillResult


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

    # Try a couple of common patterns; keep it best-effort.
    patterns = [
        r"last_claim_batch_id=([0-9a-f\-]{8,})",
        r"claim_batch_id=([0-9a-f\-]{8,})",
    ]
    for p in patterns:
        m = re.findall(p, text_content, flags=re.IGNORECASE)
        if m:
            return str(m[-1])
    return None


def _tail(text_value: str, limit: int = 4000) -> str:
    t = text_value or ""
    if len(t) <= limit:
        return t
    return t[-limit:]


@register("shadow_verify_dual_run_stage2")
@register("shadow-verify-dual-run-stage2")
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

    worker_batch_size = int(payload.get("worker_batch_size") or 0)
    worker_concurrency = int(payload.get("worker_concurrency") or 0)
    worker_poll_interval_seconds = float(payload.get("worker_poll_interval_seconds") or 0.0)
    worker_max_runtime_seconds = float(payload.get("worker_max_runtime_seconds") or 0.0)
    worker_idle_polls_before_exit = int(payload.get("worker_idle_polls_before_exit") or 0)

    if ensure_min_rows < 0:
        return DrillResult(ok=False, errors=["ensure_min_rows must be >= 0"], meta={}, summary={})
    if candidate_limit <= 0:
        return DrillResult(ok=False, errors=["candidate_limit must be > 0"], meta={}, summary={})
    if strategy not in {"soft", "strict"}:
        return DrillResult(ok=False, errors=["strategy must be one of: soft, strict"], meta={}, summary={})
    if worker_batch_size <= 0:
        return DrillResult(ok=False, errors=["worker_batch_size must be > 0"], meta={}, summary={})
    if worker_concurrency <= 0:
        return DrillResult(ok=False, errors=["worker_concurrency must be > 0"], meta={}, summary={})
    if worker_poll_interval_seconds < 0:
        return DrillResult(ok=False, errors=["worker_poll_interval_seconds must be >= 0"], meta={}, summary={})
    if worker_max_runtime_seconds <= 0:
        return DrillResult(ok=False, errors=["worker_max_runtime_seconds must be > 0"], meta={}, summary={})
    if worker_idle_polls_before_exit <= 0:
        return DrillResult(ok=False, errors=["worker_idle_polls_before_exit must be > 0"], meta={}, summary={})

    env_payload = payload.get("env")
    env: dict[str, str] = os.environ.copy()
    if isinstance(env_payload, dict):
        env.update({str(k): str(v) for k, v in env_payload.items()})

    es_url = str(payload.get("es_url") or env.get("ELASTIC_URL") or "http://127.0.0.1:19200").strip().rstrip("/")
    token = str(payload.get("token") or "").strip()
    if not token:
        token_default = "dualrun" + re.sub(r"[^0-9A-Za-z]+", "", inputs.run_id)
        token = token_default

    es_index = str(payload.get("es_index") or env.get("ELASTIC_INDEX") or _sanitize_index_name(f"wordloom-search-index-dualrun-{token}")).strip()
    es_index = _sanitize_index_name(es_index)
    recreate_index = bool(payload.get("recreate_index"))

    outdir_raw = payload.get("outdir")
    outdir = Path(str(outdir_raw)) if outdir_raw else None
    if outdir is None:
        return DrillResult(ok=False, errors=["outdir is required"], meta={}, summary={})

    scope = "all" if library_id is None else f"library:{library_id}"

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
    outbox_event_ids: list[str] = []
    pg_sql = ""

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
                   COALESCE(event_version, 0) AS event_version
            FROM search_index
            WHERE {where_sql}
            ORDER BY COALESCE(event_version, 0) ASC, entity_id::text ASC
            LIMIT :limit
        """
        pg_params = dict(base_params)
        pg_params["limit"] = candidate_limit
        pg_rows = conn.execute(text(pg_sql), pg_params).all()
        pg_candidates = [{"entity_id": str(r[0]), "event_version": int(r[1] or 0)} for r in pg_rows]

        outbox_cols = _table_columns(conn, "search_outbox_events")
        if not outbox_cols:
            return DrillResult(ok=False, errors=["table search_outbox_events not found"], meta={}, summary={})
        required_cols = {"id", "entity_type", "entity_id", "op", "event_version", "status"}
        missing_required = sorted([c for c in required_cols if c not in outbox_cols])
        if missing_required:
            return DrillResult(
                ok=False,
                errors=[f"search_outbox_events missing required columns: {missing_required}"],
                meta={},
                summary={},
            )

        now = datetime.now(timezone.utc)
        base_event: dict[str, object] = {
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

        rows = []
        for c in pg_candidates:
            ev_uuid = uuid.uuid4()
            outbox_event_ids.append(str(ev_uuid))
            row = {
                **{k: v for k, v in base_event.items() if k in chosen_cols},
                "id": ev_uuid,
                "entity_id": uuid.UUID(str(c["entity_id"])),
                "event_version": int(c["event_version"] or 0),
            }
            if "library_id" in chosen_cols:
                row["library_id"] = (uuid.UUID(library_id) if library_id else None)
            rows.append(row)

        cols_sql = ", ".join(chosen_cols)
        placeholders = ", ".join([f":{c}" for c in chosen_cols])
        outbox_insert_sql = text(f"INSERT INTO search_outbox_events ({cols_sql}) VALUES ({placeholders})")
        conn.execute(outbox_insert_sql, rows)
        conn.commit()

    probe: dict[str, object] = {
        "event": "labs.dual_run.stage2.probe",
        "lab_id": inputs.scope_id,
        "scenario": "shadow_verify_dual_run_stage2",
        "run_id": inputs.run_id,
        "scope": scope,
        "library_id": library_id,
        "token": token,
        "pg_candidates_total": len(pg_candidates),
        "outbox_enqueued_total": len(outbox_event_ids),
        "es_url": es_url,
        "es_index": es_index,
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

    worker_script = REPO_ROOT / "backend" / "scripts" / "search_outbox_worker.py"

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

    backend_path = str(REPO_ROOT / "backend")
    existing_pythonpath = str(worker_env.get("PYTHONPATH") or "").strip()
    if existing_pythonpath:
        if backend_path not in existing_pythonpath.split(os.pathsep):
            worker_env["PYTHONPATH"] = backend_path + os.pathsep + existing_pythonpath
    else:
        worker_env["PYTHONPATH"] = backend_path

    # WORDLOOM_ENV inference for the legacy worker guard.
    try:
        from urllib.parse import urlparse

        parsed = urlparse(database_url)
        db_name = (parsed.path or "").lstrip("/").split("/")[0]

        inferred_env: str | None = None
        if db_name.endswith("_test") or db_name == "wordloom_test":
            inferred_env = "test"
        elif db_name.endswith("_dev") or db_name == "wordloom_dev":
            inferred_env = "dev"
        elif db_name.endswith("_sandbox") or db_name == "wordloom_sandbox":
            inferred_env = "sandbox"

        if inferred_env:
            worker_env["WORDLOOM_ENV"] = inferred_env
        else:
            worker_env.pop("WORDLOOM_ENV", None)
    except Exception:
        worker_env.pop("WORDLOOM_ENV", None)

    worker_env["OUTBOX_EXIT_WHEN_IDLE"] = "1"
    worker_env["OUTBOX_IDLE_POLLS_BEFORE_EXIT"] = str(int(worker_idle_polls_before_exit))
    worker_env["OUTBOX_MAX_RUNTIME_SECONDS"] = str(float(worker_max_runtime_seconds))
    worker_env["OUTBOX_POLL_INTERVAL_SECONDS"] = str(float(worker_poll_interval_seconds))
    worker_env["OUTBOX_BULK_SIZE"] = str(int(worker_batch_size))
    worker_env["OUTBOX_CONCURRENCY"] = str(int(worker_concurrency))
    worker_env["OUTBOX_REQUIRE_ES_READY"] = "1"
    worker_env["OUTBOX_SHUTDOWN_GRACE_SECONDS"] = "5"

    t0 = time.time()
    worker_proc = subprocess.run(
        [sys.executable, str(worker_script)],
        cwd=str(REPO_ROOT),
        env=worker_env,
        capture_output=True,
        text=True,
        check=False,
        timeout=float(worker_max_runtime_seconds) + 10.0,
    )
    worker_runtime_s = float(time.time() - t0)
    worker_exit_code = int(worker_proc.returncode)
    worker_ok = bool(worker_exit_code == 0)

    worker_log_path = outdir / "worker.log"
    write_text(
        worker_log_path,
        (worker_proc.stdout or "") + "\n--- stderr ---\n" + (worker_proc.stderr or "") + "\n",
    )
    last_claim_batch_id = _extract_last_claim_batch_id(worker_log_path)

    worker_stdout_tail = _tail(worker_proc.stdout or "")
    worker_stderr_tail = _tail(worker_proc.stderr or "")

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

    outbox_status_counts: dict[str, int] = {}
    if outbox_event_ids:
        outbox_sql = (
            text(
                """
                SELECT status, COUNT(*) AS n
                FROM search_outbox_events
                WHERE id IN :ids
                GROUP BY status
                """
            )
            .bindparams(bindparam("ids", expanding=True))
        )
        with engine.connect() as conn:
            rows = conn.execute(outbox_sql, {"ids": [uuid.UUID(x) for x in outbox_event_ids]}).all()
            for st, n in rows:
                outbox_status_counts[str(st)] = int(n or 0)

    outbox_done = int(outbox_status_counts.get("done", 0))
    outbox_pending = int(outbox_status_counts.get("pending", 0))
    outbox_processing = int(outbox_status_counts.get("processing", 0))
    outbox_failed = int(outbox_status_counts.get("failed", 0))

    pg_ids = [str(c["entity_id"]) for c in pg_candidates]
    es_ids = [str(c["entity_id"]) for c in es_candidates]
    if strategy == "strict":
        parity_ok = bool(pg_ids == es_ids)
    else:
        parity_ok = bool(set(pg_ids) & set(es_ids))

    ok = bool(
        len(pg_candidates) > 0
        and es_health_ok
        and es_index_ok
        and worker_ok
        and es_refresh_ok
        and es_search_ok
        and outbox_failed == 0
        and outbox_pending == 0
        and outbox_processing == 0
        and outbox_done == len(outbox_event_ids)
        and parity_ok
    )

    traces_written = False
    traces_error: str | None = None
    trace_id: str | None = None
    span_id: str | None = None
    span_name = "labs.shadow_verify_dual_run_stage2.probe"

    try:
        from opentelemetry import trace  # type: ignore
        from opentelemetry.sdk.resources import Resource  # type: ignore
        from opentelemetry.sdk.trace import TracerProvider  # type: ignore
        from opentelemetry.sdk.trace.export import (  # type: ignore
            SimpleSpanProcessor,
            SpanExporter,
            SpanExportResult,
        )
        from opentelemetry.sdk.trace.sampling import ALWAYS_ON  # type: ignore

        exported_spans: list[dict[str, object]] = []

        class _JsonSpanExporter(SpanExporter):
            def export(self, spans) -> SpanExportResult:  # type: ignore[override]
                for s in spans:
                    ctx = getattr(s, "context", None)
                    if ctx is not None:
                        t_id = f"{int(ctx.trace_id):032x}"
                        s_id = f"{int(ctx.span_id):016x}"
                    else:
                        t_id = ""
                        s_id = ""

                    attrs = dict(getattr(s, "attributes", {}) or {})
                    exported_spans.append(
                        {
                            "name": getattr(s, "name", ""),
                            "trace_id": t_id,
                            "span_id": s_id,
                            "start_time_unix_nano": int(getattr(s, "start_time", 0) or 0),
                            "end_time_unix_nano": int(getattr(s, "end_time", 0) or 0),
                            "attributes": attrs,
                        }
                    )
                return SpanExportResult.SUCCESS

            def shutdown(self) -> None:  # type: ignore[override]
                return None

        provider = TracerProvider(resource=Resource.create({"service.name": "wordloom-labs"}), sampler=ALWAYS_ON)
        provider.add_span_processor(SimpleSpanProcessor(_JsonSpanExporter()))
        trace.set_tracer_provider(provider)

        tracer = trace.get_tracer("wordloom.labs")
        with tracer.start_as_current_span(span_name) as span:
            span.set_attribute("event", "labs.dual_run.stage2.probe")
            span.set_attribute("lab_id", inputs.scope_id)
            span.set_attribute("scenario", "shadow_verify_dual_run_stage2")
            span.set_attribute("run_id", inputs.run_id)
            span.set_attribute("scope", scope)
            span.set_attribute("library_id", library_id or "")
            span.set_attribute("token", token)
            span.set_attribute("pg_candidates_total", len(pg_candidates))
            span.set_attribute("outbox_enqueued_total", len(outbox_event_ids))
            span.set_attribute("outbox_done", int(outbox_done))
            span.set_attribute("outbox_failed", int(outbox_failed))
            span.set_attribute("worker_exit_code", int(worker_exit_code))
            span.set_attribute("worker_runtime_seconds", float(worker_runtime_s))
            span.set_attribute("strategy", strategy)
            span.set_attribute("ok", bool(ok))

            ctx = span.get_span_context()
            trace_id = f"{int(ctx.trace_id):032x}"
            span_id = f"{int(ctx.span_id):016x}"

        provider.force_flush()

        write_json(
            outdir / "traces.json",
            {
                "service": "wordloom-labs",
                "scenario": "shadow_verify_dual_run_stage2",
                "run_id": inputs.run_id,
                "spans": exported_spans,
            },
        )
        traces_written = True
    except Exception as e:
        traces_error = f"{type(e).__name__}: {e}"
        try:
            write_json(
                outdir / "traces.json",
                {
                    "service": "wordloom-labs",
                    "scenario": "shadow_verify_dual_run_stage2",
                    "run_id": inputs.run_id,
                    "spans": [],
                    "error": traces_error,
                },
            )
        except Exception:
            pass

    def _rel_repo(path: Path) -> str:
        try:
            return str(path.resolve().relative_to(REPO_ROOT).as_posix())
        except Exception:
            return str(path.as_posix())

    result: dict[str, object] = {
        "lab_id": inputs.scope_id,
        "scenario": "shadow_verify_dual_run_stage2",
        "run_id": inputs.run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "scope": scope,
        "inputs": {
            "token": token,
            "ensure_min_rows": int(ensure_min_rows),
            "seed_entity_type": seed_entity_type,
            "candidate_limit": int(candidate_limit),
            "strategy": strategy,
            "es_url": es_url,
            "es_index": es_index,
            "recreate_index": bool(recreate_index),
            "worker_batch_size": int(worker_batch_size),
            "worker_concurrency": int(worker_concurrency),
            "worker_poll_interval_seconds": float(worker_poll_interval_seconds),
            "worker_idle_polls_before_exit": int(worker_idle_polls_before_exit),
            "worker_max_runtime_seconds": float(worker_max_runtime_seconds),
        },
        "seed_rows_inserted": int(inserted_rows),
        "postgres": {
            "query_sql": pg_sql.strip(),
            "candidates": pg_candidates,
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
            "script": _rel_repo(worker_script),
            "exit_code": int(worker_exit_code),
            "ok": bool(worker_ok),
            "runtime_seconds": float(worker_runtime_s),
            "log_path": _rel_repo(worker_log_path),
            "last_claim_batch_id": last_claim_batch_id,
            "stdout_tail": worker_stdout_tail,
            "stderr_tail": worker_stderr_tail,
        },
        "compare": {
            "pg_ids": pg_ids,
            "es_ids": es_ids,
            "parity_ok": bool(parity_ok),
        },
        "observability": {
            "log_probe_emitted": True,
            "trace_probe": {
                "span_name": span_name,
                "trace_id": trace_id,
                "span_id": span_id,
                "traces_json_written": traces_written,
                "error": traces_error,
            },
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
            "outbox_enqueued_total": len(outbox_event_ids),
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
            "trace_id": trace_id,
            "span_id": span_id,
            "traces_json_written": bool(traces_written),
        },
        errors=[],
    )
