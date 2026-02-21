from __future__ import annotations

import os
import json
import re
import subprocess
import sys
import time
import uuid
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sqlalchemy import create_engine, text

from ..common import REPO_ROOT, write_json, write_text
from ..registry import register
from ..types import DrillInputs, DrillResult


LEGACY_SCRIPTS_DIR = REPO_ROOT / "backend" / "scripts" / "legacy"


def _http_json(
    method: str,
    url: str,
    *,
    body: dict[str, object] | None = None,
    timeout_s: float = 5.0,
) -> tuple[int, str]:
    data = None
    headers: dict[str, str] = {}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            status = int(getattr(resp, "status", 0) or 0)
            payload = resp.read().decode("utf-8", errors="replace")
            return status, payload
    except urllib.error.HTTPError as e:
        try:
            payload = e.read().decode("utf-8", errors="replace")
        except Exception:
            payload = str(e)
        return int(getattr(e, "code", 0) or 0), payload
    except Exception as e:
        return 0, f"{type(e).__name__}: {e}"


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


def _rel_repo(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT).as_posix())
    except Exception:
        return str(path.as_posix())


@register("shadow_verify_dual_run_stage1")
@register("shadow-verify-dual-run-stage1")
def run(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    database_url = str(payload.get("database_url") or "").strip()
    library_id = (str(payload.get("library_id") or "").strip() or None)

    ensure_min_rows = int(payload.get("ensure_min_rows") or 0)
    candidate_limit = int(payload.get("candidate_limit") or 0)
    backfill_batch_size = int(payload.get("backfill_batch_size") or 0)
    strategy = str(payload.get("strategy") or "").strip() or "soft"

    es_url = str(payload.get("es_url") or "").strip().rstrip("/")
    token = str(payload.get("token") or "").strip()
    es_index_raw = str(payload.get("es_index") or "").strip()
    recreate_index = bool(payload.get("recreate_index"))

    outdir_raw = payload.get("outdir")
    outdir = Path(str(outdir_raw)) if outdir_raw else None

    if not database_url:
        return DrillResult(ok=False, errors=["DATABASE_URL is required"], meta={}, summary={})

    if ensure_min_rows < 0:
        return DrillResult(ok=False, errors=["ensure_min_rows must be >= 0"], meta={}, summary={})
    if candidate_limit <= 0:
        return DrillResult(ok=False, errors=["candidate_limit must be > 0"], meta={}, summary={})
    if backfill_batch_size <= 0:
        return DrillResult(ok=False, errors=["backfill_batch_size must be > 0"], meta={}, summary={})
    if strategy not in {"soft", "strict"}:
        return DrillResult(ok=False, errors=["strategy must be one of: soft, strict"], meta={}, summary={})

    scope = "all" if library_id is None else f"library:{library_id}"

    if not es_url:
        es_url = "http://127.0.0.1:19200"

    if not token:
        token_default = "dualrun" + re.sub(r"[^0-9A-Za-z]+", "", inputs.run_id)
        token = token_default

    if not es_index_raw:
        es_index_raw = _sanitize_index_name(f"wordloom-search-index-dualrun-{token}")
    es_index = _sanitize_index_name(es_index_raw)

    seed_text_prefix = f"{token} "
    seed_entity_type = "block"

    where_parts: list[str] = ["entity_type = :entity_type", "text ILIKE :pattern"]
    base_params: dict[str, object] = {
        "entity_type": seed_entity_type,
        "pattern": f"%{token}%",
    }
    if library_id is not None:
        where_parts.append("library_id = :library_id")
        base_params["library_id"] = library_id

    where_sql = " AND ".join(where_parts)

    engine = create_engine(database_url)
    inserted_rows = 0
    pg_sql = ""
    pg_candidates: list[dict[str, object]] = []
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
                        "id": str(uuid.uuid4()),
                        "entity_type": seed_entity_type,
                        "library_id": library_id,
                        "entity_id": str(uuid.uuid4()),
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

    probe: dict[str, object] = {
        "event": "labs.dual_run.stage1.probe",
        "lab_id": inputs.scope_id,
        "scenario": "shadow_verify_dual_run_stage1",
        "run_id": inputs.run_id,
        "scope": scope,
        "library_id": library_id,
        "token": token,
        "pg_candidates_total": len(pg_candidates),
        "pg_first": (pg_candidates[0] if pg_candidates else None),
        "es_url": es_url,
        "es_index": es_index,
    }
    print(json.dumps(probe, ensure_ascii=False, separators=(",", ":")))

    es_health_status, es_health_payload = _http_json("GET", f"{es_url}", body=None, timeout_s=5.0)
    es_health_ok = bool(es_health_status == 200)

    backfill_script = LEGACY_SCRIPTS_DIR / "backfill_elastic_search_index.py"
    backfill_cmd = [
        sys.executable,
        str(backfill_script),
        "--batch-size",
        str(backfill_batch_size),
    ]
    if recreate_index:
        backfill_cmd.append("--recreate")

    env_from_payload = payload.get("env")
    merged_env: dict[str, str] = os.environ.copy()
    if isinstance(env_from_payload, dict):
        merged_env.update({str(k): str(v) for k, v in env_from_payload.items()})

    merged_env["DATABASE_URL"] = database_url
    merged_env["ELASTIC_URL"] = es_url
    merged_env["ELASTIC_INDEX"] = es_index

    backfill_proc = subprocess.run(
        backfill_cmd,
        cwd=str(REPO_ROOT),
        env=merged_env,
        capture_output=True,
        text=True,
        check=False,
    )

    backfill_exit_code = int(backfill_proc.returncode)
    backfill_ok = bool(backfill_exit_code == 0)

    backfill_log_path: Path | None = None
    if outdir is not None:
        backfill_log_path = outdir / "backfill.log"
        write_text(
            backfill_log_path,
            (backfill_proc.stdout or "") + "\n--- stderr ---\n" + (backfill_proc.stderr or "") + "\n",
        )

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

    pg_ids = [str(c["entity_id"]) for c in pg_candidates]
    es_ids = [str(c["entity_id"]) for c in es_candidates]
    if strategy == "strict":
        parity_ok = bool(pg_ids == es_ids)
    else:
        parity_ok = bool(set(pg_ids) & set(es_ids))

    ok = bool(len(pg_candidates) > 0 and es_health_ok and backfill_ok and es_search_ok and parity_ok)

    traces_written = False
    traces_error: str | None = None
    trace_id: str | None = None
    span_id: str | None = None
    span_name = "labs.shadow_verify_dual_run_stage1.probe"

    if outdir is not None:
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
                span.set_attribute("event", "labs.dual_run.stage1.probe")
                span.set_attribute("lab_id", inputs.scope_id)
                span.set_attribute("scenario", "shadow_verify_dual_run_stage1")
                span.set_attribute("run_id", inputs.run_id)
                span.set_attribute("scope", scope)
                span.set_attribute("library_id", library_id or "")
                span.set_attribute("token", token)
                span.set_attribute("pg_candidates_total", len(pg_candidates))
                span.set_attribute("es_candidates_total", len(es_candidates))
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
                    "scenario": "shadow_verify_dual_run_stage1",
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
                        "scenario": "shadow_verify_dual_run_stage1",
                        "run_id": inputs.run_id,
                        "spans": [],
                        "error": traces_error,
                    },
                )
            except Exception:
                pass

    result: dict[str, object] = {
        "lab_id": inputs.scope_id,
        "scenario": "shadow_verify_dual_run_stage1",
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
            "backfill_batch_size": int(backfill_batch_size),
        },
        "seed_rows_inserted": int(inserted_rows),
        "postgres": {
            "query_sql": pg_sql.strip(),
            "candidates": pg_candidates,
        },
        "elasticsearch": {
            "health": {"status": int(es_health_status), "ok": bool(es_health_ok), "payload": es_health_payload},
            "backfill": {
                "exit_code": int(backfill_exit_code),
                "ok": bool(backfill_ok),
                "log_path": (_rel_repo(backfill_log_path) if backfill_log_path is not None else None),
                "script": _rel_repo(backfill_script),
            },
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
            "es_health_ok": bool(es_health_ok),
            "backfill_ok": bool(backfill_ok),
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
