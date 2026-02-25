"""Stable entrypoint for the chronicle outbox worker.

The implementation currently lives under backend/scripts/legacy/.
This shim keeps docs/runbooks using backend/scripts/chronicle_outbox_worker.py working.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


def main() -> None:
    scripts_dir = Path(__file__).resolve().parent
    backend_root = scripts_dir.parent
    if str(backend_root) not in sys.path:
        sys.path.insert(0, str(backend_root))

    legacy_script = scripts_dir / "legacy" / "chronicle_outbox_worker.py"
    if not legacy_script.exists():
        raise SystemExit(f"legacy worker not found: {legacy_script}")
    runpy.run_path(str(legacy_script), run_name="__main__")


if __name__ == "__main__":
    main()
