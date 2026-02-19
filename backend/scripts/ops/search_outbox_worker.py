"""Stable shim for the search outbox worker.

The implementation currently lives under backend/scripts/legacy/.
This file exists to avoid breaking historical docs, muscle memory, and Procfiles.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


def main() -> None:
    # Ensure imports work in CI where the project isn't installed as a package.
    # We need backend/ on sys.path for `import infra.*` and `import api.*`.
    here = Path(__file__).resolve()
    repo_root = here.parents[3]
    backend_root = repo_root / "backend"

    for p in (str(backend_root), str(repo_root)):
        if p and p not in sys.path:
            sys.path.insert(0, p)

    legacy_script = backend_root / "scripts" / "legacy" / "search_outbox_worker.py"
    if not legacy_script.exists():
        raise SystemExit(f"legacy worker not found: {legacy_script}")

    try:
        runpy.run_path(str(legacy_script), run_name="__main__")
    except ModuleNotFoundError as exc:
        # Common CI failure mode: backend/ not on sys.path => cannot import infra.*
        print(
            f"[search_outbox_worker.ops] ModuleNotFoundError: {exc}. backend_root={backend_root} sys.path={sys.path}",
            file=sys.stderr,
        )
        raise


if __name__ == "__main__":
    main()
