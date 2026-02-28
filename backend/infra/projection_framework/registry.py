from __future__ import annotations

from typing import Dict, Tuple

from .spec import ProjectionSpec


_registry: Dict[str, ProjectionSpec] = {}


def register(spec: ProjectionSpec) -> None:
    name = spec.projection_name.strip()
    if not name:
        raise ValueError("projection_name must be non-empty")
    if name in _registry:
        raise ValueError(f"projection already registered: {name}")
    _registry[name] = spec


def get_spec(projection_name: str) -> ProjectionSpec:
    return _registry[projection_name]


def list_specs() -> Tuple[ProjectionSpec, ...]:
    return tuple(_registry[name] for name in sorted(_registry.keys()))


def _clear_registry_for_tests() -> None:
    _registry.clear()
