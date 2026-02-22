from __future__ import annotations

import argparse
from collections.abc import Callable
from pathlib import Path

from cli_app import runtime
from cli_app.labs import shared as _labs_shared


def export_jaeger_snapshot(
    *,
    exports_dir: Path,
    service: str,
    lookback: str,
    limit: int,
    operation: str | None,
    outbox_event_id: str | None,
    claim_batch_id: str | None,
    python_exe: Callable[[], str] = runtime.python_exe,
    legacy_scripts_dir: Path = runtime.LEGACY_SCRIPTS_DIR,
    repo_root: Path = runtime.REPO_ROOT,
    run: Callable[[list[str]], int] | Callable[[list[str], Path], int] | Callable[..., int] = runtime.run,
) -> int:
    script = legacy_scripts_dir / "labs_009_export_jaeger.py"

    cmd: list[str] = [
        python_exe(),
        str(script),
        "--outdir",
        str(exports_dir),
        "--service",
        service,
        "--lookback",
        lookback,
        "--limit",
        str(int(limit)),
    ]

    if operation:
        cmd += ["--operation", operation]

    if outbox_event_id:
        cmd += ["--outbox-event-id", outbox_event_id]

    if claim_batch_id:
        cmd += ["--claim-batch-id", claim_batch_id]

    # We intentionally pass cwd for parity with legacy behavior.
    return int(run(cmd, cwd=repo_root))  # type: ignore[call-arg]


def cmd_labs_export_jaeger(
    args: argparse.Namespace,
    *,
    default_outdir: Callable[[str], Path] = _labs_shared.default_labs009_expb_outdir,
    now_run_id: Callable[[], str] = _labs_shared.now_run_id,
    ensure_dir: Callable[[Path], None] = _labs_shared.ensure_dir,
    python_exe: Callable[[], str] = runtime.python_exe,
    legacy_scripts_dir: Path = runtime.LEGACY_SCRIPTS_DIR,
    repo_root: Path = runtime.REPO_ROOT,
    run: Callable[[list[str]], int] | Callable[[list[str], Path], int] | Callable[..., int] = runtime.run,
) -> int:
    outdir = Path(args.outdir) if args.outdir else default_outdir(now_run_id())
    exports_dir = outdir / "_exports"
    ensure_dir(exports_dir)

    return export_jaeger_snapshot(
        exports_dir=exports_dir,
        service=args.service,
        lookback=args.lookback,
        limit=int(args.limit),
        operation=(args.operation or None),
        outbox_event_id=(args.outbox_event_id or None),
        claim_batch_id=(args.claim_batch_id or None),
        python_exe=python_exe,
        legacy_scripts_dir=legacy_scripts_dir,
        repo_root=repo_root,
        run=run,
    )
