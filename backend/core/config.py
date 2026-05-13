"""
Configuration settings for the FastAPI application.
Loads environment variables from .env file.
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "The Food Store"
    PROJECT_DESCRIPTION: str = "Sistema de gestión para The Food Store"
    VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database Configuration
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/foodstore"

    # Security Configuration
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS Configuration
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Rate Limiting Configuration
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60
    RATE_LIMIT_REGISTER: str = "3/hour"
    RATE_LIMIT_LOGIN: str = "5/15minutes"
    RATE_LIMIT_PEDIDOS: str = "10/hour"

    # MercadoPago Configuration
    MP_ACCESS_TOKEN: Optional[str] = None
    MP_PUBLIC_KEY: Optional[str] = None
    MERCADOPAGO_ACCESS_TOKEN: Optional[str] = None
    MERCADOPAGO_PUBLIC_KEY: Optional[str] = None

    # URLs
    FRONTEND_URL: str = "http://localhost:3000"
    API_URL: str = "http://localhost:8000"

    # Email Configuration
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@foodstore.com"

    # Logging Configuration
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
