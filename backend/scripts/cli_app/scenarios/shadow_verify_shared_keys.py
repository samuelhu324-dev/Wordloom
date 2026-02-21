from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from sqlalchemy import create_engine, text

from ._search_index_seed import ensure_search_index_min_rows
from ..common import write_json
from ..registry import register
from ..types import DrillInputs, DrillResult


@register("shadow_verify_shared_keys")
@register("shadow-verify-shared-keys")
def run(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    database_url = str(payload.get("database_url") or "").strip()
    library_id = (str(payload.get("library_id") or "").strip() or None)
    ensure_min_rows = int(payload.get("ensure_min_rows") or 0)

    outdir_raw = payload.get("outdir")
    outdir = Path(str(outdir_raw)) if outdir_raw else None

    if not database_url:
        return DrillResult(ok=False, errors=["DATABASE_URL is required"], meta={}, summary={})

    scope = "all" if library_id is None else f"library:{library_id}"

    engine = create_engine(database_url)
    with engine.connect() as conn:
        inserted_rows = ensure_search_index_min_rows(conn=conn, ensure_min_rows=ensure_min_rows, library_id=library_id)

        sample_where = "" if library_id is None else "WHERE library_id = :library_id"
        sample_params = {} if library_id is None else {"library_id": library_id}
        rows = conn.execute(
            text(
                f"""
                SELECT entity_type, entity_id
                FROM search_index
                {sample_where}
                ORDER BY entity_type, entity_id
                LIMIT 5
                """
            ),
            sample_params,
        ).all()

    samples = [{"entity_type": str(r[0]), "entity_id": str(r[1])} for r in rows]
    ok = len(samples) > 0

    # Strong mutual evidence (minimal, machine-searchable): emit the same shared keys
    # into stdout logs + a local traces.json span.
    probe: dict[str, Any] = {
        "event": "labs.shared_keys.probe",
        "lab_id": inputs.scope_id,
        "scenario": "shadow_verify_shared_keys",
        "run_id": inputs.run_id,
        "scope": scope,
        "library_id": library_id,
        "samples_total": len(samples),
        "sample": (samples[0] if samples else None),
    }

    print(json.dumps(probe, ensure_ascii=False, separators=(",", ":")))

    traces_written = False
    traces_error: str | None = None
    trace_id: str | None = None
    span_id: str | None = None
    span_name = "labs.shadow_verify_shared_keys.probe"

    if outdir is not None:
        try:
            # Keep this exporter local and deterministic (no external collector required).
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
                span.set_attribute("event", "labs.shared_keys.probe")
                span.set_attribute("lab_id", inputs.scope_id)
                span.set_attribute("scenario", "shadow_verify_shared_keys")
                span.set_attribute("run_id", inputs.run_id)
                span.set_attribute("scope", scope)
                span.set_attribute("library_id", library_id or "")
                span.set_attribute("samples_total", len(samples))
                if samples:
                    span.set_attribute("sample.entity_type", samples[0]["entity_type"])
                    span.set_attribute("sample.entity_id", samples[0]["entity_id"])

                ctx = span.get_span_context()
                trace_id = f"{int(ctx.trace_id):032x}"
                span_id = f"{int(ctx.span_id):016x}"

            provider.force_flush()

            write_json(
                outdir / "traces.json",
                {
                    "service": "wordloom-labs",
                    "scenario": "shadow_verify_shared_keys",
                    "run_id": inputs.run_id,
                    "spans": exported_spans,
                },
            )
            traces_written = True
        except Exception as e:  # keep drill safe
            traces_error = f"{type(e).__name__}: {e}"
            try:
                write_json(
                    outdir / "traces.json",
                    {
                        "service": "wordloom-labs",
                        "scenario": "shadow_verify_shared_keys",
                        "run_id": inputs.run_id,
                        "spans": [],
                        "error": traces_error,
                    },
                )
            except Exception:
                pass

    result: dict[str, Any] = {
        "lab_id": inputs.scope_id,
        "scenario": "shadow_verify_shared_keys",
        "run_id": inputs.run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "scope": scope,
        "shared_keys": {
            "run_id": inputs.run_id,
            "library_id": library_id,
            "samples": samples,
        },
        "ensure_min_rows": int(ensure_min_rows),
        "seed_rows_inserted": int(inserted_rows),
        "evidence_queries": {
            "artifact_logs_grep": [
                "scenario=shadow_verify_shared_keys",
                f"run_id={inputs.run_id}",
                f"scope={scope}",
            ],
            "artifact_logs_grep_json": [
                '"event":"labs.shared_keys.probe"',
                f'"run_id":"{inputs.run_id}"',
            ],
            "artifact_traces_jq": [
                f'.spans[] | select(.attributes.run_id=="{inputs.run_id}")',
                '.spans[] | select(.attributes.scenario=="shadow_verify_shared_keys")',
            ],
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
            "samples_total": len(samples),
            "trace_id": trace_id,
            "span_id": span_id,
            "traces_json_written": bool(traces_written),
        },
        errors=[],
    )
