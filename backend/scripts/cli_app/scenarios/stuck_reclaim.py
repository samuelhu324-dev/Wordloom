from __future__ import annotations

import json
import re
import shutil
import subprocess
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
    prom_parse_counter_sum,
    python_exe,
    resolve_run_dir,
    run_cmd,
    scrape_metrics_text,
    with_backend_pythonpath,
)
from ._failure_drill_shared import LEGACY_SCRIPTS_DIR, LABS_SNAPSHOT_ROOT, REPO_ROOT


SCENARIO_STUCK_RECLAIM = "stuck_reclaim"


@register("stuck_reclaim.run")
def run_stuck_reclaim(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_id = str(payload.get("run_id") or "").strip()
    outdir_str = str(payload.get("outdir") or "").strip()
    outdir = Path(outdir_str) if outdir_str else default_labs_auto_run_dir(scenario=SCENARIO_STUCK_RECLAIM, run_id=run_id)

    env_file = payload.get("env_file")
    service = payload.get("service")

    duration = int(payload.get("duration") or 0)
    scrape_delay = float(payload.get("scrape_delay") or 0.0)

    metrics_port_1 = int(payload.get("metrics_port_1") or 0)
    metrics_port_2 = int(payload.get("metrics_port_2") or 0)

    lease_seconds = int(payload.get("lease_seconds") or 0)
    reclaim_interval = float(payload.get("reclaim_interval") or 0.0)
    max_processing_seconds = int(payload.get("max_processing_seconds") or 0)
    poll_interval = float(payload.get("poll_interval") or 0.0)
    batch_size = int(payload.get("batch_size") or 0)

    op = payload.get("op")
    trigger_count = int(payload.get("trigger_count") or 0)

    worker_id_1 = payload.get("worker_id_1")
    worker_id_2 = payload.get("worker_id_2")

    claim_timeout = float(payload.get("claim_timeout") or 0.0)

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
    base_env.pop("OUTBOX_EXPERIMENT_BREAK_CLAIM", None)
    base_env.pop("OUTBOX_EXPERIMENT_BREAK_CLAIM_SLEEP_SECONDS", None)

    base_env["OUTBOX_USE_ES_BULK"] = "0"

    base_env["OUTBOX_LEASE_SECONDS"] = str(int(lease_seconds))
    base_env["OUTBOX_RECLAIM_INTERVAL_SECONDS"] = str(float(reclaim_interval))
    base_env["OUTBOX_MAX_PROCESSING_SECONDS"] = str(int(max_processing_seconds))
    base_env["OUTBOX_POLL_INTERVAL_SECONDS"] = str(float(poll_interval))
    base_env["OUTBOX_BULK_SIZE"] = str(int(batch_size))
    base_env["OUTBOX_CONCURRENCY"] = "1"

    recipe = {
        "lab_id": LAB_ID_S3A_2A_3A,
        "scenario": SCENARIO_STUCK_RECLAIM,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": env_file,
        "service": service_name,
        "worker": {
            "duration_s": int(duration),
            "metrics_ports": [int(metrics_port_1), int(metrics_port_2)],
            "lease_seconds": int(lease_seconds),
            "reclaim_interval_seconds": float(reclaim_interval),
            "max_processing_seconds": int(max_processing_seconds),
            "poll_interval_seconds": float(poll_interval),
            "batch_size": int(batch_size),
        },
        "trigger": {"op": str(op), "count": int(trigger_count)},
        "crash": {"kind": "process_kill", "target": "worker1", "claim_timeout_s": float(claim_timeout)},
    }
    write_json(outdir / "_recipe.json", recipe)

    worker = LEGACY_SCRIPTS_DIR / "search_outbox_worker.py"
    cmd = [python_exe(), "-u", str(worker)]

    inserter = REPO_ROOT / "backend" / "scripts" / "labs" / "labs_009_insert_search_outbox_pending.py"
    if not inserter.exists():
        inserter = LEGACY_SCRIPTS_DIR / "labs_009_insert_search_outbox_pending.py"

    outbox_event_ids: list[str] = []
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
            print(f"[labs run {SCENARIO_STUCK_RECLAIM}] failed to insert outbox event #{i+1}: rc={proc.returncode}")
            return DrillResult(ok=False, meta={"exit_code": 3}, summary={}, errors=[])
        outbox_event_id = (proc.stdout or "").strip().splitlines()[-1].strip()
        outbox_event_ids.append(outbox_event_id)

    (outdir / "_outbox_event_ids.txt").write_text("\n".join(outbox_event_ids) + "\n", encoding="utf-8")
    print(f"[labs run {SCENARIO_STUCK_RECLAIM}] outbox_event_ids: {', '.join(outbox_event_ids)}")

    def _spawn_worker_with_retry(
        *,
        worker_id: str,
        preferred_metrics_port: int,
        log_path: Path,
        max_attempts: int = 4,
        extra_env: dict[str, str] | None = None,
    ) -> tuple[subprocess.Popen, dict[str, str], int, int]:
        candidate_ports: list[int] = []
        for i in range(max_attempts):
            p = int(preferred_metrics_port) + (i * 10_000)
            if 1024 <= p <= 65_000:
                candidate_ports.append(p)
        if not candidate_ports:
            candidate_ports = [19128, 29128, 39128, 49128]

        last_proc: subprocess.Popen | None = None
        last_env: dict[str, str] | None = None
        last_metrics_port = int(preferred_metrics_port)
        last_http_port = int(preferred_metrics_port) + 20

        for attempt, metrics_port in enumerate(candidate_ports, start=1):
            http_port = int(metrics_port) + 20
            env = base_env.copy()
            env["OUTBOX_WORKER_ID"] = str(worker_id)
            env["OUTBOX_METRICS_PORT"] = str(int(metrics_port))
            env["OUTBOX_HTTP_PORT"] = str(int(http_port))
            if extra_env:
                env.update({str(k): str(v) for k, v in extra_env.items()})

            header = (
                f"\n\n# controller: spawn attempt {attempt}/{len(candidate_ports)} "
                f"metrics_port={metrics_port} http_port={http_port}\n"
            )
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(log_path, "a", encoding="utf-8") as log_file:
                log_file.write(header)
                log_file.flush()
                proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env, stdout=log_file, stderr=subprocess.STDOUT)

                time.sleep(0.75)

                if proc.poll() is None:
                    return proc, env, int(metrics_port), int(http_port)

            try:
                tail = log_path.read_text(encoding="utf-8", errors="replace")[-4000:]
            except Exception:
                tail = ""
            if "WinError 10013" in tail or "PermissionError" in tail:
                last_proc = proc
                last_env = env
                last_metrics_port = int(metrics_port)
                last_http_port = int(http_port)
                continue
            return proc, env, int(metrics_port), int(http_port)

        assert last_proc is not None
        assert last_env is not None
        return last_proc, last_env, int(last_metrics_port), int(last_http_port)

    log_path_1 = logs_dir / f"worker1-{run_id}.log"
    log_path_2 = logs_dir / f"worker2-{run_id}.log"

    before_1_path = metrics_dir / "metrics-before-1.txt"
    before_2_path = metrics_dir / "metrics-before-2.txt"
    after_1_path = metrics_dir / "metrics-after-1.txt"
    after_2_path = metrics_dir / "metrics-after-2.txt"

    print(f"[labs run {SCENARIO_STUCK_RECLAIM}] outdir: {outdir}")
    print(f"[labs run {SCENARIO_STUCK_RECLAIM}] worker1 log: {log_path_1} (metrics :{metrics_port_1})")
    print(f"[labs run {SCENARIO_STUCK_RECLAIM}] worker2 log: {log_path_2} (metrics :{metrics_port_2})")

    killed_worker1 = False
    observed_claim = False
    worker2_exited_early = False
    worker2_terminated_by_controller = False

    rx_claimed = re.compile(r'"event"\s*:\s*"outbox\\.claim_batch".*?"claimed"\s*:\s*([1-9][0-9]*)')

    log_path_1.write_text("", encoding="utf-8")
    log_path_2.write_text("", encoding="utf-8")

    worker1_sleep_after_claim_s = max(3.0, float(int(lease_seconds)) + 1.0)

    proc1, env1, actual_metrics_port_1, actual_http_port_1 = _spawn_worker_with_retry(
        worker_id=str(worker_id_1),
        preferred_metrics_port=int(metrics_port_1),
        log_path=log_path_1,
        extra_env={"OUTBOX_EXPERIMENT_PROCESS_SLEEP_SECONDS": str(worker1_sleep_after_claim_s)},
    )
    try:
        time.sleep(max(0.5, float(scrape_delay)))
        try:
            before_1_path.write_text(scrape_metrics_text(port=int(actual_metrics_port_1), timeout_s=2.0), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            before_1_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

        claim_deadline = time.time() + float(claim_timeout)
        while time.time() < claim_deadline:
            if proc1.poll() is not None:
                break
            try:
                text = log_path_1.read_text(encoding="utf-8", errors="replace")
            except Exception:
                text = ""
            if rx_claimed.search(text):
                observed_claim = True
                break
            time.sleep(0.1)

        if proc1.poll() is None:
            killed_worker1 = True
            proc1.kill()
    except KeyboardInterrupt:
        killed_worker1 = True
        try:
            proc1.kill()
        except Exception:
            pass
    finally:
        try:
            proc1.wait(timeout=30)
        except Exception:
            pass

    after_1_path.write_text(
        f"note: worker1 was {'killed' if killed_worker1 else 'not_killed'} by controller\n"
        f"note: observed_claim={observed_claim}\n",
        encoding="utf-8",
    )

    proc2, env2, actual_metrics_port_2, actual_http_port_2 = _spawn_worker_with_retry(
        worker_id=str(worker_id_2),
        preferred_metrics_port=int(metrics_port_2),
        log_path=log_path_2,
        extra_env={"OUTBOX_EXPERIMENT_PROCESS_SLEEP_SECONDS": "0"},
    )
    try:
        time.sleep(max(0.5, float(scrape_delay)))
        try:
            before_2_path.write_text(scrape_metrics_text(port=int(actual_metrics_port_2), timeout_s=2.0), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            before_2_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

        start2 = time.time()
        while True:
            if duration > 0 and (time.time() - start2) >= duration:
                break
            if proc2.poll() is not None:
                worker2_exited_early = True
                break
            time.sleep(0.25)

        try:
            after_2_path.write_text(scrape_metrics_text(port=int(actual_metrics_port_2), timeout_s=2.0), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            after_2_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

        if proc2.poll() is None:
            worker2_terminated_by_controller = True
            proc2.terminate()
    except KeyboardInterrupt:
        try:
            proc2.terminate()
        except Exception:
            pass
    finally:
        try:
            proc2.wait(timeout=30)
        except Exception:
            pass

    exit_info = {
        "worker1": {
            "returncode": int(proc1.returncode) if proc1.returncode is not None else None,
            "killed_by_controller": bool(killed_worker1),
            "observed_claim": bool(observed_claim),
        },
        "worker2": {
            "returncode": int(proc2.returncode) if proc2.returncode is not None else None,
            "exited_early": bool(worker2_exited_early),
            "terminated_by_controller": bool(worker2_terminated_by_controller),
        },
    }
    write_json(outdir / "_worker_exit.json", exit_info)

    ports_info = {
        "worker1": {"metrics_port": int(actual_metrics_port_1), "http_port": int(actual_http_port_1)},
        "worker2": {"metrics_port": int(actual_metrics_port_2), "http_port": int(actual_http_port_2)},
    }
    write_json(outdir / "_ports.json", ports_info)

    combined = (
        "# metrics-before-1\n\n"
        + (before_1_path.read_text(encoding="utf-8", errors="replace") if before_1_path.exists() else "")
        + "\n\n# metrics-before-2\n\n"
        + (before_2_path.read_text(encoding="utf-8", errors="replace") if before_2_path.exists() else "")
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

    if worker2_exited_early and (proc2.returncode not in (None, 0)):
        print(f"[labs run {SCENARIO_STUCK_RECLAIM}] worker2 exited early: rc={proc2.returncode}")
        print(f"[labs run {SCENARIO_STUCK_RECLAIM}] see logs: {log_path_2}")
        return DrillResult(ok=False, meta={"exit_code": 4}, summary={}, errors=[])

    print(f"[labs run {SCENARIO_STUCK_RECLAIM}] done (now run verify/export/clean)")
    print(f"[labs run {SCENARIO_STUCK_RECLAIM}] outputs: {outdir}")
    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])


@register("stuck_reclaim.verify")
def verify_stuck_reclaim(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_dir = resolve_run_dir(
        run_id=str(payload.get("run_id") or "").strip() or None,
        outdir=str(payload.get("outdir") or "").strip() or None,
        scenario=SCENARIO_STUCK_RECLAIM,
    )
    metrics_dir = run_dir / "_metrics"
    logs_dir = run_dir / "_logs"

    before2 = (metrics_dir / "metrics-before-2.txt").read_text(encoding="utf-8") if (metrics_dir / "metrics-before-2.txt").exists() else ""
    after2 = (metrics_dir / "metrics-after-2.txt").read_text(encoding="utf-8") if (metrics_dir / "metrics-after-2.txt").exists() else ""

    metric_processed = "outbox_processed_total"
    metric_failed = "outbox_failed_total"

    metrics_available = (not before2.strip().startswith("scrape_failed")) and (not after2.strip().startswith("scrape_failed"))

    processed_before = prom_parse_counter_sum(before2, metric_processed) if metrics_available else 0.0
    processed_after = prom_parse_counter_sum(after2, metric_processed) if metrics_available else 0.0
    failed_before = prom_parse_counter_sum(before2, metric_failed) if metrics_available else 0.0
    failed_after = prom_parse_counter_sum(after2, metric_failed) if metrics_available else 0.0

    delta_processed = processed_after - processed_before
    delta_failed = failed_after - failed_before

    reclaimed_count = 0
    reclaim_log_found = False
    worker2_log_path: Path | None = (logs_dir / f"worker2-{payload.get('run_id')}.log") if payload.get("run_id") else None
    if not (worker2_log_path and worker2_log_path.exists()):
        worker2_logs = sorted([p for p in logs_dir.glob("worker2-*.log") if p.is_file()], key=lambda p: p.name, reverse=True)
        worker2_log_path = worker2_logs[0] if worker2_logs else None

    worker2_text = ""
    if worker2_log_path and worker2_log_path.exists():
        worker2_text = worker2_log_path.read_text(encoding="utf-8", errors="replace")

    m = re.search(r"Reclaimed\s+(\d+)\s+stuck\s+outbox\s+events", worker2_text)
    if m:
        reclaim_log_found = True
        reclaimed_count = int(m.group(1))

    processed_log_count = len(re.findall(r"Outbox\s+(upsert|delete):", worker2_text))

    min_processed_delta = float(payload.get("min_processed_delta") or 0)
    max_failed_delta = float(payload.get("max_failed_delta") or 0)
    min_reclaimed = int(payload.get("min_reclaimed") or 0)

    processed_ok = (metrics_available and (delta_processed >= min_processed_delta)) or (processed_log_count >= 1)
    ok = processed_ok and ((delta_failed <= max_failed_delta) if metrics_available else True) and (reclaim_log_found and reclaimed_count >= min_reclaimed)

    result = {
        "scenario": SCENARIO_STUCK_RECLAIM,
        "run_dir": str(run_dir),
        "checks": {
            "processed_delta_ge": float(min_processed_delta),
            "failed_delta_le": float(max_failed_delta),
            "reclaimed_ge": int(min_reclaimed),
        },
        "observed": {
            "metrics_available": bool(metrics_available),
            metric_processed: {"before": processed_before, "after": processed_after, "delta": delta_processed},
            metric_failed: {"before": failed_before, "after": failed_after, "delta": delta_failed},
            "reclaimed": {"count": int(reclaimed_count), "log_found": bool(reclaim_log_found)},
            "processed_log_count": int(processed_log_count),
            "worker2_log": str(worker2_log_path) if worker2_log_path else None,
        },
        "ok": bool(ok),
    }
    pack_artifacts(paths=build_evidence_paths_for_dir(run_dir), result=result)

    if ok:
        print(f"[labs verify {SCENARIO_STUCK_RECLAIM}] OK")
        return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])

    print(f"[labs verify {SCENARIO_STUCK_RECLAIM}] FAILED")
    return DrillResult(ok=False, meta={"exit_code": 10}, summary={}, errors=[])


@register("stuck_reclaim.export")
def export_stuck_reclaim(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_dir = resolve_run_dir(
        run_id=str(payload.get("run_id") or "").strip() or None,
        outdir=str(payload.get("outdir") or "").strip() or None,
        scenario=SCENARIO_STUCK_RECLAIM,
    )
    exports_dir = run_dir / "_exports"
    ensure_dir(exports_dir)

    exporter = LEGACY_SCRIPTS_DIR / "labs_009_export_jaeger.py"
    cmd = [
        python_exe(),
        str(exporter),
        "--outdir",
        str(exports_dir),
        "--service",
        str(payload.get("service")),
        "--lookback",
        str(payload.get("lookback")),
        "--limit",
        str(int(payload.get("limit") or 0)),
        "--operation",
        "outbox.claim_batch",
        "--tags-json",
        json.dumps({"wordloom.obs_schema": SEARCH_OUTBOX_OBS_SCHEMA_VERSION}),
    ]
    rc = int(run_cmd(cmd, cwd=REPO_ROOT, env=load_env(env_file=None)))
    return DrillResult(ok=(rc == 0), meta={"exit_code": int(rc)}, summary={}, errors=[])


@register("stuck_reclaim.clean")
def clean_stuck_reclaim(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    keep_last = payload.get("keep_last")

    if keep_last is not None:
        base = LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_STUCK_RECLAIM
        if base.exists():
            runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
            for p in runs[int(keep_last) :]:
                shutil.rmtree(p, ignore_errors=True)
        print(f"[labs clean {SCENARIO_STUCK_RECLAIM}] kept_last={keep_last}")
    else:
        print(f"[labs clean {SCENARIO_STUCK_RECLAIM}] noop")

    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])
