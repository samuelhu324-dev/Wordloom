from __future__ import annotations

import json
import subprocess
import shutil
import time
from pathlib import Path

from sqlalchemy import create_engine, text

from ..common import build_evidence_paths_for_dir, pack_artifacts, write_json
from ..registry import register
from ..types import DrillInputs, DrillResult
from ._failure_drill_shared import (
    LAB_ID_S3A_2A_3A,
    LEGACY_SCRIPTS_DIR,
    REPO_ROOT,
    SpawnedWorker,
    default_labs_auto_run_dir,
    docker_compose,
    ensure_dir,
    load_env,
    prom_parse_counter_sum,
    python_exe,
    read_json_file,
    resolve_run_dir,
    scrape_metrics_text,
    scrape_metrics_text_readiness_v1,
    readiness_sleep_v1,
    spawn_search_outbox_worker,
    with_backend_pythonpath,
)

SCENARIO_COLLECTOR_DOWN = "collector_down"

def _write_timeout_evidence(
    *,
    outdir: Path,
    stem: str,
    cmd: list[str],
    timeout_s: float,
) -> None:
    (outdir / f"{stem}.timeout.txt").write_text(
        f"timeout_s={float(timeout_s)}\ncmd={' '.join(cmd)}\n",
        encoding="utf-8",
    )


