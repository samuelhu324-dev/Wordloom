from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4

import pytest

from api.app.modules.subscription_access.application.use_cases import (
    ApplyPaymentEventUseCase,
    GetAccessContextUseCase,
    GetSubscriptionHistoryUseCase,
    GetSubscriptionStateUseCase,
)
from api.app.modules.subscription_access.domain import PaymentEvent, PaymentEventType, Plan, Subscription
from api.app.modules.subscription_access.domain.models import EntitlementSnapshot
from api.app.shared.auth_context import AuthContext


class InMemoryPlanRepo:
    def __init__(self) -> None:
        self.items = {
            "trial": Plan(code="trial", display_name="Trial"),
            "standard": Plan(code="standard", display_name="Standard"),
        }

    async def get_by_code(self, code: str) -> Plan | None:
        return self.items.get(code)


class InMemorySubscriptionRepo:
    def __init__(self, subscription: Subscription) -> None:
        self.subscription = subscription

    async def get_by_library_id(self, library_id: UUID) -> Subscription | None:
        return self.subscription if self.subscription.library_id == library_id else None

    async def save(self, subscription: Subscription) -> Subscription:
        self.subscription = subscription
        return subscription


class InMemoryEventRepo:
    def __init__(self) -> None:
        self.items: list[PaymentEvent] = []

    async def append(self, event: PaymentEvent) -> PaymentEvent:
        self.items.append(event)
        return event

    async def list_by_library_id(self, library_id: UUID) -> list[PaymentEvent]:
        return [item for item in self.items if item.library_id == library_id]


class InMemorySnapshotRepo:
    def __init__(self, snapshot: EntitlementSnapshot | None = None) -> None:
        self.snapshot = snapshot

    async def get_by_library_id(self, library_id: UUID) -> EntitlementSnapshot | None:
        if self.snapshot is None:
            return None
        return self.snapshot if self.snapshot.library_id == library_id else None

    async def create(
        self,
        *,
        library_id: UUID,
        plan_code: str,
        subscription_state: str,
        entitlements: tuple[str, ...],
    ) -> EntitlementSnapshot:
        self.snapshot = EntitlementSnapshot(
            library_id=library_id,
            plan_code=plan_code,
            subscription_state=subscription_state,
            entitlements=entitlements,
        )
        return self.snapshot

    async def save(self, snapshot: EntitlementSnapshot) -> EntitlementSnapshot:
        self.snapshot = snapshot
        return snapshot


@pytest.fixture
def library_id() -> UUID:
    return uuid4()


@pytest.fixture
def auth_context(library_id: UUID) -> AuthContext:
    return AuthContext(user_id=uuid4(), tenant_id=library_id, roles=("member",), request_id="req-1")


@pytest.fixture
def trial_subscription(library_id: UUID) -> Subscription:
    return Subscription(library_id=library_id, plan_code="trial", state="trialing")


@pytest.mark.asyncio
async def test_get_access_context_reads_existing_subscription(auth_context: AuthContext, trial_subscription: Subscription) -> None:
    usecase = GetAccessContextUseCase(InMemoryPlanRepo(), InMemorySubscriptionRepo(trial_subscription), InMemorySnapshotRepo())

    result = await usecase.execute(auth_context)

    assert result.tenant_id == auth_context.tenant_id
    assert result.plan_code == "trial"
    assert result.subscription_state == "trialing"
    assert result.entitlements == ("read_library",)


@pytest.mark.asyncio
async def test_apply_payment_event_updates_state_and_snapshot(library_id: UUID, trial_subscription: Subscription) -> None:
    plan_repo = InMemoryPlanRepo()
    subscription_repo = InMemorySubscriptionRepo(trial_subscription)
    event_repo = InMemoryEventRepo()
    snapshot_repo = InMemorySnapshotRepo()
    usecase = ApplyPaymentEventUseCase(plan_repo, subscription_repo, event_repo, snapshot_repo)

    result = await usecase.execute(library_id=library_id, event_type=PaymentEventType.UPGRADE_SUCCESS)

    assert result.subscription_state == "active"
    assert "copy_block_cross_book" not in result.entitlements
    assert len(event_repo.items) == 1
    assert snapshot_repo.snapshot is not None
    assert snapshot_repo.snapshot.subscription_state == "active"


@pytest.mark.asyncio
async def test_history_returns_applied_events(library_id: UUID, trial_subscription: Subscription) -> None:
    event_repo = InMemoryEventRepo()
    apply_usecase = ApplyPaymentEventUseCase(
        InMemoryPlanRepo(),
        InMemorySubscriptionRepo(trial_subscription),
        event_repo,
        InMemorySnapshotRepo(),
    )
    await apply_usecase.execute(library_id=library_id, event_type=PaymentEventType.UPGRADE_SUCCESS)

    history = await GetSubscriptionHistoryUseCase(event_repo).execute(library_id)

    assert len(history) == 1
    assert history[0].event_type == PaymentEventType.UPGRADE_SUCCESS