from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from api.app.modules.subscription_access.domain import PaymentEvent, PaymentEventType, compute_entitlements, derive_subscription_state
from api.app.shared.access_context import AccessContext
from api.app.shared.auth_context import AuthContext

from ..exceptions import SubscriptionAccessNotFoundError
from ..repository import (
    EntitlementSnapshotRepository,
    PaymentEventRepository,
    PlanCatalogRepository,
    SubscriptionRepository,
)


@dataclass(frozen=True)
class SubscriptionStateView:
    library_id: UUID
    plan_code: str
    subscription_state: str
    entitlements: tuple[str, ...]


class GetAccessContextUseCase:
    def __init__(
        self,
        plans: PlanCatalogRepository,
        subscriptions: SubscriptionRepository,
        snapshots: EntitlementSnapshotRepository,
    ) -> None:
        self._plans = plans
        self._subscriptions = subscriptions
        self._snapshots = snapshots

    async def execute(self, auth_context: AuthContext) -> AccessContext:
        subscription = await self._subscriptions.get_by_library_id(auth_context.tenant_id)
        if subscription is None:
            raise SubscriptionAccessNotFoundError("subscription not found")
        snapshot = await self._snapshots.get_by_library_id(auth_context.tenant_id)
        entitlements = snapshot.entitlements if snapshot is not None else compute_entitlements(subscription.plan_code, subscription.state)
        return AccessContext(
            user_id=auth_context.user_id,
            tenant_id=auth_context.tenant_id,
            roles=auth_context.roles,
            plan_code=subscription.plan_code,
            subscription_state=subscription.state,
            entitlements=tuple(entitlements),
            request_id=auth_context.request_id,
        )


class GetSubscriptionStateUseCase:
    def __init__(
        self,
        subscriptions: SubscriptionRepository,
        snapshots: EntitlementSnapshotRepository,
    ) -> None:
        self._subscriptions = subscriptions
        self._snapshots = snapshots

    async def execute(self, library_id: UUID) -> SubscriptionStateView:
        subscription = await self._subscriptions.get_by_library_id(library_id)
        if subscription is None:
            raise SubscriptionAccessNotFoundError("subscription not found")
        snapshot = await self._snapshots.get_by_library_id(library_id)
        entitlements = snapshot.entitlements if snapshot is not None else compute_entitlements(subscription.plan_code, subscription.state)
        return SubscriptionStateView(
            library_id=library_id,
            plan_code=subscription.plan_code,
            subscription_state=subscription.state,
            entitlements=tuple(entitlements),
        )


class ApplyPaymentEventUseCase:
    def __init__(
        self,
        plans: PlanCatalogRepository,
        subscriptions: SubscriptionRepository,
        events: PaymentEventRepository,
        snapshots: EntitlementSnapshotRepository,
    ) -> None:
        self._plans = plans
        self._subscriptions = subscriptions
        self._events = events
        self._snapshots = snapshots

    async def execute(self, *, library_id: UUID, event_type: PaymentEventType) -> SubscriptionStateView:
        subscription = await self._subscriptions.get_by_library_id(library_id)
        if subscription is None:
            raise SubscriptionAccessNotFoundError("subscription not found")

        next_state = derive_subscription_state(subscription.state, event_type)
        subscription.apply_state(next_state)
        await self._subscriptions.save(subscription)

        event = PaymentEvent(
            subscription_id=subscription.id,
            library_id=library_id,
            event_type=event_type,
        )
        await self._events.append(event)

        entitlements = compute_entitlements(subscription.plan_code, subscription.state)
        snapshot = await self._snapshots.get_by_library_id(library_id)
        if snapshot is None:
            snapshot = await self._snapshots.create(
                library_id=library_id,
                plan_code=subscription.plan_code,
                subscription_state=subscription.state,
                entitlements=entitlements,
            )
        else:
            snapshot.refresh(subscription.plan_code, subscription.state, entitlements)
            await self._snapshots.save(snapshot)

        return SubscriptionStateView(
            library_id=library_id,
            plan_code=subscription.plan_code,
            subscription_state=subscription.state,
            entitlements=entitlements,
        )


class GetSubscriptionHistoryUseCase:
    def __init__(self, events: PaymentEventRepository) -> None:
        self._events = events

    async def execute(self, library_id: UUID) -> list[PaymentEvent]:
        return list(await self._events.list_by_library_id(library_id))