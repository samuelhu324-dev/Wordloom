from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

from ..common import build_evidence_paths_for_dir, pack_artifacts
from ..registry import register
from ..types import DrillInputs, DrillResult
from ._failure_drill_shared import (
    LAB_ID_S3A_2A_3A,
    default_labs_auto_run_dir,
    ensure_dir,
    es_create_index_if_missing,
    es_set_index_write_block,
    load_env,
    prom_parse_counter_sum,
    python_exe,
    resolve_run_dir,
    run_cmd,
    scrape_metrics_text,
    with_backend_pythonpath,
)
from ._failure_drill_shared import LABS_SNAPSHOT_ROOT, LEGACY_SCRIPTS_DIR, REPO_ROOT


SCENARIO_ES_WRITE_BLOCK_4XX = "es_write_block_4xx"


@register("es_write_block_4xx.run")
def run_es_write_block_4xx(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_id = str(payload.get("run_id") or "").strip()
    outdir_str = str(payload.get("outdir") or "").strip()
    outdir = Path(outdir_str) if outdir_str else default_labs_auto_run_dir(scenario=SCENARIO_ES_WRITE_BLOCK_4XX, run_id=run_id)

    env_file = payload.get("env_file")
    service = payload.get("service")
    duration = int(payload.get("duration") or 0)
    metrics_port = int(payload.get("metrics_port") or 0)
    scrape_delay = float(payload.get("scrape_delay") or 0.0)

    logs_dir = outdir / "_logs"
    metrics_dir = outdir / "_metrics"
    exports_dir = outdir / "_exports"
    ensure_dir(logs_dir)
    ensure_dir(metrics_dir)
    ensure_dir(exports_dir)

    env = with_backend_pythonpath(load_env(env_file=str(env_file) if env_file else None))

    es_url = (env.get("ELASTIC_URL") or "http://localhost:19200").strip().rstrip("/")
    es_index = (env.get("ELASTIC_INDEX") or "wordloom-search-index").strip()

    service_name = service
    env.setdefault("WORDLOOM_TRACING_ENABLED", "1")
    env.setdefault("OTEL_SERVICE_NAME", service_name)
    env.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
    env.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    env.setdefault("OTEL_TRACES_SAMPLER", "always_on")

    env["LOG_LEVEL"] = "INFO"
    env["OUTBOX_EXPERIMENT_ES_429_RATIO"] = "0"
    env["OUTBOX_METRICS_PORT"] = str(int(metrics_port))

    recipe = {
        "lab_id": LAB_ID_S3A_2A_3A,
        "scenario": SCENARIO_ES_WRITE_BLOCK_4XX,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": env_file,
        "service": service_name,
        "es": {"url": es_url, "index": es_index, "inject": {"index.blocks.write": True}},
        "worker": {"duration_s": int(duration), "metrics_port": int(metrics_port)},
    }
    (outdir / "_recipe.json").write_text(json.dumps(recipe, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    worker = LEGACY_SCRIPTS_DIR / "search_outbox_worker.py"
    log_path = logs_dir / f"worker-{run_id}.log"
    cmd = [python_exe(), "-u", str(worker)]

    print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] outdir: {outdir}")
    print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] worker log: {log_path}")

    metrics_before_path = metrics_dir / "metrics-before.txt"
    metrics_after_path = metrics_dir / "metrics-after.txt"

    start = time.time()
    stopped_by_controller = False

    with open(log_path, "w", encoding="utf-8") as log_file:
        worker_proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env, stdout=log_file, stderr=subprocess.STDOUT)
        try:
            time.sleep(max(0.5, float(scrape_delay)))
            try:
                metrics_before = scrape_metrics_text(port=int(metrics_port), timeout_s=4.0)
                metrics_before_path.write_text(metrics_before, encoding="utf-8")
            except Exception as exc:  # noqa: BLE001
                metrics_before_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

            status, response_payload = es_set_index_write_block(es_url=es_url, index=es_index, enabled=True)
            if status == 404:
                c_status, c_payload = es_create_index_if_missing(es_url=es_url, index=es_index)
                (outdir / "_inject_es_create_index.response.txt").write_text(
                    f"status={c_status}\n\n{c_payload}\n", encoding="utf-8"
                )
                if c_status not in (200, 201, 400):
                    print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] failed to create index: http {c_status}")
                    worker_proc.terminate()
                    worker_proc.wait(timeout=30)
                    return DrillResult(ok=False, meta={"exit_code": 2}, summary={}, errors=[])

                status, response_payload = es_set_index_write_block(es_url=es_url, index=es_index, enabled=True)

            (outdir / "_inject_es_write_block.response.txt").write_text(
                f"status={status}\n\n{response_payload}\n", encoding="utf-8"
            )
            if status < 200 or status >= 300:
                print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] failed to enable write block: http {status}")
                worker_proc.terminate()
                worker_proc.wait(timeout=30)
                return DrillResult(ok=False, meta={"exit_code": 2}, summary={}, errors=[])

            inserter = REPO_ROOT / "backend" / "scripts" / "labs" / "labs_009_insert_search_outbox_pending.py"
            if not inserter.exists():
                inserter = LEGACY_SCRIPTS_DIR / "labs_009_insert_search_outbox_pending.py"
            trigger_env = env.copy()
            trigger_env.setdefault("OUTBOX_OP", "upsert")
            trigger_env.setdefault("OUTBOX_CREATE_SEARCH_INDEX_ROW", "1")

            proc = subprocess.run(
                [python_exe(), str(inserter)],
                cwd=str(REPO_ROOT),
                env=trigger_env,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            (outdir / "_trigger_insert_outbox.stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
            (outdir / "_trigger_insert_outbox.stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
            if proc.returncode != 0:
                print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] failed to insert outbox event: rc={proc.returncode}")
                worker_proc.terminate()
                worker_proc.wait(timeout=30)
                return DrillResult(ok=False, meta={"exit_code": 3}, summary={}, errors=[])

            outbox_event_id = (proc.stdout or "").strip().splitlines()[-1].strip()
            (outdir / "_outbox_event_id.txt").write_text(outbox_event_id + "\n", encoding="utf-8")
            print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] outbox_event_id: {outbox_event_id}")

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
        print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] worker exited early: rc={worker_proc.returncode}")
        print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] see logs: {log_path}")
        return DrillResult(ok=False, meta={"exit_code": 4}, summary={}, errors=[])

    print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] done (now run verify/export/clean)")
    print(f"[labs run {SCENARIO_ES_WRITE_BLOCK_4XX}] outputs: {outdir}")
    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])


