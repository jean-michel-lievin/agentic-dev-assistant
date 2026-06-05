from app.agents.base_agent import BaseAgent


class CodeAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__("code-analysis-agent")

    def run(self, file_content: str) -> str:
        prompt = f"""
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
        return self.llm(prompt)
