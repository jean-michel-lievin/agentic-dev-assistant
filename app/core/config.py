from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings loaded from environment variables."""

    groq_api_key: str
    model_name: str = "llama-3.1-70b-versatile"
    repo_storage_path: str = "./data/repos"
    embeddings_path: str = "./data/index"
    environment: str = "development"
    log_level: str = "debug"

    class Config:
        """Configuration for pydantic_settings.

        https://pydantic-settings.readthedocs.io/en/latest/
        """

        env_file = ".env"


settings = Settings()
