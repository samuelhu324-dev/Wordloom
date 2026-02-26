"""
Environment and application settings

Loads configuration from environment variables (.env file)
Provides centralized access to all application settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path
import os


class Settings(BaseSettings):
    """Application configuration from environment variables"""

    # Database - default to local PostgreSQL on port 5432
    database_url: str = "postgresql://postgres:pgpass@localhost:5432/wordloom"

    # API
    api_title: str = "Wordloom API"
    api_version: str = "3.0.0"

    # Debug & Environment
    debug: bool = False
    environment: str = "development"

    # CORS
    cors_origins: list = ["*"]

    # JWT Security (预留)
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Storage
    storage_backend: str = "local"  # local | s3
    storage_path: str = "./storage"

    # Logging
    log_level: str = "INFO"
    log_json: bool = True

    # Development flags
    allow_dev_library_owner_override: bool = True

    # Feature flags
    enable_search_projection: bool = True

    # Dual-run / merge migration flags
    # Chronicle read cutover default (P5-C1): read from chronicle_entries unless explicitly rolled back.
    # Rollback: set MERGED_READ_ENABLED=0
    merged_read_enabled: bool = True

    # Search dual-run / merge migration flags (independent from Chronicle)
    # Search read cutover default (S2B-5A/P1-C1): force Stage1 provider to use
    # postgres (projection-backed) unless explicitly rolled back.
    # Rollback: set SEARCH_MERGED_READ_ENABLED=0
    search_merged_read_enabled: bool = True

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent.parent / ".env"),
        case_sensitive=False,
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance

    Returns:
        Settings: Application settings singleton
    """
    return Settings()
