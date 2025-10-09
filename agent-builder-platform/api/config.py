#!/usr/bin/env python3
"""
API Configuration Management
"""

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Project Settings
    PROJECT_NAME: str = "agent-builder-platform"
    ENVIRONMENT: str = "development"
    
    # API Settings
    API_TITLE: str = "Agent Builder Platform API"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    API_HOST: str = "0.0.0.0"
    API_PORT: str = "8000"
    API_RELOAD: str = "true"
    
    # Frontend Settings
    VITE_API_URL: str = "http://localhost:8000"
    
    # Feature Flags
    ENABLE_DEV_TOOLS: str = "true"
    ENABLE_MOCK_DATA: str = "true"
    ENABLE_WEBSOCKET: str = "true"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # CORS Settings
    CORS_ORIGINS: list = ["*"]
    
    # Authentication
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # AWS Settings
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    DYNAMODB_TABLE_PREFIX: str = os.getenv("DYNAMODB_TABLE_PREFIX", "agent-builder")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "agent-builder-projects")
    
    # Agent Settings
    CONFIDENCE_THRESHOLD: float = 0.95
    MAX_CONSULTATION_TIME: int = 2700  # 45 minutes in seconds
    
    # Performance Settings
    CACHE_TTL: int = 300  # 5 minutes
    MAX_CONCURRENT_REQUESTS: int = 100
    REQUEST_TIMEOUT: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields from .env

# Global settings instance
settings = Settings()
