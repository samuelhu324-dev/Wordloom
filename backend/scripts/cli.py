"""Minimal script router for backend/scripts.

Design goals:
- Keep it tiny and dependency-free.
- Provide a stable command namespace so people stop memorizing file names.
- Enforce consistent snapshot output locations for labs.

This is intentionally not a full-featured CLI framework.
"""

from __future__ import annotations
# 在 cli.py 顶部加（或 main 里局部 import 也行）
# 注意：cli.py 以脚本方式运行（python backend/scripts/cli.py）时，sys.path[0] 是 backend/scripts。
# 因此应从同级包 cli_app 导入，而不是 backend.scripts.cli_app。
from collections.abc import Callable

from cli_app import registry as _wg_registry
from cli_app.common import build_evidence_paths, build_evidence_paths_for_dir, pack_artifacts
from cli_app.labs.collector_down import cmd_labs_clean_collector_down as _cmd_labs_clean_collector_down_impl
from cli_app.labs.collector_down import cmd_labs_export_collector_down as _cmd_labs_export_collector_down_impl
from cli_app.labs.collector_down import cmd_labs_run_collector_down as _cmd_labs_run_collector_down_impl
from cli_app.labs.collector_down import cmd_labs_verify_collector_down as _cmd_labs_verify_collector_down_impl
from cli_app.labs.failure_drills import cmd_labs_clean as _cmd_labs_clean_impl
from cli_app.labs.failure_drills import cmd_labs_export as _cmd_labs_export_impl
from cli_app.labs.failure_drills import cmd_labs_run as _cmd_labs_run_impl
from cli_app.labs.failure_drills import cmd_labs_verify as _cmd_labs_verify_impl
from cli_app.labs.jaeger_export import cmd_labs_export_jaeger as _cmd_labs_export_jaeger_impl
from cli_app.labs.jaeger_export import export_jaeger_snapshot as _export_jaeger_snapshot
from cli_app.labs.shadow_verify import (
    cmd_labs_shadow_verify_canary_dual_write as _cmd_labs_shadow_verify_canary_dual_write_impl,
)
from cli_app.labs.shadow_verify import (
    cmd_labs_shadow_verify_chronicle_entries as _cmd_labs_shadow_verify_chronicle_entries_impl,
)
from cli_app.labs.shadow_verify import (
    cmd_labs_shadow_verify_dual_run_readiness_gate as _cmd_labs_shadow_verify_dual_run_readiness_gate_impl,
)
from cli_app.labs.shadow_verify import (
    cmd_labs_shadow_verify_dual_run_stage1 as _cmd_labs_shadow_verify_dual_run_stage1_impl,
)
from cli_app.labs.shadow_verify import (
    cmd_labs_shadow_verify_dual_run_stage2 as _cmd_labs_shadow_verify_dual_run_stage2_impl,
)
from cli_app.labs.shadow_verify import (
    cmd_labs_shadow_verify_dual_run_window as _cmd_labs_shadow_verify_dual_run_window_impl,
)
from cli_app.labs.shadow_verify import (
    cmd_labs_shadow_verify_dual_write_sampling as _cmd_labs_shadow_verify_dual_write_sampling_impl,
)
from cli_app.labs.shadow_verify import cmd_labs_shadow_verify_search_index as _cmd_labs_shadow_verify_search_index_impl
from cli_app.labs.shadow_verify import (
    cmd_labs_shadow_verify_search_index_paging_stability as _cmd_labs_shadow_verify_search_index_paging_stability_impl,
)
from cli_app.labs.shadow_verify import (
    cmd_labs_shadow_verify_search_index_write_gate as _cmd_labs_shadow_verify_search_index_write_gate_impl,
)
from cli_app.labs.shadow_verify import cmd_labs_shadow_verify_shared_keys as _cmd_labs_shadow_verify_shared_keys_impl
from cli_app.parser import build_parser as _build_parser
from cli_app.types import DrillInputs

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import bindparam, create_engine, text


REPO_ROOT = Path(__file__).resolve().parents[2]
LEGACY_SCRIPTS_DIR = REPO_ROOT / "backend" / "scripts" / "legacy"
LABS_SNAPSHOT_ROOT = REPO_ROOT / "docs" / "labs" / "_snapshot"


LAB_ID_S3A_2A_3A = "S3A-2A-3A"
LAB_ID_S2B_1A_1A = "S2B-1A-1A"
LAB_ID_S2B_1A_2A = "S2B-1A-2A"
LAB_ID_S2B_2A_1A = "S2B-2A-1A"
LAB_ID_S2B_2A_2A = "S2B-2A-2A"

