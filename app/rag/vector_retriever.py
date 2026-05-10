from __future__ import annotations

from app.rag.base_retriever import BaseRetriever
from app.schemas.question import SourceDocument


class VectorRetriever(BaseRetriever):
    async def retrieve(self, query: str) -> list[SourceDocument]:
        raise NotImplementedError
