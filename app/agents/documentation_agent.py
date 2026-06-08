import os

from app.agents.base_agent import BaseAgent
from app.core.logger import get_logger


class DocumentationAgent(BaseAgent):
    """Agent to generate documentation for code files."""

    def __init__(self):
        super().__init__("documentation-agent")
        self.logger = get_logger("documentation-agent")

    def run(self, query: str) -> str:
        """Run the agent with the given query and return a response."""
        return (
            "DocumentationAgent available. Command list:\n"
            "- doc:<path> (docstring + summary)\n"
            "- doc-readme:<repo>\n"
            "- doc-api:<repo>\n"
            "- doc-arch:<repo>\n"
        )

    def document_file(self, file_path: str) -> str:
        """Generate documentation for a specific file."""
        self.logger.info(f"Generating documentation for file: {file_path}")

        if not os.path.exists(file_path):
            return f"File not found: {file_path}"

        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        prompt = f"""
Tu es un expert Python senior.

Génère pour le fichier suivant :

1. Un résumé clair du rôle du fichier
2. Une documentation technique structurée
3. Des docstrings pour toutes les fonctions et classes
4. Une section "Points importants"
5. Une section "Améliorations possibles"

---------------- CODE ----------------
{content}
--------------------------------------
"""

        return self.llm(prompt)

    def generate_readme(self, repo_path: str) -> str:
        """Generate a README for the given repository."""
        if not os.path.exists(repo_path):
            return f"Repository not found : {repo_path}"

        prompt = f"""
Tu es un expert en documentation technique.

Génère un README complet pour ce projet Python.

Inclure :
- Description du projet
- Architecture
- Installation
- Usage
- API (si applicable)
- Structure du code
- Points forts
- Améliorations possibles

---------------- REPO PATH ----------------
{repo_path}
-------------------------------------------
"""

        return self.llm(prompt)

    def generate_api_docs(self, repo_path: str) -> str:
        """Generate API documentation for the given repository."""
        prompt = f"""
Analyse ce projet Python et génère une documentation API complète :

- Endpoints
- Méthodes
- Paramètres
- Réponses
- Modèles
- Sécurité
- Exemples d'appels

Repo : {repo_path}
"""

        return self.llm(prompt)

    def generate_architecture(self, repo_path: str) -> str:
        """Generate architecture documentation for the given repository."""
        prompt = f"""
Analyse l'architecture du projet suivant :

{repo_path}

Génère une documentation d'architecture complète :

- Structure du projet
- Rôle de chaque module
- Flux de données
- Agents / services
- Points d'extension
- Schéma d'architecture (texte)
"""

        return self.llm(prompt)
