from app.agents.base_agent import BaseAgent
from app.agents.llm_client import LLMClient
from app.core.config import get_settings
from app.core.logger import get_logger

settings = get_settings()
logger = get_logger("LLMAgent")


class LLMAgent(BaseAgent):
    def __init__(self, name: str = "llm-agent"):
        super().__init__(name)
        self.llm = LLMClient()

    def run(self, query: str) -> str:
        """Run the agent with the given query and return a response."""
        self.logger.info(f"LLM agent received query: {query}")

        try:
            response = self.llm.generate(
                prompt=query,
                temperature=settings.temperature,
            )
            self.logger.info("LLM agent completed generation")
            return response
        except Exception as e:
            self.logger.exception(f"LLM agent error: {e}")
            raise RuntimeError(f"Error generating response: {e}") from e
