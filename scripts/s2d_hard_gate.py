"""S2D-3A/P1-C1-S1: local S2D hard gate runner.

This script provides a thin hard gate entrypoint around one or more
projection onboarding "suites". In v1 it only knows how to run the
S2D-1A sample onboarding package, but the structure allows additional
suites to be added later.

Semantics (v1):
- Accepts a dev/test DATABASE_URL (CLI flag or env)
- Runs the S2D-1A onboarding package script once with a fresh run_id
- Reads the appended record from ``artifacts/s2d-runs.json``
- Exits with 0 if the onboarding record reports ``ok=true``, else 2

Exit codes:
- 0: all required suites ok
- 2: at least one required suite failed or evidence is missing/invalid
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ONBOARDING_SCRIPT = "scripts/projections/s2d_1a_p3c1s1_sample_onboarding.py"
S2D_RUNS_PATH = Path("artifacts/s2d-runs.json")

S2D_1A_LOG_ID = "S2D-1A"
S2D_1A_SUITE_ID = "s2d-1a-sample-onboarding"


def _utc_now_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def _default_run_id() -> str:
    """Human-friendly default run id, stable enough for snapshot paths."""

    return time.strftime("%Y%m%d-%H%M%S")


@dataclass(frozen=True)
class SuiteResult:
    suite_id: str
    log_id: str
    run_id: str
    ok: bool
    exit_code: int
    reason: str
    record: dict[str, Any] | None


@dataclass(frozen=True)
class HardGateSummary:
    log_id: str
    phase: str
    cycle: str
    step: str
    created_at: str
    database_url: str
    overall_ok: bool
    suites: list[SuiteResult]


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="S2D hard gate local runner (v1)")
    parser.add_argument(
        "--database-url",
        dest="database_url",
        default=os.environ.get("DATABASE_URL", ""),
        help="SQLAlchemy-style DATABASE_URL for dev/test Postgres (default: $DATABASE_URL)",
    )
    parser.add_argument(
        "--suite",
        dest="suites",
        action="append",
        help="Suite id to run (default: s2d-1a-sample-onboarding)",
    )
    parser.add_argument(
        "--artifacts-path",
        dest="artifacts_path",
        default=str(S2D_RUNS_PATH),
        help="Path to artifacts/s2d-runs.json (default: artifacts/s2d-runs.json)",
    )
    return parser.parse_args(argv)


def _load_records(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []

    if isinstance(data, list):
        return [d for d in data if isinstance(d, dict)]

    return []


def _find_record(records: list[dict[str, Any]], *, log_id: str, run_id: str) -> dict[str, Any] | None:
    for rec in reversed(records):
        if rec.get("log_id") == log_id and rec.get("run_id") == run_id:
            return rec
    return None


def _run_s2d_1a_suite(*, database_url: str, artifacts_path: Path) -> SuiteResult:
    run_id = _default_run_id()

    cmd = [
        sys.executable,
        ONBOARDING_SCRIPT,
        "--database-url",
        database_url,
        "--run-id",
        run_id,
    ]

    print(f"[S2D-3A] running suite {S2D_1A_SUITE_ID}: script={ONBOARDING_SCRIPT} run_id={run_id}")
    completed = subprocess.run(cmd, text=True)
    rc = int(completed.returncode)

    records = _load_records(artifacts_path)
    record = _find_record(records, log_id=S2D_1A_LOG_ID, run_id=run_id)

    if record is None:
        ok = False
        reason = "no matching S2D-1A record found in artifacts/s2d-runs.json"
    else:
        ok = bool(record.get("ok")) and rc == 0
        reason = "ok" if ok else "suite reported failure (ok=false or non-zero exit code)"

    print(
        f"[S2D-3A] suite {S2D_1A_SUITE_ID} finished: rc={rc} ok={ok} "
        f"record_found={record is not None} run_id={run_id}"
    )

    return SuiteResult(
        suite_id=S2D_1A_SUITE_ID,
        log_id=S2D_1A_LOG_ID,
        run_id=run_id,
        ok=ok,
        exit_code=rc,
        reason=reason,
        record=record,
    )


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    database_url = str(args.database_url or "").strip()
    if not database_url:
        print("[S2D-3A] error: --database-url or $DATABASE_URL is required", file=sys.stderr)
        return 2

    artifacts_path = Path(str(args.artifacts_path)).resolve()

    suites: list[str]
    if args.suites:
        suites = args.suites
    else:
        suites = [S2D_1A_SUITE_ID]

    results: list[SuiteResult] = []

    for suite_id in suites:
        if suite_id != S2D_1A_SUITE_ID:
            print(f"[S2D-3A] error: unknown suite id: {suite_id}", file=sys.stderr)
            return 2

        result = _run_s2d_1a_suite(database_url=database_url, artifacts_path=artifacts_path)
        results.append(result)

    overall_ok = all(r.ok for r in results)

    summary = HardGateSummary(
        log_id="S2D-3A",
        phase="P1",
        cycle="C1",
        step="S1",
        created_at=_utc_now_str(),
        database_url=database_url,
        overall_ok=overall_ok,
        suites=results,
    )

    print("[S2D-3A] hard gate summary:")
    print(json.dumps(asdict(summary), ensure_ascii=False, indent=2))

    return 0 if overall_ok else 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
