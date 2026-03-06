from __future__ import annotations

import json
import socket
import threading
import time
import uuid
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
    readiness_sleep_v1,
    read_json_file,
    run_search_outbox_supply_inserter_v1,
    scrape_metrics_text,
    scrape_metrics_text_readiness_v1,
    verify_supply_rows_v1,
    with_backend_pythonpath,
)
from ._failure_drill_shared import LABS_SNAPSHOT_ROOT


SCENARIO_ES_TIMEOUT = "es_timeout"


class _BlackholeServer:
    def __init__(self) -> None:
        self._stop = threading.Event()
        self._server_sock: socket.socket | None = None
        self._clients: list[socket.socket] = []
        self._thread: threading.Thread | None = None
        self.port: int | None = None

    def start(self) -> None:
        if self._thread is not None:
            return

        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(("127.0.0.1", 0))
        server_sock.listen(16)
        server_sock.settimeout(0.25)
        self._server_sock = server_sock
        self.port = int(server_sock.getsockname()[1])

        def _run() -> None:
            assert self._server_sock is not None
            while not self._stop.is_set():
                try:
                    conn, _addr = self._server_sock.accept()
                except TimeoutError:
                    continue
                except OSError:
                    break

                try:
                    conn.settimeout(0.25)
                except Exception:
                    pass
                self._clients.append(conn)

                # Drain any request bytes then never respond; HTTPX will hit a read timeout.
                try:
                    for _ in range(4):
                        if self._stop.is_set():
                            break
                        try:
                            _ = conn.recv(4096)
                        except TimeoutError:
                            break
                        except OSError:
                            break
                except Exception:
                    pass

                # Keep socket open until stopped.
                while not self._stop.is_set():
                    time.sleep(0.1)

        self._thread = threading.Thread(target=_run, name="labs-es-blackhole", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._server_sock is not None:
            try:
                self._server_sock.close()
            except Exception:
                pass

        for c in list(self._clients):
            try:
                c.close()
            except Exception:
                pass


@register("es_timeout.run")
def run_es_timeout(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_id = str(payload.get("run_id") or "").strip()
    outdir_str = str(payload.get("outdir") or "").strip()
    outdir = (
        Path(outdir_str)
        if outdir_str
        else default_labs_auto_run_dir(scenario=SCENARIO_ES_TIMEOUT, run_id=run_id)
    )

    env_file = payload.get("env_file")
    service = payload.get("service")
    duration = int(payload.get("duration") or 0)
    metrics_port = int(payload.get("metrics_port") or 0)
    scrape_delay = float(payload.get("scrape_delay") or 0.0)
    op = payload.get("op")

    logs_dir = outdir / "_logs"
    metrics_dir = outdir / "_metrics"
    ensure_dir(logs_dir)
    ensure_dir(metrics_dir)

    run_log_path = logs_dir / f"run-{run_id}.log"
    try:
        run_log_path.write_text(
            f"[labs run {SCENARIO_ES_TIMEOUT}] start at {time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            encoding="utf-8",
        )
    except Exception:
        pass

    env = with_backend_pythonpath(load_env(env_file=str(env_file) if env_file else None))
    env.setdefault("WORDLOOM_TRACING_ENABLED", "1")
    env.setdefault("OTEL_SERVICE_NAME", service)
    env.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
    env.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    env.setdefault("OTEL_TRACES_SAMPLER", "always_on")
    env["OUTBOX_METRICS_PORT"] = str(int(metrics_port))
    env["OUTBOX_REQUIRE_ES_READY"] = "0"
    # Keep evidence stable: avoid immediate re-claim after a timeout retry is scheduled.
    env.setdefault("OUTBOX_BASE_BACKOFF_SECONDS", "30")
    env.setdefault("OUTBOX_MAX_BACKOFF_SECONDS", "30")

    # Scope worker claims to a single deterministic library_id so this run can't
    # accidentally process unrelated historical pending rows.
    scoped_library_id = str(uuid.uuid4())
    env["OUTBOX_LIBRARY_ID"] = scoped_library_id
    env["SEARCH_OUTBOX_LIBRARY_ALLOWLIST"] = scoped_library_id

    recipe_path = outdir / "_recipe.json"
    recipe = {
        "lab_id": LAB_ID_S3A_2A_3A,
        "scenario": SCENARIO_ES_TIMEOUT,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "env_file": env_file,
        "service": service,
        "inject": {"kind": "es_blackhole", "elastic_url": None},
        "worker": {"duration_s": int(duration), "metrics_port": int(metrics_port)},
        "trigger": {"op": str(op)},
        "scope": {"library_id": scoped_library_id},
    }
    write_json(recipe_path, recipe)

    log_path = logs_dir / f"worker-{run_id}.log"
    print(f"[labs run {SCENARIO_ES_TIMEOUT}] outdir: {outdir}")
    print(f"[labs run {SCENARIO_ES_TIMEOUT}] worker log: {log_path}")

    metrics_before_path = metrics_dir / "metrics-before.txt"
    metrics_after_path = metrics_dir / "metrics-after.txt"

    if not metrics_before_path.exists():
        metrics_before_path.write_text("not_scraped_yet\n", encoding="utf-8")
    if not metrics_after_path.exists():
        metrics_after_path.write_text("not_scraped_yet\n", encoding="utf-8")

    blackhole: _BlackholeServer | None = None
    worker_handle = None
    start = time.time()
    stopped_by_controller = False
    worker_env_keys = [
        "WORDLOOM_TRACING_ENABLED",
        "OTEL_SERVICE_NAME",
        "OTEL_EXPORTER_OTLP_PROTOCOL",
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        "OTEL_TRACES_SAMPLER",
        "SEARCH_OUTBOX_LIBRARY_ALLOWLIST",
        "OUTBOX_METRICS_PORT",
        "OUTBOX_REQUIRE_ES_READY",
        "OUTBOX_BASE_BACKOFF_SECONDS",
        "OUTBOX_MAX_BACKOFF_SECONDS",
        "ELASTIC_URL",
        "OUTBOX_LIBRARY_ID",
    ]

    try:
        blackhole = _BlackholeServer()
        blackhole.start()
        assert blackhole.port is not None
        env["ELASTIC_URL"] = f"http://127.0.0.1:{blackhole.port}"
        recipe["inject"] = {"kind": "es_blackhole", "elastic_url": env["ELASTIC_URL"]}
        write_json(recipe_path, recipe)

        worker_handle = spawn_search_outbox_worker(
            env=env,
            logs_dir=logs_dir,
            run_id=run_id,
            log_name=f"worker-{run_id}.log",
            evidence_env_keys=[k for k in worker_env_keys if k in env],
        )
        write_json(outdir / "_worker_start.json", worker_handle.evidence_summary())

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
            print(f"[labs run {SCENARIO_ES_TIMEOUT}] inserter timed out")
            stopped_by_controller = True
            if worker_handle is not None:
                worker_handle.terminate_and_wait(timeout_s=30)
            return DrillResult(ok=False, meta={"exit_code": 5}, summary={}, errors=[])
        if supply_res.returncode != 0:
            print(f"[labs run {SCENARIO_ES_TIMEOUT}] failed to insert outbox event: rc={supply_res.returncode}")
            stopped_by_controller = True
            if worker_handle is not None:
                worker_handle.terminate_and_wait(timeout_s=30)
            return DrillResult(ok=False, meta={"exit_code": 3}, summary={}, errors=[])

        outbox_event_id = supply_res.outbox_event_ids[-1].strip() if supply_res.outbox_event_ids else ""
        (outdir / "_outbox_event_id.txt").write_text(outbox_event_id + "\n", encoding="utf-8")
        print(f"[labs run {SCENARIO_ES_TIMEOUT}] outbox_event_id: {outbox_event_id}")

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
                    metrics_after_path.write_text(
                        f"scrape_failed: {type(exc).__name__}: {exc}\n",
                        encoding="utf-8",
                    )
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
                    metrics_after_path.write_text(
                        f"scrape_failed: {type(exc).__name__}: {exc}\n",
                        encoding="utf-8",
                    )
                break
            time.sleep(0.25)
    except KeyboardInterrupt:
        stopped_by_controller = True
        if worker_handle is not None:
            worker_handle.terminate_and_wait(timeout_s=30)
    except Exception as exc:  # noqa: BLE001
        try:
            with run_log_path.open("a", encoding="utf-8") as f:
                f.write(f"exception: {type(exc).__name__}: {exc}\n")
        except Exception:
            pass

        if not metrics_before_path.exists():
            try:
                metrics_before_path.write_text(
                    f"scrape_failed: {type(exc).__name__}: {exc}\n",
                    encoding="utf-8",
                )
            except Exception:
                pass
        if not metrics_after_path.exists():
            try:
                metrics_after_path.write_text(
                    f"scrape_failed: {type(exc).__name__}: {exc}\n",
                    encoding="utf-8",
                )
            except Exception:
                pass
        return DrillResult(ok=False, meta={"exit_code": 6, "error": type(exc).__name__}, summary={}, errors=[])
    finally:
        if blackhole is not None:
            blackhole.stop()
        if worker_handle is not None:
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
        print(f"[labs run {SCENARIO_ES_TIMEOUT}] worker exited early: rc={worker_handle.proc.returncode}")
        print(f"[labs run {SCENARIO_ES_TIMEOUT}] see logs: {log_path}")
        return DrillResult(ok=False, meta={"exit_code": 4}, summary={}, errors=[])

    print(f"[labs run {SCENARIO_ES_TIMEOUT}] done (now run verify/export/clean)")
    print(f"[labs run {SCENARIO_ES_TIMEOUT}] outputs: {outdir}")
    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])


