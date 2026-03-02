from __future__ import annotations

from typing import Optional
from uuid import UUID

from api.app.policy import check
from api.app.modules.bookshelf.exceptions import BookshelfForbiddenError
from api.app.shared.auth_context import AuthContext


REASON_NOT_OWNER = "not_owner"  # low-cardinality
REASON_NOT_MEMBER = "not_member"  # low-cardinality
REASON_NOT_ADMIN = "not_admin"  # low-cardinality
REASON_TENANT_MISMATCH = "tenant_mismatch"  # low-cardinality


def assert_actor_owns_library_for_bookshelf(
    *,
    actor_user_id: Optional[UUID],
    enforce_owner_check: bool,
    library_id: UUID,
    library_owner_user_id: Optional[UUID],
    bookshelf_id: UUID,
) -> None:
    """Policy: actor must own the library that contains the bookshelf.

    v1 simplification: library owner == only allowed actor.
    """

    if not enforce_owner_check:
        return
    if actor_user_id is None:
        return

    check(
        allowed=(library_owner_user_id == actor_user_id),
        exc_factory=lambda: BookshelfForbiddenError(
            bookshelf_id=str(bookshelf_id),
            library_id=str(library_id),
            actor_user_id=str(actor_user_id),
            reason=REASON_NOT_OWNER,
        ),
    )


def assert_actor_can_create_bookshelf(
    *,
    ctx: AuthContext,
    requested_library_id: UUID,
) -> None:
    """Policy: creating a bookshelf is an admin action.

    RBAC-lite v1 (S5A-2A):
    - allow: owner/admin
    - deny: member -> not_admin
    - deny: no membership -> not_member
    - deny: request attempts to target a different tenant -> tenant_mismatch
    """

    check(
        allowed=(requested_library_id == ctx.tenant_id),
        exc_factory=lambda: BookshelfForbiddenError(
            library_id=str(requested_library_id),
            actor_user_id=str(ctx.user_id),
            reason=REASON_TENANT_MISMATCH,
        ),
    )

    if "owner" in ctx.roles or "admin" in ctx.roles:
        return
    if "member" in ctx.roles:
        raise BookshelfForbiddenError(
            library_id=str(ctx.tenant_id),
            actor_user_id=str(ctx.user_id),
            reason=REASON_NOT_ADMIN,
        )
    raise BookshelfForbiddenError(
        library_id=str(ctx.tenant_id),
        actor_user_id=str(ctx.user_id),
        reason=REASON_NOT_MEMBER,
    )
