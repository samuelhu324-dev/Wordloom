from __future__ import annotations

from typing import Protocol, Sequence
from uuid import UUID

from .domain.models import EntitlementSnapshot, PaymentEvent, Plan, Subscription


class PlanCatalogRepository(Protocol):
    async def get_by_code(self, code: str) -> Plan | None: ...


class SubscriptionRepository(Protocol):
    async def get_by_library_id(self, library_id: UUID) -> Subscription | None: ...
    async def save(self, subscription: Subscription) -> Subscription: ...


class PaymentEventRepository(Protocol):
    async def append(self, event: PaymentEvent) -> PaymentEvent: ...
    async def list_by_library_id(self, library_id: UUID) -> Sequence[PaymentEvent]: ...


class EntitlementSnapshotRepository(Protocol):
    async def get_by_library_id(self, library_id: UUID) -> EntitlementSnapshot | None: ...
    async def create(
        self,
        *,
        library_id: UUID,
        plan_code: str,
        subscription_state: str,
        entitlements: tuple[str, ...],
    ) -> EntitlementSnapshot: ...
    async def save(self, snapshot: EntitlementSnapshot) -> EntitlementSnapshot: ...