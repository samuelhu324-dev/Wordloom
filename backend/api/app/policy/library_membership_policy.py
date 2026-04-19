"""Policy: library membership management.

RBAC-lite v1 (S5A-2A):
- allow: owner/admin
- deny: member -> not_admin
- deny: no membership -> not_member
- deny: request attempts to target a different tenant -> tenant_mismatch
"""

from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status

from api.app.shared.auth_context import AuthContext

REASON_NOT_MEMBER = "not_member"
REASON_NOT_ADMIN = "not_admin"
REASON_TENANT_MISMATCH = "tenant_mismatch"


def assert_actor_is_tenant_admin(*, ctx: AuthContext, requested_library_id: UUID) -> None:
    if requested_library_id != ctx.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"reason": REASON_TENANT_MISMATCH},
        )

    if "owner" in ctx.roles or "admin" in ctx.roles:
        return
    if "member" in ctx.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"reason": REASON_NOT_ADMIN},
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={"reason": REASON_NOT_MEMBER},
    )


def assert_actor_can_manage_memberships(*, ctx: AuthContext, requested_library_id: UUID) -> None:
    assert_actor_is_tenant_admin(ctx=ctx, requested_library_id=requested_library_id)


__all__ = [
    "assert_actor_is_tenant_admin",
    "assert_actor_can_manage_memberships",
    "REASON_NOT_MEMBER",
    "REASON_NOT_ADMIN",
    "REASON_TENANT_MISMATCH",
]
