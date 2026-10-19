import os
from typing import List


class Settings:
    """Application configuration settings."""

    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "RAKSHA-NET")
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Backend API for RAKSHA-NET college project"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

    # API configuration
    API_PREFIX: str = "/api/v1"

    # CORS configuration
    ALLOWED_ORIGINS: List[str] = ["*"]


settings = Settings()
