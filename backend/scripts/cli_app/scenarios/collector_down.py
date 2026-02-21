from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from sqlalchemy import create_engine, text

from ..common import REPO_ROOT
from ..registry import register
from ..types import DrillInputs, DrillResult


LABS_SNAPSHOT_ROOT = REPO_ROOT / "docs" / "labs" / "_snapshot"
LAB_ID_S3A_2A_3A = "S3A-2A-3A"
SCENARIO_COLLECTOR_DOWN = "collector_down"
LEGACY_SCRIPTS_DIR = REPO_ROOT / "backend" / "scripts" / "legacy"


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _read_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        raise FileNotFoundError(str(path))

    env: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if (len(value) >= 2) and ((value[0] == value[-1] == '"') or (value[0] == value[-1] == "'")):
            value = value[1:-1]
        env[key] = value
    return env


def _load_env(*, env_file: str | None) -> dict[str, str]:
    env = os.environ.copy()
    if env_file:
        env_path = (REPO_ROOT / env_file).resolve() if not Path(env_file).is_absolute() else Path(env_file)
        env.update(_read_env_file(env_path))
    return env


def _with_backend_pythonpath(env: dict[str, str]) -> dict[str, str]:
    backend_path = str(REPO_ROOT / "backend")
    existing = env.get("PYTHONPATH") or ""
    parts = [p for p in existing.split(os.pathsep) if p]
    if backend_path not in parts:
        parts.insert(0, backend_path)
    env["PYTHONPATH"] = os.pathsep.join(parts)
    return env


def _default_labs_auto_run_dir(*, scenario: str, run_id: str) -> Path:
    return LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / scenario / run_id


def _latest_child_dir(base: Path) -> Path | None:
    if not base.exists():
        return None
    children = [p for p in base.iterdir() if p.is_dir()]
    if not children:
        return None
    return sorted(children, key=lambda p: p.name, reverse=True)[0]


def _resolve_run_dir(*, run_id: str | None, outdir: str | None, scenario: str) -> Path:
    if outdir:
        return Path(outdir)
    if run_id:
        return _default_labs_auto_run_dir(scenario=scenario, run_id=run_id)
    latest = _latest_child_dir(LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / scenario)
    if latest is None:
        raise SystemExit(f"No runs found for scenario={scenario}")
    return latest


def _scrape_metrics_text(*, port: int, timeout_s: float = 2.0) -> str:
    url = f"http://localhost:{int(port)}/metrics"
    req = urllib.request.Request(url=url, headers={"Accept": "text/plain"})
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:  # noqa: S310
        return resp.read().decode("utf-8", errors="replace")


def _prom_parse_counter_sum(text: str, metric: str, *, labels: dict[str, str] | None = None) -> float:
    want = labels or {}
    total = 0.0
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if not line.startswith(metric):
            continue

        name_and_labels, *rest = line.split(None, 1)
        if not rest:
            continue
        value_str = rest[0].strip().split()[0]

        lbls: dict[str, str] = {}
        if "{" in name_and_labels and name_and_labels.endswith("}"):
            inside = name_and_labels.split("{", 1)[1][:-1]
            for part in inside.split(","):
                part = part.strip()
                if not part or "=" not in part:
                    continue
                k, v = part.split("=", 1)
                k = k.strip()
                v = v.strip()
                if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
                    v = v[1:-1]
                lbls[k] = v

        ok = True
        for k, v in want.items():
            if lbls.get(k) != v:
                ok = False
                break
        if not ok:
            continue

        try:
            total += float(value_str)
        except ValueError:
            continue

    return float(total)


def _python_exe() -> str:
    if os.getenv("VIRTUAL_ENV"):
        return sys.executable

    if os.name == "nt":
        win_venv = REPO_ROOT / ".venv" / "Scripts" / "python.exe"
        if win_venv.exists():
            return str(win_venv)
        return sys.executable

    unix_venv = REPO_ROOT / ".venv" / "bin" / "python"
    if unix_venv.exists():
        return str(unix_venv)
    return sys.executable


def _docker_compose(*, args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    cmd = ["docker", "compose"] + args
    print("[scripts] run:", " ".join(cmd))
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, check=False)


