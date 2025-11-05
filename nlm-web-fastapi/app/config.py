"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""

    # NLM Configuration
    nlm_auth_token: str = ""
    nlm_cookies: str = ""
    nlm_browser_profile: str = "Default"
    nlm_path: str = "nlm"

    # Application Configuration
    secret_key: str = "change-this-in-production"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    # Session Configuration
    session_max_age: int = 3600

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
