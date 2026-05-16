from __future__ import annotations

import json
import logging
import subprocess
import sys
from pathlib import Path

import chromadb

from app.core.config import settings
from app.rag.chunker import Chunker
from app.rag.embedding import get_embedding_function

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

        logger.info("Loading embedding model...")
        sys.stdout.flush()
        embed_fn = get_embedding_function()
        embed_fn(["warmup"])
        logger.info("Embedding model ready.")
        sys.stdout.flush()

        client = chromadb.PersistentClient(path=str(self.index_dir))

        existing = [c.name for c in client.list_collections()]
        if self.collection_name in existing:
            client.delete_collection(self.collection_name)
        collection = client.create_collection(
            self.collection_name,
            embedding_function=embed_fn,
            metadata={"hnsw:space": "cosine"},
        )

        docs = self._discover_documents()
        logger.info("Found %d documents in %s", len(docs), self.docs_dir)
        sys.stdout.flush()

        total_chunks = 0
        for path in docs:
            logger.info("Processing: %s", path.name)
            sys.stdout.flush()
            try:
                text, metadata = self._load_document(path)
            except Exception as e:
                logger.error("  Failed to load %s: %s", path.name, e)
                sys.stdout.flush()
                continue
            if not text.strip():
                logger.warning("  Skipping empty: %s", path.name)
                sys.stdout.flush()
                continue
            chunks = self.chunker.chunk(text)
            logger.info("  %s → %d chunks, embedding...", path.name, len(chunks))
            sys.stdout.flush()
            try:
                collection.add(
                    documents=chunks,
                    metadatas=[{**metadata, "chunk_index": i} for i in range(len(chunks))],
                    ids=[f"{path.name}::chunk_{i}" for i in range(len(chunks))],
                )
            except Exception as e:
                logger.error("  Failed to embed %s: %s", path.name, e)
                sys.stdout.flush()
                continue
            total_chunks += len(chunks)
            logger.info("  %s → done", path.name)
            sys.stdout.flush()

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

    _MAX_PDF_PAGES = 100
    _PDF_TIMEOUT = 60

    def _load_pdf(self, path: Path) -> tuple[str, dict]:
        data = self._extract_pdf(path)
        if data is None:
            return "", {"source": str(path), "title": path.stem, "type": "pdf"}

        logger.info("  %s: %d pages (read up to %d)", path.name, data["num_pages"], self._MAX_PDF_PAGES)
        text = "\n\n".join(p for p in data["pages"] if p.strip())

        metadata: dict = {
            "source": str(path),
            "title": data.get("title") or path.stem,
            "type": "pdf",
        }
        for key in ("author", "year", "doi"):
            if data.get(key):
                metadata[key] = data[key]

        return text, metadata

    def _extract_pdf(self, path: Path) -> dict | None:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "app.rag.pdf_extract", str(path), str(self._MAX_PDF_PAGES)],
                capture_output=True,
                text=True,
                timeout=self._PDF_TIMEOUT,
            )
            if result.returncode != 0:
                logger.warning("  PDF subprocess error: %s", result.stderr[:1000])
                return None
            return json.loads(result.stdout)
        except subprocess.TimeoutExpired:
            logger.warning("  PDF extraction timed out after %ds, skipping", self._PDF_TIMEOUT)
            return None
        except Exception as e:
            logger.warning("  PDF extraction failed: %s", e)
            return None
