import pickle

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingsEngine:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: str) -> list[float]:
        """Generate an embedding for the given text."""
        return self.model.encode(texts, convert_to_numpy=True)

    def save(self, path, data):
        """Save the embeddings data to a file."""
        with open(path, "wb") as f:
            pickle.dump(data, f)

    def load(self, path):
        """Load embeddings data from a file."""
        with open(path, "rb") as f:
            return pickle.load(f)

    def search(
        self, query_embedding: str, embeddings: list, top_k: int = 3
    ) -> tuple[list[int], list[float]]:
        """Search for the most similar embeddings to the query embedding."""
        scores = cosine_similarity([query_embedding], embeddings)[0]
        top_idx = scores.argsort()[::-1][:top_k]
        return top_idx, scores[top_idx]
