from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.app.config.security import get_auth_context
from api.app.modules.subscription_access.routers.subscription_access_router import router
from api.app.shared.auth_context import AuthContext
from api.app.shared.deps import get_db


class _FakeAccessUseCase:
    def __init__(self, payload):
        self.payload = payload

    async def execute(self, *_args, **_kwargs):
        return self.payload


class _FakeStateUseCase:
    def __init__(self, payload):
        self.payload = payload

    async def execute(self, *_args, **_kwargs):
        return self.payload


class _FakeApplyUseCase:
    def __init__(self, payload):
        self.payload = payload

    async def execute(self, *_args, **_kwargs):
        return self.payload


class _FakeHistoryUseCase:
    def __init__(self, payload):
        self.payload = payload

    async def execute(self, *_args, **_kwargs):
        return self.payload


async def _fake_db():
    yield object()


async def _fake_auth_context() -> AuthContext:
    return AuthContext(
        user_id=uuid4(),
        tenant_id=uuid4(),
        roles=("member",),
        request_id="req-test",
    )


def test_subscription_access_router_registers_expected_paths() -> None:
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")

    paths = {route.path for route in app.routes}

    assert "/api/v1/access-context/me" in paths
    assert "/api/v1/admin/subscriptions/{library_id}" in paths
    assert "/api/v1/admin/subscriptions/{library_id}/events" in paths
    assert "/api/v1/admin/subscriptions/{library_id}/history" in paths


def test_access_context_endpoint_returns_backend_payload(monkeypatch) -> None:
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    app.dependency_overrides[get_auth_context] = _fake_auth_context
    app.dependency_overrides[get_db] = _fake_db

    tenant_id = uuid4()
    payload = SimpleNamespace(
        user_id=uuid4(),
        tenant_id=tenant_id,
        roles=("member",),
        plan_code="trial",
        subscription_state="trialing",
        entitlements=("read_library",),
        request_id="req-test",
    )

    def _fake_build_use_cases(_session):
        return (
            _FakeAccessUseCase(payload),
            _FakeStateUseCase(None),
            _FakeApplyUseCase(None),
            _FakeHistoryUseCase([]),
        )

    monkeypatch.setattr(
        "api.app.modules.subscription_access.routers.subscription_access_router._build_use_cases",
        _fake_build_use_cases,
    )

    client = TestClient(app)
    response = client.get("/api/v1/access-context/me", headers={"X-Library-Id": str(tenant_id)})

    assert response.status_code == 200
    assert response.json()["plan_code"] == "trial"
    assert response.json()["subscription_state"] == "trialing"


def test_apply_event_endpoint_returns_updated_state(monkeypatch) -> None:
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    app.dependency_overrides[get_auth_context] = _fake_auth_context
    app.dependency_overrides[get_db] = _fake_db

    library_id = uuid4()
    payload = SimpleNamespace(
        library_id=library_id,
        plan_code="standard",
        subscription_state="active",
        entitlements=("read_library", "copy_block_cross_book"),
    )

    def _fake_build_use_cases(_session):
        return (
            _FakeAccessUseCase(None),
            _FakeStateUseCase(payload),
            _FakeApplyUseCase(payload),
            _FakeHistoryUseCase([]),
        )

    monkeypatch.setattr(
        "api.app.modules.subscription_access.routers.subscription_access_router._build_use_cases",
        _fake_build_use_cases,
    )

    client = TestClient(app)
    response = client.post(
        f"/api/v1/admin/subscriptions/{library_id}/events",
        headers={"X-Library-Id": str(library_id)},
        json={"event_type": "upgrade_success"},
    )

    assert response.status_code == 200
    assert response.json()["subscription_state"] == "active"
    assert "copy_block_cross_book" in response.json()["entitlements"]