"""S5B-2A P3 hard gate entrypoint.

Purpose:
- Run the S5B-2A drill suite(s) for policy entrypoint consolidation.
- For each run, locate the artifacts directory and verify it with the strict verifier.
- Exit non-zero if the suite fails (hard-gate friendly).

Usage:
  python scripts/drills/s5b2a_p3_hard_gate.py

Optional:
  S5B_2A_SUITES=bookshelf_delete_entrypoint

Exit codes (delegated to verifier):
- 0: artifacts contract OK and ok=true
- 1: artifacts contract OK but ok=false
- 2: artifacts contract violation
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import Iterable


DEFAULT_SUITES = [
    "bookshelf_delete_entrypoint",
]


@dataclass(frozen=True)
class SuiteRun:
    suite_id: str
    run_dir: str
    runner_rc: int
    verify_rc: int


def _parse_suites_env(val: str) -> list[str]:
    parts = [p.strip() for p in val.split(",")]
    return [p for p in parts if p]


def _pick_suites() -> list[str]:
    env = os.getenv("S5B_2A_SUITES", "").strip()
    if env:
        return _parse_suites_env(env)
    return list(DEFAULT_SUITES)


def _runner_env_for_suite(base_env: dict[str, str], suite_id: str) -> dict[str, str]:
    env = dict(base_env)
    env["S5B_2A_SUITE_ID"] = suite_id
    return env


from pathlib import Path

from _shared_artifacts import extract_run_dir_from_output


def _run_runner(*, suite_id: str, env: dict[str, str]) -> tuple[int, str, str]:
    cmd = [
        sys.executable,
        "scripts/drills/s5b2a_p2c1s1_drills_runner.py",
    ]
    p = subprocess.run(cmd, env=env, text=True, capture_output=True)

    combined = (p.stdout or "") + ("\n" if p.stdout and p.stderr else "") + (p.stderr or "")

    suite_root = Path("docs/labs/_snapshot/auto/S5B-2A") / suite_id
    run_dir = extract_run_dir_from_output(stdout=p.stdout or "", suite_root=suite_root, suite_id=suite_id)

    return p.returncode, run_dir, combined


def _run_verifier(*, run_dir: str, env: dict[str, str]) -> tuple[int, str]:
    cmd = [
        sys.executable,
        "scripts/drills/s5b1a_verify_artifacts.py",
        "--run-dir",
        run_dir,
    ]
    p = subprocess.run(cmd, env=env, text=True, capture_output=True)
    combined = (p.stdout or "") + ("\n" if p.stdout and p.stderr else "") + (p.stderr or "")
    return p.returncode, combined


def _print_block(lines: Iterable[str]) -> None:
    for line in lines:
        print(line)


def main() -> int:
    suites = _pick_suites()

    print("[S5B-2A] hard gate")
    print(f"suites={','.join(suites)}")

    base_env = os.environ.copy()

    worst_rc = 0
    runs: list[SuiteRun] = []

    for suite_id in suites:
        print()
        print(f"--- suite: {suite_id} ---")

        runner_env = _runner_env_for_suite(base_env, suite_id)
        runner_rc, run_dir, runner_out = _run_runner(suite_id=suite_id, env=runner_env)
        print(f"runner_rc={runner_rc}")
        print(f"run_dir={run_dir}")
        _print_block(["[runner_output]", runner_out.rstrip(), ""])

        verify_rc, verify_out = _run_verifier(run_dir=run_dir, env=base_env)
        print(f"verify_rc={verify_rc}")
        _print_block(["[verifier_output]", verify_out.rstrip(), ""])

        runs.append(SuiteRun(suite_id=suite_id, run_dir=run_dir, runner_rc=runner_rc, verify_rc=verify_rc))
        worst_rc = max(worst_rc, verify_rc)

    print("\n--- summary ---")
    for r in runs:
        print(f"suite={r.suite_id} verify_rc={r.verify_rc} run_dir={r.run_dir}")

    return worst_rc


if __name__ == "__main__":
    raise SystemExit(main())