SCENARIO_SHADOW_VERIFY_CHRONICLE_ENTRIES = "shadow_verify_chronicle_entries"
SCENARIO_SHADOW_VERIFY_SEARCH_INDEX = "shadow_verify_search_index"
SCENARIO_SHADOW_VERIFY_SEARCH_INDEX_WRITE_GATE = "shadow_verify_search_index_write_gate"
SCENARIO_SHADOW_VERIFY_SEARCH_INDEX_PAGING_STABILITY = "shadow_verify_search_index_paging_stability"
SCENARIO_ES_WRITE_BLOCK_4XX = "es_write_block_4xx"
SCENARIO_ES_429_INJECT = "es_429_inject"
SCENARIO_ES_DOWN_CONNECT = "es_down_connect"
SCENARIO_ES_BULK_PARTIAL = "es_bulk_partial"
SCENARIO_DB_CLAIM_CONTENTION = "db_claim_contention"
SCENARIO_STUCK_RECLAIM = "stuck_reclaim"
SCENARIO_DUPLICATE_DELIVERY = "duplicate_delivery"
SCENARIO_PROJECTION_VERSION = "projection_version"
SCENARIO_COLLECTOR_DOWN = "collector_down"

SCENARIO_SHADOW_VERIFY_SHARED_KEYS = "shadow_verify_shared_keys"
SCENARIO_SHADOW_VERIFY_DUAL_RUN_READINESS_GATE = "shadow_verify_dual_run_readiness_gate"
SCENARIO_SHADOW_VERIFY_DUAL_RUN_STAGE1 = "shadow_verify_dual_run_stage1"
SCENARIO_SHADOW_VERIFY_DUAL_RUN_STAGE2 = "shadow_verify_dual_run_stage2"
SCENARIO_SHADOW_VERIFY_DUAL_RUN_WINDOW = "shadow_verify_dual_run_window"
SCENARIO_SHADOW_VERIFY_CANARY_DUAL_WRITE = "shadow_verify_canary_dual_write"
SCENARIO_SHADOW_VERIFY_DUAL_WRITE_SAMPLING = "shadow_verify_dual_write_sampling"

# Keep in sync with backend/scripts/legacy/search_outbox_worker.py
SEARCH_OUTBOX_OBS_SCHEMA_VERSION = "labs-009-v2"


def _now_run_id() -> str:
    # local time is fine for manual runs; keep it filesystem-safe
    return time.strftime("%Y%m%dT%H%M%S")


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _read_env_file(path: Path) -> dict[str, str]:
    """Very small .env parser (KEY=VALUE, supports quotes, ignores comments)."""

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


def _default_labs_auto_run_dir(*, scenario: str, run_id: str) -> Path:
    return LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / scenario / run_id


def _default_s2b_auto_run_dir(*, lab_id: str, scenario: str, run_id: str) -> Path:
    return LABS_SNAPSHOT_ROOT / "auto" / lab_id / scenario / run_id


def _latest_child_dir(base: Path) -> Path | None:
    if not base.exists():
        return None
    children = [p for p in base.iterdir() if p.is_dir()]
    if not children:
        return None
    return sorted(children, key=lambda p: p.name, reverse=True)[0]


def _http_json(
    method: str,
    url: str,
    *,
    body: dict[str, object] | None = None,
    timeout_s: float = 5.0,
) -> tuple[int, str]:
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url=url, data=data, method=method.upper(), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:  # noqa: S310
            payload = resp.read().decode("utf-8", errors="replace")
            return int(resp.status), payload
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace") if getattr(exc, "fp", None) else str(exc)
        return int(getattr(exc, "code", 0) or 0), payload


def _es_set_index_write_block(*, es_url: str, index: str, enabled: bool) -> tuple[int, str]:
    es_url = es_url.strip().rstrip("/")
    index = index.strip()
    url = f"{es_url}/{index}/_settings"
    return _http_json("PUT", url, body={"index": {"blocks": {"write": bool(enabled)}}}, timeout_s=5.0)


def _es_create_index_if_missing(*, es_url: str, index: str) -> tuple[int, str]:
    """Create index if it does not exist.

    Returns (status, payload) from ES.
    - 200/201: created
    - 400: already exists (treated as ok by caller)
    """

    es_url = es_url.strip().rstrip("/")
    index = index.strip()
    url = f"{es_url}/{index}"
    return _http_json("PUT", url, body=None, timeout_s=5.0)


def _scrape_metrics_text(*, port: int, timeout_s: float = 2.0) -> str:
    url = f"http://localhost:{int(port)}/metrics"
    req = urllib.request.Request(url=url, headers={"Accept": "text/plain"})
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:  # noqa: S310
        return resp.read().decode("utf-8", errors="replace")


def _prom_parse_counter_sum(text: str, metric: str, *, labels: dict[str, str] | None = None) -> float:
    """Very small Prometheus text parser: sum matching samples for a counter metric."""

    want = labels or {}
    total = 0.0
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if not line.startswith(metric):
            continue

        # metric{a="b"} 123 or metric 123
        name_and_labels, *rest = line.split(None, 1)
        if not rest:
            continue
        value_str = rest[0].strip().split()[0]

        lbls: dict[str, str] = {}
        if "{" in name_and_labels and name_and_labels.endswith("}"):
            inside = name_and_labels.split("{", 1)[1][:-1]
            # naive split is ok because our labels are simple
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


def _default_labs009_expb_outdir(run_id: str) -> Path:
    return LABS_SNAPSHOT_ROOT / "manual" / "_lab-S3A-2A-3A-expB" / run_id


