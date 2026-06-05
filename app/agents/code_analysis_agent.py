from app.agents.base_agent import BaseAgent


class CodeAnalysisAgent(BaseAgent):
    MAX_CHARS = 20000

    def __init__(self):
        super().__init__("code-analysis-agent")

    def split_into_chunks(self, text: str, max_chars: int = None):
        """Split the given text into chunks of a specified maximum character length."""
        if max_chars is None:
            max_chars = self.MAX_CHARS

        return [text[i : i + max_chars] for i in range(0, len(text), max_chars)]

    def build_prompt(self, file_content: str) -> str:
        """Build a prompt for the LLM to analyze the given file content."""
        return f"""
Tu es un expert en analyse de code Python.

Analyse le fichier suivant :

---------------- CODE ----------------
{file_content}
--------------------------------------

Donne une réponse structurée contenant :

1. Résumé clair du rôle du fichier
2. Points forts
3. Bugs potentiels ou comportements dangereux
4. Code smells / mauvaises pratiques
5. Améliorations possibles
6. Complexité estimée (O(n), O(n²), etc.)
7. Version améliorée du code si nécessaire
8. Tests unitaires recommandés
"""

    def run(self, file_content: str) -> str:
        """Run the agent with the given file content and return an analysis response."""
        self.logger.info(f"Received file of size: {len(file_content)} chars")

        # Normal case
        if len(file_content) <= self.MAX_CHARS:
            self.logger.info("File small enough => direct analysis")
            prompt = self.build_prompt(file_content)
            return self.llm(prompt)

        # Large file case => chunking
        self.logger.info("Large file detected => chunking enabled")

        chunks = self.split_into_chunks(file_content)
        partial_analyses = []

        for i, chunk in enumerate(chunks):
            self.logger.info(f"Analyzing chunk {i + 1}/{len(chunks)}")

            prompt = f"""
Tu es un expert Python.

Analyse la partie {i + 1}/{len(chunks)} du fichier :

---------------- CODE ----------------
{chunk}
--------------------------------------

Donne une analyse PARTIELLE, concise, structurée, sans synthèse globale.
"""

            partial = self.llm(prompt)
            partial_analyses.append(f"### Partial analysis {i + 1}\n{partial}")

        self.logger.info("Generating final synthesis")

        synthesis_prompt = f"""
Tu es un expert Python senior.

Voici les analyses partielles d'un fichier volumineux :

{chr(10).join(partial_analyses)}

Fais une synthèse GLOBALE, structurée, complète, en suivant ce format :

1. Résumé clair du rôle du fichier
2. Points forts
3. Bugs potentiels ou comportements dangereux
4. Code smells / mauvaises pratiques
5. Améliorations possibles
6. Complexité estimée
7. Version améliorée du code
8. Tests unitaires recommandés
"""

        return self.llm(synthesis_prompt)