@register("es_timeout.verify")
def verify_es_timeout(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_dir = resolve_run_dir(
        run_id=str(payload.get("run_id") or "").strip() or None,
        outdir=str(payload.get("outdir") or "").strip() or None,
        scenario=SCENARIO_ES_TIMEOUT,
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

    retry_before = prom_parse_counter_sum(before, "outbox_retry_scheduled_total", labels={"reason": "es_timeout"})
    retry_after = prom_parse_counter_sum(after, "outbox_retry_scheduled_total", labels={"reason": "es_timeout"})
    failed_before = prom_parse_counter_sum(before, "outbox_failed_total", labels={"reason": "es_timeout"})
    failed_after = prom_parse_counter_sum(after, "outbox_failed_total", labels={"reason": "es_timeout"})
    terminal_before = prom_parse_counter_sum(before, "outbox_terminal_failed_total", labels={"reason": "es_timeout"})
    terminal_after = prom_parse_counter_sum(after, "outbox_terminal_failed_total", labels={"reason": "es_timeout"})

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
                expected_reason_families=["timeout"],
                expected_db_reasons=["es_timeout"],
                require_db_reasons=True,
            )
            if contract_ok is not None:
                ok = bool(ok) and bool(contract_ok)

    result = {
        "scenario": SCENARIO_ES_TIMEOUT,
        "run_dir": str(run_dir),
        "worker": worker_start,
        "supply": supply,
        "supply_db_check": supply_db_check,
        "reason_contract": {
            "expected": {"metrics_reasons": ["es_timeout"], "reason_families": ["timeout"]},
            "observed": {"db_reasons": db_reason_values, "db_reason_families": db_reason_families},
            "db_reason_check": db_reason_check,
        },
        "checks": {
            "retry_delta_ge": float(min_retry_delta),
            "failed_delta_ge": float(min_failed_delta),
            "terminal_delta_le": float(max_terminal_delta),
        },
        "observed": {
            "outbox_retry_scheduled_total_reason_es_timeout": {
                "before": retry_before,
                "after": retry_after,
                "delta": delta_retry,
            },
            "outbox_failed_total_reason_es_timeout": {
                "before": failed_before,
                "after": failed_after,
                "delta": delta_failed,
            },
            "outbox_terminal_failed_total_reason_es_timeout": {
                "before": terminal_before,
                "after": terminal_after,
                "delta": delta_terminal,
            },
        },
        "ok": bool(ok),
    }
    pack_artifacts(paths=build_evidence_paths_for_dir(run_dir), result=result)

    if ok:
        print(f"[labs verify {SCENARIO_ES_TIMEOUT}] OK")
        return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])

    print(f"[labs verify {SCENARIO_ES_TIMEOUT}] FAILED")
    return DrillResult(ok=False, meta={"exit_code": 10}, summary={}, errors=[])


@register("es_timeout.clean")
def clean_es_timeout(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    outdir = payload.get("outdir")
    keep_last = payload.get("keep_last")

    if outdir:
        out_path = Path(str(outdir))
        ensure_dir(out_path)
        (out_path / "_clean.txt").write_text(
            f"scenario={SCENARIO_ES_TIMEOUT}\n" "action=noop\n" f"at={time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            encoding="utf-8",
        )

    if keep_last is not None:
        base = LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_ES_TIMEOUT
        if base.exists():
            import shutil

            runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
            for p in runs[int(keep_last) :]:
                shutil.rmtree(p, ignore_errors=True)
            print(f"[labs clean {SCENARIO_ES_TIMEOUT}] kept_last={keep_last}")
    else:
        print(f"[labs clean {SCENARIO_ES_TIMEOUT}] noop")

    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])
