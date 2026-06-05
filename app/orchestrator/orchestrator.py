from app.agents.code_analysis_agent import CodeAnalysisAgent
from app.agents.echo_agent import EchoAgent
from app.agents.embeddings_agent import EmbeddingsAgent
from app.agents.file_system_agent import FileSystemAgent
from app.agents.git_agent import GitAgent
from app.agents.llm_agent import LLMAgent
from app.agents.refactor_agent import RefactorAgent
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

        # Simple routing logic based on keywords
        if "echo" in query.lower():
            self.logger.info("Routing to EchoAgent")
            return self.agents["echo"].run(query[5:].strip())  # Remove "echo " prefix

        if "search" in query.lower():
            self.logger.info("Routing to EmbeddingsAgent")
            return self.agents["search"].run(query[7:].strip())  # Remove "search " prefix

        if "analyze" in query.lower():
            self.logger.info("Routing to CodeAnalysisAgent")
            path = query.replace("analyze:", "").strip()
            content = self.agents["filesystem"].read_file(path)
            return self.agents["code-analysis"].run(content)

        if "clone" in query.lower():
            self.logger.info("Routing to GitAgent")
            repo_url = query.replace("clone:", "").strip()
            return self.agents["git"].clone(repo_url)

        if "refactor" in query.lower():
            self.logger.info("Routing to RefactorAgent")
            path = query.replace("refactor:", "").strip()
            content = self.agents["filesystem"].read_file(path)
            new_code = self.agents["refactor"].generate_refactor(content)
            return self.agents["refactor"].rewrite_file(path, new_code)

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
