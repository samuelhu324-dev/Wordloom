from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, FrozenSet, Tuple


@dataclass(frozen=True, slots=True)
class ProjectionSpec:
    projection_name: str
    scope_keys: Tuple[str, ...]
    requires: FrozenSet[str]
    payload_schema_version: int
    apply_entrypoint: Callable[..., object]