@register("collector_down.run")
def run_collector_down(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_id = str(payload.get("run_id") or "").strip()
    outdir_str = str(payload.get("outdir") or "").strip()
    outdir = Path(outdir_str) if outdir_str else default_labs_auto_run_dir(scenario=SCENARIO_COLLECTOR_DOWN, run_id=run_id)
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

    env["OUTBOX_METRICS_PORT"] = str(int(metrics_port))

    compose_file = str((REPO_ROOT / "docker-compose.infra.yml").resolve())
    recipe = {
        "lab_id": LAB_ID_S3A_2A_3A,
        "scenario": SCENARIO_COLLECTOR_DOWN,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": env_file,
        "service": service_name,
        "inject": {"kind": "collector_down", "compose": {"file": compose_file, "service": "jaeger", "action": "stop"}},
        "worker": {"duration_s": int(duration), "metrics_port": int(metrics_port)},
        "trigger": {"op": str(op)},
    }
    write_json(outdir / "_recipe.json", recipe)

    print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] outdir: {outdir}")

    stop_proc = docker_compose(args=["-f", compose_file, "stop", "jaeger"], cwd=REPO_ROOT)
    (outdir / "_inject_jaeger_stop.stdout.txt").write_text(stop_proc.stdout or "", encoding="utf-8")
    (outdir / "_inject_jaeger_stop.stderr.txt").write_text(stop_proc.stderr or "", encoding="utf-8")
    (outdir / "_inject_jaeger_stop.exitcode.txt").write_text(str(int(stop_proc.returncode)) + "\n", encoding="utf-8")
    if stop_proc.returncode != 0:
        print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] failed to stop jaeger: rc={stop_proc.returncode}")
        return DrillResult(ok=False, meta={"exit_code": 2}, summary={}, errors=[])

    worker_handle = spawn_search_outbox_worker(
        env=env,
        logs_dir=logs_dir,
        run_id=run_id,
        evidence_env_keys=[
            k
            for k in (
                "OUTBOX_METRICS_PORT",
                "OUTBOX_HTTP_PORT",
                "OUTBOX_LEASE_SECONDS",
                "OUTBOX_RECLAIM_INTERVAL_SECONDS",
                "OUTBOX_MAX_PROCESSING_SECONDS",
                "OUTBOX_POLL_INTERVAL_SECONDS",
                "OUTBOX_BULK_SIZE",
                "OUTBOX_CONCURRENCY",
            )
            if k in env
        ],
    )
    write_json(outdir / "_worker_start.json", worker_handle.evidence_summary())
    print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] worker log: {worker_handle.log_path}")

    metrics_before_path = metrics_dir / "metrics-before.txt"
    metrics_after_path = metrics_dir / "metrics-after.txt"

    inserter = REPO_ROOT / "backend" / "scripts" / "labs" / "labs_009_insert_search_outbox_pending.py"
    if not inserter.exists():
        inserter = LEGACY_SCRIPTS_DIR / "labs_009_insert_search_outbox_pending.py"

    start = time.time()
    stopped_by_controller = False
    try:
        readiness_sleep_v1(scrape_delay)
        metrics_before_path.write_text(
            scrape_metrics_text_readiness_v1(port=int(metrics_port), timeout_s=4.0),
            encoding="utf-8",
        )

        trigger_env = env.copy()
        trigger_env["OUTBOX_OP"] = str(op)
        trigger_env.setdefault("OUTBOX_CREATE_SEARCH_INDEX_ROW", "1")
        trigger_env.setdefault("OUTBOX_EVENT_VERSION", "0")

        insert_cmd = [python_exe(), str(inserter)]
        try:
            proc = subprocess.run(
                insert_cmd,
                cwd=str(REPO_ROOT),
                env=trigger_env,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
        except subprocess.TimeoutExpired:
            (outdir / "_trigger_insert_outbox.stdout.txt").write_text("", encoding="utf-8")
            (outdir / "_trigger_insert_outbox.stderr.txt").write_text("", encoding="utf-8")
            _write_timeout_evidence(outdir=outdir, stem="_trigger_insert_outbox", cmd=insert_cmd, timeout_s=30)
            worker_handle.terminate_and_wait(timeout_s=30)
            return DrillResult(ok=False, meta={"exit_code": 5}, summary={}, errors=[])

        (outdir / "_trigger_insert_outbox.stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
        (outdir / "_trigger_insert_outbox.stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
        if proc.returncode != 0:
            print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] failed to insert outbox event: rc={proc.returncode}")
            worker_handle.terminate_and_wait(timeout_s=30)
            return DrillResult(ok=False, meta={"exit_code": 3}, summary={}, errors=[])

        outbox_event_id = (proc.stdout or "").strip().splitlines()[-1].strip()
        (outdir / "_outbox_event_id.txt").write_text(outbox_event_id + "\n", encoding="utf-8")
        print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] outbox_event_id: {outbox_event_id}")

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
        try:
            worker_handle.wait(timeout_s=30)
        except Exception:
            pass

    exit_info = {"returncode": int(worker_handle.proc.returncode) if worker_handle.proc.returncode is not None else None}
    write_json(outdir / "_worker_exit.json", exit_info)

    if not metrics_after_path.exists():
        metrics_after_path.write_text("scrape_failed: missing_metrics_after\n", encoding="utf-8")

    if (not stopped_by_controller) and (worker_handle.proc.returncode not in (None, 0)):
        print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] worker exited early: rc={worker_handle.proc.returncode}")
        print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] see logs: {worker_handle.log_path}")
        return DrillResult(ok=False, meta={"exit_code": 4}, summary={}, errors=[])

    print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] done (now run verify/export/clean)")
    print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] outputs: {outdir}")
    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])


