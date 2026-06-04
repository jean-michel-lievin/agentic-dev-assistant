from abc import ABC, abstractmethod

from app.core.logger import get_logger


class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(name)

    @abstractmethod
    async def run(self, query: str) -> str:
        """Run the agent with the given query and return a response."""
        pass
