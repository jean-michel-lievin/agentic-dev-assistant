import os
import shutil
import subprocess

from app.agents.base_agent import BaseAgent


class GitAgent(BaseAgent):
    """Agent to clone git repositories and list Python files."""

    def __init__(self, base_path: str = "/tmp/repos"):
        super().__init__("git-agent")
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def run(self, query: str) -> str:
        """Run the agent with the given query and return a response."""
        return "GitAgent is ready to clone repositories and list Python files."

    def clone(self, url: str) -> str:
        """Clone a git repository from the given URL and return the local path."""
        repo_name = url.split("/")[-1].split(".")[0]
        repo_path = os.path.join(self.base_path, repo_name)

        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)

        subprocess.run(["git", "clone", url, repo_path], check=True)
        return repo_path

    def list_python_files(self, repo_path: str) -> list:
        """List all Python files in the repository."""
        python_files = []
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))
        return python_files
