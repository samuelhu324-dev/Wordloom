"""S2D-1C/P2-C1-S2: third projection onboarding runner (skeleton).

This script orchestrates the S2D-1C labs for the legacy projection
`search_index_to_elastic` by running them as a single onboarding
"套餐" and appending a summary record under `artifacts/s2d-runs.json`.

In v1 the underlying labs are skeletons (known red): they produce
structured `_result.json` evidence but always report `ok=false`.
Later cycles (P2/C2+) can reuse the same runner once the labs are
upgraded with minimal real logic and can report `ok=true` for a
happy path.

Exit codes:
- 0: all scenarios ok
- 2: at least one scenario failed or contract (artifacts) missing
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BACKFILL_SCRIPT = "backend/scripts/labs/s2d1c_search_index_to_elastic_backfill_smoke.py"
HARNESS_SCRIPT = "backend/scripts/labs/s2d1c_search_index_to_elastic_harness_drill.py"

BACKFILL_SCENARIO_ID = "s2d1c_search_index_to_elastic_backfill_smoke"
HARNESS_SCENARIO_ID = "s2d1c_search_index_to_elastic_harness_drill"


def _utc_now_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def _default_run_id() -> str:
    # Human-friendly default, stable enough for snapshot paths.
    return time.strftime("%Y%m%d-%H%M%S")


def _git_head_sha() -> str:
    # Best-effort; do not fail the run if git/pip is unavailable.
    try:
        subprocess.check_output([sys.executable, "-m", "pip", "--version"], text=True)
    except Exception:
        pass
    try:
        sha = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
        return sha
    except Exception:
        return ""


@dataclass(frozen=True)
class ScenarioRun:
    scenario_id: str
    script: str
    run_dir: str
    ok: bool
    exit_code: int


@dataclass(frozen=True)
class S2DRunRecord:
    log_id: str
    phase: str
    cycle: str
    step: str
    head_sha: str
    run_id: str
    database_url: str
    created_at: str
    ok: bool
    scenarios: list[ScenarioRun]


def _load_ok_from_result(path: Path) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return bool(data.get("ok"))
    except Exception:
        return False


def _run_lab(script: str, *, database_url: str, run_id: str, outdir: Path) -> tuple[int, bool]:
    outdir.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        script,
        "--database-url",
        database_url,
        "--run-id",
        run_id,
        "--outdir",
        str(outdir),
    ]

    print(f"[S2D-1C] running lab: script={script} outdir={outdir}")
    completed = subprocess.run(cmd, text=True)
    rc = int(completed.returncode)

    result_path = outdir / "_result.json"
    ok = rc == 0 and result_path.is_file() and _load_ok_from_result(result_path)

    print(f"[S2D-1C] lab finished: script={script} rc={rc} ok={ok}")
    return rc, ok


def _append_run_record(path: Path, record: S2DRunRecord) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.is_file():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(existing, list):
                existing = []
        except Exception:
            existing = []
    else:
        existing = []

    payload = asdict(record)
    for sc in payload.get("scenarios", []):
        if isinstance(sc, dict) and "run_dir" in sc:
            sc["run_dir"] = str(sc["run_dir"]).replace("\\", "/")

    existing.append(payload)
    path.write_text(
        json.dumps(existing, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="S2D-1C third projection onboarding runner (skeleton)",
    )
    p.add_argument(
        "--database-url",
        required=True,
        help="SQLAlchemy-style DATABASE_URL for dev/test Postgres",
    )
    p.add_argument(
        "--run-id",
        required=False,
        help="Optional explicit run id (default: YYYYMMDD-HHMMSS)",
    )
    p.add_argument(
        "--snapshot-root",
        required=False,
        default="docs/labs/_snapshot/auto",
        help=(
            "Root directory for lab snapshot outputs "
            "(default: docs/labs/_snapshot/auto)"
        ),
    )
    p.add_argument(
        "--phase",
        required=False,
        default="P2",
        help="Phase id for artifacts/s2d-runs.json (default: P2)",
    )
    p.add_argument(
        "--cycle",
        required=False,
        default="C1",
        help="Cycle id for artifacts/s2d-runs.json (default: C1)",
    )
    p.add_argument(
        "--step",
        required=False,
        default="S2",
        help="Step id for artifacts/s2d-runs.json (default: S2)",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    database_url = str(args.database_url).strip()
    run_id = str(args.run_id).strip() if args.run_id else _default_run_id()
    snapshot_root = Path(str(args.snapshot_root)).resolve()

    phase = str(args.phase).strip() or "P2"
    cycle = str(args.cycle).strip() or "C1"
    step = str(args.step).strip() or "S2"

    head_sha = _git_head_sha()

    backfill_outdir = snapshot_root / BACKFILL_SCENARIO_ID / run_id
    harness_outdir = snapshot_root / HARNESS_SCENARIO_ID / run_id

    backfill_rc, backfill_ok = _run_lab(
        BACKFILL_SCRIPT,
        database_url=database_url,
        run_id=run_id,
        outdir=backfill_outdir,
    )

    harness_rc, harness_ok = _run_lab(
        HARNESS_SCRIPT,
        database_url=database_url,
        run_id=run_id,
        outdir=harness_outdir,
    )

    scenarios = [
        ScenarioRun(
            scenario_id=BACKFILL_SCENARIO_ID,
            script=BACKFILL_SCRIPT,
            run_dir=str(backfill_outdir),
            ok=backfill_ok,
            exit_code=backfill_rc,
        ),
        ScenarioRun(
            scenario_id=HARNESS_SCENARIO_ID,
            script=HARNESS_SCRIPT,
            run_dir=str(harness_outdir),
            ok=harness_ok,
            exit_code=harness_rc,
        ),
    ]

    overall_ok = backfill_ok and harness_ok

    record = S2DRunRecord(
        log_id="S2D-1C",
        phase=phase,
        cycle=cycle,
        step=step,
        head_sha=head_sha,
        run_id=run_id,
        database_url=database_url,
        created_at=_utc_now_str(),
        ok=overall_ok,
        scenarios=scenarios,
    )

    artifacts_path = Path("artifacts/s2d-runs.json").resolve()
    _append_run_record(artifacts_path, record)

    print("[S2D-1C] onboarding skeleton run summary:")
    print(json.dumps(asdict(record), ensure_ascii=False, indent=2))

    return 0 if overall_ok else 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
