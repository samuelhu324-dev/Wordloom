"""S2D-2A/P1-C1-S2: dump onboarding coverage snapshot.

This lab-style helper queries the projection registry/catalog and prints
an S2D-2A onboarding coverage snapshot as JSON. It is intentionally
minimal and focuses on dev/test usage; P2 will add a dedicated drill
that writes snapshots under artifacts/.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _ensure_backend_on_path() -> None:
    here = Path(__file__).resolve()
    backend_root = here.parents[2]
    if str(backend_root) not in sys.path:
        sys.path.insert(0, str(backend_root))


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="S2D-2A onboarding coverage snapshot (dev/test only)",
    )
    parser.add_argument(
        "--output",
        dest="output",
        default="",
        help="Optional path to write JSON snapshot (default: stdout only)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    _ensure_backend_on_path()

    from infra.projection_framework.catalog import compute_coverage_snapshot

    args = _parse_args(argv)

    snapshot: dict[str, Any] = compute_coverage_snapshot()

    # Always print to stdout for quick inspection.
    print(json.dumps(snapshot, ensure_ascii=False, indent=2))

    output = (args.output or "").strip()
    if output:
        out_path = Path(output).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[S2D-2A] wrote coverage snapshot to {out_path}", file=sys.stderr)

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
