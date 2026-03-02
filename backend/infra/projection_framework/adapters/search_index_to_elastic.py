from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infra.database.models.outbox_event_models import OutboxEventModel
from infra.database.models.search_index_models import SearchIndexModel
from infra.outbox_core.payload_contract import BadPayload, require_schema_version


PROJECTION_NAME = "search_index_to_elastic"


@dataclass(frozen=True, slots=True)
class ElasticTarget:
    base_url: str
    index: str


def _normalize_env_str(value: str | None) -> str:
    return (value or "").strip()


def elastic_target_from_env() -> ElasticTarget:
    base_url = _normalize_env_str(os.getenv("ELASTIC_URL") or "http://localhost:9200").rstrip("/")
    index = _normalize_env_str(os.getenv("ELASTIC_INDEX") or "wordloom-search-index")

    if not base_url:
        raise RuntimeError(
            "ELASTIC_URL is empty. Fix by setting ELASTIC_URL (e.g. http://localhost:9200) or unsetting it to use the default."
        )
    if not (base_url.startswith("http://") or base_url.startswith("https://")):
        raise RuntimeError(f"ELASTIC_URL must include scheme (http:// or https://). Got: {base_url!r}")
    if not index:
        raise RuntimeError(
            "ELASTIC_INDEX is empty. Fix by setting ELASTIC_INDEX (e.g. wordloom-test-search-index) or unsetting it to use the default."
        )

    return ElasticTarget(base_url=base_url, index=index)


def es_doc_id(entity_type: str, entity_id: Any) -> str:
    return f"{entity_type}:{entity_id}"


def build_es_doc_from_search_row(row: SearchIndexModel) -> dict[str, Any]:
    doc = {
        # Payload contract v1 (hard gate): always emit schema_version.
        "schema_version": 1,
        "entity_type": row.entity_type,
        "library_id": (str(row.library_id) if getattr(row, "library_id", None) else None),
        "entity_id": str(row.entity_id),
        "text": row.text,
        "snippet": row.snippet,
        "rank_score": row.rank_score,
        "event_version": int(row.event_version),
    }

    # Contract violations must fail deterministically (no retry).
    require_schema_version(doc, projection=PROJECTION_NAME, supported_versions={1}, allow_missing=False)
    if not isinstance(doc.get("entity_type"), str) or not str(doc.get("entity_type") or "").strip():
        raise BadPayload(projection=PROJECTION_NAME, reason="bad_payload", message="entity_type must be non-empty")
    if not isinstance(doc.get("entity_id"), str) or not str(doc.get("entity_id") or "").strip():
        raise BadPayload(projection=PROJECTION_NAME, reason="bad_payload", message="entity_id must be non-empty")
    if not isinstance(doc.get("event_version"), int):
        raise BadPayload(projection=PROJECTION_NAME, reason="bad_payload", message="event_version must be int")

    return doc


async def load_search_row(
    session: AsyncSession,
    *,
    entity_type: str,
    entity_id: Any,
) -> SearchIndexModel | None:
    return (
        await session.execute(
            select(SearchIndexModel).where(
                SearchIndexModel.entity_type == entity_type,
                SearchIndexModel.entity_id == entity_id,
            )
        )
    ).scalar_one_or_none()


async def apply_upsert(
    session: AsyncSession,
    *,
    client: httpx.AsyncClient,
    target: ElasticTarget,
    entity_type: str,
    entity_id: Any,
) -> bool:
    """Apply an upsert outbox event.

    Returns:
      True  - ES write performed
      False - noop (no SoT row)
    """

    row = await load_search_row(session, entity_type=entity_type, entity_id=entity_id)
    if row is None:
        # Nothing to upsert anymore (deleted or never existed); treat as success.
        return False

    doc = build_es_doc_from_search_row(row)
    doc_id = es_doc_id(row.entity_type, row.entity_id)
    resp = await client.put(f"/{target.index}/_doc/{doc_id}", json=doc)
    resp.raise_for_status()
    return True


async def apply_delete(
    *,
    client: httpx.AsyncClient,
    target: ElasticTarget,
    entity_type: str,
    entity_id: Any,
) -> bool:
    """Apply a delete outbox event.

    Returns:
      True  - deleted
      False - noop (404)
    """

    doc_id = es_doc_id(entity_type, entity_id)
    resp = await client.delete(f"/{target.index}/_doc/{doc_id}")
    if resp.status_code == 404:
        return False
    resp.raise_for_status()
    return True


async def apply(*, ev: OutboxEventModel, session: AsyncSession) -> None:
    """Harness entrypoint: apply one outbox event to Elasticsearch."""

    target = elastic_target_from_env()

    op = str(getattr(ev, "op", ""))
    entity_type = str(getattr(ev, "entity_type", ""))
    entity_id = getattr(ev, "entity_id", None)
    if not entity_type.strip():
        raise BadPayload(projection=PROJECTION_NAME, reason="bad_payload", message="entity_type is required")
    if entity_id is None:
        raise BadPayload(projection=PROJECTION_NAME, reason="bad_payload", message="entity_id is required")

    async with httpx.AsyncClient(base_url=target.base_url, timeout=10.0) as client:
        if op == "upsert":
            await apply_upsert(
                session,
                client=client,
                target=target,
                entity_type=entity_type,
                entity_id=entity_id,
            )
            return

        if op == "delete":
            await apply_delete(
                client=client,
                target=target,
                entity_type=entity_type,
                entity_id=entity_id,
            )
            return

        raise ValueError(f"Unsupported outbox op for {PROJECTION_NAME}: {op!r}")