def _python_exe() -> str:
    # Prefer a repo-local venv if present, but only for the current OS.
    # This avoids WSL calling Windows python.exe with POSIX paths (exit code 2).
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


def _run(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> int:
    print("[scripts] run:", " ".join(cmd))
    return subprocess.call(cmd, cwd=str(cwd) if cwd else None, env=env)


def _docker_compose(*, args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    cmd = ["docker", "compose"] + args
    print("[scripts] run:", " ".join(cmd))
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, check=False)


def _prom_sum_reasons(text: str, metric: str, *, reasons: list[str]) -> float:
    return float(sum(_prom_parse_counter_sum(text, metric, labels={"reason": r}) for r in reasons))


def _extract_last_claim_batch_id(log_path: Path) -> str | None:
    if not log_path.exists():
        return None
    try:
        lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return None
    rx = re.compile(r'"claim_batch_id"\s*:\s*"([^"]+)"')
    for line in reversed(lines):
        m = rx.search(line)
        if m:
            return m.group(1)
    return None


def _with_backend_pythonpath(env: dict[str, str]) -> dict[str, str]:
    backend_path = str(REPO_ROOT / "backend")
    existing = env.get("PYTHONPATH") or ""
    parts = [p for p in existing.split(os.pathsep) if p]
    if backend_path not in parts:
        parts.insert(0, backend_path)
    env["PYTHONPATH"] = os.pathsep.join(parts)
    return env


def _parse_last_json_line(text: str) -> dict[str, object] | None:
    if not text:
        return None
    for raw in reversed(text.splitlines()):
        line = (raw or "").strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if isinstance(obj, dict):
            return obj
    return None


def _read_json_file(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None


def _cmd_labs_shadow_verify_chronicle_entries(args: argparse.Namespace) -> int:
    return _cmd_labs_shadow_verify_chronicle_entries_impl(
        args,
        lab_id=LAB_ID_S2B_1A_1A,
        scenario=SCENARIO_SHADOW_VERIFY_CHRONICLE_ENTRIES,
        now_run_id=_now_run_id,
        default_outdir=_default_s2b_auto_run_dir,
        ensure_dir=_ensure_dir,
        load_env=_load_env,
    )


def _cmd_labs_shadow_verify_search_index(args: argparse.Namespace) -> int:
    return _cmd_labs_shadow_verify_search_index_impl(
        args,
        lab_id=LAB_ID_S2B_1A_2A,
        scenario=SCENARIO_SHADOW_VERIFY_SEARCH_INDEX,
        now_run_id=_now_run_id,
        default_outdir=_default_s2b_auto_run_dir,
        ensure_dir=_ensure_dir,
        load_env=_load_env,
    )


def _cmd_labs_shadow_verify_search_index_write_gate(args: argparse.Namespace) -> int:
    return _cmd_labs_shadow_verify_search_index_write_gate_impl(
        args,
        lab_id=LAB_ID_S2B_2A_1A,
        scenario=SCENARIO_SHADOW_VERIFY_SEARCH_INDEX_WRITE_GATE,
        now_run_id=_now_run_id,
        default_outdir=_default_s2b_auto_run_dir,
        ensure_dir=_ensure_dir,
        load_env=_load_env,
    )


def _cmd_labs_shadow_verify_search_index_paging_stability(args: argparse.Namespace) -> int:
    return _cmd_labs_shadow_verify_search_index_paging_stability_impl(
        args,
        lab_id=LAB_ID_S2B_2A_2A,
        scenario=SCENARIO_SHADOW_VERIFY_SEARCH_INDEX_PAGING_STABILITY,
        now_run_id=_now_run_id,
        default_outdir=_default_s2b_auto_run_dir,
        ensure_dir=_ensure_dir,
        load_env=_load_env,
    )


def _cmd_labs_shadow_verify_shared_keys(args: argparse.Namespace) -> int:
    return _cmd_labs_shadow_verify_shared_keys_impl(
        args,
        lab_id=LAB_ID_S2B_2A_2A,
        scenario=SCENARIO_SHADOW_VERIFY_SHARED_KEYS,
        now_run_id=_now_run_id,
        default_outdir=_default_s2b_auto_run_dir,
        ensure_dir=_ensure_dir,
        load_env=_load_env,
    )


def _cmd_labs_shadow_verify_dual_run_readiness_gate(args: argparse.Namespace) -> int:
    return _cmd_labs_shadow_verify_dual_run_readiness_gate_impl(
        args,
        lab_id=LAB_ID_S2B_2A_2A,
        scenario=SCENARIO_SHADOW_VERIFY_DUAL_RUN_READINESS_GATE,
        now_run_id=_now_run_id,
        default_outdir=_default_s2b_auto_run_dir,
        ensure_dir=_ensure_dir,
        load_env=_load_env,
    )


def _cmd_labs_shadow_verify_dual_run_stage1(args: argparse.Namespace) -> int:
    return _cmd_labs_shadow_verify_dual_run_stage1_impl(
        args,
        lab_id=LAB_ID_S2B_2A_2A,
        scenario=SCENARIO_SHADOW_VERIFY_DUAL_RUN_STAGE1,
        now_run_id=_now_run_id,
        default_outdir=_default_s2b_auto_run_dir,
        ensure_dir=_ensure_dir,
        load_env=_load_env,
    )


def _cmd_labs_shadow_verify_dual_run_stage2(args: argparse.Namespace) -> int:
    return _cmd_labs_shadow_verify_dual_run_stage2_impl(
        args,
        lab_id=LAB_ID_S2B_2A_2A,
        scenario=SCENARIO_SHADOW_VERIFY_DUAL_RUN_STAGE2,
        now_run_id=_now_run_id,
        default_outdir=_default_s2b_auto_run_dir,
        ensure_dir=_ensure_dir,
        load_env=_load_env,
    )


def _cmd_labs_shadow_verify_dual_run_window(args: argparse.Namespace) -> int:
    return _cmd_labs_shadow_verify_dual_run_window_impl(
        args,
        lab_id=LAB_ID_S2B_2A_2A,
        scenario=SCENARIO_SHADOW_VERIFY_DUAL_RUN_WINDOW,
        now_run_id=_now_run_id,
        default_outdir=_default_s2b_auto_run_dir,
        ensure_dir=_ensure_dir,
        load_env=_load_env,
    )


def _cmd_labs_shadow_verify_canary_dual_write(args: argparse.Namespace) -> int:
    return _cmd_labs_shadow_verify_canary_dual_write_impl(
        args,
        lab_id=LAB_ID_S2B_2A_2A,
        scenario=SCENARIO_SHADOW_VERIFY_CANARY_DUAL_WRITE,
        now_run_id=_now_run_id,
        default_outdir=_default_s2b_auto_run_dir,
        ensure_dir=_ensure_dir,
        load_env=_load_env,
    )


def _cmd_labs_shadow_verify_dual_write_sampling(args: argparse.Namespace) -> int:
    return _cmd_labs_shadow_verify_dual_write_sampling_impl(
        args,
        lab_id=LAB_ID_S2B_2A_2A,
        scenario=SCENARIO_SHADOW_VERIFY_DUAL_WRITE_SAMPLING,
        now_run_id=_now_run_id,
        default_outdir=_default_s2b_auto_run_dir,
        ensure_dir=_ensure_dir,
        load_env=_load_env,
    )


def _cmd_labs_export_jaeger(args: argparse.Namespace) -> int:
    return _cmd_labs_export_jaeger_impl(
        args,
        default_outdir=_default_labs009_expb_outdir,
        now_run_id=_now_run_id,
        ensure_dir=_ensure_dir,
        python_exe=_python_exe,
        legacy_scripts_dir=LEGACY_SCRIPTS_DIR,
        repo_root=REPO_ROOT,
        run=_run,
    )


def _cmd_labs_expb_es429(args: argparse.Namespace) -> int:
    run_id = args.run_id or _now_run_id()
    outdir = Path(args.outdir) if args.outdir else _default_labs009_expb_outdir(run_id)

    exports_dir = outdir / "_exports"
    logs_dir = outdir / "_logs"
    metrics_dir = outdir / "_metrics"
    _ensure_dir(exports_dir)
    _ensure_dir(logs_dir)
    _ensure_dir(metrics_dir)

    # Prepare env (inherit, then override)
    env = _with_backend_pythonpath(os.environ.copy())

    # Tracing (opt-in). Default to grpc/4317 for stability.
    env.setdefault("WORDLOOM_TRACING_ENABLED", "1")
    env.setdefault("OTEL_SERVICE_NAME", args.service)
    env.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
    env.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    env.setdefault("OTEL_TRACES_SAMPLER", "always_on")

    # ES 429 injection knobs (deterministic-ish)
    if args.every_n is not None:
        env["OUTBOX_EXPERIMENT_ES_429_EVERY_N"] = str(args.every_n)
    if args.ratio is not None:
        env["OUTBOX_EXPERIMENT_ES_429_RATIO"] = str(args.ratio)
    if args.seed is not None:
        env["OUTBOX_EXPERIMENT_ES_429_SEED"] = str(args.seed)
    if args.ops:
        env["OUTBOX_EXPERIMENT_ES_429_OPS"] = args.ops

    # Optional: metrics port override (so users can scrape later)
    if args.metrics_port is not None:
        env["OUTBOX_METRICS_PORT"] = str(args.metrics_port)

    notes = outdir / "_notes.md"
    if not notes.exists():
        notes.write_text(
            "# Labs-009 ExpB (ES 429) run\n\n"
            f"run_id: {run_id}\n\n"
            "## Commands\n\n"
            "- This run was started via `backend/scripts/cli.py labs expb-es429`.\n"
            "\n## Checklist\n\n"
            "- [ ] metrics shows retry_scheduled_total{reason=\"es_429\"}\n"
            "- [ ] jaeger export contains outbox.process / projection spans\n"
            "- [ ] logs contain trace_id/span_id for representative event\n",
            encoding="utf-8",
        )

    worker = LEGACY_SCRIPTS_DIR / "search_outbox_worker.py"
    log_path = logs_dir / f"worker-{run_id}.log"

    # Run worker for a bounded duration using Python wrapper (no extra dependencies).
    # We run it in a subprocess and let the user stop it with Ctrl+C too.
    cmd = [_python_exe(), "-u", str(worker)]

    print(f"[scripts] output dir: {outdir}")
    print(f"[scripts] worker log: {log_path}")
    print(f"[scripts] duration: {args.duration}s")

    start = time.time()
    with open(log_path, "w", encoding="utf-8") as log_file:
        proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env, stdout=log_file, stderr=subprocess.STDOUT)
        try:
            while True:
                if args.duration > 0 and (time.time() - start) >= args.duration:
                    proc.terminate()
                    break
                ret = proc.poll()
                if ret is not None:
                    break
                time.sleep(0.25)
        except KeyboardInterrupt:
            proc.terminate()

        proc.wait(timeout=30)

    # Always export a small Jaeger snapshot at the end.
    _export_jaeger_snapshot(
        exports_dir=exports_dir,
        service=args.service,
        lookback=args.lookback,
        limit=int(args.limit),
        operation=None,
        outbox_event_id=None,
        claim_batch_id=None,
        python_exe=_python_exe,
        legacy_scripts_dir=LEGACY_SCRIPTS_DIR,
        repo_root=REPO_ROOT,
        run=_run,
    )

    print("[scripts] done")
    print(f"[scripts] outputs: {outdir}")
    return 0


def _cmd_labs_run_es_write_block_4xx(args: argparse.Namespace) -> int:
    return _cmd_labs_run_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_ES_WRITE_BLOCK_4XX,
        handler_base="es_write_block_4xx",
        now_run_id=_now_run_id,
        default_outdir=lambda scenario, run_id: _default_labs_auto_run_dir(scenario=scenario, run_id=run_id),
    )


