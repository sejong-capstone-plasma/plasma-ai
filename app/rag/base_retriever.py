from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.question import SourceDocument


class BaseRetriever(ABC):
    @abstractmethod
    async def retrieve(self, query: str) -> list[SourceDocument]:
        ...
