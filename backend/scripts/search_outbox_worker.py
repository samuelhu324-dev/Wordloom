"""Stable entrypoint for the Search Outbox → Elasticsearch worker.

This path is referenced by Procfiles and historical docs:

  python backend/scripts/search_outbox_worker.py

Implementation currently lives under backend/scripts/legacy/.

Operational controls:
- SEARCH_OUTBOX_WORKER_ENABLED=0 will exit immediately with code 0.
  This provides a simple rollback/disable switch without editing Procfiles.
"""

from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path


def _enabled() -> bool:
    raw = (os.getenv("SEARCH_OUTBOX_WORKER_ENABLED") or "").strip().lower()
    if raw == "":
        return True
    return raw in {"1", "true", "yes", "y", "on"}


def main() -> None:
    if not _enabled():
        print("[search_outbox_worker] disabled: SEARCH_OUTBOX_WORKER_ENABLED=0")
        raise SystemExit(0)

    here = Path(__file__).resolve()
    backend_root = here.parents[1]
    repo_root = backend_root.parents[0]

    for p in (str(backend_root), str(repo_root)):
        if p and p not in sys.path:
            sys.path.insert(0, p)

    legacy_script = backend_root / "scripts" / "legacy" / "search_outbox_worker.py"
    if not legacy_script.exists():
        raise SystemExit(f"legacy worker not found: {legacy_script}")

    runpy.run_path(str(legacy_script), run_name="__main__")


if __name__ == "__main__":
    main()
