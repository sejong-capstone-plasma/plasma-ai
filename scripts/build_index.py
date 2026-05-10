"""
Offline script: load documents → chunk → embed → store in vector DB.
Run this locally whenever the knowledge base is updated.

Usage:
    python scripts/build_index.py
"""
from app.rag.index_builder import IndexBuilder

if __name__ == "__main__":
    IndexBuilder().build()
