"""S5B-1A artifacts contract verifier (P1-C1-S2).

Exit codes:
- 0: contract OK and `_result.json` ok==true
- 1: contract OK but `_result.json` ok==false
- 2: contract violation (missing/empty/invalid JSON/invalid schema)

Usage:
  python scripts/drills/s5b1a_verify_artifacts.py --run-dir <path>

Notes:
- This verifier is intentionally strict and machine-friendly.
- It validates the minimal contract defined in the S5B-1A log.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Iterable, Optional


EXPECTED_RESULT_SCHEMA_VERSION = "s5b-1a.result.v1"


@dataclass(frozen=True)
class VerifyFinding:
    code: str
    message: str


class ContractViolation(Exception):
    pass


def _is_non_empty_file(path: str) -> bool:
    try:
        return os.path.isfile(path) and os.path.getsize(path) > 0
    except OSError:
        return False


def _load_json(path: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise ContractViolation(f"invalid_json:{os.path.basename(path)}:{type(e).__name__}")


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise ContractViolation(f"{code}:{message}")


def _any_non_empty_file_under(dir_path: str) -> bool:
    if not os.path.isdir(dir_path):
        return False
    for root, _dirs, files in os.walk(dir_path):
        for name in files:
            if _is_non_empty_file(os.path.join(root, name)):
                return True
    return False


def _get(obj: Any, key: str) -> Any:
    if not isinstance(obj, dict):
        return None
    return obj.get(key)


def verify_run_dir(run_dir: str) -> tuple[bool, list[VerifyFinding], bool]:
    """Return (contract_ok, findings, result_ok)."""

    findings: list[VerifyFinding] = []

    try:
        _require(os.path.isdir(run_dir), "missing_run_dir", run_dir)

        recipe_path = os.path.join(run_dir, "_recipe.json")
        result_path = os.path.join(run_dir, "_result.json")
        logs_dir = os.path.join(run_dir, "_logs")
        metrics_dir = os.path.join(run_dir, "_metrics")

        _require(_is_non_empty_file(recipe_path), "missing_or_empty", recipe_path)
        _require(_is_non_empty_file(result_path), "missing_or_empty", result_path)

        recipe = _load_json(recipe_path)
        result = _load_json(result_path)

        # Minimal JSON shape checks
        schema_version = _get(result, "schema_version")
        _require(schema_version == EXPECTED_RESULT_SCHEMA_VERSION, "schema_version_mismatch", f"expected={EXPECTED_RESULT_SCHEMA_VERSION} actual={schema_version}")

        ok_val = _get(result, "ok")
        _require(isinstance(ok_val, bool), "missing_or_invalid", "_result.json:ok")

        meta = _get(result, "meta")
        _require(isinstance(meta, dict), "missing_or_invalid", "_result.json:meta")
        for k in ("run_id", "suite_id", "started_at", "finished_at"):
            _require(isinstance(meta.get(k), str) and meta.get(k).strip() != "", "missing_or_invalid", f"_result.json:meta.{k}")

        summary = _get(result, "summary")
        _require(isinstance(summary, dict), "missing_or_invalid", "_result.json:summary")
        for k in ("total", "passed", "failed"):
            _require(isinstance(summary.get(k), int), "missing_or_invalid", f"_result.json:summary.{k}")

        cases = _get(result, "cases")
        _require(isinstance(cases, list) and len(cases) >= 1, "missing_or_invalid", "_result.json:cases")

        # Minimal artifact dir checks
        _require(_any_non_empty_file_under(logs_dir), "missing_or_empty", logs_dir)
        _require(_any_non_empty_file_under(metrics_dir), "missing_or_empty", metrics_dir)

        # Optional recipe sanity
        _require(isinstance(recipe, dict), "missing_or_invalid", "_recipe.json:root")

        findings.append(VerifyFinding(code="contract_ok", message="Artifacts contract OK"))
        return True, findings, bool(ok_val)

    except ContractViolation as e:
        findings.append(VerifyFinding(code="contract_violation", message=str(e)))
        return False, findings, False


def _print_findings(findings: Iterable[VerifyFinding]) -> None:
    for f in findings:
        print(f"[{f.code}] {f.message}")


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--run-dir", required=True, help="Path to a S5B-1A run dir (contains _recipe.json/_result.json/_logs/_metrics)")
    args = p.parse_args(argv)

    contract_ok, findings, result_ok = verify_run_dir(args.run_dir)
    _print_findings(findings)

    if not contract_ok:
        return 2
    return 0 if result_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
