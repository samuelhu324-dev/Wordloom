from __future__ import annotations

import json
import time
from pathlib import Path

from ..common import build_evidence_paths_for_dir, pack_artifacts, write_json
from ..registry import register
from ..types import DrillInputs, DrillResult
from ._failure_drill_shared import (
    LAB_ID_S3A_2A_3A,
    default_labs_auto_run_dir,
    ensure_dir,
    eval_db_reason_contract_v1,
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
    python_exe,
    with_backend_pythonpath,
    verify_supply_rows_v1,
)
from ._failure_drill_shared import LEGACY_SCRIPTS_DIR, LABS_SNAPSHOT_ROOT, REPO_ROOT


SCENARIO_ES_429_INJECT = "es_429_inject"


@register("es_429_inject.run")
def run_es_429_inject(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_id = str(payload.get("run_id") or "").strip()
    outdir_str = str(payload.get("outdir") or "").strip()
    outdir = Path(outdir_str) if outdir_str else default_labs_auto_run_dir(scenario=SCENARIO_ES_429_INJECT, run_id=run_id)

    env_file = payload.get("env_file")
    service = payload.get("service")
    duration = int(payload.get("duration") or 0)
    metrics_port = int(payload.get("metrics_port") or 0)
    scrape_delay = float(payload.get("scrape_delay") or 0.0)
    op = payload.get("op")

    every_n = payload.get("every_n")
    ratio = payload.get("ratio")
    ops = payload.get("ops")
    seed = payload.get("seed")

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

    if every_n is not None and int(every_n) > 0:
        env["OUTBOX_EXPERIMENT_ES_429_EVERY_N"] = str(int(every_n))
        env.pop("OUTBOX_EXPERIMENT_ES_429_RATIO", None)
    else:
        env["OUTBOX_EXPERIMENT_ES_429_RATIO"] = str(float(ratio))
        env.pop("OUTBOX_EXPERIMENT_ES_429_EVERY_N", None)

    env["OUTBOX_EXPERIMENT_ES_429_OPS"] = str(ops)
    if seed is not None:
        env["OUTBOX_EXPERIMENT_ES_429_SEED"] = str(int(seed))
    else:
        env.pop("OUTBOX_EXPERIMENT_ES_429_SEED", None)

    env["OUTBOX_METRICS_PORT"] = str(int(metrics_port))

    recipe = {
        "lab_id": LAB_ID_S3A_2A_3A,
        "scenario": SCENARIO_ES_429_INJECT,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": env_file,
        "service": service_name,
        "inject": {
            "kind": "es_429",
            "mode": "every_n" if (every_n is not None and int(every_n) > 0) else "ratio",
            "every_n": int(every_n) if (every_n is not None) else None,
            "ratio": float(ratio),
            "ops": str(ops),
            "seed": int(seed) if seed is not None else None,
        },
        "worker": {"duration_s": int(duration), "metrics_port": int(metrics_port)},
        "trigger": {"op": str(op)},
    }
    write_json(outdir / "_recipe.json", recipe)

    log_path = logs_dir / f"worker-{run_id}.log"

    print(f"[labs run {SCENARIO_ES_429_INJECT}] outdir: {outdir}")
    print(f"[labs run {SCENARIO_ES_429_INJECT}] worker log: {log_path}")

    metrics_before_path = metrics_dir / "metrics-before.txt"
    metrics_after_path = metrics_dir / "metrics-after.txt"

    start = time.time()
    stopped_by_controller = False
    worker_env_keys = [
        "WORDLOOM_TRACING_ENABLED",
        "OTEL_SERVICE_NAME",
        "OTEL_EXPORTER_OTLP_PROTOCOL",
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        "OTEL_TRACES_SAMPLER",
        "OUTBOX_EXPERIMENT_ES_429_EVERY_N",
        "OUTBOX_EXPERIMENT_ES_429_RATIO",
        "OUTBOX_EXPERIMENT_ES_429_OPS",
        "OUTBOX_EXPERIMENT_ES_429_SEED",
        "OUTBOX_METRICS_PORT",
    ]

    worker_handle = spawn_search_outbox_worker(
        env=env,
        logs_dir=logs_dir,
        run_id=run_id,
        log_name=f"worker-{run_id}.log",
        evidence_env_keys=[k for k in worker_env_keys if k in env],
    )
    write_json(outdir / "_worker_start.json", worker_handle.evidence_summary())
    try:
            readiness_sleep_v1(scrape_delay)
            metrics_before_path.write_text(
                scrape_metrics_text_readiness_v1(port=int(metrics_port), timeout_s=4.0),
                encoding="utf-8",
            )

            supply_res = run_search_outbox_supply_inserter_v1(
                outdir=outdir,
                env=env,
                op=str(op),
                insert_count=1,
                create_search_index_row=True,
                event_version=0,
                timeout_s=30.0,
                file_prefix="_trigger_insert_outbox",
            )
            if supply_res.returncode is None:
                print(f"[labs run {SCENARIO_ES_429_INJECT}] inserter timed out")
                worker_handle.terminate_and_wait(timeout_s=30)
                exit_info = {
                    "returncode": int(worker_handle.proc.returncode)
                    if worker_handle.proc.returncode is not None
                    else None
                }
                write_json(outdir / "_worker_exit.json", exit_info)
                return DrillResult(ok=False, meta={"exit_code": 5}, summary={}, errors=[])
            if supply_res.returncode != 0:
                print(
                    f"[labs run {SCENARIO_ES_429_INJECT}] failed to insert outbox event: rc={supply_res.returncode}"
                )
                worker_handle.terminate_and_wait(timeout_s=30)
                return DrillResult(ok=False, meta={"exit_code": 3}, summary={}, errors=[])

            outbox_event_id = supply_res.outbox_event_ids[-1].strip() if supply_res.outbox_event_ids else ""
            (outdir / "_outbox_event_id.txt").write_text(outbox_event_id + "\n", encoding="utf-8")
            print(f"[labs run {SCENARIO_ES_429_INJECT}] outbox_event_id: {outbox_event_id}")

            supply_evidence = dict(supply_res.evidence or {})
            supply_evidence["outbox_event_id"] = outbox_event_id
            supply_evidence["outbox_event_ids"] = list(supply_res.outbox_event_ids)
            supply_evidence["insert_count"] = int(supply_evidence.get("insert_count") or 1)
            write_json(outdir / "_supply.json", supply_evidence)

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
        print(f"[labs run {SCENARIO_ES_429_INJECT}] worker exited early: rc={worker_handle.proc.returncode}")
        print(f"[labs run {SCENARIO_ES_429_INJECT}] see logs: {log_path}")
        return DrillResult(ok=False, meta={"exit_code": 4}, summary={}, errors=[])

    print(f"[labs run {SCENARIO_ES_429_INJECT}] done (now run verify/export/clean)")
    print(f"[labs run {SCENARIO_ES_429_INJECT}] outputs: {outdir}")
    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])


