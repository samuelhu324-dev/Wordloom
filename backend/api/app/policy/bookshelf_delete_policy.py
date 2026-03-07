"""Policy entrypoint for `bookshelf.delete`.

Phase: S5B-2A (Policy entrypoint consolidation v1)

Intent:
- Centralize authorization decisions (roles + tenant boundary classification)
- Produce a low-cardinality deny reason suitable for audit_log.reason

Notes:
- This entrypoint is intentionally async and DB-aware so routers do not need to
  run raw SQL probes for tenant mismatch classification.
- It does not perform the delete; it only decides whether the request may proceed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from fastapi import status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from api.app.policy.library_membership_policy import (
    REASON_NOT_ADMIN,
    REASON_NOT_MEMBER,
    REASON_TENANT_MISMATCH,
)
from api.app.shared.auth_context import AuthContext


@dataclass(frozen=True)
class BookshelfDeleteDecision:
    allowed: bool
    http_status: int
    audit_result: str
    reason: Optional[str]
    bookshelf_library_id: Optional[UUID] = None


async def authorize_bookshelf_delete(
    *,
    ctx: AuthContext,
    bookshelf_id: UUID,
    session: AsyncSession,
) -> BookshelfDeleteDecision:
    """Authorize the `bookshelf.delete` action.

    Contract (S5B-2A/P0-C1-S2):
    - allow: owner/admin
    - deny: member -> 403 + denied + not_admin
    - deny: no membership -> 403 + denied + not_member
    - tenant mismatch (write-path) -> 403 + denied + tenant_mismatch
    - not found -> 404 + not_found + reason=null
    """

    roles = ctx.roles or []

    if not roles:
        return BookshelfDeleteDecision(
            allowed=False,
            http_status=status.HTTP_403_FORBIDDEN,
            audit_result="denied",
            reason=REASON_NOT_MEMBER,
        )

    if "owner" not in roles and "admin" not in roles:
        if "member" in roles:
            return BookshelfDeleteDecision(
                allowed=False,
                http_status=status.HTTP_403_FORBIDDEN,
                audit_result="denied",
                reason=REASON_NOT_ADMIN,
            )
        return BookshelfDeleteDecision(
            allowed=False,
            http_status=status.HTTP_403_FORBIDDEN,
            audit_result="denied",
            reason=REASON_NOT_MEMBER,
        )

    q = text("SELECT library_id FROM bookshelves WHERE id = :bookshelf_id")
    row = (await session.execute(q, {"bookshelf_id": str(bookshelf_id)})).first()
    if not row or row[0] is None:
        return BookshelfDeleteDecision(
            allowed=False,
            http_status=status.HTTP_404_NOT_FOUND,
            audit_result="not_found",
            reason=None,
        )

    bookshelf_library_id = row[0]
    if str(bookshelf_library_id) != str(ctx.tenant_id):
        return BookshelfDeleteDecision(
            allowed=False,
            http_status=status.HTTP_403_FORBIDDEN,
            audit_result="denied",
            reason=REASON_TENANT_MISMATCH,
            bookshelf_library_id=bookshelf_library_id,
        )

    return BookshelfDeleteDecision(
        allowed=True,
        http_status=status.HTTP_204_NO_CONTENT,
        audit_result="allowed",
        reason=None,
        bookshelf_library_id=bookshelf_library_id,
    )


__all__ = ["BookshelfDeleteDecision", "authorize_bookshelf_delete"]
