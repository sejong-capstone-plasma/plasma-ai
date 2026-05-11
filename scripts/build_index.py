"""
Offline script: load documents → chunk → embed → store in vector DB.
Run this locally whenever the knowledge base is updated.

Usage:
    python -m scripts.build_index
"""
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
)

from app.rag.index_builder import IndexBuilder

if __name__ == "__main__":
    IndexBuilder().build()
