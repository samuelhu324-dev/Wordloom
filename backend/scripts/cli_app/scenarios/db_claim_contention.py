from __future__ import annotations

import json
import time
from pathlib import Path

from ..common import build_evidence_paths_for_dir, pack_artifacts, write_json
from ..registry import register
from ..types import DrillInputs, DrillResult
from ._failure_drill_shared import (
    LAB_ID_S3A_2A_3A,
    SEARCH_OUTBOX_OBS_SCHEMA_VERSION,
    default_labs_auto_run_dir,
    ensure_dir,
    extract_last_claim_batch_id,
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
    write_json(outdir / "_recipe.json", recipe)

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

    run_label = run_id or outdir.name
    run_log_path = logs_dir / f"run-{run_label}.log"
    run_log_path.write_text(
        f"scenario={SCENARIO_DB_CLAIM_CONTENTION}\n"
        f"run_id={run_id}\n"
        f"outdir={outdir}\n"
        f"at={time.strftime('%Y-%m-%d %H:%M:%S')}\n",
        encoding="utf-8",
    )

    for p in (before_1_path, before_2_path, after_1_path, after_2_path):
        try:
            if not p.exists():
                p.write_text("pending\n", encoding="utf-8")
        except Exception:
            pass

    start = time.time()
    stopped_by_controller = False
    outbox_event_ids: list[str] = []

    worker_env_keys = [
        "WORDLOOM_TRACING_ENABLED",
        "OTEL_SERVICE_NAME",
        "OTEL_EXPORTER_OTLP_PROTOCOL",
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        "OTEL_TRACES_SAMPLER",
        "ELASTIC_URL",
        "ELASTIC_INDEX",
        "LOG_LEVEL",
        "OUTBOX_EXPERIMENT_ES_429_RATIO",
        "OUTBOX_USE_ES_BULK",
        "OUTBOX_EXPERIMENT_BREAK_CLAIM",
        "OUTBOX_EXPERIMENT_BREAK_CLAIM_SLEEP_SECONDS",
        "OUTBOX_EXPERIMENT_PROCESS_SLEEP_SECONDS",
        "OUTBOX_POLL_INTERVAL_SECONDS",
        "OUTBOX_BULK_SIZE",
        "OUTBOX_CONCURRENCY",
        "OUTBOX_WORKER_ID",
        "OUTBOX_METRICS_PORT",
        "OUTBOX_HTTP_PORT",
    ]

    worker1_handle = None
    worker2_handle = None

    try:
        worker1_handle = spawn_search_outbox_worker(
            env=env1,
            logs_dir=logs_dir,
            run_id=run_id,
            log_name=log_path_1.name,
            evidence_env_keys=[k for k in worker_env_keys if k in env1],
        )
        worker2_handle = spawn_search_outbox_worker(
            env=env2,
            logs_dir=logs_dir,
            run_id=run_id,
            log_name=log_path_2.name,
            evidence_env_keys=[k for k in worker_env_keys if k in env2],
        )
        write_json(
            outdir / "_worker_start.json",
            {
                "worker1": worker1_handle.evidence_summary(),
                "worker2": worker2_handle.evidence_summary(),
            },
        )

        readiness_sleep_v1(scrape_delay)
        before_1_path.write_text(
            scrape_metrics_text_readiness_v1(port=int(metrics_port_1), timeout_s=4.0),
            encoding="utf-8",
        )
        before_2_path.write_text(
            scrape_metrics_text_readiness_v1(port=int(metrics_port_2), timeout_s=4.0),
            encoding="utf-8",
        )

        supply_res = run_search_outbox_supply_inserter_v1(
            outdir=outdir,
            env=base_env,
            op=str(op),
            insert_count=int(trigger_count),
            create_search_index_row=True,
            event_version=0,
            timeout_s=30.0,
            file_prefix="_trigger_insert_outbox",
        )
        if supply_res.returncode is None:
            print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] inserter timed out")
            if worker1_handle is not None:
                worker1_handle.terminate_and_wait(timeout_s=30)
            if worker2_handle is not None:
                worker2_handle.terminate_and_wait(timeout_s=30)
            return DrillResult(ok=False, meta={"exit_code": 5}, summary={}, errors=[])

        if supply_res.returncode != 0:
            print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] failed to insert outbox events: rc={supply_res.returncode}")
            if worker1_handle is not None:
                worker1_handle.terminate_and_wait(timeout_s=30)
            if worker2_handle is not None:
                worker2_handle.terminate_and_wait(timeout_s=30)
            return DrillResult(ok=False, meta={"exit_code": 3}, summary={}, errors=[])

        outbox_event_ids = list(supply_res.outbox_event_ids)
        (outdir / "_outbox_event_ids.txt").write_text("\n".join(outbox_event_ids) + "\n", encoding="utf-8")
        print(f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] outbox_event_ids: {', '.join(outbox_event_ids)}")

        supply_evidence = dict(supply_res.evidence or {})
        supply_evidence["outbox_event_ids"] = list(outbox_event_ids)
        supply_evidence["insert_count"] = int(
            supply_evidence.get("insert_count") or len(outbox_event_ids) or int(trigger_count)
        )
        write_json(outdir / "_supply.json", supply_evidence)

        while True:
            if duration > 0 and (time.time() - start) >= duration:
                try:
                    after_1_path.write_text(
                        scrape_metrics_text(port=int(metrics_port_1), timeout_s=4.0),
                        encoding="utf-8",
                    )
                except Exception as exc:  # noqa: BLE001
                    after_1_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                try:
                    after_2_path.write_text(
                        scrape_metrics_text(port=int(metrics_port_2), timeout_s=4.0),
                        encoding="utf-8",
                    )
                except Exception as exc:  # noqa: BLE001
                    after_2_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                stopped_by_controller = True
                if worker1_handle is not None:
                    worker1_handle.terminate_and_wait(timeout_s=30)
                if worker2_handle is not None:
                    worker2_handle.terminate_and_wait(timeout_s=30)
                break

            ret1 = worker1_handle.proc.poll() if worker1_handle is not None else 0
            ret2 = worker2_handle.proc.poll() if worker2_handle is not None else 0
            if ret1 is not None or ret2 is not None:
                try:
                    after_1_path.write_text(
                        scrape_metrics_text(port=int(metrics_port_1), timeout_s=4.0),
                        encoding="utf-8",
                    )
                except Exception as exc:  # noqa: BLE001
                    after_1_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                try:
                    after_2_path.write_text(
                        scrape_metrics_text(port=int(metrics_port_2), timeout_s=4.0),
                        encoding="utf-8",
                    )
                except Exception as exc:  # noqa: BLE001
                    after_2_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")
                break
            time.sleep(0.25)
    except KeyboardInterrupt:
        stopped_by_controller = True
        try:
            run_log_path.write_text(
                run_log_path.read_text(encoding="utf-8", errors="replace")
                + "keyboard_interrupt\n",
                encoding="utf-8",
            )
        except Exception:
            pass
        if worker1_handle is not None:
            worker1_handle.terminate_and_wait(timeout_s=30)
        if worker2_handle is not None:
            worker2_handle.terminate_and_wait(timeout_s=30)
    except Exception as exc:  # noqa: BLE001
        try:
            run_log_path.write_text(
                run_log_path.read_text(encoding="utf-8", errors="replace")
                + f"exception: {type(exc).__name__}: {exc}\n",
                encoding="utf-8",
            )
        except Exception:
            pass
        if worker1_handle is not None:
            worker1_handle.terminate_and_wait(timeout_s=30)
        if worker2_handle is not None:
            worker2_handle.terminate_and_wait(timeout_s=30)
        write_json(outdir / "_worker_exit.json", {"error": f"{type(exc).__name__}: {exc}"})
        return DrillResult(ok=False, meta={"exit_code": 6}, summary={}, errors=[])
    finally:
        if worker1_handle is not None:
            if worker1_handle.proc.poll() is None:
                worker1_handle.terminate_and_wait(timeout_s=30)
            else:
                worker1_handle.wait(timeout_s=30)

        if worker2_handle is not None:
            if worker2_handle.proc.poll() is None:
                worker2_handle.terminate_and_wait(timeout_s=30)
            else:
                worker2_handle.wait(timeout_s=30)

    exit_info = {
        "worker1": {
            "returncode": int(worker1_handle.proc.returncode)
            if (worker1_handle is not None and worker1_handle.proc.returncode is not None)
            else None
        },
        "worker2": {
            "returncode": int(worker2_handle.proc.returncode)
            if (worker2_handle is not None and worker2_handle.proc.returncode is not None)
            else None
        },
    }
    write_json(outdir / "_worker_exit.json", exit_info)

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

    if (not stopped_by_controller) and (
        worker1_handle.proc.returncode not in (None, 0) or worker2_handle.proc.returncode not in (None, 0)
    ):
        print(
            f"[labs run {SCENARIO_DB_CLAIM_CONTENTION}] a worker exited early: rc1={worker1_handle.proc.returncode} rc2={worker2_handle.proc.returncode}"
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

    worker_start_path = run_dir / "_worker_start.json"
    worker_start = None
    if worker_start_path.exists():
        try:
            worker_start = json.loads(worker_start_path.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            worker_start = None

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

    supply = read_json_file(run_dir / "_supply.json")
    supply_db_check: dict[str, object] = {"skipped": True, "reason": "missing_supply"}
    supply_db_ok = True
    try:
        if isinstance(supply, dict) and supply.get("outbox_event_ids"):
            env = load_env_from_run_recipe_v1(run_dir=run_dir)
            database_url = (env.get("DATABASE_URL") or "").strip()
            if database_url:
                supply_db_check = verify_supply_rows_v1(database_url=database_url, supply=supply)
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
        (delta_mismatch >= min_owner_mismatch_delta)
        and (delta_processed >= min_processed_delta)
        and (delta_failed <= max_failed_delta)
        and bool(supply_db_ok)
    )

    result = {
        "scenario": SCENARIO_DB_CLAIM_CONTENTION,
        "run_dir": str(run_dir),
        "workers": worker_start,
        "checks": {
            "owner_mismatch_delta_ge": float(min_owner_mismatch_delta),
            "processed_delta_ge": float(min_processed_delta),
            "failed_delta_le": float(max_failed_delta),
        },
        "observed": {
            metric_owner_mismatch: {"before": mismatch_before, "after": mismatch_after, "delta": delta_mismatch},
            metric_processed: {"before": processed_before, "after": processed_after, "delta": delta_processed},
            metric_failed: {"before": failed_before, "after": failed_after, "delta": delta_failed},
            "supply": supply,
            "supply_db_check": supply_db_check,
        },
        "ok": bool(ok),
    }
    pack_artifacts(paths=build_evidence_paths_for_dir(run_dir), result=result)

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
