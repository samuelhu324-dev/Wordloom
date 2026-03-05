from __future__ import annotations

import argparse
import os
import subprocess
import time
from pathlib import Path
from typing import Callable

from cli_app import runtime
from cli_app.labs import shared as _labs_shared

from .jaeger_export import export_jaeger_snapshot


def cmd_labs_expb_es429(
    args: argparse.Namespace,
    *,
    now_run_id: Callable[[], str] = _labs_shared.now_run_id,
    default_outdir: Callable[[str], Path] = _labs_shared.default_labs009_expb_outdir,
    ensure_dir: Callable[[Path], None] = _labs_shared.ensure_dir,
    with_backend_pythonpath: Callable[[dict[str, str]], dict[str, str]] = runtime.with_backend_pythonpath,
    python_exe: Callable[[], str] = runtime.python_exe,
    legacy_scripts_dir: Path = runtime.LEGACY_SCRIPTS_DIR,
    repo_root: Path = runtime.REPO_ROOT,
    run: Callable[..., int] = runtime.run,
) -> int:
    run_id = args.run_id or now_run_id()
    outdir = Path(args.outdir) if args.outdir else default_outdir(run_id)

    exports_dir = outdir / "_exports"
    logs_dir = outdir / "_logs"
    metrics_dir = outdir / "_metrics"
    ensure_dir(exports_dir)
    ensure_dir(logs_dir)
    ensure_dir(metrics_dir)

    env = with_backend_pythonpath(os.environ.copy())

    env.setdefault("WORDLOOM_TRACING_ENABLED", "1")
    env.setdefault("OTEL_SERVICE_NAME", args.service)
    env.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
    env.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    env.setdefault("OTEL_TRACES_SAMPLER", "always_on")

    if args.every_n is not None:
        env["OUTBOX_EXPERIMENT_ES_429_EVERY_N"] = str(args.every_n)
    if args.ratio is not None:
        env["OUTBOX_EXPERIMENT_ES_429_RATIO"] = str(args.ratio)
    if args.seed is not None:
        env["OUTBOX_EXPERIMENT_ES_429_SEED"] = str(args.seed)
    if args.ops:
        env["OUTBOX_EXPERIMENT_ES_429_OPS"] = args.ops

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

    worker = repo_root / "backend" / "scripts" / "search_outbox_worker.py"
    log_path = logs_dir / f"worker-{run_id}.log"

    cmd = [python_exe(), "-u", str(worker)]

    print(f"[scripts] output dir: {outdir}")
    print(f"[scripts] worker log: {log_path}")
    print(f"[scripts] duration: {args.duration}s")

    start = time.time()
    with open(log_path, "w", encoding="utf-8") as log_file:
        proc = subprocess.Popen(
            cmd,
            cwd=str(repo_root),
            env=env,
            stdout=log_file,
            stderr=subprocess.STDOUT,
        )
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

    export_jaeger_snapshot(
        exports_dir=exports_dir,
        service=args.service,
        lookback=args.lookback,
        limit=int(args.limit),
        operation=None,
        outbox_event_id=None,
        claim_batch_id=None,
        python_exe=python_exe,
        legacy_scripts_dir=legacy_scripts_dir,
        repo_root=repo_root,
        run=run,
    )

    print("[scripts] done")
    print(f"[scripts] outputs: {outdir}")
    return 0
