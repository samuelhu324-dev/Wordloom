from unittest.mock import MagicMock

import pytest

from api.app.config.setting import get_settings
from api.app.dependencies_real import DIContainerReal


@pytest.fixture(autouse=True)
def _reset_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_chronicle_query_service_uses_events_repo_by_default(monkeypatch):
    monkeypatch.delenv("MERGED_READ_ENABLED", raising=False)
    get_settings.cache_clear()

    di = DIContainerReal(MagicMock())
    service = di.get_chronicle_query_service()

    assert service._repo is di.chronicle_entries_repo


def test_chronicle_query_service_uses_entries_repo_when_enabled(monkeypatch):
    monkeypatch.setenv("MERGED_READ_ENABLED", "1")
    get_settings.cache_clear()

    di = DIContainerReal(MagicMock())
    service = di.get_chronicle_query_service()

    assert service._repo is di.chronicle_entries_repo


def test_chronicle_query_service_uses_events_repo_when_rolled_back(monkeypatch):
    monkeypatch.setenv("MERGED_READ_ENABLED", "0")
    get_settings.cache_clear()

    di = DIContainerReal(MagicMock())
    service = di.get_chronicle_query_service()

    assert service._repo is di.chronicle_repo
