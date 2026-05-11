"""Subprocess helper: extract text and metadata from a single PDF.

Usage: python -m app.rag.pdf_extract <path> <max_pages>
Outputs a single JSON line to stdout.
"""
from __future__ import annotations

import json
import re
import sys


def _valid_author(author: str) -> bool:
    if not author or len(author) < 2 or len(author) > 200:
        return False
    if re.search(r'[\\/:*?"<>|]|\d{4} \w+ \d{2} \d{2}:\d{2}', author):
        return False
    return True


def _extract_doi(text: str) -> str | None:
    match = re.search(r"10\.\d{4,9}/[^\s\"'<>]+", text)
    return match.group(0).rstrip(".,;)") if match else None


def _extract_year(meta: dict, doi: str | None) -> int | None:
    date_str = meta.get("/CreationDate") or meta.get("/ModDate") or ""
    year_match = re.search(r"(\d{4})", date_str)
    if year_match:
        year = int(year_match.group(1))
        if 1990 <= year <= 2100:
            return year
    if doi:
        doi_year = re.search(r"/(19|20)(\d{2})[./]", doi)
        if doi_year:
            return int(doi_year.group(1) + doi_year.group(2))
    return None


def extract(path: str, max_pages: int) -> dict:
    from pypdf import PdfReader

    reader = PdfReader(path)
    pages = []
    for page in reader.pages[:max_pages]:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            pages.append("")

    meta = reader.metadata or {}
    title = (meta.get("/Title") or "").strip()
    raw_author = (meta.get("/Author") or "").strip()
    first_page = pages[0] if pages else ""

    doi = _extract_doi(first_page)
    year = _extract_year(meta, doi)

    return {
        "pages": pages,
        "num_pages": len(reader.pages),
        "title": title or None,
        "author": raw_author if _valid_author(raw_author) else None,
        "year": year,
        "doi": doi,
    }


if __name__ == "__main__":
    path, max_pages = sys.argv[1], int(sys.argv[2])
    print(json.dumps(extract(path, max_pages)))
