"""Unified outbox migration helpers.

This package contains small, dependency-light helpers used during the
legacy->unified outbox transition.
"""

from .toggles import is_unified_outbox_read_enabled, is_unified_outbox_write_enabled

__all__ = [
    "is_unified_outbox_read_enabled",
    "is_unified_outbox_write_enabled",
]
