from __future__ import annotations

import json
import re
import shutil
import subprocess
import time
import uuid
from pathlib import Path

from ..common import build_evidence_paths_for_dir, pack_artifacts
from ..registry import register
from ..types import DrillInputs, DrillResult
from ._failure_drill_shared import (
    LAB_ID_S3A_2A_3A,
    SEARCH_OUTBOX_OBS_SCHEMA_VERSION,
    default_labs_auto_run_dir,
    ensure_dir,
    load_env,
    prom_parse_counter_sum,
    python_exe,
    resolve_run_dir,
    run_cmd,
    scrape_metrics_text,
    with_backend_pythonpath,
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
    (outdir / "_recipe.json").write_text(json.dumps(recipe, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    worker = LEGACY_SCRIPTS_DIR / "search_outbox_worker.py"
    log_path = logs_dir / f"worker-{run_id}.log"
    cmd = [python_exe(), "-u", str(worker)]

    print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] outdir: {outdir}")
    print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] worker log: {log_path}")
    print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] entity_id: {entity_id}")

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

            upsert_env = env.copy()
            upsert_env["OUTBOX_ENTITY_TYPE"] = str(entity_type)
            upsert_env["OUTBOX_ENTITY_ID"] = entity_id
            upsert_env["OUTBOX_OP"] = "upsert"
            upsert_env["OUTBOX_CREATE_SEARCH_INDEX_ROW"] = "1"
            upsert_env.setdefault("OUTBOX_EVENT_VERSION", "0")

            proc = subprocess.run(
                [python_exe(), str(inserter)],
                cwd=str(REPO_ROOT),
                env=upsert_env,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            (outdir / "_trigger_upsert.stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
            (outdir / "_trigger_upsert.stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
            if proc.returncode != 0:
                print(
                    f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] failed to insert upsert outbox event: rc={proc.returncode}"
                )
                worker_proc.terminate()
                worker_proc.wait(timeout=30)
                return DrillResult(ok=False, meta={"exit_code": 3}, summary={}, errors=[])

            upsert_event_id = (proc.stdout or "").strip().splitlines()[-1].strip()
            outbox_event_ids.append(upsert_event_id)
            time.sleep(1.5)

            delete_env = env.copy()
            delete_env["OUTBOX_ENTITY_TYPE"] = str(entity_type)
            delete_env["OUTBOX_ENTITY_ID"] = entity_id
            delete_env["OUTBOX_OP"] = "delete"
            delete_env.setdefault("OUTBOX_EVENT_VERSION", "0")
            delete_env["OUTBOX_CREATE_SEARCH_INDEX_ROW"] = "0"

            for idx in range(max(1, int(delete_count))):
                proc2 = subprocess.run(
                    [python_exe(), str(inserter)],
                    cwd=str(REPO_ROOT),
                    env=delete_env,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
                (outdir / f"_trigger_delete_{idx+1}.stdout.txt").write_text(proc2.stdout or "", encoding="utf-8")
                (outdir / f"_trigger_delete_{idx+1}.stderr.txt").write_text(proc2.stderr or "", encoding="utf-8")
                if proc2.returncode != 0:
                    print(
                        f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] failed to insert delete outbox event #{idx+1}: rc={proc2.returncode}"
                    )
                    worker_proc.terminate()
                    worker_proc.wait(timeout=30)
                    return DrillResult(ok=False, meta={"exit_code": 4}, summary={}, errors=[])
                delete_event_id = (proc2.stdout or "").strip().splitlines()[-1].strip()
                outbox_event_ids.append(delete_event_id)

            (outdir / "_outbox_event_ids.txt").write_text("\n".join(outbox_event_ids) + "\n", encoding="utf-8")

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
    (outdir / "_worker_exit.json").write_text(
        json.dumps(exit_info, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    if not metrics_after_path.exists():
        metrics_after_path.write_text("scrape_failed: missing_metrics_after\n", encoding="utf-8")

    if (not stopped_by_controller) and (worker_proc.returncode not in (None, 0)):
        print(f"[labs run {SCENARIO_DUPLICATE_DELIVERY}] worker exited early: rc={worker_proc.returncode}")
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

    ok = (
        (delta_processed >= min_processed_delta)
        and (delta_failed <= max_failed_delta)
        and ((delta_noop >= min_noop_delta) or (noop_log_count >= min_noop_logs))
    )

    result = {
        "scenario": SCENARIO_DUPLICATE_DELIVERY,
        "run_dir": str(run_dir),
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
