from __future__ import annotations

import os
import time
from pathlib import Path

from cli_app.common import REPO_ROOT, ensure_dir


LABS_SNAPSHOT_ROOT = REPO_ROOT / "docs" / "labs" / "_snapshot"


def now_run_id() -> str:
    # local time is fine for manual runs; keep it filesystem-safe
    return time.strftime("%Y%m%dT%H%M%S")


def default_auto_outdir(*, lab_id: str, scenario: str, run_id: str) -> Path:
    return LABS_SNAPSHOT_ROOT / "auto" / lab_id / scenario / run_id


def default_labs009_expb_outdir(run_id: str) -> Path:
    return LABS_SNAPSHOT_ROOT / "manual" / "_lab-S3A-2A-3A-expB" / run_id


def read_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        raise FileNotFoundError(str(path))

    env: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if (len(value) >= 2) and ((value[0] == value[-1] == '"') or (value[0] == value[-1] == "'")):
            value = value[1:-1]
        env[key] = value
    return env


def load_env(*, env_file: str | None) -> dict[str, str]:
    env = os.environ.copy()
    if env_file:
        env_path = (REPO_ROOT / env_file).resolve() if not Path(env_file).is_absolute() else Path(env_file)
        env.update(read_env_file(env_path))
    return env
