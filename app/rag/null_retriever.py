from __future__ import annotations

from app.rag.base_retriever import BaseRetriever
from app.schemas.question import SourceDocument


class NullRetriever(BaseRetriever):
    async def retrieve(self, query: str) -> list[SourceDocument]:
        return []
