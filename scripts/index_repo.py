import os

from app.core.embeddings import EmbeddingsEngine


def load_repo_files(path):
    """Load all text files from the given repository path."""
    texts = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith((".py", ".md", ".txt")):
                full = os.path.join(root, file)
                with open(full, encoding="utf-8", errors="ignore") as f:
                    texts.append(f.read())
    return texts


def index_repository(repo_path, embedding_path):
    """Index the repository files and save the embeddings."""
    engine = EmbeddingsEngine()
    texts = load_repo_files(repo_path)
    embeddings = engine.embed(texts)
    data = {"texts": texts, "embeddings": embeddings}
    engine.save(embedding_path, data)


if __name__ == "__main__":
    index_repository("app/", "data/embeddings.pkl")
