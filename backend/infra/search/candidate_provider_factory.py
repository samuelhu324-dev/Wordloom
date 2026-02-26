from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from api.app.modules.search.application.ports.candidate_provider import CandidateProvider
from infra.search.postgres_fts_candidate_provider import PostgresFTSCandidateProvider

logger = logging.getLogger(__name__)


def get_stage1_candidate_provider(session: AsyncSession) -> CandidateProvider:
    """Factory for Stage1 candidate providers.

    S2B-5A deletion slice 2:
    - Search read is merged-only (projection-backed Postgres).
    - Legacy rollback wiring via SEARCH_MERGED_READ_ENABLED / SEARCH_STAGE1_PROVIDER
      has been removed.
    """

    provider = "postgres"
    selected: CandidateProvider = PostgresFTSCandidateProvider(session)

    logger.info(
        {
            "event": "search.stage1.provider.selected",
            "provider": provider,
            "search_merged_read_enabled": True,
        }
    )
    return selected


__all__ = ["get_stage1_candidate_provider"]
