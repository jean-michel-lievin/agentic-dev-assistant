from abc import ABC, abstractmethod

from groq import Groq

from app.core.config import get_settings
from app.core.logger import get_logger

settings = get_settings()


class BaseAgent(ABC):
    """Base class for all agents in the application."""

    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(name)
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = settings.model_name

    @abstractmethod
    def run(self, query: str) -> str:
        """Run the agent with the given query and return a response."""
        pass

    def llm(self, prompt: str) -> str:
        """Generate a response from the LLM based on the given prompt."""
        return (
            self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Tu es un expert Python, concis et structuré.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            .choices[0]
            .message.content
        )
