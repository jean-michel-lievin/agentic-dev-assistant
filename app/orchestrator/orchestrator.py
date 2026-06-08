from app.agents.code_analysis_agent import CodeAnalysisAgent
from app.agents.documentation_agent import DocumentationAgent
from app.agents.echo_agent import EchoAgent
from app.agents.embeddings_agent import EmbeddingsAgent
from app.agents.file_system_agent import FileSystemAgent
from app.agents.git_agent import GitAgent
from app.agents.llm_agent import LLMAgent
from app.agents.refactor_agent import RefactorAgent
from app.agents.tests_agent import TestsAgent
from app.agents.workflow_agent import WorkflowAgent
from app.core.logger import get_logger


class Orchestrator:
    """Orchestrator class to route queries to appropriate agents."""

    def __init__(self):
        self.logger = get_logger("Orchestrator")

        # Available agents register
        self.agents = {
            "llm": LLMAgent(),
            "echo": EchoAgent(),
            "search": EmbeddingsAgent(
                repo_path="app/",
                embedding_path="data/embeddings.pkl",
            ),
            "code-analysis": CodeAnalysisAgent(),
            "filesystem": FileSystemAgent(),
            "git": GitAgent(),
            "refactor": RefactorAgent(),
            "documentation": DocumentationAgent(),
            "tests": TestsAgent(),
            "workflow": WorkflowAgent(self),
        }

    def classify(self, query: str) -> str:
        """Classify the query to determine the appropriate agent."""
        classifier_prompt = f"""
Tu es un routeur d'agents.

Analyse la requête suivante et réponds UNIQUEMENT par un mot parmi :

- echo
- search
- code-analysis
- filesystem
- git
- llm
- refactor
Requête : {query}
"""

        result = self.agents["llm"].run(classifier_prompt).strip().lower()
        return result

    def route(self, query: str) -> str:
        """Route the query to the appropriate agent based on simple keyword matching."""
        self.logger.info(f"Orchestrator received query: {query}")

        q = query.lower().strip()

        # Echo
        if q.startswith("echo:"):
            return self.agents["echo"].run(query.replace("echo:", "").strip())

        # Search
        if q.startswith("search:"):
            return self.agents["search"].run(query.replace("search:", "").strip())

        # Analyze
        if q.startswith("analyze:"):
            path = query.replace("analyze:", "").strip()
            content = self.agents["filesystem"].read_file(path)
            return self.agents["code-analysis"].run(content)

        # Clone repo
        if q.startswith("clone:"):
            repo_url = query.replace("clone:", "").strip()
            return self.agents["git"].clone(repo_url)

        # List files in repo
        if q.startswith("list:"):
            repo_name = query.replace("list:", "").strip()
            return self.agents["git"].list_files(repo_name)

        # List python files in repo
        if q.startswith("list-py:"):
            repo_name = query.replace("list-py:", "").strip()
            return self.agents["git"].list_python_files(repo_name)

        # Open file
        if q.startswith("open:"):
            repo, path = query.replace("open:", "").strip().split("/", 1)
            return self.agents["git"].open_file(repo, path)

        # Refactor
        if q.startswith("refactor:"):
            path = query.replace("refactor:", "").strip()
            content = self.agents["filesystem"].read_file(path)
            new_code = self.agents["refactor"].generate_refactor(content)
            return self.agents["refactor"].rewrite_file(path, new_code)

        # Documentation
        if q.startswith("doc:"):
            path = query.replace("doc:", "").strip()
            return self.agents["documentation"].document_file(path)

        if q.startswith("doc-readme:"):
            repo = query.replace("doc-readme:", "").strip()
            return self.agents["documentation"].generate_readme(f"/tmp/repos/{repo}")

        if q.startswith("doc-api:"):
            repo = query.replace("doc-api:", "").strip()
            return self.agents["documentation"].generate_api_docs(f"/tmp/repos/{repo}")

        if q.startswith("doc-arch:"):
            repo = query.replace("doc-arch:", "").strip()
            return self.agents["documentation"].generate_architecture(
                f"/tmp/repos/{repo}"
            )

        # Tests
        if q.startswith("test:"):
            file_path = query.replace("test:", "").strip()
            return self.agents["tests"].generate_tests_for_file(file_path)

        if q.startswith("test-api:"):
            repo_path = query.replace("test-api:", "").strip()
            return self.agents["tests"].generate_api_tests(f"/tmp/repos/{repo_path}")

        if q.startswith("test-class:"):
            file_path = query.replace("test-class:", "").strip()
            return self.agents["tests"].generate_tests_for_class(file_path)

        # Workflow
        if q.startswith("workflow:"):
            repo_url = query.replace("workflow:", "").strip()
            return self.agents["workflow"].full_workflow(repo_url)

        agent_name = self.classify(query)
        self.logger.info(f"Classifier selected agent: {agent_name}")

        if agent_name == "code-analysis" and ".py" in query:
            content = self.agents["filesystem"].read_file(query.strip())
            return self.agents["code-analysis"].run(content)

        if agent_name in self.agents:
            return self.agents[agent_name].run(query)

        # Fallback
        self.logger.info("Routing to LLMAgent")
        return self.agents["llm"].run(query)
