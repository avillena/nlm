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
    title: str = "NLM Web Interface"
    host: str = "0.0.0.0"
    port: int = 8080
    reload: bool = True
    dark_mode: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
