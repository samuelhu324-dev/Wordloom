from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple
from uuid import UUID


@dataclass(frozen=True)
class AccessContext:
    user_id: UUID
    tenant_id: UUID
    roles: Tuple[str, ...]
    plan_code: str
    subscription_state: str
    entitlements: Tuple[str, ...]
    request_id: str


__all__ = ["AccessContext"]