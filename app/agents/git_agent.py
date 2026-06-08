import os
import shutil
import subprocess

from app.agents.base_agent import BaseAgent
from app.core.embeddings import EmbeddingIndexer
from app.core.logger import get_logger


class GitAgent(BaseAgent):
    """Agent to clone git repositories and list Python files."""

    def __init__(self, base_path: str = "/tmp/repos"):
        super().__init__("git-agent")
        self.base_path = base_path
        self.logger = get_logger("git-agent")
        os.makedirs(self.base_path, exist_ok=True)

    def run(self, query: str) -> str:
        """Run the agent with the given query and return a response."""
        return (
            "Available commands for GitAgent:\n"
            "- clone:<url>\n"
            "- list:<repo>\n"
            "- list-py:<repo>\n"
            "- open:<repo>/<path>\n"
        )

    def clone(self, url: str) -> str:
        """Clone a git repository from the given URL and return the local path."""
        try:
            repo_name = url.split("/")[-1].split(".")[0]
            repo_path = os.path.join(self.base_path, repo_name)

            if os.path.exists(repo_path):
                shutil.rmtree(repo_path)
            self.logger.info(f"Cloning repository from {url} to {repo_path}")

            subprocess.run(["git", "clone", url, repo_path], check=True)
            return f"Repository cloned into: {repo_path}"

        except Exception as e:
            self.logger.error(f"Error cloning repository: {e}")
            return f"Error cloning repository: {e}"

    def index_repo(self, repo_name: str, repo_path: str):
        """Index the cloned repository using embeddings for later search and analysis."""
        self.logger.info(f"Repository Indexation : {repo_name}")

        indexer = EmbeddingIndexer(
            repo_path=repo_path,
            embedding_path=f"data/repos/{repo_name}/embeddings.pkl",
        )

        os.makedirs(f"data/repos/{repo_name}", exist_ok=True)

        indexer.index_repository()

        self.logger.info(f"Indexation completed for {repo_name}")

    def list_files(self, repo_name: str) -> str:
        """List all files in the cloned repository."""
        repo_path = os.path.join(self.base_path, repo_name)

        if not os.path.exists(repo_path):
            return f"Repository '{repo_name}' not found. Clone it first."

        files = []
        for root, _, filenames in os.walk(repo_path):
            for f in filenames:
                files.append(os.path.join(root, f))

        if not files:
            return f"No files found in {repo_name}."

        return "\n".join(files)

    def list_python_files(self, repo_name: str) -> str:
        """List all Python files in the repository."""
        repo_path = os.path.join(self.base_path, repo_name)

        if not os.path.exists(repo_path):
            return f"Repository '{repo_name}' not found. Clone it first."

        python_files = []
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))

        if not python_files:
            return f"No Python files found in {repo_name}."

        return "\n".join(python_files)

    def open_file(self, repo_name: str, relative_path: str) -> str:
        """Open a file from the repository and return its content."""
        repo_path = os.path.join(self.base_path, repo_name)
        file_path = os.path.join(repo_path, relative_path)

        if not os.path.exists(repo_path):
            return f"Repo '{repo_name}' not found. Clone it first."

        if not os.path.exists(file_path):
            return f"File not found : {relative_path}"

        try:
            with open(file_path, encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file : {e}"
