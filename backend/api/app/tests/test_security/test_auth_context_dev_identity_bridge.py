from __future__ import annotations

from uuid import UUID, uuid4

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from api.app.config.security import get_auth_context
from api.app.shared.deps import get_db


async def _fake_db():
    yield object()


def test_dev_identity_header_drives_membership_backed_roles(monkeypatch) -> None:
    app = FastAPI()

    @app.get('/api/v1/_auth-context')
    async def _route(auth_context=Depends(get_auth_context)):
        return {
            'user_id': str(auth_context.user_id),
            'tenant_id': str(auth_context.tenant_id),
            'roles': list(auth_context.roles),
        }

    app.dependency_overrides[get_db] = _fake_db

    tenant_id = uuid4()
    dev_user_id = UUID('22222222-2222-4222-8222-222222222222')

    async def _fake_get_role(self, *, library_id, user_id):
        assert library_id == tenant_id
        assert user_id == dev_user_id
        return 'admin'

    monkeypatch.setattr(
        'infra.storage.library_membership_repository_impl.SQLAlchemyLibraryMembershipRepository.get_role',
        _fake_get_role,
    )

    client = TestClient(app)
    response = client.get(
        '/api/v1/_auth-context',
        headers={
            'X-Library-Id': str(tenant_id),
            'X-Dev-User-Id': str(dev_user_id),
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'user_id': str(dev_user_id),
        'tenant_id': str(tenant_id),
        'roles': ['admin', 'member'],
    }