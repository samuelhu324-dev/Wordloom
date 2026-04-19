from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.app.config.security import get_auth_context
from api.app.modules.library.routers.library_router import router
from api.app.shared.auth_context import AuthContext
from api.app.shared.deps import get_db


async def _fake_db():
    yield object()


def _make_fake_auth_context(*, tenant_id, roles):
    async def _fake_auth() -> AuthContext:
        return AuthContext(
            user_id=uuid4(),
            tenant_id=tenant_id,
            roles=roles,
            request_id='req-membership-test',
        )

    return _fake_auth


def test_admin_can_list_library_memberships(monkeypatch) -> None:
    app = FastAPI()
    app.include_router(router, prefix='/api/v1/libraries')
    app.dependency_overrides[get_db] = _fake_db

    library_id = uuid4()
    app.dependency_overrides[get_auth_context] = _make_fake_auth_context(
        tenant_id=library_id,
        roles=('admin', 'member'),
    )

    async def _fake_list_by_library(self, *, library_id):
        return [
            SimpleNamespace(
                id=uuid4(),
                library_id=library_id,
                user_id=uuid4(),
                role='member',
                created_at=SimpleNamespace(isoformat=lambda: '2026-04-17T00:00:00+00:00'),
                updated_at=SimpleNamespace(isoformat=lambda: '2026-04-17T00:00:00+00:00'),
            )
        ]

    monkeypatch.setattr(
        'infra.storage.library_membership_repository_impl.SQLAlchemyLibraryMembershipRepository.list_by_library',
        _fake_list_by_library,
    )

    client = TestClient(app)
    response = client.get(
        f'/api/v1/libraries/{library_id}/memberships',
        headers={'X-Library-Id': str(library_id)},
    )

    assert response.status_code == 200
    assert len(response.json()['items']) == 1
    assert response.json()['items'][0]['role'] == 'member'


def test_member_cannot_list_library_memberships() -> None:
    app = FastAPI()
    app.include_router(router, prefix='/api/v1/libraries')
    app.dependency_overrides[get_db] = _fake_db

    library_id = uuid4()
    app.dependency_overrides[get_auth_context] = _make_fake_auth_context(
        tenant_id=library_id,
        roles=('member',),
    )

    client = TestClient(app)
    response = client.get(
        f'/api/v1/libraries/{library_id}/memberships',
        headers={'X-Library-Id': str(library_id)},
    )

    assert response.status_code == 403
    assert response.json()['detail']['reason'] == 'not_admin'