"""ChromaDB vector store management for Bug-Report Triage Agent (Phase 9).

Initializes a persistent vector database pointing to data/chroma_db/, indexes
all training issues using precomputed SentenceTransformer embeddings, and provides
similarity query capabilities for duplicate and related issue retrieval.
"""

from pathlib import Path
import sqlite3
import sys
from typing import Any, Union

import chromadb
from chromadb.api.models.Collection import Collection
import numpy as np

# Support running directly or as module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from features.db import DEFAULT_DB_PATH, get_db_connection

CHROMA_DIR = Path("data/chroma_db")
COLLECTION_NAME = "issues"


def init_chroma(persist_dir: Union[Path, str] = CHROMA_DIR) -> tuple[chromadb.PersistentClient, Collection]:
    """Initialize a persistent ChromaDB client and retrieve or create the issues collection."""
    path = Path(persist_dir)
    path.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(path))
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    return client, collection


def index_train_issues(
    db_path: Union[Path, str] = DEFAULT_DB_PATH,
    persist_dir: Union[Path, str] = CHROMA_DIR,
    batch_size: int = 500,
) -> int:
    """Load train split issue embeddings from SQLite and index them into ChromaDB.

    Converts existing text_vec BLOBs to Python lists without recomputing embeddings.
    """
    conn = get_db_connection(db_path)
    try:
        cursor = conn.cursor()
        print("Querying training issues and text embeddings from SQLite...")
        cursor.execute(
            """
            SELECT i.issue_id, i.title, i.label, i.created_at, e.text_vec
            FROM issues i
            JOIN embeddings e ON i.issue_id = e.issue_id
            WHERE i.split = 'train'
              AND e.text_vec IS NOT NULL
            ORDER BY i.issue_id ASC;
            """
        )
        rows = cursor.fetchall()
        total_train = len(rows)

        if total_train == 0:
            print("No training issues found to index.")
            return 0

        print(f"Found {total_train} training issues. Connecting to ChromaDB at: {persist_dir}...")
        client, collection = init_chroma(persist_dir)

        # Clear existing collection items if re-indexing to ensure clean state
        existing_count = collection.count()
        if existing_count > 0:
            print(f"Collection currently contains {existing_count} items. Refreshing index...")
            client.delete_collection(COLLECTION_NAME)
            collection = client.create_collection(
                name=COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"},
            )

        # Insert in memory-friendly batches
        for i in range(0, total_train, batch_size):
            batch = rows[i : i + batch_size]
            ids = [str(r["issue_id"]) for r in batch]
            metadatas = [
                {
                    "issue_id": int(r["issue_id"]),
                    "title": (r["title"] or "")[:200],
                    "label": r["label"] or "",
                    "created_at": r["created_at"] or "",
                }
                for r in batch
            ]
            embeddings = [
                np.frombuffer(r["text_vec"], dtype=np.float32).tolist()
                for r in batch
            ]

            collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
            )
            print(f"  Indexed issues {i + 1} to {min(i + len(batch), total_train)} / {total_train}...")

        final_count = collection.count()
        print(f"\nSuccessfully indexed {final_count} training issues in ChromaDB collection '{COLLECTION_NAME}'!")
        return final_count

    finally:
        conn.close()


def query_similar_issues(
    query_embedding: Union[np.ndarray, list[float]],
    n_results: int = 5,
    persist_dir: Union[Path, str] = CHROMA_DIR,
) -> dict[str, Any]:
    """Query ChromaDB for the top N most similar training issues given a query embedding vector."""
    _, collection = init_chroma(persist_dir)

    if isinstance(query_embedding, np.ndarray):
        query_vec = query_embedding.tolist()
    else:
        query_vec = list(query_embedding)

    results = collection.query(
        query_embeddings=[query_vec],
        n_results=n_results,
    )
    return results


if __name__ == "__main__":
    print("=" * 65)
    print("Phase 9: Building ChromaDB Training Vector Index")
    print("=" * 65)
    count = index_train_issues()
    print(f"Indexing complete. Total documents in ChromaDB: {count}")
