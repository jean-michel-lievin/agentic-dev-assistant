from app.agents.base_agent import BaseAgent


class EchoAgent(BaseAgent):
    """A simple agent that echoes back the input query. Useful for testing and debugging."""

    def __init__(self, name: str = "echo-agent"):
        super().__init__(name)

    def run(self, query: str) -> str:
        """Run the agent with the given query and return a response."""
        self.logger.info(f"Echo agent received query: {query}")
        return f"[echo]: {query}"