def _resolve_run_dir(*, run_id: str | None, outdir: str | None, scenario: str) -> Path:
    if outdir:
        return Path(outdir)
    if run_id:
        return _default_labs_auto_run_dir(scenario=scenario, run_id=run_id)
    latest = _latest_child_dir(LABS_SNAPSHOT_ROOT / "auto" / LAB_ID_S3A_2A_3A / scenario)
    if latest is None:
        raise SystemExit(f"No runs found for scenario={scenario}")
    return latest


def _cmd_labs_verify_es_write_block_4xx(args: argparse.Namespace) -> int:
    return _cmd_labs_verify_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_ES_WRITE_BLOCK_4XX,
        handler_base="es_write_block_4xx",
        resolve_run_dir=lambda run_id, outdir, scenario: _resolve_run_dir(run_id=run_id, outdir=outdir, scenario=scenario),
    )


def _cmd_labs_export_es_write_block_4xx(args: argparse.Namespace) -> int:
    return _cmd_labs_export_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_ES_WRITE_BLOCK_4XX,
        handler_base="es_write_block_4xx",
        resolve_run_dir=lambda run_id, outdir, scenario: _resolve_run_dir(run_id=run_id, outdir=outdir, scenario=scenario),
    )


def _cmd_labs_run_es_429_inject(args: argparse.Namespace) -> int:
    return _cmd_labs_run_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_ES_429_INJECT,
        handler_base="es_429_inject",
        now_run_id=_now_run_id,
        default_outdir=lambda scenario, run_id: _default_labs_auto_run_dir(scenario=scenario, run_id=run_id),
    )


