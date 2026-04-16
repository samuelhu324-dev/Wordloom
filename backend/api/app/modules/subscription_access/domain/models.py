from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from .event_types import PaymentEventType


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class Plan:
    code: str
    display_name: str


@dataclass
class Subscription:
    library_id: UUID
    plan_code: str
    state: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=_utcnow)
    updated_at: datetime = field(default_factory=_utcnow)

    def apply_state(self, next_state: str) -> None:
        self.state = next_state
        self.updated_at = _utcnow()


@dataclass(frozen=True)
class PaymentEvent:
    subscription_id: UUID
    library_id: UUID
    event_type: PaymentEventType
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=_utcnow)


@dataclass
class EntitlementSnapshot:
    library_id: UUID
    plan_code: str
    subscription_state: str
    entitlements: tuple[str, ...]
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=_utcnow)
    updated_at: datetime = field(default_factory=_utcnow)

    def refresh(self, plan_code: str, subscription_state: str, entitlements: tuple[str, ...]) -> None:
        self.plan_code = plan_code
        self.subscription_state = subscription_state
        self.entitlements = entitlements
        self.updated_at = _utcnow()