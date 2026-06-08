from app.agents.base_agent import BaseAgent
from app.core.logger import get_logger


class WorkflowAgent(BaseAgent):
    """Agent to orchestrate the workflow of other agents based on the query."""

    def __init__(self, orchestrator):
        super().__init__("workflow-agent")
        self.orchestrator = orchestrator
        self.logger = get_logger("workflow-agent")

    def run(self, query: str) -> str:
        """Run the agent with the given query and return a response."""
        return "WorkflowAgent available. Command list :\n- workflow:<repo_url>\n"

    def full_workflow(self, repo_url: str) -> str:
        """Run the full workflow for a given repository URL."""
        logs = []

        # 1. Clone
        logs.append("=== CLONE ===")
        clone_result = self.orchestrator.agents["git"].clone(repo_url)
        logs.append(clone_result)

        repo_name = repo_url.split("/")[-1].replace(".git", "")
        repo_path = f"/tmp/repos/{repo_name}"

        # 2. Indexation (already done automatically)
        logs.append("=== INDEXATION ===")
        logs.append(f"Indexation completed for {repo_name}")

        # 3. List Python files
        logs.append("=== LIST PY ===")
        py_files = self.orchestrator.agents["git"].list_python_files(repo_name)
        logs.append(py_files)

        # 4. Analyze of first python file
        first_file = py_files.split("\n")[0]
        logs.append(f"=== ANALYSE : {first_file} ===")
        content = self.orchestrator.agents["filesystem"].read_file(first_file)
        analysis = self.orchestrator.agents["code-analysis"].run(content)
        logs.append(analysis)

        # 5. Refactoring
        logs.append("=== REFACTOR ===")
        new_code = self.orchestrator.agents["refactor"].generate_refactor(content)
        refactor_result = self.orchestrator.agents["refactor"].rewrite_file(
            first_file, new_code
        )
        logs.append(refactor_result)

        # 6. Tests
        logs.append("=== TESTS ===")
        tests = self.orchestrator.agents["tests"].generate_tests_for_file(first_file)
        logs.append(tests)

        # 7. Documentation
        logs.append("=== DOCUMENTATION ===")
        docs = self.orchestrator.agents["documentation"].generate_readme(repo_path)
        logs.append(docs)

        return "\n\n".join(logs)