@register("collector_down.run")
def run_collector_down(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    run_id = str(payload.get("run_id") or "").strip()
    outdir = Path(str(payload.get("outdir") or "").strip())
    env_file = payload.get("env_file")
    service = payload.get("service")
    duration = int(payload.get("duration") or 0)
    metrics_port = int(payload.get("metrics_port") or 0)
    scrape_delay = float(payload.get("scrape_delay") or 0.0)
    op = payload.get("op")

    logs_dir = outdir / "_logs"
    metrics_dir = outdir / "_metrics"
    exports_dir = outdir / "_exports"
    _ensure_dir(logs_dir)
    _ensure_dir(metrics_dir)
    _ensure_dir(exports_dir)

    env = _with_backend_pythonpath(_load_env(env_file=str(env_file) if env_file else None))

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
    (outdir / "_recipe.json").write_text(json.dumps(recipe, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] outdir: {outdir}")

    stop_proc = _docker_compose(args=["-f", compose_file, "stop", "jaeger"], cwd=REPO_ROOT)
    (outdir / "_inject_jaeger_stop.stdout.txt").write_text(stop_proc.stdout or "", encoding="utf-8")
    (outdir / "_inject_jaeger_stop.stderr.txt").write_text(stop_proc.stderr or "", encoding="utf-8")
    (outdir / "_inject_jaeger_stop.exitcode.txt").write_text(str(int(stop_proc.returncode)) + "\n", encoding="utf-8")
    if stop_proc.returncode != 0:
        print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] failed to stop jaeger: rc={stop_proc.returncode}")
        return DrillResult(ok=False, meta={"exit_code": 2}, summary={}, errors=[])

    worker = LEGACY_SCRIPTS_DIR / "search_outbox_worker.py"
    log_path = logs_dir / f"worker-{run_id}.log"
    cmd = [_python_exe(), "-u", str(worker)]

    print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] worker log: {log_path}")

    metrics_before_path = metrics_dir / "metrics-before.txt"
    metrics_after_path = metrics_dir / "metrics-after.txt"

    inserter = REPO_ROOT / "backend" / "scripts" / "labs" / "labs_009_insert_search_outbox_pending.py"
    if not inserter.exists():
        inserter = LEGACY_SCRIPTS_DIR / "labs_009_insert_search_outbox_pending.py"

    start = time.time()
    stopped_by_controller = False
    with open(log_path, "w", encoding="utf-8") as log_file:
        worker_proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env, stdout=log_file, stderr=subprocess.STDOUT)
        try:
            time.sleep(max(0.5, float(scrape_delay)))
            try:
                metrics_before = _scrape_metrics_text(port=int(metrics_port), timeout_s=4.0)
                metrics_before_path.write_text(metrics_before, encoding="utf-8")
            except Exception as exc:  # noqa: BLE001
                metrics_before_path.write_text(f"scrape_failed: {type(exc).__name__}: {exc}\n", encoding="utf-8")

            trigger_env = env.copy()
            trigger_env["OUTBOX_OP"] = str(op)
            trigger_env.setdefault("OUTBOX_CREATE_SEARCH_INDEX_ROW", "1")
            trigger_env.setdefault("OUTBOX_EVENT_VERSION", "0")

            proc = subprocess.run(
                [_python_exe(), str(inserter)],
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
                print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] failed to insert outbox event: rc={proc.returncode}")
                worker_proc.terminate()
                worker_proc.wait(timeout=30)
                return DrillResult(ok=False, meta={"exit_code": 3}, summary={}, errors=[])

            outbox_event_id = (proc.stdout or "").strip().splitlines()[-1].strip()
            (outdir / "_outbox_event_id.txt").write_text(outbox_event_id + "\n", encoding="utf-8")
            print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] outbox_event_id: {outbox_event_id}")

            while True:
                if duration > 0 and (time.time() - start) >= duration:
                    try:
                        metrics_after = _scrape_metrics_text(port=int(metrics_port), timeout_s=4.0)
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
                        metrics_after = _scrape_metrics_text(port=int(metrics_port), timeout_s=4.0)
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
        print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] worker exited early: rc={worker_proc.returncode}")
        print(f"[labs run {SCENARIO_COLLECTOR_DOWN}] see logs: {log_path}")
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

    run_dir = _resolve_run_dir(run_id=run_id, outdir=str(outdir) if outdir else None, scenario=SCENARIO_COLLECTOR_DOWN)
    metrics_dir = run_dir / "_metrics"

    before_path = metrics_dir / "metrics-before.txt"
    after_path = metrics_dir / "metrics-after.txt"

    before = before_path.read_text(encoding="utf-8") if before_path.exists() else ""
    after = after_path.read_text(encoding="utf-8") if after_path.exists() else ""

    before_scrape_ok = "scrape_failed" not in before
    after_scrape_ok = "scrape_failed" not in after

    processed_before = _prom_parse_counter_sum(before, "outbox_processed_total")
    processed_after = _prom_parse_counter_sum(after, "outbox_processed_total")
    failed_before = _prom_parse_counter_sum(before, "outbox_failed_total")
    failed_after = _prom_parse_counter_sum(after, "outbox_failed_total")

    delta_processed = processed_after - processed_before
    delta_failed = failed_after - failed_before

    outbox_event_id_path = run_dir / "_outbox_event_id.txt"
    outbox_event_id = outbox_event_id_path.read_text(encoding="utf-8").strip() if outbox_event_id_path.exists() else None

    db_observed: dict[str, object] = {}
    db_ok = False
    try:
        recipe_env_file = None
        recipe_path = run_dir / "_recipe.json"
        if recipe_path.exists():
            try:
                recipe = json.loads(recipe_path.read_text(encoding="utf-8"))
                recipe_env_file = (recipe or {}).get("env_file")
            except Exception:
                recipe_env_file = None

        env = _load_env(env_file=str(recipe_env_file) if recipe_env_file else None)
        database_url = (env.get("DATABASE_URL") or "").strip()
        if database_url and outbox_event_id:
            engine = create_engine(database_url, pool_pre_ping=True)
            with engine.connect() as conn:
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
        },
        "ok": bool(ok),
    }
    (run_dir / "_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

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

    run_dir = _resolve_run_dir(run_id=run_id, outdir=str(outdir) if outdir else None, scenario=SCENARIO_COLLECTOR_DOWN)
    exports_dir = run_dir / "_exports"
    _ensure_dir(exports_dir)

    outbox_event_id_path = run_dir / "_outbox_event_id.txt"
    outbox_event_id = outbox_event_id_path.read_text(encoding="utf-8").strip() if outbox_event_id_path.exists() else None

    cmd = [
        _python_exe(),
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
    start_proc = _docker_compose(args=["-f", compose_file, "start", "jaeger"], cwd=REPO_ROOT)
    print(f"[labs clean {SCENARIO_COLLECTOR_DOWN}] start jaeger: rc={start_proc.returncode}")

    if outdir:
        outdir_path = Path(str(outdir))
        _ensure_dir(outdir_path)
        (outdir_path / "_clean.txt").write_text(
            f"scenario={SCENARIO_COLLECTOR_DOWN}\n" "action=start_jaeger\n" f"at={time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            encoding="utf-8",
        )
        (outdir_path / "_clean_jaeger_start.stdout.txt").write_text(start_proc.stdout or "", encoding="utf-8")
        (outdir_path / "_clean_jaeger_start.stderr.txt").write_text(start_proc.stderr or "", encoding="utf-8")
        (outdir_path / "_clean_jaeger_start.exitcode.txt").write_text(str(int(start_proc.returncode)) + "\n", encoding="utf-8")

    if keep_last is not None:
        base = LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / SCENARIO_COLLECTOR_DOWN
        if base.exists():
            runs = sorted([p for p in base.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
            for p in runs[int(keep_last) :]:
                shutil.rmtree(p, ignore_errors=True)
            print(f"[labs clean {SCENARIO_COLLECTOR_DOWN}] kept_last={keep_last}")

    return DrillResult(ok=True, meta={"exit_code": 0}, summary={}, errors=[])
