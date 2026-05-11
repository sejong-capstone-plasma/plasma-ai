from __future__ import annotations

from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

_MODEL_NAME = "all-MiniLM-L6-v2"


def get_embedding_function() -> SentenceTransformerEmbeddingFunction:
    return SentenceTransformerEmbeddingFunction(model_name=_MODEL_NAME)
