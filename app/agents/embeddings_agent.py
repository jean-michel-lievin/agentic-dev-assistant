from app.agents.base_agent import BaseAgent
from app.core.embeddings import EmbeddingsEngine


class EmbeddingsAgent(BaseAgent):
    def __init__(self, repo_path: str = "app/", embedding_path: str = "data/embeddings.pkl"):
        super().__init__("embeddings-agent")
        self.repo_path = repo_path
        self.embedding_path = embedding_path
        self.engine = EmbeddingsEngine()
        self.logger.info("EmbeddingsAgent initialized")

    def run(self, query: str) -> str:
        """Run the agent with the given query and return a response."""
        # Load embeddings
        data = self.engine.load(self.embedding_path)
        texts = data["texts"]
        embeddings = data["embeddings"]

        # Embed the query
        query_emb = self.engine.embed([query])[0]

        # Search
        idx, scores = self.engine.search(query_emb, embeddings)

        # Build the response
        results = []
        for i, score in zip(idx, scores, strict=False):
            results.append(f"[score={score:.3f}] {texts[i][:200]}...")

        return "\n".join(results)
