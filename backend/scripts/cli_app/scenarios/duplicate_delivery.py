from __future__ import annotations

import json
import re
import shutil
import time
import uuid
from pathlib import Path

from ..common import build_evidence_paths_for_dir, pack_artifacts, write_json
from ..registry import register
from ..types import DrillInputs, DrillResult
from ._failure_drill_shared import (
    LAB_ID_S3A_2A_3A,
    SEARCH_OUTBOX_OBS_SCHEMA_VERSION,
    default_labs_auto_run_dir,
    ensure_dir,
    load_env,
    load_env_from_run_recipe_v1,
    prom_parse_counter_sum,
    spawn_search_outbox_worker,
    resolve_run_dir,
    run_cmd,
    run_search_outbox_supply_inserter_v1,
    scrape_metrics_text,
    scrape_metrics_text_readiness_v1,
    readiness_sleep_v1,
    read_json_file,
    with_backend_pythonpath,
    verify_supply_rows_v1,
)
from ._failure_drill_shared import LEGACY_SCRIPTS_DIR, LABS_SNAPSHOT_ROOT, REPO_ROOT


SCENARIO_DUPLICATE_DELIVERY = "duplicate_delivery"


@register("duplicate_delivery.run")
def run_duplicate_delivery(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_id = str(payload.get("run_id") or "").strip()
    outdir_str = str(payload.get("outdir") or "").strip()
    outdir = Path(outdir_str) if outdir_str else default_labs_auto_run_dir(scenario=SCENARIO_DUPLICATE_DELIVERY, run_id=run_id)

    env_file = payload.get("env_file")
    service = payload.get("service")
    duration = int(payload.get("duration") or 0)
    metrics_port = int(payload.get("metrics_port") or 0)
    scrape_delay = float(payload.get("scrape_delay") or 0.0)

    entity_type = payload.get("entity_type")
    entity_id = str(payload.get("entity_id") or "").strip() if payload.get("entity_id") else str(uuid.uuid4())
    delete_count = int(payload.get("delete_count") or 0)

    logs_dir = outdir / "_logs"
    metrics_dir = outdir / "_metrics"
    exports_dir = outdir / "_exports"
    ensure_dir(logs_dir)
    ensure_dir(metrics_dir)
    ensure_dir(exports_dir)

    env = with_backend_pythonpath(load_env(env_file=str(env_file) if env_file else None))

    service_name = service
    env.setdefault("WORDLOOM_TRACING_ENABLED", "1")
    env.setdefault("OTEL_SERVICE_NAME", service_name)
    env.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
    env.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    env.setdefault("OTEL_TRACES_SAMPLER", "always_on")

    env["OUTBOX_USE_ES_BULK"] = "0"

    env.setdefault("ELASTIC_URL", "http://localhost:19200")
    env.setdefault("ELASTIC_INDEX", "wordloom-test-search-index")

    env["OUTBOX_EXPERIMENT_ES_429_RATIO"] = "0"
    env.pop("OUTBOX_EXPERIMENT_ES_429_EVERY_N", None)
    env["OUTBOX_EXPERIMENT_ES_BULK_PARTIAL"] = "0"
    env["OUTBOX_EXPERIMENT_BREAK_CLAIM"] = "0"
    env["OUTBOX_EXPERIMENT_PROCESS_SLEEP_SECONDS"] = "0"

    env["OUTBOX_METRICS_PORT"] = str(int(metrics_port))

    (outdir / "_entity_id.txt").write_text(entity_id + "\n", encoding="utf-8")

    recipe = {
        "lab_id": LAB_ID_S3A_2A_3A,
        "scenario": SCENARIO_DUPLICATE_DELIVERY,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": env_file,
        "service": service_name,
        "entity": {"entity_type": str(entity_type), "entity_id": entity_id},
        "worker": {"duration_s": int(duration), "metrics_port": int(metrics_port)},
        "trigger": {"upsert_count": 1, "delete_count": int(delete_count)},
        "expect": {"idempotent_noop": {"kind": "es_delete_404", "count": 1}},
    }
    write_json(outdir / "_recipe.json", recipe)

    log_path = logs_dir / f"worker-{run_id}.log"

    print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] outdir: {outdir}")
    print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] worker log: {log_path}")
    print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] entity_id: {entity_id}")

    metrics_before_path = metrics_dir / "metrics-before.txt"
    metrics_after_path = metrics_dir / "metrics-after.txt"

    start = time.time()
    stopped_by_controller = False
    outbox_event_ids: list[str] = []

    worker_env_keys = [
        "WORDLOOM_TRACING_ENABLED",
        "OTEL_SERVICE_NAME",
        "OTEL_EXPORTER_OTLP_PROTOCOL",
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        "OTEL_TRACES_SAMPLER",
        "OUTBOX_USE_ES_BULK",
        "ELASTIC_URL",
        "ELASTIC_INDEX",
        "OUTBOX_EXPERIMENT_ES_429_RATIO",
        "OUTBOX_EXPERIMENT_ES_BULK_PARTIAL",
        "OUTBOX_EXPERIMENT_BREAK_CLAIM",
        "OUTBOX_EXPERIMENT_PROCESS_SLEEP_SECONDS",
        "OUTBOX_METRICS_PORT",
    ]
    worker_handle = spawn_search_outbox_worker(
        env=env,
        logs_dir=logs_dir,
        run_id=run_id,
        log_name=log_path.name,
        evidence_env_keys=[k for k in worker_env_keys if k in env],
    )
    write_json(outdir / "_worker_start.json", worker_handle.evidence_summary())
    try:
            readiness_sleep_v1(scrape_delay)
            metrics_before_path.write_text(
                scrape_metrics_text_readiness_v1(port=int(metrics_port), timeout_s=4.0),
                encoding="utf-8",
            )

            upsert_env = env.copy()
            upsert_env["OUTBOX_ENTITY_TYPE"] = str(entity_type)
            upsert_env["OUTBOX_ENTITY_ID"] = entity_id

            upsert_supply_res = run_search_outbox_supply_inserter_v1(
                outdir=outdir,
                env=upsert_env,
                op="upsert",
                insert_count=1,
                create_search_index_row=True,
                event_version=0,
                timeout_s=30.0,
                file_prefix="_trigger_upsert",
            )
            if upsert_supply_res.returncode is None:
                print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] upsert inserter timed out")
                worker_handle.terminate_and_wait(timeout_s=30)
                exit_info = {
                    "returncode": int(worker_handle.proc.returncode)
                    if worker_handle.proc.returncode is not None
                    else None
                }
                write_json(outdir / "_worker_exit.json", exit_info)
                return DrillResult(ok=False, meta={"exit_code": 5}, summary={}, errors=[])
            if upsert_supply_res.returncode != 0:
                print(
                    f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] failed to insert upsert outbox event: rc={upsert_supply_res.returncode}"
                )
                worker_handle.terminate_and_wait(timeout_s=30)
                return DrillResult(ok=False, meta={"exit_code": 3}, summary={}, errors=[])

            outbox_event_ids.extend(list(upsert_supply_res.outbox_event_ids))
            time.sleep(1.5)

            delete_env = env.copy()
            delete_env["OUTBOX_ENTITY_TYPE"] = str(entity_type)
            delete_env["OUTBOX_ENTITY_ID"] = entity_id

            delete_supply_res = run_search_outbox_supply_inserter_v1(
                outdir=outdir,
                env=delete_env,
                op="delete",
                insert_count=max(1, int(delete_count)),
                create_search_index_row=False,
                event_version=0,
                timeout_s=30.0,
                file_prefix="_trigger_delete",
            )
            if delete_supply_res.returncode is None:
                print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] delete inserter timed out")
                worker_handle.terminate_and_wait(timeout_s=30)
                exit_info = {
                    "returncode": int(worker_handle.proc.returncode)
                    if worker_handle.proc.returncode is not None
                    else None
                }
                write_json(outdir / "_worker_exit.json", exit_info)
                return DrillResult(ok=False, meta={"exit_code": 5}, summary={}, errors=[])
            if delete_supply_res.returncode != 0:
                print(
                    f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] failed to insert delete outbox events: rc={delete_supply_res.returncode}"
                )
                worker_handle.terminate_and_wait(timeout_s=30)
                return DrillResult(ok=False, meta={"exit_code": 4}, summary={}, errors=[])

            outbox_event_ids.extend(list(delete_supply_res.outbox_event_ids))

            (outdir / "_outbox_event_ids.txt").write_text("\n".join(outbox_event_ids) + "\n", encoding="utf-8")

            upsert_supply = dict(upsert_supply_res.evidence or {})
            upsert_supply["outbox_event_ids"] = list(upsert_supply_res.outbox_event_ids)
            upsert_supply["insert_count"] = int(upsert_supply.get("insert_count") or 1)
            delete_supply = dict(delete_supply_res.evidence or {})
            delete_supply["outbox_event_ids"] = list(delete_supply_res.outbox_event_ids)
            delete_supply["insert_count"] = int(delete_supply.get("insert_count") or len(delete_supply_res.outbox_event_ids) or max(1, int(delete_count)))
            write_json(
                outdir / "_supply.json",
                {"supplies": [upsert_supply, delete_supply], "outbox_event_ids": list(outbox_event_ids)},
            )

            while True:
                if duration > 0 and (time.time() - start) >= duration:
                    try:
                        metrics_after = scrape_metrics_text(port=int(metrics_port), timeout_s=4.0)
                        metrics_after_path.write_text(metrics_after, encoding="utf-8")
                        (outdir / "_metrics.txt").write_text(metrics_after, encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        metrics_after_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    stopped_by_controller = True
                    worker_handle.terminate_and_wait(timeout_s=30)
                    break

                ret = worker_handle.proc.poll()
                if ret is not None:
                    try:
                        metrics_after = scrape_metrics_text(port=int(metrics_port), timeout_s=4.0)
                        metrics_after_path.write_text(metrics_after, encoding="utf-8")
                        (outdir / "_metrics.txt").write_text(metrics_after, encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        metrics_after_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    break
                time.sleep(0.25)
    except KeyboardInterrupt:
        stopped_by_controller = True
        worker_handle.terminate_and_wait(timeout_s=30)
    finally:
        if worker_handle.proc.poll() is None:
            worker_handle.terminate_and_wait(timeout_s=30)
        else:
            worker_handle.wait(timeout_s=30)

    exit_info = {
        "returncode": int(worker_handle.proc.returncode) if worker_handle.proc.returncode is not None else None
    }
    write_json(outdir / "_worker_exit.json", exit_info)

    if not metrics_after_path.exists():
        metrics_after_path.write_text("scrape_failed: missing_metrics_after\n", encoding="utf-8")

    if (not stopped_by_controller) and (worker_handle.proc.returncode not in (None, 0)):
        print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] worker exited early: rc={worker_handle.proc.returncode}")
        print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] see logs: {log_path}")
        return DrillResult(ok=False, meta={"exit_code": 5}, summary={}, errors=[])

    print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] done (now run verify/export/clean)")
    print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] outputs: {outdir}")
    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])


