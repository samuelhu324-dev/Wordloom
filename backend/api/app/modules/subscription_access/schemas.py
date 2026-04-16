from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class AccessContextResponse(BaseModel):
    user_id: UUID
    tenant_id: UUID
    roles: tuple[str, ...]
    plan_code: str
    subscription_state: str
    entitlements: tuple[str, ...]
    request_id: str


class SubscriptionStateResponse(BaseModel):
    library_id: UUID
    plan_code: str
    subscription_state: str
    entitlements: tuple[str, ...]


class ApplyPaymentEventRequest(BaseModel):
    event_type: str


class PaymentEventResponse(BaseModel):
    id: UUID
    subscription_id: UUID
    library_id: UUID
    event_type: str
    created_at: datetime


class SubscriptionHistoryResponse(BaseModel):
    items: List[PaymentEventResponse]