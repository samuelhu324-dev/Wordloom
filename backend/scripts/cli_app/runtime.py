from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


# NOTE: This module intentionally keeps a tiny surface area.
# It centralizes subprocess + path glue that used to live in backend/scripts/cli.py.

# backend/scripts/cli_app/runtime.py -> repo root
REPO_ROOT = Path(__file__).resolve().parents[3]
LEGACY_SCRIPTS_DIR = REPO_ROOT / "backend" / "scripts" / "legacy"


def python_exe() -> str:
    """Return a Python executable suitable for invoking legacy scripts.

    Preference order:
    - If already inside an activated venv, use current interpreter.
    - Otherwise prefer repo-local .venv for the current OS.
    """

    if os.getenv("VIRTUAL_ENV"):
        return sys.executable

    if os.name == "nt":
        win_venv = REPO_ROOT / ".venv" / "Scripts" / "python.exe"
        if win_venv.exists():
            return str(win_venv)
        return sys.executable

    unix_venv = REPO_ROOT / ".venv" / "bin" / "python"
    if unix_venv.exists():
        return str(unix_venv)
    return sys.executable


def run(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> int:
    print("[scripts] run:", " ".join(cmd))
    return int(subprocess.call(cmd, cwd=str(cwd) if cwd else None, env=env))


def with_backend_pythonpath(env: dict[str, str]) -> dict[str, str]:
    backend_path = str(REPO_ROOT / "backend")
    existing = env.get("PYTHONPATH") or ""
    parts = [p for p in existing.split(os.pathsep) if p]
    if backend_path not in parts:
        parts.insert(0, backend_path)
    env["PYTHONPATH"] = os.pathsep.join(parts)
    return env
