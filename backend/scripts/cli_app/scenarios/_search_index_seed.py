from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import text


def ensure_search_index_min_rows(
    *,
    conn,
    ensure_min_rows: int,
    library_id: str | None,
    seed_entity_type: str = "seed",
    seed_text_prefix: str | None = None,
) -> int:
    if ensure_min_rows <= 0:
        return 0

    where_parts: list[str] = []
    params: dict[str, object] = {}
    if library_id is not None:
        where_parts.append("library_id = :library_id")
        params["library_id"] = library_id
    where_sql = ("WHERE " + " AND ".join(where_parts)) if where_parts else ""

    existing = int(conn.execute(text(f"SELECT COUNT(*) FROM search_index {where_sql}"), params).scalar() or 0)
    need = int(ensure_min_rows) - existing
    if need <= 0:
        return 0

    now = datetime.now(timezone.utc)
    rows = []
    for i in range(need):
        prefix = seed_text_prefix if seed_text_prefix is not None else f"seed:{seed_entity_type}:"
        rows.append(
            {
                "id": str(uuid.uuid4()),
                "entity_type": seed_entity_type,
                "library_id": library_id,
                "entity_id": str(uuid.uuid4()),
                "text": f"{prefix}{i}",
                "snippet": None,
                "rank_score": 0.0,
                "created_at": now,
                "updated_at": now,
                "event_version": int(i + 1),
            }
        )

    conn.execute(
        text(
            """
            INSERT INTO search_index
              (id, entity_type, library_id, entity_id, text, snippet, rank_score, created_at, updated_at, event_version)
            VALUES
              (:id, :entity_type, :library_id, :entity_id, :text, :snippet, :rank_score, :created_at, :updated_at, :event_version)
            """
        ),
        rows,
    )
    conn.commit()
    return int(need)
