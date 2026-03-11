"""S2D-1C/P1-C1-S1: search_index_to_elastic harness drill (skeleton).

This lab is a skeleton placeholder for the legacy projection
`search_index_to_elastic` harness/correctness drill. It is
intentionally "known red" in v1:

- It accepts the standard S2D lab CLI contract
  (`--database-url/--run-id/--outdir`).
- It writes `<outdir>/_result.json` with a minimal evidence payload.
- It always reports `ok=false` with reason
  `"skeleton_not_implemented_yet"` and exits with status code 2.

Later cycles (P2/C2+) can replace this implementation with a real
end-to-end harness drill that verifies the outbox → Elastic path.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECTION_NAME = "search_index_to_elastic"
LAB_ID = "s2d1c_search_index_to_elastic_harness_drill"
SCENARIO_ID = "verify/search_index_to_elastic/harness_drill_skeleton"


def _utc_now_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


@dataclass(frozen=True)
class EvidenceResult:
    lab_id: str
    scenario: str
    run_id: str
    created_at: str
    ok: bool
    database_url: str
    projection_name: str
    reason: str
    notes: dict[str, Any]


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="S2D-1C search_index_to_elastic harness drill (skeleton)",
    )
    p.add_argument(
        "--database-url",
        required=True,
        help="SQLAlchemy-style DATABASE_URL for dev/test Postgres",
    )
    p.add_argument("--run-id", required=True, help="Logical run id for this lab")
    p.add_argument(
        "--outdir",
        required=True,
        help="Output directory for _result.json (will be created if missing)",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    database_url = str(args.database_url).strip()
    run_id = str(args.run_id).strip()
    outdir = Path(str(args.outdir)).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    result = EvidenceResult(
        lab_id=LAB_ID,
        scenario=SCENARIO_ID,
        run_id=run_id,
        created_at=_utc_now_str(),
        ok=False,
        database_url=database_url,
        projection_name=PROJECTION_NAME,
        reason="skeleton_not_implemented_yet",
        notes={
            "message": "S2D-1C skeleton only; harness drill not implemented yet",
        },
    )

    result_path = outdir / "_result.json"
    result_path.write_text(
        json.dumps(asdict(result), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(
        "[S2D-1C] harness drill skeleton wrote _result.json; "
        "ok=false by design (reason=skeleton_not_implemented_yet)",
    )

    # Known red skeleton: non-zero exit so runners treat this as a failed scenario.
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
