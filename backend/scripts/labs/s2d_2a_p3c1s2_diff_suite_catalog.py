from __future__ import annotations

"""S2D-2A/P3-C1-S2: diff coverage-based suite suggestions with current SUITE_CATALOG.

This helper compares:
- the suggested SUITE_CATALOG fragment derived from an onboarding
  coverage JSON snapshot; and
- the current `SUITE_CATALOG` configuration in `scripts/s2d_hard_gate.py`.

v1 is read-only: it prints a JSON diff to stdout and does not mutate
any configuration. It is intended for manual inspection or for use as a
soft check in CI.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


def _ensure_repo_root_on_path() -> None:
    """Ensure the repository root is on sys.path.

    The file lives under `backend/scripts/labs/...`, so the repo root is
    three levels up from this file.
    """

    here = Path(__file__).resolve()
    repo_root = here.parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "S2D-2A/P3-C1-S2: diff coverage-based SUITE_CATALOG suggestions "
            "with scripts/s2d_hard_gate.py"
        ),
    )
    parser.add_argument(
        "--coverage-path",
        dest="coverage_path",
        required=True,
        help="Path to a coverage JSON snapshot (artifacts/s2d-coverage-*.json)",
    )
    return parser.parse_args(argv)


def _load_coverage(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"coverage JSON not found: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"failed to parse coverage JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit("coverage JSON must be an object at the top level")

    return data


def _suggest_from_coverage(coverage: Dict[str, Any]) -> Dict[str, Any]:
    """Rebuild the suggested SUITE_CATALOG fragment from coverage JSON.

    This mirrors the logic in `s2d_2a_p3c1s1_suggest_suite_catalog.py`
    so that the diff script is self-contained while remaining consistent
    with the projection→suite mapping used there.
    """

    from backend.scripts.labs.s2d_2a_p3c1s1_suggest_suite_catalog import (
        PROJECTION_SUITE_MAP,
    )

    projections = coverage.get("projections") or []
    if not isinstance(projections, list):
        raise SystemExit("coverage JSON 'projections' must be a list")

    platformized: List[Dict[str, Any]] = []
    for row in projections:
        if not isinstance(row, dict):
            continue
        if row.get("onboarding_status") != "platformized":
            continue
        platformized.append(row)

    suggestions: Dict[str, Dict[str, Any]] = {}

    for row in platformized:
        name = str(row.get("projection_name") or "").strip()
        if not name:
            continue

        mapping = PROJECTION_SUITE_MAP.get(name)
        if not mapping:
            # v1 ignores platformized projections it doesn't know
            # how to map to a concrete hard-gate suite.
            continue

        suite_id = mapping["suite_id"]
        log_id = mapping["log_id"]
        suggestions[suite_id] = {
            "log_id": log_id,
            "required": True,
        }

    return suggestions


def _compute_diff(
    *,
    suggested: Dict[str, Dict[str, Any]],
    current: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    missing: List[str] = []  # in suggested, not in current
    extra: List[str] = []  # in current, not in suggested
    mismatched: Dict[str, Dict[str, Any]] = {}

    suggested_keys = set(suggested.keys())
    current_keys = set(current.keys())

    for suite_id in sorted(suggested_keys - current_keys):
        missing.append(suite_id)

    for suite_id in sorted(current_keys - suggested_keys):
        extra.append(suite_id)

    for suite_id in sorted(suggested_keys & current_keys):
        s_val = suggested[suite_id]
        c_val = current[suite_id]
        if (s_val.get("log_id") != c_val.get("log_id")) or (
            bool(s_val.get("required", True))
            != bool(c_val.get("required", True))
        ):
            mismatched[suite_id] = {
                "suggested": s_val,
                "current": c_val,
            }

    has_diff = bool(missing or extra or mismatched)

    return {
        "has_diff": has_diff,
        "missing_in_hard_gate": missing,
        "extra_in_hard_gate": extra,
        "mismatched_entries": mismatched,
    }


def main(argv: List[str] | None = None) -> int:
    _ensure_repo_root_on_path()

    from scripts.s2d_hard_gate import SUITE_CATALOG

    args = _parse_args(argv)
    coverage_path = Path(args.coverage_path).resolve()

    coverage = _load_coverage(coverage_path)
    suggested = _suggest_from_coverage(coverage)

    diff = _compute_diff(suggested=suggested, current=SUITE_CATALOG)

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_coverage_path": str(coverage_path),
        "suggested_suite_catalog": suggested,
        "current_suite_catalog": SUITE_CATALOG,
        **diff,
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))
    # v1 always exits 0; CI can choose to interpret has_diff as warning.
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
