"""Stable entrypoint for the chronicle outbox worker.

The implementation now lives in the Route A projection harness.
This shim keeps docs/runbooks using backend/scripts/chronicle_outbox_worker.py working.
"""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> None:
    scripts_dir = Path(__file__).resolve().parent
    backend_root = scripts_dir.parent
    if str(backend_root) not in sys.path:
        sys.path.insert(0, str(backend_root))

    # Stable behavior: running this script should start the Chronicle worker
    # without requiring CLI flags.
    from infra.projection_framework.harness import main as harness_main

    args = list(sys.argv[1:])
    if not args:
        sys.argv = [sys.argv[0], "--projection", "chronicle_events_to_entries"]
    harness_main()


if __name__ == "__main__":
    main()