def _cmd_labs_verify_es_429_inject(args: argparse.Namespace) -> int:
    return _cmd_labs_verify_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_ES_429_INJECT,
        handler_base="es_429_inject",
        resolve_run_dir=lambda run_id, outdir, scenario: _resolve_run_dir(run_id=run_id, outdir=outdir, scenario=scenario),
    )


def _cmd_labs_run_es_down_connect(args: argparse.Namespace) -> int:
    return _cmd_labs_run_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_ES_DOWN_CONNECT,
        handler_base="es_down_connect",
        now_run_id=_now_run_id,
        default_outdir=lambda scenario, run_id: _default_labs_auto_run_dir(scenario=scenario, run_id=run_id),
    )


def _cmd_labs_verify_es_down_connect(args: argparse.Namespace) -> int:
    return _cmd_labs_verify_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_ES_DOWN_CONNECT,
        handler_base="es_down_connect",
        resolve_run_dir=lambda run_id, outdir, scenario: _resolve_run_dir(run_id=run_id, outdir=outdir, scenario=scenario),
    )


def _cmd_labs_export_es_down_connect(args: argparse.Namespace) -> int:
    return _cmd_labs_export_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_ES_DOWN_CONNECT,
        handler_base="es_down_connect",
        resolve_run_dir=lambda run_id, outdir, scenario: _resolve_run_dir(run_id=run_id, outdir=outdir, scenario=scenario),
    )


