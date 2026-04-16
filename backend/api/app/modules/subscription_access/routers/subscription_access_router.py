from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.app.config.security import get_auth_context
from api.app.modules.subscription_access.application.use_cases import (
    ApplyPaymentEventUseCase,
    GetAccessContextUseCase,
    GetSubscriptionHistoryUseCase,
    GetSubscriptionStateUseCase,
)
from api.app.modules.subscription_access.domain import PaymentEventType
from api.app.modules.subscription_access.exceptions import SubscriptionAccessNotFoundError
from api.app.modules.subscription_access.schemas import (
    AccessContextResponse,
    ApplyPaymentEventRequest,
    PaymentEventResponse,
    SubscriptionHistoryResponse,
    SubscriptionStateResponse,
)
from api.app.shared.auth_context import AuthContext
from api.app.shared.deps import get_db
from infra.storage.entitlement_snapshot_repository_impl import SQLAlchemyEntitlementSnapshotRepository
from infra.storage.payment_event_repository_impl import SQLAlchemyPaymentEventRepository
from infra.storage.plan_catalog_repository_impl import SQLAlchemyPlanCatalogRepository
from infra.storage.subscription_repository_impl import SQLAlchemySubscriptionRepository

router = APIRouter(tags=["subscription-access"])


def _build_use_cases(session: AsyncSession) -> tuple[
    GetAccessContextUseCase,
    GetSubscriptionStateUseCase,
    ApplyPaymentEventUseCase,
    GetSubscriptionHistoryUseCase,
]:
    plan_repo = SQLAlchemyPlanCatalogRepository(session)
    subscription_repo = SQLAlchemySubscriptionRepository(session)
    event_repo = SQLAlchemyPaymentEventRepository(session)
    snapshot_repo = SQLAlchemyEntitlementSnapshotRepository(session)
    return (
        GetAccessContextUseCase(plan_repo, subscription_repo, snapshot_repo),
        GetSubscriptionStateUseCase(subscription_repo, snapshot_repo),
        ApplyPaymentEventUseCase(plan_repo, subscription_repo, event_repo, snapshot_repo),
        GetSubscriptionHistoryUseCase(event_repo),
    )


@router.get("/access-context/me", response_model=AccessContextResponse)
async def get_access_context(
    auth_context: AuthContext = Depends(get_auth_context),
    session: AsyncSession = Depends(get_db),
) -> AccessContextResponse:
    access_uc, _, _, _ = _build_use_cases(session)
    try:
        result = await access_uc.execute(auth_context)
    except SubscriptionAccessNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return AccessContextResponse.model_validate(result.__dict__)


@router.get("/admin/subscriptions/{library_id}", response_model=SubscriptionStateResponse)
async def get_subscription_state(
    library_id: UUID,
    _: AuthContext = Depends(get_auth_context),
    session: AsyncSession = Depends(get_db),
) -> SubscriptionStateResponse:
    _, state_uc, _, _ = _build_use_cases(session)
    try:
        result = await state_uc.execute(library_id)
    except SubscriptionAccessNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return SubscriptionStateResponse.model_validate(result.__dict__)


@router.post("/admin/subscriptions/{library_id}/events", response_model=SubscriptionStateResponse)
async def apply_payment_event(
    library_id: UUID,
    request: ApplyPaymentEventRequest,
    _: AuthContext = Depends(get_auth_context),
    session: AsyncSession = Depends(get_db),
) -> SubscriptionStateResponse:
    _, _, apply_uc, _ = _build_use_cases(session)
    try:
        event_type = PaymentEventType(request.event_type)
        result = await apply_uc.execute(library_id=library_id, event_type=event_type)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid event_type") from exc
    except SubscriptionAccessNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return SubscriptionStateResponse.model_validate(result.__dict__)


@router.get("/admin/subscriptions/{library_id}/history", response_model=SubscriptionHistoryResponse)
async def get_subscription_history(
    library_id: UUID,
    _: AuthContext = Depends(get_auth_context),
    session: AsyncSession = Depends(get_db),
) -> SubscriptionHistoryResponse:
    _, _, _, history_uc = _build_use_cases(session)
    items = await history_uc.execute(library_id)
    return SubscriptionHistoryResponse(
        items=[
            PaymentEventResponse(
                id=item.id,
                subscription_id=item.subscription_id,
                library_id=item.library_id,
                event_type=item.event_type.value,
                created_at=item.created_at,
            )
            for item in items
        ]
    )