"""Configuration layer - Centralized settings management.

Exports:
- Settings: Application settings from environment variables
- get_settings: Cached settings instance
- Base: ORM declarative base

Security-related dependencies (such as ``get_current_user_id``) are defined in
``api.app.config.security`` and should be imported from there directly to avoid
introducing import cycles during application startup or when running scripts.
"""

from .setting import Settings, get_settings
from .database import Base

__all__ = [
    "Settings",
    "get_settings",
    "Base",
]