@register("collector_down.verify")
def verify_collector_down(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_id = (str(payload.get("run_id") or "").strip() or None)
    outdir = payload.get("outdir")
    min_processed_delta = float(payload.get("min_processed_delta") or 0.0)
    max_failed_delta = float(payload.get("max_failed_delta") or 0.0)

    run_dir = resolve_run_dir(run_id=run_id, outdir=str(outdir) if outdir else None, scenario=SCENARIO_COLLECTOR_DOWN)
    metrics_dir = run_dir / "_metrics"

    before_path = metrics_dir / "metrics-before.txt"
    after_path = metrics_dir / "metrics-after.txt"

    before = before_path.read_text(encoding="utf-8") if before_path.exists() else ""
    after = after_path.read_text(encoding="utf-8") if after_path.exists() else ""

    before_scrape_ok = "scrape_failed" not in before
    after_scrape_ok = "scrape_failed" not in after

    processed_before = prom_parse_counter_sum(before, "outbox_processed_total")
    processed_after = prom_parse_counter_sum(after, "outbox_processed_total")
    failed_before = prom_parse_counter_sum(before, "outbox_failed_total")
    failed_after = prom_parse_counter_sum(after, "outbox_failed_total")

    delta_processed = processed_after - processed_before
    delta_failed = failed_after - failed_before

    outbox_event_id_path = run_dir / "_outbox_event_id.txt"
    outbox_event_id = outbox_event_id_path.read_text(encoding="utf-8").strip() if outbox_event_id_path.exists() else None

    db_observed: dict[str, object] = {}
    db_ok = False
    try:
        recipe = read_json_file(run_dir / "_recipe.json") or {}
        recipe_env_file = (recipe or {}).get("env_file")

        env = load_env(env_file=str(recipe_env_file) if recipe_env_file else None)
        database_url = (env.get("DATABASE_URL") or "").strip()
        if database_url and outbox_event_id:
            engine = create_engine(database_url, pool_pre_ping=True)
            with engine.connect() as conn:
                # Support both legacy search_outbox_events and unified outbox_events.
                exists = lambda name: bool(
                    conn.execute(
                        text(
                            """
                            SELECT 1
                            FROM information_schema.tables
                            WHERE table_schema = 'public' AND table_name = :name
                            LIMIT 1
                            """
                        ),
                        {"name": name},
                    ).fetchone()
                )

                if exists("outbox_events"):
                    row = conn.execute(
                        text(
                            """
                            SELECT status, processed_at, attempts, error_reason
                            FROM outbox_events
                            WHERE id = CAST(:id AS uuid)
                            """
                        ),
                        {"id": outbox_event_id},
                    ).mappings().fetchone()
                else:
                    row = conn.execute(
                        text(
                            """
                            SELECT status, processed_at, attempts, error_reason
                            FROM search_outbox_events
                            WHERE id = CAST(:id AS uuid)
                            """
                        ),
                        {"id": outbox_event_id},
                    ).mappings().fetchone()

            if row is None:
                db_observed = {"found": False}
            else:
                status = row.get("status")
                processed_at = row.get("processed_at")
                attempts = row.get("attempts")
                error_reason = row.get("error_reason")
                db_observed = {
                    "found": True,
                    "status": status,
                    "processed_at": str(processed_at) if processed_at is not None else None,
                    "attempts": int(attempts) if attempts is not None else None,
                    "error_reason": error_reason,
                }
                db_ok = (status == "done") and (processed_at is not None)
    except Exception as exc:  # noqa: BLE001
        db_observed = {"error": f"{type(exc).__name__}: {exc}"}
        db_ok = False

    inject_exitcode_path = run_dir / "_inject_jaeger_stop.exitcode.txt"
    inject_exitcode = None
    if inject_exitcode_path.exists():
        try:
            inject_exitcode = int((inject_exitcode_path.read_text(encoding="utf-8", errors="replace") or "").strip() or "0")
        except Exception:
            inject_exitcode = None

    metrics_ok = (
        before_scrape_ok
        and after_scrape_ok
        and (delta_processed >= float(min_processed_delta))
        and (delta_failed <= float(max_failed_delta))
    )

    ok = (inject_exitcode == 0) and (metrics_ok or db_ok)

    result = {
        "scenario": SCENARIO_COLLECTOR_DOWN,
        "run_dir": str(run_dir),
        "outbox_event_id": outbox_event_id,
        "checks": {
            "inject_jaeger_stop_exitcode_eq": 0,
            "min_processed_delta": float(min_processed_delta),
            "max_failed_delta": float(max_failed_delta),
            "metrics_scrape_required": True,
            "db_outbox_processed_fallback_allowed": True,
        },
        "observed": {
            "inject_jaeger_stop_exitcode": inject_exitcode,
            "metrics_before_scrape_ok": bool(before_scrape_ok),
            "metrics_after_scrape_ok": bool(after_scrape_ok),
            "outbox_processed_total": {"before": processed_before, "after": processed_after, "delta": delta_processed},
            "outbox_failed_total": {"before": failed_before, "after": failed_after, "delta": delta_failed},
            "db_outbox_event": db_observed,
            "worker": read_json_file(run_dir / "_worker_start.json"),
        },
        "ok": bool(ok),
    }
    pack_artifacts(paths=build_evidence_paths_for_dir(run_dir), result=result)

    if ok:
        print(f"[labs verify {SCENARIO_COLLECTOR_DOWN}] OK")
        return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])

    why = []
    if inject_exitcode != 0:
        why.append(f"inject_exitcode={inject_exitcode}")
    if not metrics_ok:
        why.append(
            f"metrics_ok=false (before_ok={before_scrape_ok} after_ok={after_scrape_ok} delta_processed={delta_processed} delta_failed={delta_failed})"
        )
    if not db_ok:
        why.append("db_ok=false")
    print(f"[labs verify {SCENARIO_COLLECTOR_DOWN}] FAILED: {'; '.join(why) if why else 'unknown'}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return DrillResult(ok=False, meta={"exit_code": 10}, summary={}, errors=[])


@register("collector_down.export")
def export_collector_down(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_id = (str(payload.get("run_id") or "").strip() or None)
    outdir = payload.get("outdir")
    service = payload.get("service")
    lookback = payload.get("lookback")
    limit = payload.get("limit")

    run_dir = resolve_run_dir(run_id=run_id, outdir=str(outdir) if outdir else None, scenario=SCENARIO_COLLECTOR_DOWN)
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
        str(service),
        "--lookback",
        str(lookback),
        "--limit",
        str(limit),
    ]
    if outbox_event_id:
        cmd += ["--outbox-event-id", outbox_event_id]

    print("[scripts] run:", " ".join(cmd))
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True, check=False)
    (run_dir / "_export_jaeger.stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (run_dir / "_export_jaeger.stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (run_dir / "_export_jaeger.exitcode.txt").write_text(str(int(proc.returncode)) + "\n", encoding="utf-8")

    if proc.returncode != 0:
        (run_dir / "_export_note.txt").write_text(
            "collector_down: Jaeger is intentionally stopped; trace export failure is expected.\n",
            encoding="utf-8",
        )

    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])


