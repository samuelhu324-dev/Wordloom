from __future__ import annotations

from enum import Enum


class PaymentEventType(str, Enum):
    UPGRADE_SUCCESS = "upgrade_success"
    RENEWAL_FAILED = "renewal_failed"
    ADMIN_CORRECTION = "admin_correction"
