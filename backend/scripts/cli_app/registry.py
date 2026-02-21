from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from .types import DrillInputs, DrillResult


class ScenarioHandler(Protocol):
    def __call__(self, inputs: DrillInputs) -> DrillResult: ...


_registry: dict[str, ScenarioHandler] = {}


def register(name: str) -> Callable[[ScenarioHandler], ScenarioHandler]:
    """Decorator to register a scenario handler under a stable string key."""

    def _decorator(handler: ScenarioHandler) -> ScenarioHandler:
        if name in _registry:
            raise KeyError(f"Scenario already registered: {name}")
        _registry[name] = handler
        return handler

    return _decorator


def get(name: str) -> ScenarioHandler:
    try:
        return _registry[name]
    except KeyError as e:
        known = ", ".join(sorted(_registry.keys()))
        raise KeyError(f"Unknown scenario: {name}. Known: [{known}]") from e


def list_scenarios() -> list[str]:
    return sorted(_registry.keys())


def load_builtin_scenarios() -> None:
    """Import scenario modules so they can self-register via @register."""

    from .scenarios import shadow_verify_search_index_write_gate  # noqa: F401
    from .scenarios import shadow_verify_search_index_paging_stability  # noqa: F401
    from .scenarios import shadow_verify_shared_keys  # noqa: F401
    from .scenarios import shadow_verify_dual_run_stage1  # noqa: F401
    from .scenarios import shadow_verify_dual_run_stage2  # noqa: F401
    from .scenarios import shadow_verify_dual_run_readiness_gate  # noqa: F401
    from .scenarios import shadow_verify_dual_run_window  # noqa: F401

    return None
