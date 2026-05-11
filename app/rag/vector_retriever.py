from __future__ import annotations

import chromadb

from app.core.config import settings
from app.rag.base_retriever import BaseRetriever
from app.rag.embedding import get_embedding_function
from app.schemas.question import SourceDocument, SourceMetadata


class VectorRetriever(BaseRetriever):
    def __init__(
        self,
        index_dir: str | None = None,
        collection_name: str | None = None,
        top_k: int = 5,
    ) -> None:
        self.index_dir = index_dir or str(settings.rag_index_dir)
        self.collection_name = collection_name or settings.rag_collection_name
        self.top_k = top_k
        self._collection: chromadb.Collection | None = None

    def _get_collection(self) -> chromadb.Collection:
        if self._collection is None:
            client = chromadb.PersistentClient(path=self.index_dir)
            self._collection = client.get_collection(
                self.collection_name,
                embedding_function=get_embedding_function(),
            )
        return self._collection

    async def retrieve(self, query: str) -> list[SourceDocument]:
        collection = self._get_collection()
        results = collection.query(
            query_texts=[query],
            n_results=min(self.top_k, collection.count()),
            include=["documents", "metadatas", "distances"],
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        output: list[SourceDocument] = []
        for doc, meta, distance in zip(documents, metadatas, distances):
            score = max(0.0, 1.0 - distance)
            output.append(
                SourceDocument(
                    title=meta.get("title", ""),
                    chunk=doc,
                    score=round(score, 4),
                    metadata=SourceMetadata(
                        source=meta.get("source", ""),
                        section=meta.get("section"),
                        page=meta.get("page"),
                        author=meta.get("author"),
                        year=meta.get("year"),
                        doi=meta.get("doi"),
                    ),
                )
            )

        return output
