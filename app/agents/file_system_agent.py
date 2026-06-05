import os
from app.agents.base_agent import BaseAgent


class FileSystemAgent(BaseAgent):
    """Agent to read/write files from the filesystem."""

    def __init__(self, base_path: str = "/app"):
        super().__init__("filesystem-agent")
        self.base_path = base_path

    def run(self, query: str) -> str:
        """Run the agent with the given query and return a response."""
        self.logger.info(f"FileSystem agent received query: {query}")
        return "FileSystemAgent is ready to read/write files."

    def read_file(self, path: str) -> str:
        """Read the content of a file at the given path."""
        self.logger.info(f"Reading file at path: {path}")
        full = os.path.join(self.base_path, path)
        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            self.logger.exception(f"Error reading file: {e}")
            raise RuntimeError(f"Error reading file at {path}: {e}") from e

    def write_file(self, path: str, content: str) -> None:
        """Write the given content to a file at the given path."""
        self.logger.info(f"Writing file at path: {path}")
        full = os.path.join(self.base_path, path)
        try:
            with open(full, "w", encoding="utf-8", errors="ignore") as f:
                f.write(content)
        except Exception as e:
            self.logger.exception(f"Error writing file: {e}")
            raise RuntimeError(f"Error writing file at {path}: {e}") from e
