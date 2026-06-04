from fastapi import FastAPI

from app.core.config import get_settings
from app.routers.llm import router as llm_router
from app.routers.orchestrator import router as orchestrator_router

settings = get_settings()

app = FastAPI(title="Agentic Dev Assistant")
app.include_router(llm_router)
app.include_router(orchestrator_router)


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint to verify that the application is running."""
    return {"status": "ok"}


if settings.environment == "development":

    @app.get("/check-config")
    def check_config() -> dict:
        """Endpoint to check the current configuration settings."""
        return {
            "model_name": settings.model_name,
            "environment": settings.environment,
            "log_level": settings.log_level,
        }
