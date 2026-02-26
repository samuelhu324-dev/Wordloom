from __future__ import annotations

import logging
import os

from sqlalchemy.ext.asyncio import AsyncSession

from api.app.modules.search.application.ports.candidate_provider import CandidateProvider
from infra.search.postgres_fts_candidate_provider import PostgresFTSCandidateProvider
from infra.search.elastic_candidate_provider import ElasticCandidateProvider

logger = logging.getLogger(__name__)


def _env_truthy(name: str) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return False
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def _env_truthy_default(name: str, *, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def get_stage1_candidate_provider(session: AsyncSession) -> CandidateProvider:
    """Factory for Stage1 candidate providers.

    Controlled by env var:
      - SEARCH_STAGE1_PROVIDER=postgres|elastic

        Read switch (independent from Chronicle) controlled by env var:
            - SEARCH_MERGED_READ_ENABLED=0/1

        When enabled, forces provider=postgres (projection-backed), regardless of
        SEARCH_STAGE1_PROVIDER, to support a safe, rollbackable read switch.

        Cutover default:
        - Default to merged-enabled (projection-backed postgres) when the env var is
            unset.
        - Rollback: set SEARCH_MERGED_READ_ENABLED=0, and optionally
            SEARCH_STAGE1_PROVIDER=elastic.
    """

        merged_enabled = _env_truthy_default("SEARCH_MERGED_READ_ENABLED", default=True)
    provider = (
        "postgres"
        if merged_enabled
        else (os.getenv("SEARCH_STAGE1_PROVIDER") or "postgres").strip().lower()
    )

    if provider == "postgres":
        selected: CandidateProvider = PostgresFTSCandidateProvider(session)
    elif provider == "elastic":
        selected = ElasticCandidateProvider()
    else:
        raise ValueError(f"Unknown SEARCH_STAGE1_PROVIDER={provider!r}")

    logger.info(
        {
            "event": "search.stage1.provider.selected",
            "provider": provider,
            "search_merged_read_enabled": merged_enabled,
        }
    )
    return selected


__all__ = ["get_stage1_candidate_provider"]
