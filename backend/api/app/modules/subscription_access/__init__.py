from .application.use_cases import (
    ApplyPaymentEventUseCase,
    GetAccessContextUseCase,
    GetSubscriptionHistoryUseCase,
    GetSubscriptionStateUseCase,
)
from .domain import EntitlementSnapshot, PaymentEvent, PaymentEventType, Plan, Subscription
from .exceptions import SubscriptionAccessError, SubscriptionAccessNotFoundError
from .schemas import (
    AccessContextResponse,
    ApplyPaymentEventRequest,
    SubscriptionHistoryResponse,
    SubscriptionStateResponse,
)

try:
    from .routers.subscription_access_router import router
except Exception:
    router = None

__all__ = [
    "Plan",
    "Subscription",
    "PaymentEvent",
    "EntitlementSnapshot",
    "PaymentEventType",
    "GetAccessContextUseCase",
    "GetSubscriptionStateUseCase",
    "ApplyPaymentEventUseCase",
    "GetSubscriptionHistoryUseCase",
    "AccessContextResponse",
    "SubscriptionStateResponse",
    "ApplyPaymentEventRequest",
    "SubscriptionHistoryResponse",
    "SubscriptionAccessError",
    "SubscriptionAccessNotFoundError",
    "router",
]