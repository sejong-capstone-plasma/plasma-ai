from __future__ import annotations

import logging
import re
from pathlib import Path

import chromadb

from app.core.config import settings
from app.rag.chunker import Chunker

logger = logging.getLogger(__name__)


class IndexBuilder:
    def __init__(
        self,
        docs_dir: Path | None = None,
        index_dir: Path | None = None,
        collection_name: str | None = None,
        chunker: Chunker | None = None,
    ) -> None:
        self.docs_dir = docs_dir or settings.rag_docs_dir
        self.index_dir = index_dir or settings.rag_index_dir
        self.collection_name = collection_name or settings.rag_collection_name
        self.chunker = chunker or Chunker(
            chunk_size=settings.rag_chunk_size,
            overlap=settings.rag_chunk_overlap,
        )

    def build(self) -> None:
        self.index_dir.mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(path=str(self.index_dir))

        existing = [c.name for c in client.list_collections()]
        if self.collection_name in existing:
            client.delete_collection(self.collection_name)
        collection = client.create_collection(self.collection_name)

        docs = self._discover_documents()
        logger.info("Found %d documents in %s", len(docs), self.docs_dir)

        total_chunks = 0
        for path in docs:
            text, metadata = self._load_document(path)
            if not text.strip():
                logger.warning("Skipping empty document: %s", path.name)
                continue
            chunks = self.chunker.chunk(text)
            collection.add(
                documents=chunks,
                metadatas=[{**metadata, "chunk_index": i} for i in range(len(chunks))],
                ids=[f"{path.name}::chunk_{i}" for i in range(len(chunks))],
            )
            total_chunks += len(chunks)
            logger.info("  %s → %d chunks", path.name, len(chunks))

        logger.info("Index built: %d chunks from %d documents", total_chunks, len(docs))

    def _discover_documents(self) -> list[Path]:
        paths: list[Path] = []
        for pattern in ("*.md", "*.pdf"):
            paths.extend(self.docs_dir.rglob(pattern))
        return sorted(paths)

    def _load_document(self, path: Path) -> tuple[str, dict]:
        if path.suffix == ".md":
            return self._load_markdown(path)
        return self._load_pdf(path)

    def _load_markdown(self, path: Path) -> tuple[str, dict]:
        text = path.read_text(encoding="utf-8")
        title = path.stem.replace("_", " ")
        for line in text.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        return text, {"source": str(path), "title": title, "type": "markdown"}

    def _load_pdf(self, path: Path) -> tuple[str, dict]:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        text = "\n\n".join(p for p in pages if p.strip())

        meta = reader.metadata or {}
        title = meta.get("/Title") or path.stem
        raw_author = meta.get("/Author") or ""
        author = raw_author if self._is_valid_author(raw_author) else None

        first_page = pages[0] if pages else ""
        doi = self._extract_doi(first_page)
        year = self._extract_year(meta, doi)

        metadata: dict = {"source": str(path), "title": title, "type": "pdf"}
        if author:
            metadata["author"] = author
        if year:
            metadata["year"] = year
        if doi:
            metadata["doi"] = doi

        return text, metadata

    @staticmethod
    def _is_valid_author(author: str) -> bool:
        if not author or len(author) < 2 or len(author) > 200:
            return False
        # 경로 문자나 날짜 패턴이 포함된 garbage 값 제외
        if re.search(r"[\\/:*?\"<>|]|\d{4} \w+ \d{2} \d{2}:\d{2}", author):
            return False
        return True

    @staticmethod
    def _extract_doi(text: str) -> str | None:
        match = re.search(r"10\.\d{4,9}/[^\s\"'<>]+", text)
        return match.group(0).rstrip(".,;)") if match else None

    @staticmethod
    def _extract_year(meta: dict, doi: str | None) -> int | None:
        # PDF 메타데이터의 생성일에서 연도 추출 (형식: D:20230101...)
        date_str = meta.get("/CreationDate") or meta.get("/ModDate") or ""
        year_match = re.search(r"(\d{4})", date_str)
        if year_match:
            year = int(year_match.group(1))
            if 1990 <= year <= 2100:
                return year
        # DOI에서 연도 힌트 추출 (일부 DOI에 연도 포함)
        if doi:
            doi_year = re.search(r"/(19|20)(\d{2})[./]", doi)
            if doi_year:
                return int(doi_year.group(1) + doi_year.group(2))
        return None