@register("es_write_block_4xx.verify")
def verify_es_write_block_4xx(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_id = payload.get("run_id")
    outdir = payload.get("outdir")

    min_failed_delta = float(payload.get("min_failed_delta") or 0)
    max_retry_delta = float(payload.get("max_retry_delta") or 0)

    run_dir = resolve_run_dir(run_id=str(run_id) if run_id else None, outdir=str(outdir) if outdir else None, scenario=SCENARIO_ES_WRITE_BLOCK_4XX)
    metrics_dir = run_dir / "_metrics"
    before_path = metrics_dir / "metrics-before.txt"
    after_path = metrics_dir / "metrics-after.txt"

    before = before_path.read_text(encoding="utf-8") if before_path.exists() else ""
    after = after_path.read_text(encoding="utf-8") if after_path.exists() else ""

    failed_before = prom_parse_counter_sum(before, "outbox_failed_total", labels={"reason": "es_4xx"})
    failed_after = prom_parse_counter_sum(after, "outbox_failed_total", labels={"reason": "es_4xx"})
    retry_before = prom_parse_counter_sum(before, "outbox_retry_scheduled_total", labels={"reason": "es_4xx"})
    retry_after = prom_parse_counter_sum(after, "outbox_retry_scheduled_total", labels={"reason": "es_4xx"})

    delta_failed = failed_after - failed_before
    delta_retry = retry_after - retry_before

    ok = (delta_failed >= float(min_failed_delta)) and (delta_retry <= float(max_retry_delta))
    result = {
        "scenario": SCENARIO_ES_WRITE_BLOCK_4XX,
        "run_dir": str(run_dir),
        "checks": {
            "failed_delta_ge": float(min_failed_delta),
            "retry_delta_le": float(max_retry_delta),
        },
        "observed": {
            "outbox_failed_total_reason_es_4xx": {"before": failed_before, "after": failed_after, "delta": delta_failed},
            "outbox_retry_scheduled_total_reason_es_4xx": {"before": retry_before, "after": retry_after, "delta": delta_retry},
        },
        "ok": bool(ok),
    }
    pack_artifacts(paths=build_evidence_paths_for_dir(run_dir), result=result)

    if ok:
        print(f"[labs verify {SCENARIO_ES_WRITE_BLOCK_4XX}] OK")
        return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])

    print(f"[labs verify {SCENARIO_ES_WRITE_BLOCK_4XX}] FAILED")
    return DrillResult(ok=False, meta={"exit_code": 10}, summary={}, errors=[])


@register("es_write_block_4xx.export")
def export_es_write_block_4xx(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_dir = resolve_run_dir(
        run_id=str(payload.get("run_id") or "").strip() or None,
        outdir=str(payload.get("outdir") or "").strip() or None,
        scenario=SCENARIO_ES_WRITE_BLOCK_4XX,
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


@register("es_write_block_4xx.clean")
def clean_es_write_block_4xx(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    env_file = payload.get("env_file")
    outdir = payload.get("outdir")
    keep_last = payload.get("keep_last")

    env = load_env(env_file=str(env_file) if env_file else None)
    es_url = (env.get("ELASTIC_URL") or "http://localhost:19200").strip().rstrip("/")
    es_index = (env.get("ELASTIC_INDEX") or "wordloom-search-index").strip()

    status, response_payload = es_set_index_write_block(es_url=es_url, index=es_index, enabled=False)
    print(f"[labs clean {SCENARIO_ES_WRITE_BLOCK_4XX}] disable write block: http {status}")
    if outdir:
        out_path = Path(str(outdir))
        ensure_dir(out_path)
        (out_path / "_clean_es_write_block.response.txt").write_text(
            f"status={status}\n\n{response_payload}\n", encoding="utf-8"
        )

    if keep_last is not None:
        base = LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_ES_WRITE_BLOCK_4XX
        if base.exists():
            runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
            for p in runs[int(keep_last) :]:
                import shutil

                shutil.rmtree(p, ignore_errors=True)
            print(f"[labs clean {SCENARIO_ES_WRITE_BLOCK_4XX}] kept_last={keep_last}")

    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])
