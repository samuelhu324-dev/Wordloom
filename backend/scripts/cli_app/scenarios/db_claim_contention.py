from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

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


SCENARIO_DB_CLAIM_CONTENTION = "db_claim_contention"


@register("db_claim_contention.run")
def run_db_claim_contention(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_id = str(payload.get("run_id") or "").strip()
    outdir_str = str(payload.get("outdir") or "").strip()
    outdir = Path(outdir_str) if outdir_str else default_labs_auto_run_dir(scenario=SCENARIO_DB_CLAIM_CONTENTION, run_id=run_id)

    env_file = payload.get("env_file")
    service = payload.get("service")
    duration = int(payload.get("duration") or 0)

    metrics_port_1 = int(payload.get("metrics_port_1") or 0)
    metrics_port_2 = int(payload.get("metrics_port_2") or 0)
    scrape_delay = float(payload.get("scrape_delay") or 0.0)

    op = payload.get("op")
    trigger_count = int(payload.get("trigger_count") or 0)

    break_claim_sleep = float(payload.get("break_claim_sleep") or 0.0)
    poll_interval = float(payload.get("poll_interval") or 0.0)
    batch_size = int(payload.get("batch_size") or 0)

    worker_id_1 = payload.get("worker_id_1")
    worker_id_2 = payload.get("worker_id_2")

    logs_dir = outdir / "_logs"
    metrics_dir = outdir / "_metrics"
    exports_dir = outdir / "_exports"
    ensure_dir(logs_dir)
    ensure_dir(metrics_dir)
    ensure_dir(exports_dir)

    base_env = with_backend_pythonpath(load_env(env_file=str(env_file) if env_file else None))

    service_name = service
    base_env.setdefault("WORDLOOM_TRACING_ENABLED", "1")
    base_env.setdefault("OTEL_SERVICE_NAME", service_name)
    base_env.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
    base_env.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    base_env.setdefault("OTEL_TRACES_SAMPLER", "always_on")

    base_env.setdefault("ELASTIC_URL", "http://localhost:19200")
    base_env.setdefault("ELASTIC_INDEX", "wordloom-test-search-index")

    base_env["LOG_LEVEL"] = "INFO"

    base_env["OUTBOX_EXPERIMENT_ES_429_RATIO"] = "0"
    base_env.pop("OUTBOX_EXPERIMENT_ES_429_EVERY_N", None)
    base_env.pop("OUTBOX_EXPERIMENT_ES_BULK_PARTIAL", None)

    base_env["OUTBOX_USE_ES_BULK"] = "0"

    base_env["OUTBOX_EXPERIMENT_BREAK_CLAIM"] = "1"
    base_env["OUTBOX_EXPERIMENT_BREAK_CLAIM_SLEEP_SECONDS"] = str(float(break_claim_sleep))

    base_env["OUTBOX_EXPERIMENT_PROCESS_SLEEP_SECONDS"] = str(max(1.0, float(break_claim_sleep)))

    base_env["OUTBOX_POLL_INTERVAL_SECONDS"] = str(float(poll_interval))
    base_env["OUTBOX_BULK_SIZE"] = str(int(batch_size))
    base_env["OUTBOX_CONCURRENCY"] = "1"

    recipe = {
        "lab_id": LAB_ID_S3A_2A_3A,
        "scenario": SCENARIO_DB_CLAIM_CONTENTION,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": env_file,
        "service": service_name,
        "inject": {
            "kind": "break_claim_atomicity",
            "enabled": True,
            "sleep_seconds": float(break_claim_sleep),
        },
        "worker": {
            "duration_s": int(duration),
            "metrics_ports": [int(metrics_port_1), int(metrics_port_2)],
            "poll_interval_seconds": float(poll_interval),
            "batch_size": int(batch_size),
        },
        "trigger": {"op": str(op), "count": int(trigger_count)},
    }
    (outdir / "_recipe.json").write_text(json.dumps(recipe, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    worker = LEGACY_SCRIPTS_DIR / "search_outbox_worker.py"
    cmd = [python_exe(), "-u", str(worker)]

    env1 = base_env.copy()
    env1["OUTBOX_WORKER_ID"] = str(worker_id_1)
    env1["OUTBOX_METRICS_PORT"] = str(int(metrics_port_1))
    env1["OUTBOX_HTTP_PORT"] = str(int(metrics_port_1) + 20)

    env2 = base_env.copy()
    env2["OUTBOX_WORKER_ID"] = str(worker_id_2)
    env2["OUTBOX_METRICS_PORT"] = str(int(metrics_port_2))
    env2["OUTBOX_HTTP_PORT"] = str(int(metrics_port_2) + 20)

    log_path_1 = logs_dir / f"worker1-{run_id}.log"
    log_path_2 = logs_dir / f"worker2-{run_id}.log"

    print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] outdir: {outdir}")
    print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] worker1 log: {log_path_1} (metrics :{metrics_port_1})")
    print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] worker2 log: {log_path_2} (metrics :{metrics_port_2})")

    before_1_path = metrics_dir / "metrics-before-1.txt"
    before_2_path = metrics_dir / "metrics-before-2.txt"
    after_1_path = metrics_dir / "metrics-after-1.txt"
    after_2_path = metrics_dir / "metrics-after-2.txt"

    inserter = REPO_ROOT / "backend" / "scripts" / "labs" / "labs_009_insert_search_outbox_pending.py"
    if not inserter.exists():
        inserter = LEGACY_SCRIPTS_DIR / "labs_009_insert_search_outbox_pending.py"

    start = time.time()
    stopped_by_controller = False
    outbox_event_ids: list[str] = []

    with open(log_path_1, "w", encoding="utf-8") as log_file_1, open(log_path_2, "w", encoding="utf-8") as log_file_2:
        proc1 = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env1, stdout=log_file_1, stderr=subprocess.STDOUT)
        proc2 = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env2, stdout=log_file_2, stderr=subprocess.STDOUT)
        try:
            time.sleep(max(0.5, float(scrape_delay)))
            try:
                before_1_path.write_text(scrape_metrics_text(port=int(metrics_port_1), timeout_s=4.0), encoding="utf-8")
            except Exception as exc:  # noqa: BLE001
                before_1_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
            try:
                before_2_path.write_text(scrape_metrics_text(port=int(metrics_port_2), timeout_s=4.0), encoding="utf-8")
            except Exception as exc:  # noqa: BLE001
                before_2_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

            for i in range(int(trigger_count)):
                trigger_env = base_env.copy()
                trigger_env["OUTBOX_OP"] = str(op)
                trigger_env.setdefault("OUTBOX_CREATE_SEARCH_INDEX_ROW", "1")
                trigger_env.setdefault("OUTBOX_EVENT_VERSION", "0")

                proc = subprocess.run(
                    [python_exe(), str(inserter)],
                    cwd=str(REPO_ROOT),
                    env=trigger_env,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
                (outdir / f"_trigger_insert_outbox_{i+1}.stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
                (outdir / f"_trigger_insert_outbox_{i+1}.stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
                if proc.returncode != 0:
                    print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] failed to insert outbox event #{i+1}: rc={proc.returncode}")
                    proc1.terminate()
                    proc2.terminate()
                    proc1.wait(timeout=30)
                    proc2.wait(timeout=30)
                    return DrillResult(ok=False, meta={"exit_code": 3}, summary={}, errors=[])
                outbox_event_id = (proc.stdout or "").strip().splitlines()[-1].strip()
                outbox_event_ids.append(outbox_event_id)

            (outdir / "_outbox_event_ids.txt").write_text("\n".join(outbox_event_ids) + "\n", encoding="utf-8")
            print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] outbox_event_ids: {', '.join(outbox_event_ids)}")

            while True:
                if duration > 0 and (time.time() - start) >= duration:
                    try:
                        after_1_path.write_text(scrape_metrics_text(port=int(metrics_port_1), timeout_s=4.0), encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        after_1_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    try:
                        after_2_path.write_text(scrape_metrics_text(port=int(metrics_port_2), timeout_s=4.0), encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        after_2_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    stopped_by_controller = True
                    proc1.terminate()
                    proc2.terminate()
                    break

                ret1 = proc1.poll()
                ret2 = proc2.poll()
                if ret1 is not None or ret2 is not None:
                    try:
                        after_1_path.write_text(scrape_metrics_text(port=int(metrics_port_1), timeout_s=4.0), encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        after_1_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    try:
                        after_2_path.write_text(scrape_metrics_text(port=int(metrics_port_2), timeout_s=4.0), encoding="utf-8")
                    except Exception as exc:  # noqa: BLE001
                        after_2_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                    break
                time.sleep(0.25)
        except KeyboardInterrupt:
            stopped_by_controller = True
            proc1.terminate()
            proc2.terminate()

        proc1.wait(timeout=30)
        proc2.wait(timeout=30)

    exit_info = {
        "worker1": {"returncode": int(proc1.returncode) if proc1.returncode is not None else None},
        "worker2": {"returncode": int(proc2.returncode) if proc2.returncode is not None else None},
    }
    (outdir / "_worker_exit.json").write_text(json.dumps(exit_info, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    combined = (
        "# metrics-after-1\n\n"
        + (after_1_path.read_text(encoding="utf-8", errors="replace") if after_1_path.exists() else "")
        + "\n\n# metrics-after-2\n\n"
        + (after_2_path.read_text(encoding="utf-8", errors="replace") if after_2_path.exists() else "")
    )
    (outdir / "_metrics.txt").write_text(combined, encoding="utf-8")

    claim_batch_ids: list[str] = []
    for lp in (log_path_1, log_path_2):
        cid = extract_last_claim_batch_id(lp)
        if cid:
            claim_batch_ids.append(cid)
    if claim_batch_ids:
        (outdir / "_claim_batch_ids.txt").write_text("\n".join(claim_batch_ids) + "\n", encoding="utf-8")

    if (not stopped_by_controller) and (proc1.returncode not in (None, 0) or proc2.returncode not in (None, 0)):
        print(
            f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] a worker exited early: rc1={proc1.returncode} rc2={proc2.returncode}"
        )
        print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] see logs: {log_path_1} {log_path_2}")
        return DrillResult(ok=False, meta={"exit_code": 4}, summary={}, errors=[])

    print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] done (now run verify/export/clean)")
    print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] outputs: {outdir}")
    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])


