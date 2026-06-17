# config/settings.py
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Immutable application configuration loaded from environment variables."""
    postgres_host: str = os.getenv("POSTGRES_HOST", "db")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_db: str = os.getenv("POSTGRES_DB", "internship")
    postgres_user: str = os.getenv("POSTGRES_USER", "app")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    def __post_init__(self):
        if not self.postgres_password:
            raise ValueError("POSTGRES_PASSWORD is required. Set it in .env")