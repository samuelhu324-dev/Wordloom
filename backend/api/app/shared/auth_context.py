from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple
from uuid import UUID


@dataclass(frozen=True)
class AuthContext:
    """Unified request auth context (authn + tenant selection).

    v1 contract (S5A-1A):
    - JWT Bearer auth
    - tenant_id == library_id
    - roles are intentionally minimal and may be empty
    - request_id is required for audit/log correlation
    """

    user_id: UUID
    tenant_id: UUID
    roles: Tuple[str, ...]
    request_id: str
