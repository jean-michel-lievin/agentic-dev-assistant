import difflib

from app.agents.base_agent import BaseAgent
from app.core.logger import get_logger


class RefactorAgent(BaseAgent):
    """Agent to refactor code based on LLM suggestions."""

    def __init__(self):
        super().__init__("refactor-agent")
        self.logger = get_logger("refactor-agent")

    def run(self, query: str) -> str:
        """Run the agent with the given query and return a response."""
        return "RefactorAgent available. Command list:\n- refactor:<path>\n- dry-refactor:<path>\n"

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
- respect des conventions PEP8

Renvoie UNIQUEMENT le code refactorisé, sans explication.

---------------- CODE ----------------
{file_content}
--------------------------------------

Renvoie UNIQUEMENT le code refactorisé.
"""
        return self.llm(prompt)

    def validate_syntax(self, code: str) -> tuple[bool, str]:
        """Validate the syntax of the given code."""
        try:
            compile(code, "<refactor>", "exec")
            return True, "OK"
        except SyntaxError as e:
            return False, f"Syntax error : {e}"

    def generate_diff(self, old: str, new: str) -> str:
        """Generate a unified diff between the old and new code."""
        diff = difflib.unified_diff(
            old.splitlines(),
            new.splitlines(),
            fromfile="original",
            tofile="refactored",
            lineterm="",
        )
        return "\n".join(diff)

    def dry_run(self, path: str) -> str:
        """Perform a dry run refactor by generating the refactored code and showing the diff."""
        with open(path, encoding="utf-8") as f:
            original = f.read()

        refactored = self.generate_refactor(original)
        diff = self.generate_diff(original, refactored)

        return f"--- DIFF (dry-run) ---\n{diff}"

    def rewrite_file(self, path: str, new_content: str) -> str:
        """Rewrite the content of a file at the given path."""
        self.logger.info(f"Rewriting file at path: {path}")

        try:
            # Read original file
            with open(path, encoding="utf-8") as f:
                original = f.read()

            # Check syntax of new content before writing
            ok, msg = self.validate_syntax(new_content)
            if not ok:
                return f"Refactoring cancelled : {msg}"

            # Save backup
            backup_path = path + ".backup"
            with open(backup_path, "w", encoding="utf-8") as f:
                f.write(original)

            # Write new code
            with open(path, "w", encoding="utf-8", errors="ignore") as f:
                f.write(new_content)
            return f"File at {path} rewritten successfully."
        except Exception as e:
            self.logger.exception(f"Error rewriting file: {e}")
            raise RuntimeError(f"Error rewriting file at {path}: {e}") from e