@register("es_429_inject.verify")
def verify_es_429_inject(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_dir = resolve_run_dir(
        run_id=str(payload.get("run_id") or "").strip() or None,
        outdir=str(payload.get("outdir") or "").strip() or None,
        scenario=SCENARIO_ES_429_INJECT,
    )
    metrics_dir = run_dir / "_metrics"
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

    retry_before = prom_parse_counter_sum(before, "outbox_retry_scheduled_total", labels={"reason": "es_429"})
    retry_after = prom_parse_counter_sum(after, "outbox_retry_scheduled_total", labels={"reason": "es_429"})
    failed_before = prom_parse_counter_sum(before, "outbox_failed_total", labels={"reason": "es_429"})
    failed_after = prom_parse_counter_sum(after, "outbox_failed_total", labels={"reason": "es_429"})
    terminal_before = prom_parse_counter_sum(before, "outbox_terminal_failed_total", labels={"reason": "es_429"})
    terminal_after = prom_parse_counter_sum(after, "outbox_terminal_failed_total", labels={"reason": "es_429"})

    delta_retry = retry_after - retry_before
    delta_failed = failed_after - failed_before
    delta_terminal = terminal_after - terminal_before

    min_retry_delta = float(payload.get("min_retry_delta") or 0)
    min_failed_delta = float(payload.get("min_failed_delta") or 0)
    max_terminal_delta = float(payload.get("max_terminal_delta") or 0)

    ok = (delta_retry >= min_retry_delta) and (delta_failed >= min_failed_delta) and (delta_terminal <= max_terminal_delta)

    supply = read_json_file(run_dir / "_supply.json")
    supply_db_check = None
    db_reason_check = None
    db_reason_values: list[str] = []
    db_reason_families: list[str] = []
    if supply is not None:
        env = load_env_from_run_recipe_v1(run_dir=run_dir)
        db_url = str(env.get("DATABASE_URL") or "").strip()
        if db_url:
            supply_db_check = verify_supply_rows_v1(database_url=db_url, supply=supply)
            if not bool(supply_db_check.get("skipped")):
                ok = bool(ok) and bool(supply_db_check.get("ok"))

            contract_ok, db_reason_check, db_reason_values, db_reason_families = eval_db_reason_contract_v1(
                database_url=db_url,
                supply=supply,
                expected_reason_families=["rate_limit"],
                expected_db_reasons=["es_429"],
                require_db_reasons=True,
            )
            if contract_ok is not None:
                ok = bool(ok) and bool(contract_ok)

    result = {
        "scenario": SCENARIO_ES_429_INJECT,
        "run_dir": str(run_dir),
        "worker": worker_start,
        "supply": supply,
        "supply_db_check": supply_db_check,
        "reason_contract": {
            "expected": {
                "metrics_reasons": ["es_429"],
                "reason_families": ["rate_limit"],
            },
            "observed": {
                "db_reasons": db_reason_values,
                "db_reason_families": db_reason_families,
            },
            "db_reason_check": db_reason_check,
        },
        "checks": {
            "retry_delta_ge": float(min_retry_delta),
            "failed_delta_ge": float(min_failed_delta),
            "terminal_delta_le": float(max_terminal_delta),
        },
        "observed": {
            "outbox_retry_scheduled_total_reason_es_429": {"before": retry_before, "after": retry_after, "delta": delta_retry},
            "outbox_failed_total_reason_es_429": {"before": failed_before, "after": failed_after, "delta": delta_failed},
            "outbox_terminal_failed_total_reason_es_429": {"before": terminal_before, "after": terminal_after, "delta": delta_terminal},
        },
        "ok": bool(ok),
    }
    pack_artifacts(paths=build_evidence_paths_for_dir(run_dir), result=result)

    if ok:
        print(f"[labs verify {SCENARIO_ES_429_INJECT}] OK")
        return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])

    print(f"[labs verify {SCENARIO_ES_429_INJECT}] FAILED")
    return DrillResult(ok=False, meta={"exit_code": 10}, summary={}, errors=[])