@register("db_claim_contention.verify")
def verify_db_claim_contention(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_dir = resolve_run_dir(
        run_id=str(payload.get("run_id") or "").strip() or None,
        outdir=str(payload.get("outdir") or "").strip() or None,
        scenario=SCENARIO_DB_CLAIM_CONTENTION,
    )
    metrics_dir = run_dir / "_metrics"

    before1 = (metrics_dir / "metrics-before-1.txt").read_text(encoding="utf-8") if (metrics_dir / "metrics-before-1.txt").exists() else ""
    before2 = (metrics_dir / "metrics-before-2.txt").read_text(encoding="utf-8") if (metrics_dir / "metrics-before-2.txt").exists() else ""
    after1 = (metrics_dir / "metrics-after-1.txt").read_text(encoding="utf-8") if (metrics_dir / "metrics-after-1.txt").exists() else ""
    after2 = (metrics_dir / "metrics-after-2.txt").read_text(encoding="utf-8") if (metrics_dir / "metrics-after-2.txt").exists() else ""

    metric_owner_mismatch = "outbox_owner_mismatch_skips_total"
    metric_processed = "outbox_processed_total"
    metric_failed = "outbox_failed_total"

    mismatch_before = prom_parse_counter_sum(before1, metric_owner_mismatch) + prom_parse_counter_sum(before2, metric_owner_mismatch)
    mismatch_after = prom_parse_counter_sum(after1, metric_owner_mismatch) + prom_parse_counter_sum(after2, metric_owner_mismatch)

    processed_before = prom_parse_counter_sum(before1, metric_processed) + prom_parse_counter_sum(before2, metric_processed)
    processed_after = prom_parse_counter_sum(after1, metric_processed) + prom_parse_counter_sum(after2, metric_processed)

    failed_before = prom_parse_counter_sum(before1, metric_failed) + prom_parse_counter_sum(before2, metric_failed)
    failed_after = prom_parse_counter_sum(after1, metric_failed) + prom_parse_counter_sum(after2, metric_failed)

    delta_mismatch = mismatch_after - mismatch_before
    delta_processed = processed_after - processed_before
    delta_failed = failed_after - failed_before

    min_owner_mismatch_delta = float(payload.get("min_owner_mismatch_delta") or 0)
    min_processed_delta = float(payload.get("min_processed_delta") or 0)
    max_failed_delta = float(payload.get("max_failed_delta") or 0)

    ok = (delta_mismatch >= min_owner_mismatch_delta) and (delta_processed >= min_processed_delta) and (delta_failed <= max_failed_delta)

    result = {
        "scenario": SCENARIO_DB_CLAIM_CONTENTION,
        "run_dir": str(run_dir),
        "checks": {
            "owner_mismatch_delta_ge": float(min_owner_mismatch_delta),
            "processed_delta_ge": float(min_processed_delta),
            "failed_delta_le": float(max_failed_delta),
        },
        "observed": {
            metric_owner_mismatch: {"before": mismatch_before, "after": mismatch_after, "delta": delta_mismatch},
            metric_processed: {"before": processed_before, "after": processed_after, "delta": delta_processed},
            metric_failed: {"before": failed_before, "after": failed_after, "delta": delta_failed},
        },
        "ok": bool(ok),
    }
    (run_dir / "_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if ok:
        print(f"[labs verify {SCENARIO_DB_CLAIM_CONTENTION}] OK")
        return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])

    print(f"[labs verify {SCENARIO_DB_CLAIM_CONTENTION}] FAILED")
    return DrillResult(ok=False, meta={"exit_code": 10}, summary={}, errors=[])


