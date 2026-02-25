"""Stable shim for search outbox replay tool.

This entrypoint is kept for backwards compatibility (ops/runbook muscle memory).
It intentionally forwards to the canonical stable entrypoint under backend/scripts/.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


def main() -> None:
    backend_root = Path(__file__).resolve().parents[2]
    if str(backend_root) not in sys.path:
        sys.path.insert(0, str(backend_root))

    stable_entrypoint = Path(__file__).resolve().parents[1] / "search_outbox_replay_failed.py"
    if not stable_entrypoint.exists():
        raise SystemExit(f"stable entrypoint not found: {stable_entrypoint}")
    runpy.run_path(str(stable_entrypoint), run_name="__main__")


if __name__ == "__main__":
    main()
