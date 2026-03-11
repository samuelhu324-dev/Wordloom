"""S2D-1B/P1-C1-S2: chronicle_events_to_entries backfill smoke skeleton (local, DB-only).

This lab is a **skeleton** for the legacy projection `chronicle_events_to_entries`.
For v1 it does not talk to the database yet; it only writes a
placeholder `_result.json` with `ok=false` so that Evidence JSON and
artifacts layout match the S2D-1A pattern.

Later cycles can replace the body of `_run()` with a real backfill
smoke using the generic backfill template.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECTION_NAME = "chronicle_events_to_entries"


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
    notes: dict[str, Any]


def _run(*, database_url: str, run_id: str, outdir: Path) -> EvidenceResult:
    outdir.mkdir(parents=True, exist_ok=True)

    result = EvidenceResult(
        lab_id="s2d1b_chronicle_events_to_entries_backfill_smoke",
        scenario="skeleton/chronicle_events_to_entries/backfill_smoke",
        run_id=run_id,
        created_at=_utc_now_str(),
        ok=False,
        database_url=database_url,
        projection_name=PROJECTION_NAME,
        notes={
            "reason": "skeleton_not_implemented_yet",
            "details": "This lab currently only writes placeholder Evidence; replace _run() with a real backfill smoke in later cycles.",
        },
    )

    (outdir / "_result.json").write_text(
        json.dumps(asdict(result), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return result


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="S2D-1B chronicle_events_to_entries backfill smoke skeleton",
    )
    p.add_argument("--database-url", required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--outdir", required=True)
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)

    database_url = str(args.database_url).strip()
    run_id = str(args.run_id).strip()
    outdir = Path(str(args.outdir).strip())

    result = _run(database_url=database_url, run_id=run_id, outdir=outdir)

    # Skeleton is intentionally red until a real implementation is added.
    return 0 if result.ok else 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