@register("duplicate_delivery.verify")
def verify_duplicate_delivery(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_dir = resolve_run_dir(
        run_id=str(payload.get("run_id") or "").strip() or None,
        outdir=str(payload.get("outdir") or "").strip() or None,
        scenario=SCENARIO_DUPLICATE_DELIVERY,
    )
    metrics_dir = run_dir / "_metrics"
    logs_dir = run_dir / "_logs"

    before_path = metrics_dir / "metrics-before.txt"
    after_path = metrics_dir / "metrics-after.txt"

    before = before_path.read_text(encoding="utf-8") if before_path.exists() else ""
    after = after_path.read_text(encoding="utf-8") if after_path.exists() else ""

    worker_start_path = run_dir / "_worker_start.json"
    worker_start = None
    if worker_start_path.exists():
        try:
            worker_start = json.loads(worker_start_path.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            worker_start = None

    processed_before = prom_parse_counter_sum(before, "outbox_processed_total")
    processed_after = prom_parse_counter_sum(after, "outbox_processed_total")
    failed_before = prom_parse_counter_sum(before, "outbox_failed_total")
    failed_after = prom_parse_counter_sum(after, "outbox_failed_total")
    noop_before = prom_parse_counter_sum(before, "outbox_idempotent_noop_total")
    noop_after = prom_parse_counter_sum(after, "outbox_idempotent_noop_total")

    delta_processed = processed_after - processed_before
    delta_failed = failed_after - failed_before
    delta_noop = noop_after - noop_before

    metrics_available = ("scrape_failed" not in before.lower()) and ("scrape_failed" not in after.lower())

    log_paths = sorted([p for p in logs_dir.glob("*.log") if p.is_file()])
    noop_log_count = 0
    if log_paths:
        try:
            text = log_paths[0].read_text(encoding="utf-8", errors="replace")
            noop_log_count = len(re.findall(r"Outbox delete: doc .* not found in ES \(noop\)", text))
        except Exception:
            noop_log_count = 0

    min_processed_delta = float(payload.get("min_processed_delta") or 0)
    max_failed_delta = float(payload.get("max_failed_delta") or 0)
    min_noop_delta = float(payload.get("min_noop_delta") or 0)
    min_noop_logs = int(payload.get("min_noop_logs") or 0)

    supply = read_json_file(run_dir / "_supply.json")
    supply_db_check: dict[str, object] = {"skipped": True, "reason": "missing_supply"}
    supply_db_ok = True
    try:
        supply_ids: list[str] = []
        supply_for_check: dict[str, object] | None = None
        if isinstance(supply, dict) and isinstance(supply.get("supplies"), list):
            for s in supply.get("supplies") or []:
                if isinstance(s, dict) and s.get("outbox_event_ids"):
                    supply_ids.extend([str(x) for x in (s.get("outbox_event_ids") or [])])
            # Reuse the first supply's table/projection evidence, but check all ids.
            first_supply = next((s for s in (supply.get("supplies") or []) if isinstance(s, dict)), None)
            if isinstance(first_supply, dict):
                supply_for_check = dict(first_supply)
                supply_for_check["outbox_event_ids"] = list(supply_ids)
        elif isinstance(supply, dict) and supply.get("outbox_event_ids"):
            supply_for_check = supply

        if supply_for_check and supply_for_check.get("outbox_event_ids"):
            env = load_env_from_run_recipe_v1(run_dir)
            database_url = (env.get("DATABASE_URL") or "").strip()
            if database_url:
                supply_db_check = verify_supply_rows_v1(database_url=database_url, supply=supply_for_check)
                if "ok" in supply_db_check:
                    supply_db_ok = bool(supply_db_check.get("ok"))
            else:
                supply_db_check = {"skipped": True, "reason": "missing_database_url"}
        else:
            supply_db_check = {"skipped": True, "reason": "missing_outbox_event_ids"}
    except Exception as exc:  # noqa: BLE001
        supply_db_check = {"error": f"{type(exc).__name__}: {exc}"}
        supply_db_ok = False

    ok = (
        (delta_processed >= min_processed_delta)
        and (delta_failed <= max_failed_delta)
        and ((delta_noop >= min_noop_delta) or (noop_log_count >= min_noop_logs))
        and bool(supply_db_ok)
    )

    result = {
        "scenario": SCENARIO_DUPLICATE_DELIVERY,
        "run_dir": str(run_dir),
        "worker": worker_start,
        "checks": {
            "min_processed_delta": float(min_processed_delta),
            "max_failed_delta": float(max_failed_delta),
            "min_noop_delta": float(min_noop_delta),
            "min_noop_logs": int(min_noop_logs),
        },
        "observed": {
            "metrics_available": bool(metrics_available),
            "outbox_processed_total": {"before": processed_before, "after": processed_after, "delta": delta_processed},
            "outbox_failed_total": {"before": failed_before, "after": failed_after, "delta": delta_failed},
            "outbox_idempotent_noop_total": {"before": noop_before, "after": noop_after, "delta": delta_noop},
            "noop_log_count": int(noop_log_count),
            "supply": supply,
            "supply_db_check": supply_db_check,
        },
        "ok": bool(ok),
    }
    pack_artifacts(paths=build_evidence_paths_for_dir(run_dir), result=result)

    if ok:
        print(f"[labs verify {SCENARIO_DUPLICATE_DELIVERY}] OK")
        return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])

    print(f"[labs verify {SCENARIO_DUPLICATE_DELIVERY}] FAILED")
    return DrillResult(ok=False, meta={"exit_code": 10}, summary={}, errors=[])


