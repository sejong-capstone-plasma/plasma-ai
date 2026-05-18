from __future__ import annotations

from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from app.core.config import settings


def get_embedding_function() -> SentenceTransformerEmbeddingFunction:
    return SentenceTransformerEmbeddingFunction(model_name=settings.rag_embedding_model)
