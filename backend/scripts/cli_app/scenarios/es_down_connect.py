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
    docker_compose,
    ensure_dir,
    load_env,
    load_env_from_run_recipe_v1,
    fetch_supply_error_reasons_v1,
    prom_sum_reasons,
    reason_family_v1,
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


SCENARIO_ES_DOWN_CONNECT = "es_down_connect"


@register("es_down_connect.run")
def run_es_down_connect(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_id = str(payload.get("run_id") or "").strip()
    outdir_str = str(payload.get("outdir") or "").strip()
    outdir = Path(outdir_str) if outdir_str else default_labs_auto_run_dir(scenario=SCENARIO_ES_DOWN_CONNECT, run_id=run_id)

    env_file = payload.get("env_file")
    service = payload.get("service")
    duration = int(payload.get("duration") or 0)
    metrics_port = int(payload.get("metrics_port") or 0)
    scrape_delay = float(payload.get("scrape_delay") or 0.0)
    op = payload.get("op")

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

    env["OUTBOX_EXPERIMENT_ES_429_RATIO"] = "0"
    env.pop("OUTBOX_EXPERIMENT_ES_429_EVERY_N", None)

    env["OUTBOX_METRICS_PORT"] = str(int(metrics_port))

    compose_file = str((REPO_ROOT / "docker-compose.infra.yml").resolve())
    recipe = {
        "lab_id": LAB_ID_S3A_2A_3A,
        "scenario": SCENARIO_ES_DOWN_CONNECT,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": env_file,
        "service": service_name,
        "inject": {"kind": "es_down", "compose": {"file": compose_file, "service": "es", "action": "stop"}},
        "worker": {"duration_s": int(duration), "metrics_port": int(metrics_port)},
        "trigger": {"op": str(op)},
    }
    write_json(outdir / "_recipe.json", recipe)

    print(f"[labs run {SCENARIO_ES_DOWN_CONNECT}] outdir: {outdir}")

    stop_proc = docker_compose(args=["-f", compose_file, "stop", "es"], cwd=REPO_ROOT)
    (outdir / "_inject_es_stop.stdout.txt").write_text(stop_proc.stdout or "", encoding="utf-8")
    (outdir / "_inject_es_stop.stderr.txt").write_text(stop_proc.stderr or "", encoding="utf-8")
    (outdir / "_inject_es_stop.exitcode.txt").write_text(str(int(stop_proc.returncode)) + "\n", encoding="utf-8")
    if stop_proc.returncode != 0:
        print(f"[labs run {SCENARIO_ES_DOWN_CONNECT}] failed to stop es: rc={stop_proc.returncode}")
        return DrillResult(ok=False, meta={"exit_code": 2}, summary={}, errors=[])

    log_path = logs_dir / f"worker-{run_id}.log"

    print(f"[labs run {SCENARIO_ES_DOWN_CONNECT}] worker log: {log_path}")

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
        "OUTBOX_EXPERIMENT_ES_429_RATIO",
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
            print(f"[labs run {SCENARIO_ES_DOWN_CONNECT}] inserter timed out")
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
                f"[labs run {SCENARIO_ES_DOWN_CONNECT}] failed to insert outbox event: rc={supply_res.returncode}"
            )
            worker_handle.terminate_and_wait(timeout_s=30)
            return DrillResult(ok=False, meta={"exit_code": 3}, summary={}, errors=[])

        outbox_event_id = supply_res.outbox_event_ids[-1].strip() if supply_res.outbox_event_ids else ""
        (outdir / "_outbox_event_id.txt").write_text(outbox_event_id + "\n", encoding="utf-8")
        print(f"[labs run {SCENARIO_ES_DOWN_CONNECT}] outbox_event_id: {outbox_event_id}")

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
        print(f"[labs run {SCENARIO_ES_DOWN_CONNECT}] worker exited early: rc={worker_handle.proc.returncode}")
        print(f"[labs run {SCENARIO_ES_DOWN_CONNECT}] see logs: {log_path}")
        return DrillResult(ok=False, meta={"exit_code": 4}, summary={}, errors=[])

    print(f"[labs run {SCENARIO_ES_DOWN_CONNECT}] done (now run verify/export/clean)")
    print(f"[labs run {SCENARIO_ES_DOWN_CONNECT}] outputs: {outdir}")
    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])


