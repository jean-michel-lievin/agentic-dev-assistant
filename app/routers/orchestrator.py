from fastapi import APIRouter

from app.orchestrator.orchestrator import Orchestrator

router = APIRouter(prefix="/orchestrator", tags=["orchestrator"])


@router.get("/run")
def run(query: str) -> dict[str, str]:
    """Run the orchestrator with the given query."""
    orchestrator = Orchestrator()
    return {"response": orchestrator.route(query)}
