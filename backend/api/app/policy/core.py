from __future__ import annotations

from collections.abc import Callable


def check(allowed: bool, exc_factory: Callable[[], Exception]) -> None:
    """Minimal policy gate.

    Keep this intentionally small:
    - centralized allow/deny branching
    - lets callers provide domain-specific exceptions
    """

    if allowed:
        return
    raise exc_factory()
