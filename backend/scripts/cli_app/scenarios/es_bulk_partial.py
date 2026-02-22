from __future__ import annotations

import json
import shutil
import subprocess
import time
from pathlib import Path

from ..common import build_evidence_paths_for_dir, pack_artifacts
from ..registry import register
from ..types import DrillInputs, DrillResult
from ._failure_drill_shared import (
    LAB_ID_S3A_2A_3A,
    SEARCH_OUTBOX_OBS_SCHEMA_VERSION,
    default_labs_auto_run_dir,
    ensure_dir,
    extract_last_claim_batch_id,
    load_env,
    prom_parse_counter_sum,
    python_exe,
    resolve_run_dir,
    run_cmd,
    scrape_metrics_text,
    with_backend_pythonpath,
)
from ._failure_drill_shared import LEGACY_SCRIPTS_DIR, LABS_SNAPSHOT_ROOT, REPO_ROOT


SCENARIO_ES_BULK_PARTIAL = "es_bulk_partial"


@register("es_bulk_partial.run")
def run_es_bulk_partial(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_id = str(payload.get("run_id") or "").strip()
    outdir_str = str(payload.get("outdir") or "").strip()
    outdir = Path(outdir_str) if outdir_str else default_labs_auto_run_dir(scenario=SCENARIO_ES_BULK_PARTIAL, run_id=run_id)

    env_file = payload.get("env_file")
    service = payload.get("service")
    duration = int(payload.get("duration") or 0)
    metrics_port = int(payload.get("metrics_port") or 0)
    scrape_delay = float(payload.get("scrape_delay") or 0.0)
    op = payload.get("op")
    trigger_count = int(payload.get("trigger_count") or 0)
    bulk_size = int(payload.get("bulk_size") or 0)
    partial_status = int(payload.get("partial_status") or 0)

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

    env["OUTBOX_USE_ES_BULK"] = "1"
    env["OUTBOX_BULK_SIZE"] = str(int(bulk_size))
    env["OUTBOX_EXPERIMENT_ES_BULK_PARTIAL"] = "1"
    env["OUTBOX_EXPERIMENT_ES_BULK_PARTIAL_STATUS"] = str(int(partial_status))

    env["OUTBOX_POLL_INTERVAL_SECONDS"] = "5.0"

    env.setdefault("ELASTIC_URL", "http://localhost:19200")
    env.setdefault("ELASTIC_INDEX", "wordloom-test-search-index")

    env["OUTBOX_EXPERIMENT_ES_429_RATIO"] = "0"
    env.pop("OUTBOX_EXPERIMENT_ES_429_EVERY_N", None)

    env["OUTBOX_METRICS_PORT"] = str(int(metrics_port))

    recipe = {
        "lab_id": LAB_ID_S3A_2A_3A,
        "scenario": SCENARIO_ES_BULK_PARTIAL,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": env_file,
        "service": service_name,
        "inject": {
            "kind": "es_bulk_partial",
            "enabled": True,
            "status": int(partial_status),
        },
        "worker": {
            "duration_s": int(duration),
            "metrics_port": int(metrics_port),
            "use_es_bulk": True,
            "bulk_size": int(bulk_size),
        },
        "trigger": {"op": str(op), "count": int(trigger_count)},
    }
    (outdir / "_recipe.json").write_text(json.dumps(recipe, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    worker = LEGACY_SCRIPTS_DIR / "search_outbox_worker.py"
    log_path = logs_dir / f"worker-{run_id}.log"
    cmd = [python_exe(), "-u", str(worker)]

    print(f"[labs run {SCENARIO_ES_BULK_PARTIAL}] outdir: {outdir}")
    print(f"[labs run {SCENARIO_ES_BULK_PARTIAL}] worker log: {log_path}")

    metrics_before_path = metrics_dir / "metrics-before.txt"
    metrics_after_path = metrics_dir / "metrics-after.txt"

    inserter = REPO_ROOT / "backend" / "scripts" / "labs" / "labs_009_insert_search_outbox_pending.py"
    if not inserter.exists():
        inserter = LEGACY_SCRIPTS_DIR / "labs_009_insert_search_outbox_pending.py"

    start = time.time()
    stopped_by_controller = False
    outbox_event_ids: list[str] = []

    with open(log_path, "w", encoding="utf-8") as log_file:
        worker_proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env, stdout=log_file, stderr=subprocess.STDOUT)
        try:
            time.sleep(max(0.5, float(scrape_delay)))
            try:
                metrics_before = scrape_metrics_text(port=int(metrics_port), timeout_s=4.0)
                metrics_before_path.write_text(metrics_before, encoding="utf-8")
            except Exception as exc:  # noqa: BLE001
                metrics_before_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

            trigger_env = env.copy()
            trigger_env["OUTBOX_OP"] = str(op)
            trigger_env.setdefault("OUTBOX_CREATE_SEARCH_INDEX_ROW", "1")
            trigger_env.setdefault("OUTBOX_EVENT_VERSION", "0")
            trigger_env["OUTBOX_INSERT_COUNT"] = str(int(trigger_count))

            proc = subprocess.run(
                [python_exe(), str(inserter)],
                cwd=str(REPO_ROOT),
                env=trigger_env,
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
            (outdir / "_trigger_insert_outbox.stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
            (outdir / "_trigger_insert_outbox.stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
            if proc.returncode != 0:
                print(f"[labs run {SCENARIO_ES_BULK_PARTIAL}] failed to insert outbox events: rc={proc.returncode}")
                return DrillResult(ok=False, meta={"exit_code": 3}, summary={}, errors=[])

            outbox_event_ids = [ln.strip() for ln in (proc.stdout or "").splitlines() if ln.strip()]
            (outdir / "_outbox_event_ids.txt").write_text("\n".join(outbox_event_ids) + "\n", encoding="utf-8")
            print(f"[labs run {SCENARIO_ES_BULK_PARTIAL}] outbox_event_ids: {', '.join(outbox_event_ids)}")

            while True:
                if duration > 0 and (time.time() - start) >= duration:
                    try:
                        metrics_after = scrape_metrics_text(port=int(metrics_port), timeout_s=4.0)
                        metrics_after_path.write_text(metrics_after, encoding="utf-8")
                        (outdir / "_metrics.txt").write_text(metrics_after, encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        metrics_after_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    stopped_by_controller = True
                    worker_proc.terminate()
                    break

                ret = worker_proc.poll()
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
            worker_proc.terminate()

        worker_proc.wait(timeout=30)

    exit_info = {"returncode": int(worker_proc.returncode) if worker_proc.returncode is not None else None}
    (outdir / "_worker_exit.json").write_text(json.dumps(exit_info, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if not metrics_after_path.exists():
        metrics_after_path.write_text("scrape_failed: missing_metrics_after\n", encoding="utf-8")

    claim_batch_id = extract_last_claim_batch_id(log_path)
    if claim_batch_id:
        (outdir / "_claim_batch_id.txt").write_text(claim_batch_id + "\n", encoding="utf-8")

    if (not stopped_by_controller) and (worker_proc.returncode not in (None, 0)):
        print(f"[labs run {SCENARIO_ES_BULK_PARTIAL}] worker exited early: rc={worker_proc.returncode}")
        print(f"[labs run {SCENARIO_ES_BULK_PARTIAL}] see logs: {log_path}")
        return DrillResult(ok=False, meta={"exit_code": 4}, summary={}, errors=[])

    print(f"[labs run {SCENARIO_ES_BULK_PARTIAL}] done (now run verify/export/clean)")
    print(f"[labs run {SCENARIO_ES_BULK_PARTIAL}] outputs: {outdir}")
    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])


@register("es_bulk_partial.verify")
def verify_es_bulk_partial(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_dir = resolve_run_dir(
        run_id=str(payload.get("run_id") or "").strip() or None,
        outdir=str(payload.get("outdir") or "").strip() or None,
        scenario=SCENARIO_ES_BULK_PARTIAL,
    )
    metrics_dir = run_dir / "_metrics"
    before_path = metrics_dir / "metrics-before.txt"
    after_path = metrics_dir / "metrics-after.txt"

    before = before_path.read_text(encoding="utf-8") if before_path.exists() else ""
    after = after_path.read_text(encoding="utf-8") if after_path.exists() else ""

    partial_before = prom_parse_counter_sum(before, "outbox_es_bulk_requests_total", labels={"result": "partial"})
    partial_after = prom_parse_counter_sum(after, "outbox_es_bulk_requests_total", labels={"result": "partial"})

    success_items_before = (
        prom_parse_counter_sum(before, "outbox_es_bulk_items_total", labels={"op": "index", "result": "success"})
        + prom_parse_counter_sum(before, "outbox_es_bulk_items_total", labels={"op": "delete", "result": "success"})
    )
    success_items_after = (
        prom_parse_counter_sum(after, "outbox_es_bulk_items_total", labels={"op": "index", "result": "success"})
        + prom_parse_counter_sum(after, "outbox_es_bulk_items_total", labels={"op": "delete", "result": "success"})
    )

    failed_items_before = (
        prom_parse_counter_sum(before, "outbox_es_bulk_items_total", labels={"op": "index", "result": "failed"})
        + prom_parse_counter_sum(before, "outbox_es_bulk_items_total", labels={"op": "delete", "result": "failed"})
    )
    failed_items_after = (
        prom_parse_counter_sum(after, "outbox_es_bulk_items_total", labels={"op": "index", "result": "failed"})
        + prom_parse_counter_sum(after, "outbox_es_bulk_items_total", labels={"op": "delete", "result": "failed"})
    )

    failed_4xx_before = (
        prom_parse_counter_sum(before, "outbox_es_bulk_item_failures_total", labels={"op": "index", "failure_class": "4xx"})
        + prom_parse_counter_sum(before, "outbox_es_bulk_item_failures_total", labels={"op": "delete", "failure_class": "4xx"})
    )
    failed_4xx_after = (
        prom_parse_counter_sum(after, "outbox_es_bulk_item_failures_total", labels={"op": "index", "failure_class": "4xx"})
        + prom_parse_counter_sum(after, "outbox_es_bulk_item_failures_total", labels={"op": "delete", "failure_class": "4xx"})
    )

    delta_partial = partial_after - partial_before
    delta_success_items = success_items_after - success_items_before
    delta_failed_items = failed_items_after - failed_items_before
    delta_failed_4xx = failed_4xx_after - failed_4xx_before

    min_partial_delta = float(payload.get("min_partial_delta") or 0)
    min_success_items_delta = float(payload.get("min_success_items_delta") or 0)
    min_failed_items_delta = float(payload.get("min_failed_items_delta") or 0)
    min_failed_4xx_delta = float(payload.get("min_failed_4xx_delta") or 0)

    ok = (
        (delta_partial >= min_partial_delta)
        and (delta_success_items >= min_success_items_delta)
        and (delta_failed_items >= min_failed_items_delta)
        and (delta_failed_4xx >= min_failed_4xx_delta)
    )

    result = {
        "scenario": SCENARIO_ES_BULK_PARTIAL,
        "run_dir": str(run_dir),
        "checks": {
            "partial_delta_ge": float(min_partial_delta),
            "success_items_delta_ge": float(min_success_items_delta),
            "failed_items_delta_ge": float(min_failed_items_delta),
            "failed_4xx_delta_ge": float(min_failed_4xx_delta),
        },
        "observed": {
            "outbox_es_bulk_requests_total_result_partial": {"before": partial_before, "after": partial_after, "delta": delta_partial},
            "outbox_es_bulk_items_total_success_sum": {"before": success_items_before, "after": success_items_after, "delta": delta_success_items},
            "outbox_es_bulk_items_total_failed_sum": {"before": failed_items_before, "after": failed_items_after, "delta": delta_failed_items},
            "outbox_es_bulk_item_failures_total_failure_class_4xx_sum": {"before": failed_4xx_before, "after": failed_4xx_after, "delta": delta_failed_4xx},
        },
        "ok": bool(ok),
    }
    pack_artifacts(paths=build_evidence_paths_for_dir(run_dir), result=result)

    if ok:
        print(f"[labs verify {SCENARIO_ES_BULK_PARTIAL}] OK")
        return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])

    print(f"[labs verify {SCENARIO_ES_BULK_PARTIAL}] FAILED")
    return DrillResult(ok=False, meta={"exit_code": 10}, summary={}, errors=[])


@register("es_bulk_partial.export")
def export_es_bulk_partial(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_dir = resolve_run_dir(
        run_id=str(payload.get("run_id") or "").strip() or None,
        outdir=str(payload.get("outdir") or "").strip() or None,
        scenario=SCENARIO_ES_BULK_PARTIAL,
    )
    exports_dir = run_dir / "_exports"
    ensure_dir(exports_dir)

    claim_batch_id_path = run_dir / "_claim_batch_id.txt"
    claim_batch_id = claim_batch_id_path.read_text(encoding="utf-8").strip() if claim_batch_id_path.exists() else None

    exporter = LEGACY_SCRIPTS_DIR / "labs_009_export_jaeger.py"
    base_cmd = [
        python_exe(),
        str(exporter),
        "--outdir",
        str(exports_dir),
        "--service",
        str(payload.get("service")),
        "--lookback",
        str(payload.get("lookback")),
        "--limit",
        str(payload.get("limit")),
    ]

    if claim_batch_id:
        rc = run_cmd(base_cmd + ["--claim-batch-id", claim_batch_id], cwd=REPO_ROOT)
        return DrillResult(ok=(rc == 0), meta={"exit_code": int(rc)}, summary={}, errors=[])

    rc = run_cmd(
        base_cmd
        + ["--tags-json", json.dumps({"wordloom.obs_schema": SEARCH_OUTBOX_OBS_SCHEMA_VERSION}, ensure_ascii=False)],
        cwd=REPO_ROOT,
    )
    return DrillResult(ok=(rc == 0), meta={"exit_code": int(rc)}, summary={}, errors=[])


@register("es_bulk_partial.clean")
def clean_es_bulk_partial(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    outdir = payload.get("outdir")
    keep_last = payload.get("keep_last")

    if outdir:
        out_path = Path(str(outdir))
        ensure_dir(out_path)
        (out_path / "_clean.txt").write_text(
            f"scenario={SCENARIO_ES_BULK_PARTIAL}\n" "action=noop\n" f"at={time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            encoding="utf-8",
        )

    if keep_last is not None:
        base = LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_ES_BULK_PARTIAL
        if base.exists():
            runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
            for p in runs[int(keep_last) :]:
                shutil.rmtree(p, ignore_errors=True)
            print(f"[labs clean {SCENARIO_ES_BULK_PARTIAL}] kept_last={keep_last}")
    else:
        print(f"[labs clean {SCENARIO_ES_BULK_PARTIAL}] noop")

    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])
