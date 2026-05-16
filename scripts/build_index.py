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

import sqlite3
from pathlib import Path

from app.core.config import settings
from app.rag.index_builder import IndexBuilder

if __name__ == "__main__":
    IndexBuilder().build()

    for db_file in Path(str(settings.rag_index_dir)).rglob("*.sqlite3"):
        try:
            conn = sqlite3.connect(str(db_file))
            conn.execute("PRAGMA wal_checkpoint(FULL)")
            conn.close()
            logging.info("WAL checkpoint: %s", db_file)
        except Exception as e:
            logging.warning("WAL checkpoint failed for %s: %s", db_file, e)
