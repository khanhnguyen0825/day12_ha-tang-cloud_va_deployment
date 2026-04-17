from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Production AI Agent"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Security
    AGENT_API_KEY: str = "super-secret-key-123"
    ALLOWED_ORIGINS: List[str] = ["*"]

    # LLM Settings
    LLM_MODEL: str = "mock-gpt-4o"
    
    # Redis (Scaling & Stateless)
    REDIS_URL: str = "redis://localhost:6379/0"

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 10
    
    # Cost Guard ($10/month = $0.33/day)
    MONTHLY_BUDGET_USD: float = 0.33

    class Config:
        env_file = ".env"

settings = Settings()
