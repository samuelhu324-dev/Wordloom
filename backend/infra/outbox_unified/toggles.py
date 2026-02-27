"""Projection-scoped toggles for unified outbox cutover.

Env vars:
- OUTBOX_UNIFIED_WRITE_ENABLED
- OUTBOX_UNIFIED_READ_ENABLED

Values:
- empty / falsey => disabled
- "true" | "1" | "all" | "*" => enabled for all projections
- comma/space/semicolon-separated projection names => enabled for those projections

Examples:
- OUTBOX_UNIFIED_WRITE_ENABLED=search_index_to_elastic
- OUTBOX_UNIFIED_READ_ENABLED=chronicle_events_to_entries,search_index_to_elastic
"""

from __future__ import annotations

import os


def _is_all_token(raw: str) -> bool:
    v = (raw or "").strip().lower()
    return v in {"1", "true", "all", "*"}


def _parse_projection_set(raw: str) -> tuple[bool, set[str]]:
    if not raw:
        return False, set()

    if _is_all_token(raw):
        return True, set()

    parts = [p.strip() for p in raw.replace(";", ",").replace(" ", ",").split(",") if p.strip()]
    return False, set(parts)


def _enabled_for_projection(*, env_name: str, projection: str) -> bool:
    raw = (os.getenv(env_name) or "").strip()
    if raw == "":
        return False

    all_enabled, projections = _parse_projection_set(raw)
    if all_enabled:
        return True

    return projection in projections


def is_unified_outbox_write_enabled(projection: str) -> bool:
    return _enabled_for_projection(env_name="OUTBOX_UNIFIED_WRITE_ENABLED", projection=str(projection))


def is_unified_outbox_read_enabled(projection: str) -> bool:
    return _enabled_for_projection(env_name="OUTBOX_UNIFIED_READ_ENABLED", projection=str(projection))


__all__ = [
    "is_unified_outbox_read_enabled",
    "is_unified_outbox_write_enabled",
]
