from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

from ..common import build_evidence_paths_for_dir, pack_artifacts, write_json
from ..registry import register
from ..types import DrillInputs, DrillResult
from ._failure_drill_shared import (
    LAB_ID_S3A_2A_3A,
    default_labs_auto_run_dir,
    ensure_dir,
    load_env,
    parse_last_json_line,
    SpawnedWorker,
    python_exe,
    read_json_file,
    resolve_run_dir,
    run_cmd,
    scrape_metrics_text,
    spawn_chronicle_outbox_worker,
    with_backend_pythonpath,
)
from ._failure_drill_shared import LEGACY_SCRIPTS_DIR, LABS_SNAPSHOT_ROOT, REPO_ROOT


SCENARIO_PROJECTION_VERSION = "projection_version"


@register("projection_version.run")
def run_projection_version(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_id = str(payload.get("run_id") or "").strip()
    outdir_str = str(payload.get("outdir") or "").strip()
    outdir = Path(outdir_str) if outdir_str else default_labs_auto_run_dir(scenario=SCENARIO_PROJECTION_VERSION, run_id=run_id)

    env_file = payload.get("env_file")
    service = payload.get("service")

    duration = int(payload.get("duration") or 0)
    poll_interval = float(payload.get("poll_interval") or 0.0)
    batch_size = int(payload.get("batch_size") or 0)
    lease_seconds = int(payload.get("lease_seconds") or 0)
    reclaim_interval = float(payload.get("reclaim_interval") or 0.0)
    max_processing_seconds = int(payload.get("max_processing_seconds") or 0)

    projection_version_1 = int(payload.get("projection_version_1") or 0)
    projection_version_2 = int(payload.get("projection_version_2") or 0)

    metrics_port = int(payload.get("metrics_port") or 0)
    scrape_delay = float(payload.get("scrape_delay") or 0.0)

    logs_dir = outdir / "_logs"
    metrics_dir = outdir / "_metrics"
    ensure_dir(logs_dir)
    ensure_dir(metrics_dir)

    run_log_path = logs_dir / f"run-{run_id}.log"
    try:
        run_log_path.write_text(
            f"[labs run {SCENARIO_PROJECTION_VERSION}] start at {time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            encoding="utf-8",
        )
    except Exception:
        pass

    metrics_note_path = metrics_dir / "metrics-note.txt"
    try:
        metrics_note_path.write_text(
            f"note: metrics files may be added later (scenario={SCENARIO_PROJECTION_VERSION} run_id={run_id})\n",
            encoding="utf-8",
        )
    except Exception:
        pass

    env = with_backend_pythonpath(load_env(env_file=str(env_file) if env_file else None))

    env["OUTBOX_RUN_SECONDS"] = str(int(duration))
    env["OUTBOX_POLL_INTERVAL_SECONDS"] = str(float(poll_interval))
    env["OUTBOX_BATCH_SIZE"] = str(int(batch_size))
    env["OUTBOX_LEASE_SECONDS"] = str(int(lease_seconds))
    env["OUTBOX_RECLAIM_INTERVAL_SECONDS"] = str(float(reclaim_interval))
    env["OUTBOX_MAX_PROCESSING_SECONDS"] = str(int(max_processing_seconds))
    env["LOG_LEVEL"] = "INFO"

    env.pop("OUTBOX_EXPERIMENT_PROCESS_SLEEP_SECONDS", None)

    recipe = {
        "lab_id": LAB_ID_S3A_2A_3A,
        "scenario": SCENARIO_PROJECTION_VERSION,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": env_file,
        "service": service,
        "phase": {
            "v1": int(projection_version_1),
            "v2": int(projection_version_2),
        },
        "worker": {
            "duration_s": int(duration),
            "preferred_metrics_port": int(metrics_port),
            "poll_interval_seconds": float(poll_interval),
            "batch_size": int(batch_size),
            "lease_seconds": int(lease_seconds),
            "reclaim_interval_seconds": float(reclaim_interval),
            "max_processing_seconds": int(max_processing_seconds),
        },
    }
    write_json(outdir / "_recipe.json", recipe)

    inserter = REPO_ROOT / "backend" / "scripts" / "labs" / "labs_009_insert_chronicle_outbox_pending.py"
    if not inserter.exists():
        inserter = LEGACY_SCRIPTS_DIR / "labs_009_insert_chronicle_outbox_pending.py"

    prober = REPO_ROOT / "backend" / "scripts" / "labs" / "labs_009_probe_chronicle_entry.py"
    if not prober.exists():
        prober = LEGACY_SCRIPTS_DIR / "labs_009_probe_chronicle_entry.py"

    def _spawn_worker_with_retry(
        *,
        preferred_metrics_port: int,
        log_path: Path,
        extra_env: dict[str, str] | None = None,
        max_attempts: int = 4,
    ) -> tuple[SpawnedWorker, dict[str, str], int, int]:
        candidate_ports: list[int] = []
        for i in range(max_attempts):
            p = int(preferred_metrics_port) + (i * 10_000)
            if 1024 <= p <= 65_000:
                candidate_ports.append(p)
        if not candidate_ports:
            candidate_ports = [19110, 29110, 39110, 49110]

        last_worker: SpawnedWorker | None = None
        last_env: dict[str, str] | None = None
        last_metrics_port = int(preferred_metrics_port)
        last_http_port = int(preferred_metrics_port) + 2

        for attempt, metrics_port_candidate in enumerate(candidate_ports, start=1):
            http_port = int(metrics_port_candidate) + 2
            run_env = env.copy()
            run_env["OUTBOX_METRICS_PORT"] = str(int(metrics_port_candidate))
            run_env["OUTBOX_HTTP_PORT"] = str(int(http_port))
            if extra_env:
                run_env.update({str(k): str(v) for k, v in extra_env.items()})

            header = (
                f"\n\n# controller: spawn attempt {attempt}/{len(candidate_ports)} "
                f"metrics_port={metrics_port_candidate} http_port={http_port}\n"
            )
            worker_handle = spawn_chronicle_outbox_worker(
                env=run_env,
                logs_dir=log_path.parent,
                run_id=run_id,
                log_name=log_path.name,
                evidence_env_keys=[
                    k
                    for k in (
                        "OUTBOX_METRICS_PORT",
                        "OUTBOX_HTTP_PORT",
                        "OUTBOX_RUN_SECONDS",
                        "OUTBOX_POLL_INTERVAL_SECONDS",
                        "OUTBOX_BATCH_SIZE",
                        "OUTBOX_LEASE_SECONDS",
                        "OUTBOX_RECLAIM_INTERVAL_SECONDS",
                        "OUTBOX_MAX_PROCESSING_SECONDS",
                        "CHRONICLE_PROJECTION_VERSION",
                    )
                    if k in run_env
                ],
                log_mode="a",
                log_header=header,
            )

            time.sleep(0.75)
            if worker_handle.proc.poll() is None:
                return worker_handle, run_env, int(metrics_port_candidate), int(http_port)

            try:
                worker_handle.wait(timeout_s=1.0)
            except Exception:
                pass

            try:
                tail = log_path.read_text(encoding="utf-8", errors="replace")[-4000:]
            except Exception:
                tail = ""
            if "WinError 10013" in tail or "PermissionError" in tail:
                last_worker = worker_handle
                last_env = run_env
                last_metrics_port = int(metrics_port_candidate)
                last_http_port = int(http_port)
                continue

            return worker_handle, run_env, int(metrics_port_candidate), int(http_port)

        assert last_worker is not None
        assert last_env is not None
        return last_worker, last_env, int(last_metrics_port), int(last_http_port)

    def _run_probe(*, chronicle_event_id: str, out_path: Path) -> None:
        probe_env = env.copy()
        probe_env["OUTBOX_CHRONICLE_EVENT_ID"] = chronicle_event_id
        proc = subprocess.run(
            [python_exe(), str(prober)],
            cwd=str(REPO_ROOT),
            env=probe_env,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        out_path.write_text((proc.stdout or "").strip() + "\n", encoding="utf-8")
        if proc.returncode != 0:
            (out_path.parent / (out_path.name + ".stderr.txt")).write_text(proc.stderr or "", encoding="utf-8")

    print(f"[labs run {SCENARIO_PROJECTION_VERSION}] outdir: {outdir}")

    insert_env = env.copy()
    insert_cmd_1 = [python_exe(), str(inserter)]
    try:
        insert_proc_1 = subprocess.run(
            insert_cmd_1,
            cwd=str(REPO_ROOT),
            env=insert_env,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except subprocess.TimeoutExpired:
        (outdir / "_trigger_insert_v1.stdout.txt").write_text("", encoding="utf-8")
        (outdir / "_trigger_insert_v1.stderr.txt").write_text("", encoding="utf-8")
        (outdir / "_trigger_insert_v1.timeout.txt").write_text(
            f"timeout_s=60\ncmd={' '.join(insert_cmd_1)}\n",
            encoding="utf-8",
        )
        return DrillResult(ok=False, meta={"exit_code": 5}, summary={}, errors=[])
    (outdir / "_trigger_insert_v1.stdout.txt").write_text(insert_proc_1.stdout or "", encoding="utf-8")
    (outdir / "_trigger_insert_v1.stderr.txt").write_text(insert_proc_1.stderr or "", encoding="utf-8")
    if insert_proc_1.returncode != 0:
        print(f"[labs run {SCENARIO_PROJECTION_VERSION}] failed to insert v1 outbox: rc={insert_proc_1.returncode}")
        return DrillResult(ok=False, meta={"exit_code": 3}, summary={}, errors=[])

    insert_obj_1 = parse_last_json_line(insert_proc_1.stdout or "") or {}
    chronicle_event_id = str(insert_obj_1.get("chronicle_event_id") or "").strip()
    outbox_event_id_1 = str(insert_obj_1.get("outbox_event_id") or "").strip()
    if not chronicle_event_id or not outbox_event_id_1:
        print(f"[labs run {SCENARIO_PROJECTION_VERSION}] unexpected inserter output; see _trigger_insert_v1.stdout.txt")
        return DrillResult(ok=False, meta={"exit_code": 3}, summary={}, errors=[])

    (outdir / "_chronicle_event_id.txt").write_text(chronicle_event_id + "\n", encoding="utf-8")
    (outdir / "_outbox_event_id_v1.txt").write_text(outbox_event_id_1 + "\n", encoding="utf-8")

    log_v1 = logs_dir / f"worker-v1-{run_id}.log"
    log_v1.write_text("", encoding="utf-8")
    before_v1 = metrics_dir / "metrics-before-v1.txt"
    after_v1 = metrics_dir / "metrics-after-v1.txt"

    worker1, _env1, actual_metrics_port_1, _http1 = _spawn_worker_with_retry(
        preferred_metrics_port=int(metrics_port),
        log_path=log_v1,
        extra_env={"CHRONICLE_PROJECTION_VERSION": str(int(projection_version_1))},
    )
    write_json(outdir / "_worker_start.json", {"v1": worker1.evidence_summary()})
    try:
        time.sleep(max(0.5, float(scrape_delay)))
        try:
            before_v1.write_text(scrape_metrics_text(port=int(actual_metrics_port_1), timeout_s=2.0), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            before_v1.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

        worker1.wait(timeout_s=max(10, int(duration) + 20))
    except Exception:
        try:
            worker1.terminate_and_wait(timeout_s=30)
        except Exception:
            pass
    finally:
        try:
            after_v1.write_text(scrape_metrics_text(port=int(actual_metrics_port_1), timeout_s=2.0), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            after_v1.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

    _run_probe(chronicle_event_id=chronicle_event_id, out_path=(outdir / "_probe_entry_v1.json"))

    insert_env_2 = env.copy()
    insert_env_2["OUTBOX_CHRONICLE_EVENT_ID"] = chronicle_event_id
    insert_cmd_2 = [python_exe(), str(inserter)]
    try:
        insert_proc_2 = subprocess.run(
            insert_cmd_2,
            cwd=str(REPO_ROOT),
            env=insert_env_2,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except subprocess.TimeoutExpired:
        (outdir / "_trigger_insert_v2.stdout.txt").write_text("", encoding="utf-8")
        (outdir / "_trigger_insert_v2.stderr.txt").write_text("", encoding="utf-8")
        (outdir / "_trigger_insert_v2.timeout.txt").write_text(
            f"timeout_s=60\ncmd={' '.join(insert_cmd_2)}\n",
            encoding="utf-8",
        )
        return DrillResult(ok=False, meta={"exit_code": 5}, summary={}, errors=[])
    (outdir / "_trigger_insert_v2.stdout.txt").write_text(insert_proc_2.stdout or "", encoding="utf-8")
    (outdir / "_trigger_insert_v2.stderr.txt").write_text(insert_proc_2.stderr or "", encoding="utf-8")
    if insert_proc_2.returncode != 0:
        print(f"[labs run {SCENARIO_PROJECTION_VERSION}] failed to insert v2 outbox: rc={insert_proc_2.returncode}")
        return DrillResult(ok=False, meta={"exit_code": 3}, summary={}, errors=[])

    insert_obj_2 = parse_last_json_line(insert_proc_2.stdout or "") or {}
    outbox_event_id_2 = str(insert_obj_2.get("outbox_event_id") or "").strip()
    if not outbox_event_id_2:
        print(f"[labs run {SCENARIO_PROJECTION_VERSION}] unexpected v2 inserter output; see _trigger_insert_v2.stdout.txt")
        return DrillResult(ok=False, meta={"exit_code": 3}, summary={}, errors=[])
    (outdir / "_outbox_event_id_v2.txt").write_text(outbox_event_id_2 + "\n", encoding="utf-8")

    log_v2 = logs_dir / f"worker-v2-{run_id}.log"
    log_v2.write_text("", encoding="utf-8")
    before_v2 = metrics_dir / "metrics-before-v2.txt"
    after_v2 = metrics_dir / "metrics-after-v2.txt"

    worker2, _env2, actual_metrics_port_2, _http2 = _spawn_worker_with_retry(
        preferred_metrics_port=int(metrics_port) + 1,
        log_path=log_v2,
        extra_env={"CHRONICLE_PROJECTION_VERSION": str(int(projection_version_2))},
    )
    write_json(outdir / "_worker_start.json", {"v1": worker1.evidence_summary(), "v2": worker2.evidence_summary()})
    try:
        time.sleep(max(0.5, float(scrape_delay)))
        try:
            before_v2.write_text(scrape_metrics_text(port=int(actual_metrics_port_2), timeout_s=2.0), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            before_v2.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

        worker2.wait(timeout_s=max(10, int(duration) + 20))
    except Exception:
        try:
            worker2.terminate_and_wait(timeout_s=30)
        except Exception:
            pass
    finally:
        try:
            after_v2.write_text(scrape_metrics_text(port=int(actual_metrics_port_2), timeout_s=2.0), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            after_v2.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

    _run_probe(chronicle_event_id=chronicle_event_id, out_path=(outdir / "_probe_entry_v2.json"))

    result = {
        "scenario": SCENARIO_PROJECTION_VERSION,
        "run_id": run_id,
        "chronicle_event_id": chronicle_event_id,
        "outbox_event_ids": {"v1": outbox_event_id_1, "v2": outbox_event_id_2},
        "worker": read_json_file(outdir / "_worker_start.json"),
        "worker_logs": {
            "v1": str(log_v1.relative_to(REPO_ROOT)),
            "v2": str(log_v2.relative_to(REPO_ROOT)),
        },
        "probe": {
            "v1": read_json_file(outdir / "_probe_entry_v1.json"),
            "v2": read_json_file(outdir / "_probe_entry_v2.json"),
        },
    }
    write_json(outdir / "_run.json", result)

    print(f"[labs run {SCENARIO_PROJECTION_VERSION}] chronicle_event_id: {chronicle_event_id}")
    print(f"[labs run {SCENARIO_PROJECTION_VERSION}] done (now run verify/export/clean)")
    print(f"[labs run {SCENARIO_PROJECTION_VERSION}] outputs: {outdir}")
    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])


@register("projection_version.verify")
def verify_projection_version(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_dir = resolve_run_dir(
        run_id=str(payload.get("run_id") or "").strip() or None,
        outdir=str(payload.get("outdir") or "").strip() or None,
        scenario=SCENARIO_PROJECTION_VERSION,
    )
    if not run_dir.exists():
        print(f"[labs verify {SCENARIO_PROJECTION_VERSION}] run_dir not found: {run_dir}")
        return DrillResult(ok=False, meta={"exit_code": 2}, summary={}, errors=[])

    probe1 = read_json_file(run_dir / "_probe_entry_v1.json") or {}
    probe2 = read_json_file(run_dir / "_probe_entry_v2.json") or {}

    want1 = int(payload.get("projection_version_1") or 0)
    want2 = int(payload.get("projection_version_2") or 0)
    got1 = probe1.get("projection_version")
    got2 = probe2.get("projection_version")

    ok = True
    errors: list[str] = []
    if got1 != want1:
        ok = False
        errors.append(f"probe v1 projection_version mismatch: got={got1!r} want={want1}")
    if got2 != want2:
        ok = False
        errors.append(f"probe v2 projection_version mismatch: got={got2!r} want={want2}")

    checks = [
        {
            "name": "probe v1 projection_version match",
            "expected": want1,
            "observed": got1,
            "ok": bool(got1 == want1),
        },
        {
            "name": "probe v2 projection_version match",
            "expected": want2,
            "observed": got2,
            "ok": bool(got2 == want2),
        },
    ]

    why = "ok" if ok else (errors[0] if errors else "verify failed")

    result = {
        "scenario": SCENARIO_PROJECTION_VERSION,
        "run_id": run_dir.name,
        "ok": bool(ok),
        "why": why,
        "checks": checks,
        "expected": {"v1": want1, "v2": want2},
        "observed": {"v1": got1, "v2": got2, "worker": read_json_file(run_dir / "_worker_start.json")},
        "errors": errors,
    }

    pack_artifacts(paths=build_evidence_paths_for_dir(run_dir), result=result)
    write_json(run_dir / "_verify_result.json", result)

    if ok:
        print(f"[labs verify {SCENARIO_PROJECTION_VERSION}] OK")
        return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])

    print(f"[labs verify {SCENARIO_PROJECTION_VERSION}] FAILED")
    for e in errors:
        print("  -", e)
    return DrillResult(ok=False, meta={"exit_code": 2}, summary={}, errors=[])


@register("projection_version.export")
def export_projection_version(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_dir = resolve_run_dir(
        run_id=str(payload.get("run_id") or "").strip() or None,
        outdir=str(payload.get("outdir") or "").strip() or None,
        scenario=SCENARIO_PROJECTION_VERSION,
    )
    if not run_dir.exists():
        print(f"[labs export {SCENARIO_PROJECTION_VERSION}] run_dir not found: {run_dir}")
        return DrillResult(ok=False, meta={"exit_code": 2}, summary={}, errors=[])

    event_id_path = run_dir / "_chronicle_event_id.txt"
    if not event_id_path.exists():
        print(f"[labs export {SCENARIO_PROJECTION_VERSION}] missing: {event_id_path}")
        return DrillResult(ok=False, meta={"exit_code": 2}, summary={}, errors=[])
    chronicle_event_id = (event_id_path.read_text(encoding="utf-8", errors="replace") or "").strip()
    if not chronicle_event_id:
        print(f"[labs export {SCENARIO_PROJECTION_VERSION}] empty chronicle_event_id")
        return DrillResult(ok=False, meta={"exit_code": 2}, summary={}, errors=[])

    exports_dir = run_dir / "_exports"
    ensure_dir(exports_dir)

    script = LEGACY_SCRIPTS_DIR / "labs_009_export_jaeger.py"
    cmd = [
        python_exe(),
        str(script),
        "--outdir",
        str(exports_dir),
        "--service",
        str(payload.get("service")),
        "--lookback",
        str(payload.get("lookback")),
        "--limit",
        str(int(payload.get("limit") or 0)),
        "--operation",
        "outbox.process",
        "--tags-json",
        json.dumps({"wordloom.entity.id": chronicle_event_id}, ensure_ascii=False),
    ]
    rc = run_cmd(cmd, cwd=REPO_ROOT)
    return DrillResult(ok=(rc == 0), meta={"exit_code": int(rc)}, summary={}, errors=[])


@register("projection_version.clean")
def clean_projection_version(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    keep_last = payload.get("keep_last")

    if keep_last is not None:
        base = LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_PROJECTION_VERSION
        if base.exists():
            import shutil

            runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
            for p in runs[int(keep_last) :]:
                shutil.rmtree(p, ignore_errors=True)
            print(f"[labs clean {SCENARIO_PROJECTION_VERSION}] kept_last={keep_last}")
    else:
        print(f"[labs clean {SCENARIO_PROJECTION_VERSION}] noop")

    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])
