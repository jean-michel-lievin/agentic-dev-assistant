from app.agents.echo_agent import EchoAgent
from app.agents.embeddings_agent import EmbeddingsAgent
from app.agents.llm_agent import LLMAgent
from app.core.logger import get_logger


class Orchestrator:
    """Orchestrator class to route queries to appropriate agents."""

    def __init__(self):
        self.logger = get_logger("Orchestrator")

        # Available agents register
        self.agents = {
            "llm": LLMAgent(),
            "echo": EchoAgent(),
            "search": EmbeddingsAgent(
                repo_path="app/",
                embedding_path="data/embeddings.pkl",
            ),
        }

    def route(self, query: str) -> str:
        """Route the query to the appropriate agent based on simple keyword matching."""
        self.logger.info(f"Orchestrator received query: {query}")

        # Simple routing logic based on keywords
        if "echo" in query.lower():
            self.logger.info("Routing to EchoAgent")
            return self.agents["echo"].run(query)

        if "search" in query.lower():
            self.logger.info("Routing to EmbeddingsAgent")
            return self.agents["search"].run(query[7:].strip())  # Remove "search " prefix

        # Default
        self.logger.info("Routing to LLMAgent")
        return self.agents["llm"].run(query)
