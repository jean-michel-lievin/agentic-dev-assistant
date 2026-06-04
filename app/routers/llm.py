from fastapi import APIRouter

from app.agents.llm_agent import LLMAgent

router = APIRouter(prefix="/llm", tags=["llm"])


@router.get("/ask")
def ask(query: str) -> dict[str, str]:
    """Ask a question to the LLM."""
    agent = LLMAgent()
    return {"response": agent.run(query)}
