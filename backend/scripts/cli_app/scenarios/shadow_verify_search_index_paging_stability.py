from __future__ import annotations

import time
from typing import Any

from sqlalchemy import create_engine, text

from ._search_index_seed import ensure_search_index_min_rows
from ..registry import register
from ..types import DrillInputs, DrillResult


@register("shadow_verify_search_index_paging_stability")
@register("shadow-verify-search-index-paging-stability")
def run(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    database_url = str(payload.get("database_url") or "").strip()
    library_id = (str(payload.get("library_id") or "").strip() or None)
    page_size = int(payload.get("page_size") or 0)
    pages_checked = int(payload.get("pages_checked") or 0)
    ensure_min_rows = int(payload.get("ensure_min_rows") or 0)

    if not database_url:
        return DrillResult(ok=False, errors=["DATABASE_URL is required"], meta={}, summary={})

    # Stable ordering contract: (entity_type, entity_id) as tie-breaker.
    order_key = ["entity_type", "entity_id"]
    scope = "all" if library_id is None else f"library:{library_id}"

    def _fetch_page(
        *,
        conn,
        cursor_entity_type: str | None,
        cursor_entity_id: str | None,
    ) -> list[tuple[str, str]]:
        where_parts: list[str] = []
        params: dict[str, object] = {"limit": page_size}

        if library_id is not None:
            where_parts.append("library_id = :library_id")
            params["library_id"] = library_id

        if cursor_entity_type is not None and cursor_entity_id is not None:
            # Keyset pagination on (entity_type, entity_id)
            where_parts.append(
                "(entity_type > :cursor_entity_type OR (entity_type = :cursor_entity_type AND entity_id > :cursor_entity_id))"
            )
            params["cursor_entity_type"] = cursor_entity_type
            params["cursor_entity_id"] = cursor_entity_id

        where_sql = ("WHERE " + " AND ".join(where_parts)) if where_parts else ""
        sql = f"""
            SELECT entity_type, entity_id
            FROM search_index
            {where_sql}
            ORDER BY entity_type, entity_id
            LIMIT :limit
        """
        rows = conn.execute(text(sql), params).all()
        return [(str(r[0]), str(r[1])) for r in rows]

    engine = create_engine(database_url)
    pages: list[list[tuple[str, str]]] = []
    with engine.connect() as conn:
        inserted_rows = ensure_search_index_min_rows(conn=conn, ensure_min_rows=ensure_min_rows, library_id=library_id)
        count_where = "" if library_id is None else "WHERE library_id = :library_id"
        count_params = {} if library_id is None else {"library_id": library_id}
        rows_total = int(conn.execute(text(f"SELECT COUNT(*) FROM search_index {count_where}"), count_params).scalar() or 0)

        cursor_entity_type: str | None = None
        cursor_entity_id: str | None = None

        for _ in range(pages_checked):
            page = _fetch_page(
                conn=conn,
                cursor_entity_type=cursor_entity_type,
                cursor_entity_id=cursor_entity_id,
            )
            pages.append(page)
            if not page:
                break
            cursor_entity_type, cursor_entity_id = page[-1]

    # Verify ordering and no overlap across pages.
    ordering_ok = True
    for page in pages:
        if page != sorted(page):
            ordering_ok = False
            break

    seen: set[tuple[str, str]] = set()
    duplicates_across_pages_total = 0
    for page in pages:
        for k in page:
            if k in seen:
                duplicates_across_pages_total += 1
            else:
                seen.add(k)

    data_sufficient = rows_total >= (page_size * pages_checked)
    ok = ordering_ok and duplicates_across_pages_total == 0 and data_sufficient and (len(pages) >= pages_checked)

    result: dict[str, Any] = {
        "lab_id": inputs.scope_id,
        "scenario": "shadow_verify_search_index_paging_stability",
        "run_id": inputs.run_id,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "scope": scope,
        "order_key": order_key,
        "rows_total": int(rows_total),
        "ensure_min_rows": int(ensure_min_rows),
        "seed_rows_inserted": int(inserted_rows),
        "data_sufficient": bool(data_sufficient),
        "page_size": int(page_size),
        "pages_checked": int(pages_checked),
        "pages_returned": len(pages),
        "page_lengths": [len(p) for p in pages],
        "duplicates_across_pages_total": int(duplicates_across_pages_total),
        "ordering_ok": bool(ordering_ok),
        "ok": bool(ok),
    }
    if pages and pages[0]:
        result["first_key"] = {"entity_type": pages[0][0][0], "entity_id": pages[0][0][1]}
        result["last_key"] = {"entity_type": pages[-1][-1][0], "entity_id": pages[-1][-1][1]}

    return DrillResult(
        ok=bool(ok),
        meta=result,
        summary={
            "scope": scope,
            "rows_total": int(rows_total),
            "data_sufficient": bool(data_sufficient),
            "ordering_ok": bool(ordering_ok),
            "duplicates_across_pages_total": int(duplicates_across_pages_total),
        },
        errors=[],
    )
