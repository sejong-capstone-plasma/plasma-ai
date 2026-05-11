from __future__ import annotations

import re


class Chunker:
    def __init__(self, chunk_size: int = 500, overlap: int = 100) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[str]:
        text = text.strip()
        if not text:
            return []

        paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]

        chunks: list[str] = []
        buffer = ""

        for para in paragraphs:
            candidate = (buffer + "\n\n" + para).strip() if buffer else para

            if len(candidate) <= self.chunk_size:
                buffer = candidate
            else:
                if buffer:
                    chunks.append(buffer)
                if len(para) > self.chunk_size:
                    chunks.extend(self._hard_split(para))
                    buffer = ""
                else:
                    buffer = self._tail(buffer) + "\n\n" + para if buffer else para

        if buffer:
            chunks.append(buffer)

        return chunks

    def _tail(self, text: str) -> str:
        return text[-self.overlap:].strip() if len(text) > self.overlap else text

    def _hard_split(self, text: str) -> list[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start = end - self.overlap
        return chunks
