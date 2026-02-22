"""Lab S2B-2A-1A: shadow verify write-gate (idempotency/uniqueness).

Outputs:
- Writes <OUTDIR>/_result.json when OUTDIR is provided (recommended).
- Exits 0 when ok; exits 2 when gate fails.

Env vars:
- DATABASE_URL (required)
- OUTDIR (optional)
- RUN_ID (optional)
- LIBRARY_ID (optional, UUID)
"""

from __future__ import annotations

import json
import os
import sys
import time
import uuid
from pathlib import Path

from sqlalchemy import create_engine, text


_SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from cli_app.common import write_json

LAB_ID = "S2B-2A-1A"
SCENARIO = "shadow_verify_search_index_write_gate"


def _now_run_id() -> str:
    return time.strftime("%Y%m%dT%H%M%S")


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _count_duplicates(conn, *, where_sql: str, params: dict[str, object]) -> tuple[int, int, list[dict[str, object]]]:
    # groups: count of (entity_type, entity_id) with COUNT(*) > 1
    # extra_rows: sum(COUNT(*) - 1) over those groups
    groups = int(
        conn.execute(
            text(
                f"""
                SELECT COUNT(*)
                FROM (
                  SELECT entity_type, entity_id
                  FROM search_index
                  WHERE {where_sql}
                  GROUP BY entity_type, entity_id
                  HAVING COUNT(*) > 1
                ) t
                """
            ),
            params,
        ).scalar()
        or 0
    )

    extra_rows = int(
        conn.execute(
            text(
                f"""
                SELECT COALESCE(SUM(cnt - 1), 0)
                FROM (
                  SELECT COUNT(*) AS cnt
                  FROM search_index
                  WHERE {where_sql}
                  GROUP BY entity_type, entity_id
                  HAVING COUNT(*) > 1
                ) t
                """
            ),
            params,
        ).scalar()
        or 0
    )

    by_type_rows = conn.execute(
        text(
            f"""
            SELECT entity_type,
                   COUNT(*) AS duplicate_groups,
                   COALESCE(SUM(cnt - 1), 0) AS duplicate_extra_rows
            FROM (
              SELECT entity_type, entity_id, COUNT(*) AS cnt
              FROM search_index
              WHERE {where_sql}
              GROUP BY entity_type, entity_id
              HAVING COUNT(*) > 1
            ) t
            GROUP BY entity_type
            ORDER BY entity_type
            """
        ),
        params,
    ).all()

    by_type: list[dict[str, object]] = [
        {
            "entity_type": str(r[0]),
            "duplicate_groups": int(r[1] or 0),
            "duplicate_extra_rows": int(r[2] or 0),
        }
        for r in by_type_rows
    ]

    return groups, extra_rows, by_type


def main() -> int:
    run_id = os.getenv("RUN_ID") or _now_run_id()
    outdir_raw = (os.getenv("OUTDIR") or "").strip() or None
    outdir = Path(outdir_raw) if outdir_raw else None

    database_url = (os.getenv("DATABASE_URL") or "").strip()
    if not database_url:
        print("[lab-S2B-2A-1A] DATABASE_URL is required")
        return 2

    library_id = (os.getenv("LIBRARY_ID") or "").strip() or None
    if library_id is not None:
        try:
            uuid.UUID(library_id)
        except ValueError:
            print(f"[lab-S2B-2A-1A] invalid LIBRARY_ID: {library_id}")
            return 2

    engine = create_engine(database_url)
    with engine.connect() as conn:
        groups_total, extra_total, by_type = _count_duplicates(conn, where_sql="1=1", params={})

        if library_id is None:
            scope = "all"
            groups_scoped = None
            extra_scoped = None
        else:
            scope = f"library:{library_id}"
            groups_scoped, extra_scoped, _ = _count_duplicates(
                conn,
                where_sql="library_id = :library_id",
                params={"library_id": library_id},
            )

    ok = extra_total == 0

    result: dict[str, object] = {
        "lab_id": LAB_ID,
        "scenario": SCENARIO,
        "run_id": run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "scope": scope,
        "duplicates_groups_total": int(groups_total),
        "duplicates_extra_rows_total": int(extra_total),
        "duplicates_by_entity_type": by_type,
        "ok": bool(ok),
    }

    if groups_scoped is not None:
        result["duplicates_groups_scoped"] = int(groups_scoped)
    if extra_scoped is not None:
        result["duplicates_extra_rows_scoped"] = int(extra_scoped)

    if outdir is not None:
        _ensure_dir(outdir)
        write_json(outdir / "_result.json", result)

    print("labs-012.shadow_verify_search_index_write_gate")
    print(f"scope={scope}")
    print(f"duplicates_groups_total={groups_total}")
    print(f"duplicates_extra_rows_total={extra_total}")
    if groups_scoped is not None:
        print(f"duplicates_groups_scoped={groups_scoped}")
    if extra_scoped is not None:
        print(f"duplicates_extra_rows_scoped={extra_scoped}")
    if outdir is not None:
        print(f"outputs: {outdir}")

    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