@register("es_429_inject.export")
def export_es_429_inject(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_dir = resolve_run_dir(
        run_id=str(payload.get("run_id") or "").strip() or None,
        outdir=str(payload.get("outdir") or "").strip() or None,
        scenario=SCENARIO_ES_429_INJECT,
    )
    exports_dir = run_dir / "_exports"
    ensure_dir(exports_dir)

    outbox_event_id_path = run_dir / "_outbox_event_id.txt"
    outbox_event_id = outbox_event_id_path.read_text(encoding="utf-8").strip() if outbox_event_id_path.exists() else None

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
    ]
    if outbox_event_id:
        cmd += ["--outbox-event-id", outbox_event_id]

    rc = run_cmd(cmd, cwd=REPO_ROOT)
    return DrillResult(ok=(rc == 0), meta={"exit_code": int(rc)}, summary={}, errors=[])


@register("es_429_inject.clean")
def clean_es_429_inject(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    outdir = payload.get("outdir")
    keep_last = payload.get("keep_last")

    if outdir:
        out_path = Path(str(outdir))
        ensure_dir(out_path)
        (out_path / "_clean.txt").write_text(
            f"scenario={SCENARIO_ES_429_INJECT}\n" "action=noop\n" f"at={time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            encoding="utf-8",
        )

    if keep_last is not None:
        base = LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_ES_429_INJECT
        if base.exists():
            import shutil

            runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
            for p in runs[int(keep_last) :]:
                shutil.rmtree(p, ignore_errors=True)
            print(f"[labs clean {SCENARIO_ES_429_INJECT}] kept_last={keep_last}")
    else:
        print(f"[labs clean {SCENARIO_ES_429_INJECT}] noop")

    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])