def _cmd_labs_run_collector_down(args: argparse.Namespace) -> int:
    """P1: observability failure drill - stop Jaeger OTLP collector while worker runs.

    We use the `jaeger` service in docker-compose.infra.yml as the OTLP receiver.
    Expected behavior: business processing continues; traces export is unavailable.
    """

    return _cmd_labs_run_collector_down_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_COLLECTOR_DOWN,
        handler_base="collector_down",
        now_run_id=_now_run_id,
        default_outdir=lambda scenario, run_id: _default_labs_auto_run_dir(scenario=scenario, run_id=run_id),
    )


def _cmd_labs_verify_collector_down(args: argparse.Namespace) -> int:
    return _cmd_labs_verify_collector_down_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_COLLECTOR_DOWN,
        handler_base="collector_down",
        resolve_run_dir=lambda run_id, outdir, scenario: _resolve_run_dir(run_id=run_id, outdir=outdir, scenario=scenario),
    )


def _cmd_labs_export_collector_down(args: argparse.Namespace) -> int:
    """Export evidence for collector_down.

    Jaeger is intentionally stopped, so trace export may fail. We treat that failure
    as expected and still return rc=0 after writing evidence files.
    """

    return _cmd_labs_export_collector_down_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_COLLECTOR_DOWN,
        handler_base="collector_down",
        resolve_run_dir=lambda run_id, outdir, scenario: _resolve_run_dir(run_id=run_id, outdir=outdir, scenario=scenario),
    )


def _cmd_labs_clean_collector_down(args: argparse.Namespace) -> int:
    return _cmd_labs_clean_collector_down_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        handler_base="collector_down",
        now_run_id=_now_run_id,
    )


def _cmd_labs_run_duplicate_delivery(args: argparse.Namespace) -> int:
    """ExpG: duplicate delivery / idempotency via delete-on-missing (404 noop).

    Strategy:
    1) Insert 1 upsert for a fixed entity_id and ensure a search_index row exists.
    2) Insert 2 deletes for the same entity_id (second should be a noop: ES 404).
    """

    return _cmd_labs_run_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_DUPLICATE_DELIVERY,
        handler_base="duplicate_delivery",
        now_run_id=_now_run_id,
        default_outdir=lambda scenario, run_id: _default_labs_auto_run_dir(scenario=scenario, run_id=run_id),
    )


def _cmd_labs_verify_duplicate_delivery(args: argparse.Namespace) -> int:
    return _cmd_labs_verify_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_DUPLICATE_DELIVERY,
        handler_base="duplicate_delivery",
        resolve_run_dir=lambda run_id, outdir, scenario: _resolve_run_dir(run_id=run_id, outdir=outdir, scenario=scenario),
    )


def _cmd_labs_export_duplicate_delivery(args: argparse.Namespace) -> int:
    return _cmd_labs_export_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_DUPLICATE_DELIVERY,
        handler_base="duplicate_delivery",
        resolve_run_dir=lambda run_id, outdir, scenario: _resolve_run_dir(run_id=run_id, outdir=outdir, scenario=scenario),
    )


def _cmd_labs_clean_duplicate_delivery(args: argparse.Namespace) -> int:
    return _cmd_labs_clean_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        handler_base="duplicate_delivery",
        now_run_id=_now_run_id,
    )


def _cmd_labs_run_es_bulk_partial(args: argparse.Namespace) -> int:
    return _cmd_labs_run_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_ES_BULK_PARTIAL,
        handler_base="es_bulk_partial",
        now_run_id=_now_run_id,
        default_outdir=lambda scenario, run_id: _default_labs_auto_run_dir(scenario=scenario, run_id=run_id),
    )


def _cmd_labs_verify_es_bulk_partial(args: argparse.Namespace) -> int:
    return _cmd_labs_verify_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_ES_BULK_PARTIAL,
        handler_base="es_bulk_partial",
        resolve_run_dir=lambda run_id, outdir, scenario: _resolve_run_dir(run_id=run_id, outdir=outdir, scenario=scenario),
    )


def _cmd_labs_export_es_bulk_partial(args: argparse.Namespace) -> int:
    return _cmd_labs_export_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_ES_BULK_PARTIAL,
        handler_base="es_bulk_partial",
        resolve_run_dir=lambda run_id, outdir, scenario: _resolve_run_dir(run_id=run_id, outdir=outdir, scenario=scenario),
    )


def _cmd_labs_clean_es_bulk_partial(args: argparse.Namespace) -> int:
    return _cmd_labs_clean_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        handler_base="es_bulk_partial",
        now_run_id=_now_run_id,
    )


def _cmd_labs_run_db_claim_contention(args: argparse.Namespace) -> int:
    return _cmd_labs_run_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_DB_CLAIM_CONTENTION,
        handler_base="db_claim_contention",
        now_run_id=_now_run_id,
        default_outdir=lambda scenario, run_id: _default_labs_auto_run_dir(scenario=scenario, run_id=run_id),
    )


