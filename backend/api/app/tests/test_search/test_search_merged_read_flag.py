from unittest.mock import MagicMock

import pytest

from infra.search.candidate_provider_factory import get_stage1_candidate_provider
from infra.search.elastic_candidate_provider import ElasticCandidateProvider
from infra.search.postgres_fts_candidate_provider import PostgresFTSCandidateProvider


@pytest.mark.parametrize(
    "env_value, expected",
    [
        (None, PostgresFTSCandidateProvider),
        ("0", PostgresFTSCandidateProvider),
        ("false", PostgresFTSCandidateProvider),
    ],
)
def test_search_stage1_provider_respects_env_default_postgres(monkeypatch, env_value, expected):
    monkeypatch.delenv("SEARCH_STAGE1_PROVIDER", raising=False)
    monkeypatch.delenv("SEARCH_MERGED_READ_ENABLED", raising=False)
    if env_value is not None:
        monkeypatch.setenv("SEARCH_MERGED_READ_ENABLED", env_value)

    provider = get_stage1_candidate_provider(MagicMock())
    assert isinstance(provider, expected)


def test_search_stage1_provider_can_select_elastic_when_not_merged(monkeypatch):
    monkeypatch.setenv("SEARCH_STAGE1_PROVIDER", "elastic")
    monkeypatch.delenv("SEARCH_MERGED_READ_ENABLED", raising=False)

    provider = get_stage1_candidate_provider(MagicMock())
    assert isinstance(provider, ElasticCandidateProvider)


@pytest.mark.parametrize("truthy", ["1", "true", "yes", "on"]) 
def test_search_stage1_provider_forces_postgres_when_merged_enabled(monkeypatch, truthy):
    monkeypatch.setenv("SEARCH_STAGE1_PROVIDER", "elastic")
    monkeypatch.setenv("SEARCH_MERGED_READ_ENABLED", truthy)

    provider = get_stage1_candidate_provider(MagicMock())
    assert isinstance(provider, PostgresFTSCandidateProvider)