@register("es_down_connect.verify")
def verify_es_down_connect(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_dir = resolve_run_dir(
        run_id=str(payload.get("run_id") or "").strip() or None,
        outdir=str(payload.get("outdir") or "").strip() or None,
        scenario=SCENARIO_ES_DOWN_CONNECT,
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

    reasons = ["es_connect", "es_unreachable"]
    expected_reason_families = ["transport"]

    retry_before = prom_sum_reasons(before, "outbox_retry_scheduled_total", reasons=reasons)
    retry_after = prom_sum_reasons(after, "outbox_retry_scheduled_total", reasons=reasons)
    failed_before = prom_sum_reasons(before, "outbox_failed_total", reasons=reasons)
    failed_after = prom_sum_reasons(after, "outbox_failed_total", reasons=reasons)
    terminal_before = prom_sum_reasons(before, "outbox_terminal_failed_total", reasons=reasons)
    terminal_after = prom_sum_reasons(after, "outbox_terminal_failed_total", reasons=reasons)

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

            db_reason_check = fetch_supply_error_reasons_v1(database_url=db_url, supply=supply)
            if not bool(db_reason_check.get("skipped")):
                ok = bool(ok) and bool(db_reason_check.get("ok"))

                rows = db_reason_check.get("rows")
                if isinstance(rows, list):
                    for row in rows:
                        if not isinstance(row, dict):
                            continue
                        raw = row.get("error_reason")
                        if raw:
                            val = str(raw).strip()
                            if val:
                                db_reason_values.append(val)

                db_reason_values = sorted(set(db_reason_values))
                fams = [reason_family_v1(r) for r in db_reason_values]
                db_reason_families = sorted({f for f in fams if f})

                # Hard contract: DB reasons must be present and in expected families.
                ok = bool(ok) and bool(db_reason_values)
                ok = bool(ok) and all((f in expected_reason_families) for f in db_reason_families)

    result = {
        "scenario": SCENARIO_ES_DOWN_CONNECT,
        "run_dir": str(run_dir),
        "worker": worker_start,
        "supply": supply,
        "supply_db_check": supply_db_check,
        "reason_contract": {
            "expected": {
                "metrics_reasons": reasons,
                "reason_families": expected_reason_families,
            },
            "observed": {
                "db_reasons": db_reason_values,
                "db_reason_families": db_reason_families,
            },
            "db_reason_check": db_reason_check,
        },
        "checks": {
            "reasons": reasons,
            "expected_reason_families": expected_reason_families,
            "retry_delta_ge": float(min_retry_delta),
            "failed_delta_ge": float(min_failed_delta),
            "terminal_delta_le": float(max_terminal_delta),
        },
        "observed": {
            "outbox_retry_scheduled_total_reason_es_connect_or_unreachable": {"before": retry_before, "after": retry_after, "delta": delta_retry},
            "outbox_failed_total_reason_es_connect_or_unreachable": {"before": failed_before, "after": failed_after, "delta": delta_failed},
            "outbox_terminal_failed_total_reason_es_connect_or_unreachable": {"before": terminal_before, "after": terminal_after, "delta": delta_terminal},
        },
        "ok": bool(ok),
    }
    pack_artifacts(paths=build_evidence_paths_for_dir(run_dir), result=result)

    if ok:
        print(f"[labs verify {SCENARIO_ES_DOWN_CONNECT}] OK")
        return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])

    print(f"[labs verify {SCENARIO_ES_DOWN_CONNECT}] FAILED")
    return DrillResult(ok=False, meta={"exit_code": 10}, summary={}, errors=[])


@register("es_down_connect.export")
def export_es_down_connect(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_dir = resolve_run_dir(
        run_id=str(payload.get("run_id") or "").strip() or None,
        outdir=str(payload.get("outdir") or "").strip() or None,
        scenario=SCENARIO_ES_DOWN_CONNECT,
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


@register("es_down_connect.clean")
def clean_es_down_connect(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    outdir = payload.get("outdir")
    keep_last = payload.get("keep_last")

    compose_file = str((REPO_ROOT / "docker-compose.infra.yml").resolve())
    start_proc = docker_compose(args=["-f", compose_file, "start", "es"], cwd=REPO_ROOT)
    print(f"[labs clean {SCENARIO_ES_DOWN_CONNECT}] start es: rc={start_proc.returncode}")

    if outdir:
        out_path = Path(str(outdir))
        ensure_dir(out_path)
        (out_path / "_clean.txt").write_text(
            f"scenario={SCENARIO_ES_DOWN_CONNECT}\n" "action=start_es\n" f"at={time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            encoding="utf-8",
        )
        (out_path / "_clean_es_start.stdout.txt").write_text(start_proc.stdout or "", encoding="utf-8")
        (out_path / "_clean_es_start.stderr.txt").write_text(start_proc.stderr or "", encoding="utf-8")
        (out_path / "_clean_es_start.exitcode.txt").write_text(str(int(start_proc.returncode)) + "\n", encoding="utf-8")

    if keep_last is not None:
        base = LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_ES_DOWN_CONNECT
        if base.exists():
            import shutil

            runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
            for p in runs[int(keep_last) :]:
                shutil.rmtree(p, ignore_errors=True)
            print(f"[labs clean {SCENARIO_ES_DOWN_CONNECT}] kept_last={keep_last}")

    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])
