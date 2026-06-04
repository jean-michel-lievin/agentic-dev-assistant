import groq

from app.core.config import get_settings
from app.core.logger import get_logger

logger = get_logger("LLMClient")
settings = get_settings()


class LLMClient:
    def __init__(self):
        self.client = groq.Groq(api_key=settings.groq_api_key)
        self.model = settings.model_name

    def generate(self, prompt: str, temperature: float = 0.3) -> str:
        """Generate a response from the LLM based on the given prompt."""
        logger.info(f"Calling LLM model={self.model}")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.exception(f"Error generating response: {e}")
            raise
