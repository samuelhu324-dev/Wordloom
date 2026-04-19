from __future__ import annotations

from .event_types import PaymentEventType


def derive_subscription_state(current_state: str, event_type: PaymentEventType) -> str:
    if event_type == PaymentEventType.UPGRADE_SUCCESS:
        return "active"
    if event_type == PaymentEventType.RENEWAL_FAILED:
        return "past_due"
    if event_type == PaymentEventType.ADMIN_CORRECTION:
        return current_state
    return current_state


def compute_entitlements(plan_code: str, subscription_state: str) -> tuple[str, ...]:
    base = ("read_library",)
    if subscription_state == "active":
        if plan_code in {"standard", "vip"}:
            return base + ("copy_block_cross_book",)
        if plan_code == "internal":
            return base + ("copy_block_cross_book", "export_book")
    if subscription_state == "trialing" and plan_code == "vip":
        return base + ("copy_block_cross_book",)
    return base