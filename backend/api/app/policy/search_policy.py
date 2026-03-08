"""Policy entrypoints for search module.

Phase: S5B-4A (search query authorization + tenant isolation v1)

This module centralizes authorization decisions for search endpoints so that
routers do not have to duplicate role/tenant logic.

Current focus (v1):
- `GET /search/blocks/two-stage` → `search.blocks.two_stage`
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from fastapi import status
from uuid import UUID

from api.app.policy.library_membership_policy import (
    REASON_NOT_MEMBER,
    REASON_TENANT_MISMATCH,
)
from api.app.shared.auth_context import AuthContext


@dataclass(frozen=True)
class SearchBlocksTwoStageDecision:
    """Decision for `search.blocks.two_stage`.

    Fields are aligned with S5B-1A/S5B-4A contracts so that routers can map
    directly to HTTP + audit_log.
    """

    allowed: bool
    http_status: int
    audit_result: str
    reason: Optional[str]


async def authorize_search_blocks_two_stage(
    *,
    ctx: AuthContext,
    requested_library_id: Optional[UUID],
) -> SearchBlocksTwoStageDecision:
    """Authorize two-stage block search.

    Contract (S5B-4A/P0-C1-S2):
    - Tenant boundary:
      - If client passes a library_id that does not match ctx.tenant_id → deny
        with `result=denied, reason=tenant_mismatch` (HTTP 403).
      - If no library_id is provided, use ctx.tenant_id as effective scope.
    - Membership:
      - If actor has no roles for the selected tenant (roles empty) → deny with
        `result=denied, reason=not_member` (HTTP 403).
      - Otherwise (owner/admin/member) → allow.
    """

    # Enforce tenant boundary first.
    if requested_library_id is not None and str(requested_library_id) != str(ctx.tenant_id):
        return SearchBlocksTwoStageDecision(
            allowed=False,
            http_status=status.HTTP_403_FORBIDDEN,
            audit_result="denied",
            reason=REASON_TENANT_MISMATCH,
        )

    roles = tuple(ctx.roles or ())
    if not roles:
        return SearchBlocksTwoStageDecision(
            allowed=False,
            http_status=status.HTTP_403_FORBIDDEN,
            audit_result="denied",
            reason=REASON_NOT_MEMBER,
        )

    return SearchBlocksTwoStageDecision(
        allowed=True,
        http_status=status.HTTP_200_OK,
        audit_result="success",
        reason=None,
    )


__all__ = [
    "SearchBlocksTwoStageDecision",
    "authorize_search_blocks_two_stage",
]