def _cmd_labs_verify_db_claim_contention(args: argparse.Namespace) -> int:
    return _cmd_labs_verify_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_DB_CLAIM_CONTENTION,
        handler_base="db_claim_contention",
        resolve_run_dir=lambda run_id, outdir, scenario: _resolve_run_dir(run_id=run_id, outdir=outdir, scenario=scenario),
    )


def _cmd_labs_export_db_claim_contention(args: argparse.Namespace) -> int:
    return _cmd_labs_export_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_DB_CLAIM_CONTENTION,
        handler_base="db_claim_contention",
        resolve_run_dir=lambda run_id, outdir, scenario: _resolve_run_dir(run_id=run_id, outdir=outdir, scenario=scenario),
    )


def _cmd_labs_clean_db_claim_contention(args: argparse.Namespace) -> int:
    return _cmd_labs_clean_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        handler_base="db_claim_contention",
        now_run_id=_now_run_id,
    )


def _cmd_labs_run_stuck_reclaim(args: argparse.Namespace) -> int:
    return _cmd_labs_run_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_STUCK_RECLAIM,
        handler_base="stuck_reclaim",
        now_run_id=_now_run_id,
        default_outdir=lambda scenario, run_id: _default_labs_auto_run_dir(scenario=scenario, run_id=run_id),
    )


def _cmd_labs_verify_stuck_reclaim(args: argparse.Namespace) -> int:
    return _cmd_labs_verify_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_STUCK_RECLAIM,
        handler_base="stuck_reclaim",
        resolve_run_dir=lambda run_id, outdir, scenario: _resolve_run_dir(run_id=run_id, outdir=outdir, scenario=scenario),
    )


def _cmd_labs_export_stuck_reclaim(args: argparse.Namespace) -> int:
    return _cmd_labs_export_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_STUCK_RECLAIM,
        handler_base="stuck_reclaim",
        resolve_run_dir=lambda run_id, outdir, scenario: _resolve_run_dir(run_id=run_id, outdir=outdir, scenario=scenario),
    )


def _cmd_labs_clean_stuck_reclaim(args: argparse.Namespace) -> int:
    return _cmd_labs_clean_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        handler_base="stuck_reclaim",
        now_run_id=_now_run_id,
    )


def _cmd_labs_clean_es_down_connect(args: argparse.Namespace) -> int:
    return _cmd_labs_clean_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        handler_base="es_down_connect",
        now_run_id=_now_run_id,
    )


def _cmd_labs_export_es_429_inject(args: argparse.Namespace) -> int:
    return _cmd_labs_export_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_ES_429_INJECT,
        handler_base="es_429_inject",
        resolve_run_dir=lambda run_id, outdir, scenario: _resolve_run_dir(run_id=run_id, outdir=outdir, scenario=scenario),
    )


def _cmd_labs_clean_es_429_inject(args: argparse.Namespace) -> int:
    return _cmd_labs_clean_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        handler_base="es_429_inject",
        now_run_id=_now_run_id,
    )


def _cmd_labs_clean_es_write_block_4xx(args: argparse.Namespace) -> int:
    return _cmd_labs_clean_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        handler_base="es_write_block_4xx",
        now_run_id=_now_run_id,
    )


def _cmd_labs_run_projection_version(args: argparse.Namespace) -> int:
    return _cmd_labs_run_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_PROJECTION_VERSION,
        handler_base="projection_version",
        now_run_id=_now_run_id,
        default_outdir=lambda scenario, run_id: _default_labs_auto_run_dir(scenario=scenario, run_id=run_id),
    )


def _cmd_labs_verify_projection_version(args: argparse.Namespace) -> int:
    return _cmd_labs_verify_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_PROJECTION_VERSION,
        handler_base="projection_version",
        resolve_run_dir=lambda run_id, outdir, scenario: _resolve_run_dir(run_id=run_id, outdir=outdir, scenario=scenario),
        fallback_exit_code=lambda ok: 0 if ok else 2,
    )


def _cmd_labs_export_projection_version(args: argparse.Namespace) -> int:
    return _cmd_labs_export_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        scenario=SCENARIO_PROJECTION_VERSION,
        handler_base="projection_version",
        resolve_run_dir=lambda run_id, outdir, scenario: _resolve_run_dir(run_id=run_id, outdir=outdir, scenario=scenario),
        fallback_exit_code=lambda ok: 0 if ok else 2,
    )


def _cmd_labs_clean_projection_version(args: argparse.Namespace) -> int:
    return _cmd_labs_clean_impl(
        args,
        scope_id=LAB_ID_S3A_2A_3A,
        handler_base="projection_version",
        now_run_id=_now_run_id,
    )


