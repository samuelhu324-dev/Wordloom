class SubscriptionAccessError(Exception):
    pass


class SubscriptionAccessNotFoundError(SubscriptionAccessError):
    pass


__all__ = ["SubscriptionAccessError", "SubscriptionAccessNotFoundError"]