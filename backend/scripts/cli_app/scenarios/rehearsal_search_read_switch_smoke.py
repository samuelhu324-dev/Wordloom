from __future__ import annotations

import asyncio
import os
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from infra.search.candidate_provider_factory import get_stage1_candidate_provider
from infra.search.elastic_candidate_provider import ElasticCandidateProvider
from infra.search.postgres_fts_candidate_provider import PostgresFTSCandidateProvider

from ..registry import register
from ..types import DrillInputs, DrillResult


def _env_snapshot(names: list[str]) -> dict[str, str | None]:
    return {n: os.environ.get(n) for n in names}


def _env_restore(snapshot: dict[str, str | None]) -> None:
    for k, v in snapshot.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


async def _probe(*, database_url: str) -> dict[str, Any]:
    engine = create_async_engine(database_url)
    try:
        async with AsyncSession(engine) as session:
            await session.execute(text("SELECT 1"))

            names = ["SEARCH_STAGE1_PROVIDER", "SEARCH_MERGED_READ_ENABLED"]
            before = _env_snapshot(names)
            try:
                os.environ["SEARCH_STAGE1_PROVIDER"] = "elastic"
                os.environ["SEARCH_MERGED_READ_ENABLED"] = "0"
                provider_a = get_stage1_candidate_provider(session)

                os.environ["SEARCH_MERGED_READ_ENABLED"] = "1"
                provider_b = get_stage1_candidate_provider(session)
            finally:
                _env_restore(before)

            return {
                "provider_default_name": type(provider_a).__name__,
                "provider_merged_name": type(provider_b).__name__,
                "provider_default_is_elastic": isinstance(provider_a, ElasticCandidateProvider),
                "provider_merged_is_postgres": isinstance(provider_b, PostgresFTSCandidateProvider),
            }
    finally:
        await engine.dispose()


@register("rehearsal_search_read_switch_smoke")
@register("rehearsal-search-read-switch-smoke")
def run(inputs: DrillInputs) -> DrillResult:
    payload = inputs.model_dump()

    database_url = str(payload.get("database_url") or "").strip()
    if not database_url:
        return DrillResult(ok=False, errors=["DATABASE_URL is required"], meta={}, summary={})

    try:
        probe = asyncio.run(_probe(database_url=database_url))
    except Exception as exc:  # noqa: BLE001
        return DrillResult(ok=False, errors=[f"probe failed: {exc}"], meta={}, summary={})

    ok = bool(probe.get("provider_default_is_elastic")) and bool(probe.get("provider_merged_is_postgres"))
    errors: list[str] = []
    if not probe.get("provider_default_is_elastic"):
        errors.append("expected provider=Elastic when SEARCH_STAGE1_PROVIDER=elastic and SEARCH_MERGED_READ_ENABLED=0")
    if not probe.get("provider_merged_is_postgres"):
        errors.append("expected provider=Postgres when SEARCH_MERGED_READ_ENABLED=1 (forces postgres)")

    return DrillResult(
        ok=ok,
        errors=errors,
        meta={
            "probe": probe,
        },
        summary={
            "search_read_switch": {
                "search_stage1_provider": "elastic",
                "merged_read_enabled_values": ["0", "1"],
                "expected": {
                    "merged_disabled": "ElasticCandidateProvider",
                    "merged_enabled": "PostgresFTSCandidateProvider",
                },
                "observed": {
                    "merged_disabled": probe.get("provider_default_name"),
                    "merged_enabled": probe.get("provider_merged_name"),
                },
            }
        },
    )