def _build_argparse_callbacks() -> dict[str, Callable[[argparse.Namespace], int]]:
    names = [
        "_cmd_labs_export_jaeger",
        "_cmd_labs_shadow_verify_chronicle_entries",
        "_cmd_labs_shadow_verify_search_index",
        "_cmd_labs_shadow_verify_search_index_write_gate",
        "_cmd_labs_shadow_verify_search_index_paging_stability",
        "_cmd_labs_shadow_verify_shared_keys",
        "_cmd_labs_shadow_verify_dual_run_readiness_gate",
        "_cmd_labs_shadow_verify_dual_run_stage1",
        "_cmd_labs_shadow_verify_dual_run_stage2",
        "_cmd_labs_shadow_verify_dual_run_window",
        "_cmd_labs_shadow_verify_canary_dual_write",
        "_cmd_labs_shadow_verify_dual_write_sampling",
        "_cmd_labs_expb_es429",
        "_cmd_labs_run_es_write_block_4xx",
        "_cmd_labs_run_es_429_inject",
        "_cmd_labs_run_es_down_connect",
        "_cmd_labs_run_collector_down",
        "_cmd_labs_run_es_bulk_partial",
        "_cmd_labs_run_db_claim_contention",
        "_cmd_labs_run_stuck_reclaim",
        "_cmd_labs_run_duplicate_delivery",
        "_cmd_labs_run_projection_version",
        "_cmd_labs_verify_es_write_block_4xx",
        "_cmd_labs_verify_es_429_inject",
        "_cmd_labs_verify_es_down_connect",
        "_cmd_labs_verify_collector_down",
        "_cmd_labs_verify_es_bulk_partial",
        "_cmd_labs_verify_db_claim_contention",
        "_cmd_labs_verify_stuck_reclaim",
        "_cmd_labs_verify_duplicate_delivery",
        "_cmd_labs_verify_projection_version",
        "_cmd_labs_export_es_write_block_4xx",
        "_cmd_labs_export_es_429_inject",
        "_cmd_labs_export_es_down_connect",
        "_cmd_labs_export_collector_down",
        "_cmd_labs_export_es_bulk_partial",
        "_cmd_labs_export_db_claim_contention",
        "_cmd_labs_export_stuck_reclaim",
        "_cmd_labs_export_duplicate_delivery",
        "_cmd_labs_export_projection_version",
        "_cmd_labs_clean_es_write_block_4xx",
        "_cmd_labs_clean_es_429_inject",
        "_cmd_labs_clean_es_down_connect",
        "_cmd_labs_clean_collector_down",
        "_cmd_labs_clean_es_bulk_partial",
        "_cmd_labs_clean_db_claim_contention",
        "_cmd_labs_clean_stuck_reclaim",
        "_cmd_labs_clean_duplicate_delivery",
        "_cmd_labs_clean_projection_version",
    ]
    return {name: globals()[name] for name in names}


def build_parser() -> argparse.ArgumentParser:
    return _build_parser(callbacks=_build_argparse_callbacks())


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # 1) 确保内置 scenarios 被 import 并注册
    _wg_registry.load_builtin_scenarios()

    # 2) 识别 scenario：统一兼容 write_gate_scenario / scenario + _ / - 命名风格
    raw_scenario = getattr(args, "write_gate_scenario", None) or getattr(args, "scenario", None)
    scenario: str | None = None
    scenario_candidates: list[str] = []
    if isinstance(raw_scenario, str) and raw_scenario.strip():
        scenario = raw_scenario.strip()
        scenario_candidates.append(scenario)
        if "-" in scenario:
            scenario_candidates.append(scenario.replace("-", "_"))
        if "_" in scenario:
            scenario_candidates.append(scenario.replace("_", "-"))

    # 去重并保持顺序
    seen: set[str] = set()
    scenario_candidates = [s for s in scenario_candidates if not (s in seen or seen.add(s))]

    # 3) 只要匹配到“新架构的 scenario”，就抢先执行并退出（不走 args.func）
    if scenario_candidates:
        handler = None
        matched_scenario: str | None = None
        for candidate in scenario_candidates:
            try:
                handler = _wg_registry.get(candidate)
                matched_scenario = candidate
                break
            except KeyError:
                continue

        if handler is not None:
            scenario = matched_scenario or scenario_candidates[0]
            scope_id = getattr(args, "scope_id", None) or "S2B"
            run_id = getattr(args, "run_id", None) or "local"

            # pydantic 输入边界：自动透传 argparse 字段（extra=allow）
            input_payload = {k: v for k, v in vars(args).items() if k not in {"func"}}
            input_payload.update(
                {
                    "scenario": scenario,
                    "scope_id": scope_id,
                    "run_id": run_id,
                    "timeout_s": getattr(args, "timeout_s", None),
                    "sampling": getattr(args, "sampling", None),
                }
            )
            inputs = DrillInputs.model_validate(input_payload)

            result = handler(inputs)

            # 4) 按你的证据 contract 落盘：_result.json + summary.json（先做最小闭环）
            outdir_arg = getattr(args, "outdir", None)
            if outdir_arg:
                paths = build_evidence_paths_for_dir(Path(str(outdir_arg)))
            else:
                paths = build_evidence_paths(scope_id=inputs.scope_id, scenario=inputs.scenario, run_id=inputs.run_id)

            # Keep legacy evidence structure: _result.json is the scenario's meta dict.
            pack_artifacts(
                paths=paths,
                result=result.meta,
                summary=result.summary,
                zip_when="on_failure",
                zip_path=paths.snapshot_dir / "evidence.zip",
            )

            return 0 if result.ok else 2

    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
