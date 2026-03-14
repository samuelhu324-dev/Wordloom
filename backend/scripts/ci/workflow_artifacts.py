from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import Any


def _repo_root_from_here() -> Path:
    # backend/scripts/ci/workflow_artifacts.py -> repo root is parents[3]
    return Path(__file__).resolve().parents[3]


def _import_common() -> Any:
    repo_root = _repo_root_from_here()
    scripts_dir = repo_root / "backend" / "scripts"
    sys.path.insert(0, str(scripts_dir))
    from cli_app import common  # type: ignore

    return common


def _copy_if_exists(src: Path, dst: Path) -> bool:
    if not src.exists() or not src.is_file():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    return True


def action_placeholder(*, scenario: str, artifacts_dir: Path) -> int:
    common = _import_common()

    payload = {"scenario": scenario, "ok": False, "error": "drill did not complete"}
    common.write_json(artifacts_dir / "summary.json", payload)
    return 0


def action_finalize(*, scenario: str, run_id: str | None, exit_code: int, snapshot_dir: Path, artifacts_dir: Path) -> int:
    common = _import_common()

    artifacts_dir.mkdir(parents=True, exist_ok=True)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    # traces.json: copy if exists, else minimal placeholder
    if not _copy_if_exists(snapshot_dir / "traces.json", artifacts_dir / "traces.json"):
        common.write_text(artifacts_dir / "traces.json", "[]\n")

    # Optional logs (best-effort)
    _copy_if_exists(snapshot_dir / "backfill.log", artifacts_dir / "backfill.log")
    _copy_if_exists(snapshot_dir / "worker.log", artifacts_dir / "worker.log")

    result_path = snapshot_dir / "_result.json"
    summary_path = artifacts_dir / "summary.json"

    if result_path.exists():
        _copy_if_exists(result_path, summary_path)
        return 0

    payload = {
        "scenario": scenario,
        "run_id": run_id,
        "ok": False,
        "error": "missing _result.json",
        "exit_code": int(exit_code),
    }
    common.write_json(result_path, payload)
    common.write_json(summary_path, payload)
    return 0


def action_zip(*, artifacts_dir: Path, zip_path: Path) -> int:
    common = _import_common()

    artifacts_dir.mkdir(parents=True, exist_ok=True)
    common.zip_directory(source_dir=artifacts_dir, zip_path=zip_path)
    return 0


def action_result_summary(
    *,
    scenario: str,
    run_id: str | None,
    result_path: Path,
    artifacts_dir: Path,
) -> int:
    common = _import_common()

    artifacts_dir.mkdir(parents=True, exist_ok=True)
    summary_path = artifacts_dir / "summary.json"

    if result_path.exists() and result_path.is_file():
        _copy_if_exists(result_path, summary_path)
        return 0

    payload = {
        "scenario": scenario,
        "run_id": run_id,
        "ok": False,
        "error": "missing _result.json",
        "result_path": str(result_path),
    }
    common.write_json(summary_path, payload)
    return 0


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="workflow_artifacts", add_help=True)
    sub = p.add_subparsers(dest="cmd", required=True)

    p_placeholder = sub.add_parser("placeholder")
    p_placeholder.add_argument("--scenario", required=True)
    p_placeholder.add_argument("--artifacts-dir", default="artifacts")

    p_finalize = sub.add_parser("finalize")
    p_finalize.add_argument("--scenario", required=True)
    p_finalize.add_argument("--run-id", default=None)
    p_finalize.add_argument("--exit-code", default=2, type=int)
    p_finalize.add_argument("--snapshot-dir", default=".drill_snapshot")
    p_finalize.add_argument("--artifacts-dir", default="artifacts")

    p_zip = sub.add_parser("zip")
    p_zip.add_argument("--artifacts-dir", default="artifacts")
    p_zip.add_argument("--zip-path", default="artifacts.zip")

    p_result_summary = sub.add_parser("result-summary")
    p_result_summary.add_argument("--scenario", required=True)
    p_result_summary.add_argument("--run-id", default=None)
    p_result_summary.add_argument("--result-path", required=True)
    p_result_summary.add_argument("--artifacts-dir", default="artifacts")

    return p


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    cmd = str(args.cmd)

    if cmd == "placeholder":
        return int(action_placeholder(scenario=str(args.scenario), artifacts_dir=Path(str(args.artifacts_dir))))

    if cmd == "finalize":
        run_id = args.run_id
        if run_id is not None:
            run_id = str(run_id)
        return int(
            action_finalize(
                scenario=str(args.scenario),
                run_id=run_id,
                exit_code=int(args.exit_code),
                snapshot_dir=Path(str(args.snapshot_dir)),
                artifacts_dir=Path(str(args.artifacts_dir)),
            )
        )

    if cmd == "zip":
        return int(action_zip(artifacts_dir=Path(str(args.artifacts_dir)), zip_path=Path(str(args.zip_path))))

    if cmd == "result-summary":
        run_id = args.run_id
        if run_id is not None:
            run_id = str(run_id)
        return int(
            action_result_summary(
                scenario=str(args.scenario),
                run_id=run_id,
                result_path=Path(str(args.result_path)),
                artifacts_dir=Path(str(args.artifacts_dir)),
            )
        )

    raise SystemExit(f"unknown command: {cmd}")


if __name__ == "__main__":
    os.environ.setdefault("PYTHONUTF8", "1")
    raise SystemExit(main())
