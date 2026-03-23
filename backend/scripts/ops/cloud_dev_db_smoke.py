"""Minimal cloud-dev DB smoke for S4C-3A.

This script is intentionally DB-only for the first runtime integration step:
- load DATABASE_URL from an env file or process env
- open one connection
- verify current_database/current_user/select 1

It does not mutate application data.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, make_url


def _load_env_file(env_file: Path) -> None:
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        # When --env-file is passed, it should be the source of truth for this run.
        os.environ[key.strip()] = value.strip().strip('"').strip("'")


def _mask_url(raw_url: str) -> str:
    url: URL = make_url(raw_url)
    return str(url.render_as_string(hide_password=True))


def _validate_database_url(raw_url: str) -> None:
    placeholders = ("<password>", "<current-rds-endpoint>", "<rds-endpoint>", "<user>")
    if any(token in raw_url for token in placeholders):
        raise SystemExit(
            "DATABASE_URL still contains placeholders. Fill the real password and live RDS endpoint in .env.cloud.dev first."
        )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Minimal cloud-dev DB smoke")
    parser.add_argument(
        "--env-file",
        help="Optional repo-root env file such as .env.cloud.dev",
    )
    parser.add_argument(
        "--database-url",
        help="Explicit database URL override; otherwise DATABASE_URL is used",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()

    if args.env_file:
        env_path = Path(args.env_file)
        if not env_path.is_absolute():
            repo_root = Path(__file__).resolve().parents[3]
            env_path = repo_root / env_path
        if not env_path.exists():
            raise SystemExit(f"env file not found: {env_path}")
        _load_env_file(env_path)

    database_url = args.database_url or os.getenv("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL is required")

    _validate_database_url(database_url)

    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 5},
    )
    try:
        with engine.connect() as conn:
            row = conn.execute(
                text(
                    """
                    select
                      current_database() as current_database,
                      current_user as current_user,
                      inet_server_addr()::text as server_addr,
                      inet_server_port() as server_port,
                      1 as ping_ok
                    """
                )
            ).mappings().one()
    finally:
        engine.dispose()

    result: dict[str, Any] = {
        "ok": True,
        "environment": os.getenv("ENVIRONMENT") or "",
        "wordloom_env": os.getenv("WORDLOOM_ENV") or "",
        "database_url_masked": _mask_url(database_url),
        "current_database": row["current_database"],
        "current_user": row["current_user"],
        "server_addr": row["server_addr"],
        "server_port": row["server_port"],
        "ping_ok": row["ping_ok"] == 1,
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())