@register("collector_down.clean")
def clean_collector_down(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    outdir = payload.get("outdir")
    keep_last = payload.get("keep_last")

    compose_file = str((REPO_ROOT / "docker-compose.infra.yml").resolve())
    start_proc = docker_compose(args=["-f", compose_file, "start", "jaeger"], cwd=REPO_ROOT)
    print(f"[labs clean {SCENARIO_COLLECTOR_DOWN}] start jaeger: rc={start_proc.returncode}")

    if outdir:
        outdir_path = Path(str(outdir))
        ensure_dir(outdir_path)
        (outdir_path / "_clean.txt").write_text(
            f"scenario={SCENARIO_COLLECTOR_DOWN}\n" "action=start_jaeger\n" f"at={time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            encoding="utf-8",
        )
        (outdir_path / "_clean_jaeger_start.stdout.txt").write_text(start_proc.stdout or "", encoding="utf-8")
        (outdir_path / "_clean_jaeger_start.stderr.txt").write_text(start_proc.stderr or "", encoding="utf-8")
        (outdir_path / "_clean_jaeger_start.exitcode.txt").write_text(str(int(start_proc.returncode)) + "\n", encoding="utf-8")

    if keep_last is not None:
        base = REPO_ROOT / "docs" / "labs" / "_snapshot" / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_COLLECTOR_DOWN
        if base.exists():
            runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
            for p in runs[int(keep_last) :]:
                shutil.rmtree(p, ignore_errors=True)
            print(f"[labs clean {SCENARIO_COLLECTOR_DOWN}] kept_last={keep_last}")

    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])
