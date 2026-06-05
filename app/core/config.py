from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings loaded from environment variables."""

    # --- ENV variables ---
    groq_api_key: str
    model_name: str = "llama-3.3-70b-versatile"
    repo_storage_path: str = "./data/repos"
    embeddings_path: str = "./data/index"
    environment: str = "development"
    log_level: str = "debug"

    # --- Internal app settings ---
    app_name: str = "Agentic Dev Assistant"
    temperature: float = 0.3
    max_tokens: int = 4096

    class Config:
        """Configuration for pydantic_settings.

        https://pydantic-settings.readthedocs.io/en/latest/
        """

        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """Get the application settings, cached for performance."""
    return Settings()
