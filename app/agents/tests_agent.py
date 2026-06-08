import os

from app.agents.base_agent import BaseAgent
from app.core.logger import get_logger


class TestsAgent(BaseAgent):
    """Agent to generate tests for code files."""

    def __init__(self):
        super().__init__("tests-agent")
        self.logger = get_logger("tests-agent")

    def run(self, query: str) -> str:
        """Run the agent with the given query and return a response."""
        return (
            "TestsAgent available. Command list :\n"
            "- test:<path> (Unit test or a file)\n"
            "- test-api:<repo> (API tests for FastAPI/Flask)\n"
            "- test-class:<path> (tests for a class)\n"
        )

    def generate_tests_for_file(self, file_path: str) -> str:
        """Generate tests for a specific file."""
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"

        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        prompt = f"""
Tu es un expert Python senior spécialisé en tests unitaires.

Génère des tests pytest pour le fichier suivant :

- Tests unitaires pour chaque fonction
- Tests pour chaque classe et méthode
- Fixtures si nécessaire
- Mocks pour les dépendances
- Cas limites
- Cas d'erreur
- Structure de fichier test_<nom>.py

Renvoie UNIQUEMENT le code des tests.

---------------- CODE ----------------
{content}
--------------------------------------
"""

        return self.llm(prompt)

    def generate_api_tests(self, repo_path: str) -> str:
        """Generate API tests for a given repository."""
        prompt = f"""
Tu es un expert en tests API.

Analyse ce projet Python et génère des tests API complets :

- Tests GET/POST/PUT/DELETE
- Tests de validation
- Tests d'erreurs
- Tests d'authentification
- Tests de modèles
- Tests de routes principales

Repo : {repo_path}

Renvoie UNIQUEMENT le code pytest.
"""
        return self.llm(prompt)

    def generate_tests_for_class(self, file_path: str) -> str:
        """Generate tests for a specific class in a file."""
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"

        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        prompt = f"""
Tu es un expert Python.

Génère des tests unitaires pytest pour les classes présentes dans ce fichier.

Inclure :
- Tests de méthodes
- Tests de comportements
- Tests d'erreurs
- Mocks si nécessaire
- Fixtures

Renvoie UNIQUEMENT le code des tests.

---------------- CODE ----------------
{content}
--------------------------------------
"""
        return self.llm(prompt)
