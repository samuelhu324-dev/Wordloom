from __future__ import annotations

"""S2D-2A/P3-C1-S1: suggest SUITE_CATALOG entries from coverage JSON.

This is a small lab helper that reads an onboarding coverage snapshot
(JSON produced by `s2d_2a_p1c1s2_dump_coverage.py`) and emits a
suggested `SUITE_CATALOG` fragment for S2D-3A hard gate configuration.

v1 is intentionally conservative:
- Only projections marked as `onboarding_status=platformized` in the
  coverage JSON are considered.
- A static map is used to translate projection names into known
  hard-gate suite ids and log ids.
- The output is JSON printed to stdout; it is not applied
  automatically. Humans (or a later phase) can wire it into
  `scripts/s2d_hard_gate.py` as needed.
"""

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


# Known mapping from projection names to hard gate suites.
# v1 only knows about the S2D-1A sample projection.
PROJECTION_SUITE_MAP: Dict[str, Dict[str, str]] = {
    "chronicle_daily_stats": {
        "suite_id": "s2d-1a-sample-onboarding",
        "log_id": "S2D-1A",
    },
}


@dataclass(frozen=True)
class SuiteSuggestion:
    projection_name: str
    suite_id: str
    log_id: str
    reason: str


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="S2D-2A/P3-C1-S1: suggest SUITE_CATALOG entries from coverage JSON",
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


def _build_suggestions(coverage: Dict[str, Any]) -> Dict[str, Any]:
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
    suggestion_rows: List[SuiteSuggestion] = []

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
        suggestion_rows.append(
            SuiteSuggestion(
                projection_name=name,
                suite_id=suite_id,
                log_id=log_id,
                reason="platformized in coverage snapshot; mapped via PROJECTION_SUITE_MAP",
            )
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_coverage_path": coverage.get("_source_path"),
        "platformized_projections": [row.get("projection_name") for row in platformized],
        "suggested_suite_catalog": suggestions,
        "suggestions": [asdict(s) for s in suggestion_rows],
    }


def main(argv: List[str] | None = None) -> int:
    args = _parse_args(argv)
    coverage_path = Path(args.coverage_path).resolve()

    coverage = _load_coverage(coverage_path)
    # Record the source path in the coverage dict for traceability in the output.
    coverage["_source_path"] = str(coverage_path)

    result = _build_suggestions(coverage)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
