"""Projection framework primitives (Route A / S2C).

This package intentionally starts minimal: a `ProjectionSpec` definition and later a registry/harness.
"""

from .builtins import register_builtin_specs
from .registry import get_spec, list_specs, register
from .spec import ProjectionSpec

__all__ = [
    "get_spec",
    "list_specs",
    "ProjectionSpec",
    "register_builtin_specs",
    "register",
]
