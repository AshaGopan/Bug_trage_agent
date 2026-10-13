"""Text embedding generation for Bug-Report Triage Agent (Phase 7).

Generates dense text embeddings for all issues across train, val, and test splits
using SentenceTransformers on CPU. Saves vector embeddings as BLOBs in the
SQLite embeddings table.
"""

from pathlib import Path
import sqlite3
import sys
import time

import numpy as np
from sentence_transformers import SentenceTransformer

# Support running directly or as module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from features.db import DEFAULT_DB_PATH, get_db_connection


def load_model() -> SentenceTransformer:
    """Load the primary or fallback SentenceTransformer model on CPU."""
    primary_model_name = "google/embeddinggemma-300m"
    fallback_model_name = "all-MiniLM-L6-v2"

    try:
        print(f"Loading embedding model '{primary_model_name}' on CPU...")
        model = SentenceTransformer(primary_model_name, device="cpu")
        print(f"Successfully loaded '{primary_model_name}'.")
        return model
    except Exception as exc:
        print(
            f"\nNotice: Failed to load '{primary_model_name}' ({exc}).\n"
            f"Falling back to lightweight CPU model '{fallback_model_name}'..."
        )
        model = SentenceTransformer(fallback_model_name, device="cpu")
        print(f"Successfully loaded fallback model '{fallback_model_name}'.")
        return model


def embed_all_issues():
    """Fetch all issues, encode concatenated text, and store in SQLite embeddings table."""
    if not DEFAULT_DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at: {DEFAULT_DB_PATH}")

    print("=" * 65)
    print("Phase 7: Text Embeddings Generation")
    print(f"Database: {DEFAULT_DB_PATH}")
    print("=" * 65)

    conn = get_db_connection(DEFAULT_DB_PATH)
    try:
        cursor = conn.cursor()

        # 1. Fetch issue_id, title, and body_clean for all splits
        print("Fetching issues from database...")
        cursor.execute("SELECT issue_id, title, body_clean FROM issues ORDER BY issue_id ASC;")
        rows = cursor.fetchall()
        total_issues = len(rows)
        print(f"Found {total_issues} issues to embed.")

        if total_issues == 0:
            print("No issues found to embed. Exiting.")
            return

        issue_ids = []
        texts = []
        for row in rows:
            issue_ids.append(row["issue_id"])
            title = (row["title"] or "").strip()
            body = (row["body_clean"] or "").strip()
            # Combine title and body
            combined_text = f"{title} {body}".strip()
            texts.append(combined_text)

        # 2. Load model (with CPU fallback)
        model = load_model()

        # 3. Encode all texts with progress bar
        print(f"\nEncoding {total_issues} texts into dense vectors (device=cpu)...")
        start_time = time.time()
        embeddings = model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            convert_to_numpy=True,
        )
        elapsed_seconds = time.time() - start_time
        print(f"Encoding finished in {elapsed_seconds:.1f}s ({total_issues / elapsed_seconds:.1f} issues/sec).")
        print(f"Embeddings shape: {embeddings.shape}, dtype: {embeddings.dtype}")

        # 4. Insert or replace text_vec as BLOBs in SQLite embeddings table
        print("\nStoring vector embeddings in SQLite 'embeddings' table...")
        insert_records = []
        for issue_id, vec in zip(issue_ids, embeddings):
            vec_bytes = np.asarray(vec, dtype=np.float32).tobytes()
            insert_records.append((issue_id, vec_bytes))

        cursor.executemany(
            """
            INSERT INTO embeddings (issue_id, text_vec)
            VALUES (?, ?)
            ON CONFLICT(issue_id) DO UPDATE SET text_vec = excluded.text_vec;
            """,
            insert_records,
        )
        conn.commit()

        # 5. Verify stored count and dimensions
        cursor.execute("SELECT COUNT(*) FROM embeddings WHERE text_vec IS NOT NULL;")
        stored_count = cursor.fetchone()[0]

        cursor.execute("SELECT text_vec FROM embeddings WHERE text_vec IS NOT NULL LIMIT 1;")
        sample_blob = cursor.fetchone()[0]
        sample_vec = np.frombuffer(sample_blob, dtype=np.float32)

        print("\n" + "=" * 65)
        print("Text Embedding Generation Completed Successfully!")
        print("=" * 65)
        print(f"  - Total Issues Embedded   : {stored_count}")
        print(f"  - Embedding Vector Length : {len(sample_vec)} dimensions")
        print(f"  - Storage Location        : {DEFAULT_DB_PATH} -> 'embeddings' table")
        print("=" * 65)

    finally:
        conn.close()


if __name__ == "__main__":
    embed_all_issues()
