"""Configuration management using pydantic-settings."""

from functools import lru_cache
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # -------------------------------------------------------------------------
    # General
    # -------------------------------------------------------------------------
    environment: str = "development"
    debug: bool = True
    secret_key: str = "dev-secret-key-change-in-production"

    # -------------------------------------------------------------------------
    # Database
    # -------------------------------------------------------------------------
    database_url: str = "postgresql+asyncpg://agent_user:password@localhost:5432/multimodal_agent"

    # -------------------------------------------------------------------------
    # Redis
    # -------------------------------------------------------------------------
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # -------------------------------------------------------------------------
    # MinIO
    # -------------------------------------------------------------------------
    minio_endpoint: str = "localhost:9000"
    minio_root_user: str = "minioadmin"
    minio_root_password: str = "minioadmin"
    minio_bucket: str = "agent-files"
    minio_use_ssl: bool = False

    # -------------------------------------------------------------------------
    # Clerk Authentication
    # -------------------------------------------------------------------------
    clerk_secret_key: str = ""

    # -------------------------------------------------------------------------
    # E2E Networks LLMs
    # -------------------------------------------------------------------------
    e2e_api_token: str = ""

    # Vision Model (Qwen)
    qwen_base_url: str = ""
    qwen_model: str = "Qwen/Qwen2.5-VL-7B-Instruct"

    # Reasoning Model (Llama 3.1)
    llama_base_url: str = ""
    llama_model: str = "meta-llama/Llama-3.1-8B-Instruct"

    # Code Generation Model (DeepSeek)
    deepseek_base_url: str = ""
    deepseek_model: str = "deepseek-ai/deepseek-coder-7b-instruct-v1.5"

    # -------------------------------------------------------------------------
    # Observability
    # -------------------------------------------------------------------------
    sentry_dsn: str = ""
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_host: str = "https://cloud.langfuse.com"

    # -------------------------------------------------------------------------
    # Sandbox
    # -------------------------------------------------------------------------
    sandbox_cpu_limit: int = 2
    sandbox_memory_limit: str = "2g"
    sandbox_timeout_seconds: int = 120
    sandbox_network_enabled: bool = False

    # -------------------------------------------------------------------------
    # API
    # -------------------------------------------------------------------------
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # -------------------------------------------------------------------------
    # Rate Limiting (Phase 6)
    # -------------------------------------------------------------------------
    rate_limit_requests: int = 100  # requests per window
    rate_limit_window: int = 60  # window in seconds

    # -------------------------------------------------------------------------
    # Cache TTL (Phase 6)
    # -------------------------------------------------------------------------
    cache_ttl_active_job: int = 10  # seconds for pending/processing jobs
    cache_ttl_completed_job: int = 3600  # 1 hour for completed/failed jobs

    # -------------------------------------------------------------------------
    # Logging (Phase 6)
    # -------------------------------------------------------------------------
    log_level: str = "INFO"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            import json

            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [origin.strip() for origin in v.split(",")]
        return v

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment == "production"

    @property
    def is_staging(self) -> bool:
        """Check if running in staging mode."""
        return self.environment == "staging"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Create settings instance for direct import
settings = get_settings()