@register("duplicate_delivery.export")
def export_duplicate_delivery(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_dir = resolve_run_dir(
        run_id=str(payload.get("run_id") or "").strip() or None,
        outdir=str(payload.get("outdir") or "").strip() or None,
        scenario=SCENARIO_DUPLICATE_DELIVERY,
    )
    exports_dir = run_dir / "_exports"
    ensure_dir(exports_dir)

    entity_id_path = run_dir / "_entity_id.txt"
    entity_id = entity_id_path.read_text(encoding="utf-8").strip() if entity_id_path.exists() else None

    tags = {
        "wordloom.obs_schema": SEARCH_OUTBOX_OBS_SCHEMA_VERSION,
    }
    if entity_id:
        tags["wordloom.entity_id"] = str(entity_id)

    cmd = [
        python_exe(),
        str(LEGACY_SCRIPTS_DIR / "labs_009_export_jaeger.py"),
        "--outdir",
        str(exports_dir),
        "--service",
        str(payload.get("service")),
        "--lookback",
        str(payload.get("lookback")),
        "--limit",
        str(payload.get("limit")),
        "--operation",
        "outbox.process",
        "--tags-json",
        json.dumps(tags, ensure_ascii=False),
    ]
    rc = run_cmd(cmd, cwd=REPO_ROOT)
    return DrillResult(ok=(rc == 0), meta={"exit_code": int(rc)}, summary={}, errors=[])


@register("duplicate_delivery.clean")
def clean_duplicate_delivery(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    keep_last = payload.get("keep_last")

    if keep_last is None:
        return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])

    base = LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_DUPLICATE_DELIVERY
    if not base.exists():
        return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])

    runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
    for p in runs[int(keep_last) :]:
        shutil.rmtree(p, ignore_errors=True)
    print(f"[labs clean {SCENARIO_DUPLICATE_DELIVERY}] kept_last={keep_last}")
    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])
