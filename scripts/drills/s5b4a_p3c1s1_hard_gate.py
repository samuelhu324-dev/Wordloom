"""S5B-4A P3-C1-S1 hard gate entrypoint (search query authorization).

This script provides a single command that:
- runs the S5B-4A search_query_authorization drills runner
- discovers the resulting run_dir from stdout or filesystem
- invokes the shared S5B-1A verifier against that run_dir
- appends a summary record into artifacts/s5b4a-runs.json
- exits with the verifier's exit code (hard gate semantics)

Usage:
  python scripts/drills/s5b4a_p3c1s1_hard_gate.py

Optional env:
  S5B_4A_SUITE_ID=search_query_authorization

Exit codes (delegated to verifier):
- 0: artifacts contract OK and ok=true
- 1: artifacts contract OK but ok=false
- 2: artifacts contract violation
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Tuple

from _shared_artifacts import HardGateRunRecord, append_run_record, extract_run_dir_from_output, utc_now_iso


LOG_ID = "S5B-4A"
DEFAULT_SUITE_ID = "search_query_authorization"


def _run_runner(*, suite_id: str, env: dict[str, str]) -> Tuple[int, str, str]:
    cmd = [
        sys.executable,
        "scripts/drills/s5b4a_p2c1s1_drills_runner.py",
    ]
    p = subprocess.run(cmd, env=env, text=True, capture_output=True)

    combined = (p.stdout or "") + ("\n" if p.stdout and p.stderr else "") + (p.stderr or "")

    suite_root = Path("docs/labs/_snapshot/auto/S5B-4A") / suite_id
    run_dir = extract_run_dir_from_output(stdout=p.stdout or "", suite_root=suite_root, suite_id=suite_id)

    return p.returncode, run_dir, combined


def _run_verifier(*, run_dir: str, env: dict[str, str]) -> Tuple[int, str]:
    cmd = [
        sys.executable,
        "scripts/drills/s5b1a_verify_artifacts.py",
        "--run-dir",
        run_dir,
    ]
    p = subprocess.run(cmd, env=env, text=True, capture_output=True)
    combined = (p.stdout or "") + ("\n" if p.stdout and p.stderr else "") + (p.stderr or "")
    return p.returncode, combined


def _get_head_sha() -> str:
    try:
        p = subprocess.run(["git", "rev-parse", "HEAD"], text=True, capture_output=True, check=False)
        sha = (p.stdout or "").strip()
        return sha
    except Exception:
        return ""


def _print_block(lines: Iterable[str]) -> None:
    for line in lines:
        print(line)


def main() -> int:
    base_env = os.environ.copy()

    suite_id = base_env.get("S5B_4A_SUITE_ID", DEFAULT_SUITE_ID)

    print("[S5B-4A] hard gate")
    print(f"suite={suite_id}")

    runner_rc, run_dir, runner_out = _run_runner(suite_id=suite_id, env=base_env)
    print(f"runner_rc={runner_rc}")
    print(f"run_dir={run_dir}")
    _print_block(["[runner_output]", runner_out.rstrip(), ""])

    verify_rc, verify_out = _run_verifier(run_dir=run_dir, env=base_env)
    print(f"verify_rc={verify_rc}")
    _print_block(["[verifier_output]", verify_out.rstrip(), ""])

    # Map verifier rc to contract_ok/result_ok per s5b1a_verify_artifacts semantics.
    contract_ok = verify_rc != 2
    result_ok = verify_rc == 0

    # Read _result.json.ok (best-effort).
    result_ok_flag = result_ok
    try:
        result_path = Path(run_dir) / "_result.json"
        if result_path.is_file():
            result_obj = json.loads(result_path.read_text(encoding="utf-8"))
            if isinstance(result_obj, dict) and isinstance(result_obj.get("ok"), bool):
                result_ok_flag = bool(result_obj["ok"])
    except Exception:
        pass

    head_sha = _get_head_sha()

    record = HardGateRunRecord(
        log_id=LOG_ID,
        phase="P3",
        cycle="C1",
        step="S1",
        head_sha=head_sha,
        run_dir=run_dir,
        suite_id=suite_id,
        ok=result_ok_flag,
        contract_ok=contract_ok,
        result_ok=result_ok,
        ci_url=None,
        created_at=utc_now_iso(),
    )

    append_run_record(Path("artifacts") / "s5b4a-runs.json", record)

    print("\n--- summary ---")
    print(
        f"log_id={record.log_id} phase={record.phase} cycle={record.cycle} step={record.step} "
        f"ok={record.ok} contract_ok={record.contract_ok} result_ok={record.result_ok} run_dir={record.run_dir}"
    )

    # verifier rc 已编码 hard gate 语义：0=OK，1=result fail，2=contract fail。
    return verify_rc


if __name__ == "__main__":
    raise SystemExit(main())
