from __future__ import annotations

import time
from typing import Any

from sqlalchemy import create_engine, text
from ..registry import register
from ..types import DrillInputs, DrillResult


@register("shadow_verify_search_index_write_gate")
@register("shadow-verify-search-index-write-gate")
def run(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    database_url = str(payload.get("database_url") or "").strip()
    library_id = (str(payload.get("library_id") or "").strip() or None)

    # Validation is expected to be handled by the shim (legacy CLI) to preserve behavior.
    if not database_url:
        return DrillResult(ok=False, errors=["DATABASE_URL is required"], meta={}, summary={})

    duplicates_groups_total = 0
    duplicates_extra_rows_total = 0
    duplicates_by_entity_type: list[dict[str, Any]] = []
    duplicates_groups_scoped: int | None = None
    duplicates_extra_rows_scoped: int | None = None

    engine = create_engine(database_url)
    with engine.connect() as conn:
        duplicates_groups_total = int(
            conn.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM (
                      SELECT entity_type, entity_id
                      FROM search_index
                      GROUP BY entity_type, entity_id
                      HAVING COUNT(*) > 1
                    ) t
                    """
                )
            ).scalar()
            or 0
        )
        duplicates_extra_rows_total = int(
            conn.execute(
                text(
                    """
                    SELECT COALESCE(SUM(cnt - 1), 0)
                    FROM (
                      SELECT COUNT(*) AS cnt
                      FROM search_index
                      GROUP BY entity_type, entity_id
                      HAVING COUNT(*) > 1
                    ) t
                    """
                )
            ).scalar()
            or 0
        )
        rows = conn.execute(
            text(
                """
                SELECT entity_type,
                       COUNT(*) AS duplicate_groups,
                       COALESCE(SUM(cnt - 1), 0) AS duplicate_extra_rows
                FROM (
                  SELECT entity_type, entity_id, COUNT(*) AS cnt
                  FROM search_index
                  GROUP BY entity_type, entity_id
                  HAVING COUNT(*) > 1
                ) t
                GROUP BY entity_type
                ORDER BY entity_type
                """
            )
        ).all()
        duplicates_by_entity_type = [
            {
                "entity_type": str(r[0]),
                "duplicate_groups": int(r[1] or 0),
                "duplicate_extra_rows": int(r[2] or 0),
            }
            for r in rows
        ]

        if library_id is not None:
            duplicates_groups_scoped = int(
                conn.execute(
                    text(
                        """
                        SELECT COUNT(*)
                        FROM (
                          SELECT entity_type, entity_id
                          FROM search_index
                          WHERE library_id = :library_id
                          GROUP BY entity_type, entity_id
                          HAVING COUNT(*) > 1
                        ) t
                        """
                    ),
                    {"library_id": library_id},
                ).scalar()
                or 0
            )
            duplicates_extra_rows_scoped = int(
                conn.execute(
                    text(
                        """
                        SELECT COALESCE(SUM(cnt - 1), 0)
                        FROM (
                          SELECT COUNT(*) AS cnt
                          FROM search_index
                          WHERE library_id = :library_id
                          GROUP BY entity_type, entity_id
                          HAVING COUNT(*) > 1
                        ) t
                        """
                    ),
                    {"library_id": library_id},
                ).scalar()
                or 0
            )

    scope = "all" if library_id is None else f"library:{library_id}"
    ok = duplicates_extra_rows_total == 0

    result: dict[str, Any] = {
        "lab_id": inputs.scope_id,
        "scenario": "shadow_verify_search_index_write_gate",
        "run_id": inputs.run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "scope": scope,
        "duplicates_groups_total": int(duplicates_groups_total),
        "duplicates_extra_rows_total": int(duplicates_extra_rows_total),
        "duplicates_by_entity_type": duplicates_by_entity_type,
        "ok": bool(ok),
    }
    if duplicates_groups_scoped is not None:
        result["duplicates_groups_scoped"] = int(duplicates_groups_scoped)
    if duplicates_extra_rows_scoped is not None:
        result["duplicates_extra_rows_scoped"] = int(duplicates_extra_rows_scoped)

    return DrillResult(
        ok=bool(ok),
        meta=result,
        summary={
            "scope": scope,
            "duplicates_extra_rows_total": int(duplicates_extra_rows_total),
        },
        errors=[],
    )
