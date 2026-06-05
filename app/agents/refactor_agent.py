from app.agents.base_agent import BaseAgent


class RefactorAgent(BaseAgent):
    """Agent to refactor code based on LLM suggestions."""

    def __init__(self):
        super().__init__("refactor-agent")

    def run(self, query: str) -> str:
        """Run the agent with the given query and return a response."""
        self.logger.info(f"Refactor agent received query: {query}")
        return "RefactorAgent is ready to refactor code based on LLM suggestions."

    def rewrite_file(self, path: str, new_content: str) -> str:
        """Rewrite the content of a file at the given path."""
        self.logger.info(f"Rewriting file at path: {path}")

        try:
            with open(path, "w", encoding="utf-8", errors="ignore") as f:
                f.write(new_content)
            return f"File at {path} rewritten successfully."
        except Exception as e:
            self.logger.exception(f"Error rewriting file: {e}")
            raise RuntimeError(f"Error rewriting file at {path}: {e}") from e

    def generate_refactor(self, file_content: str) -> str:
        """Generate a refactor plan based on the given code."""
        self.logger.info("Generating refactor plan from code")
        prompt = f"""
Tu es un expert Python senior.

Refactorise le code suivant en améliorant :
- lisibilité
- structure
- robustesse
- typage
- cohérence

---------------- CODE ----------------
{file_content}
--------------------------------------

Renvoie UNIQUEMENT le code refactorisé.
"""
        return self.llm(prompt)
