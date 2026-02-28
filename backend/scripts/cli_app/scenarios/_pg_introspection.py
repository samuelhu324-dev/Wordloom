from __future__ import annotations

from typing import Any

from sqlalchemy import text


def table_exists(conn: Any, table_name: str, *, schema: str = "public") -> bool:
    """Return True if the table exists in Postgres.

    Uses to_regclass() so it is safe and fast.
    """

    name = f"{schema}.{table_name}" if schema else table_name
    return bool(conn.execute(text("SELECT to_regclass(:name) IS NOT NULL"), {"name": name}).scalar())