@register("db_claim_contention.export")
def export_db_claim_contention(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_dir = resolve_run_dir(
        run_id=str(payload.get("run_id") or "").strip() or None,
        outdir=str(payload.get("outdir") or "").strip() or None,
        scenario=SCENARIO_DB_CLAIM_CONTENTION,
    )
    exports_dir = run_dir / "_exports"
    ensure_dir(exports_dir)

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

    rc = run_cmd(
        base_cmd
        + [
            "--operation",
            "outbox.claim_batch",
            "--tags-json",
            json.dumps({"wordloom.obs_schema": SEARCH_OUTBOX_OBS_SCHEMA_VERSION}, ensure_ascii=False),
        ],
        cwd=REPO_ROOT,
    )

    return DrillResult(ok=(rc == 0), meta={"exit_code": int(rc)}, summary={}, errors=[])


@register("db_claim_contention.clean")
def clean_db_claim_contention(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    outdir = payload.get("outdir")
    keep_last = payload.get("keep_last")

    if outdir:
        out_path = Path(str(outdir))
        ensure_dir(out_path)
        (out_path / "_clean.txt").write_text(
            f"scenario={SCENARIO_DB_CLAIM_CONTENTION}\n" "action=noop\n" f"at={time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            encoding="utf-8",
        )

    if keep_last is not None:
        base = LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_DB_CLAIM_CONTENTION
        if base.exists():
            import shutil

            runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
            for p in runs[int(keep_last) :]:
                shutil.rmtree(p, ignore_errors=True)
            print(f"[labs clean {SCENARIO_DB_CLAIM_CONTENTION}] kept_last={keep_last}")
    else:
        print(f"[labs clean {SCENARIO_DB_CLAIM_CONTENTION}] noop")

    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])
