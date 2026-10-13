"""Neighbor label awareness feature generation for Bug-Report Triage Agent (Phase 8).

Computes neighbor label distributions to inject topological category context
into classification models, strictly aggregating from training neighbors (split == 'train')
to prevent test and validation set data leakage.
"""

from collections import defaultdict
from pathlib import Path
import sqlite3
import sys

import numpy as np

# Support running directly or as module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from features.db import DEFAULT_DB_PATH, get_db_connection

# Fixed canonical ordering of the 7 SIG labels
TARGET_LABELS = sorted([
    "sig/node",
    "sig/network",
    "sig/api-machinery",
    "sig/scheduling",
    "sig/storage",
    "sig/cli",
    "sig/auth",
])
LABEL_TO_IDX = {lbl: idx for idx, lbl in enumerate(TARGET_LABELS)}
NUM_CLASSES = len(TARGET_LABELS)  # 7


def ensure_column_exists(conn: sqlite3.Connection):
    """Ensure the label_aware_vec column exists in the embeddings table."""
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(embeddings);")
    columns = [row["name"] for row in cursor.fetchall()]
    if "label_aware_vec" not in columns:
        print("Adding column 'label_aware_vec' to table 'embeddings'...")
        cursor.execute("ALTER TABLE embeddings ADD COLUMN label_aware_vec BLOB;")
        conn.commit()


def compute_label_distribution(train_neighbor_labels: list[str]) -> np.ndarray:
    """Compute a normalized 7D label probability vector.

    If a node has no training neighbors, falls back to a uniform distribution [1/7, ...].
    """
    if not train_neighbor_labels:
        return np.full(NUM_CLASSES, 1.0 / NUM_CLASSES, dtype=np.float32)

    counts = np.zeros(NUM_CLASSES, dtype=np.float32)
    for lbl in train_neighbor_labels:
        if lbl in LABEL_TO_IDX:
            counts[LABEL_TO_IDX[lbl]] += 1.0

    total = counts.sum()
    if total == 0:
        return np.full(NUM_CLASSES, 1.0 / NUM_CLASSES, dtype=np.float32)

    return (counts / total).astype(np.float32)


def generate_and_save_label_awareness():
    """Extract neighbor label distributions and persist into SQLite embeddings table."""
    if not DEFAULT_DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at: {DEFAULT_DB_PATH}")

    print("=" * 65)
    print("Phase 8: Training-Neighbor Label Awareness Feature Generation")
    print("=" * 65)

    conn = get_db_connection(DEFAULT_DB_PATH)
    try:
        ensure_column_exists(conn)
        cursor = conn.cursor()

        # 1. Fetch all issues: issue_id, label, split
        cursor.execute("SELECT issue_id, label, split FROM issues ORDER BY issue_id ASC;")
        issues_rows = cursor.fetchall()
        issues_meta = {
            row["issue_id"]: {"label": row["label"], "split": row["split"]}
            for row in issues_rows
        }
        all_issue_ids = [row["issue_id"] for row in issues_rows]
        print(f"Total Issues in Database: {len(all_issue_ids)}")

        # 2. Fetch all edges (both directions represent graph neighbors)
        cursor.execute("SELECT src_issue, dst_issue FROM edges;")
        edge_rows = cursor.fetchall()

        adjacency = defaultdict(set)
        for row in edge_rows:
            src = row["src_issue"]
            dst = row["dst_issue"]
            if src in issues_meta and dst in issues_meta:
                adjacency[src].add(dst)
                adjacency[dst].add(src)

        print(f"Total Edges Analyzed    : {len(edge_rows)}")

        # 3. For every node, aggregate ONLY neighbors where split == 'train'
        nodes_with_train_neighbors = 0
        update_records = []

        for issue_id in all_issue_ids:
            # All undirected neighbors (excluding self-loops)
            all_neighbors = adjacency[issue_id] - {issue_id}

            # STRICT LEAKAGE PREVENTION: Keep ONLY neighbors in the train split!
            train_neighbors = [
                nbr for nbr in all_neighbors
                if issues_meta[nbr]["split"] == "train"
            ]

            if train_neighbors:
                nodes_with_train_neighbors += 1

            # Extract labels of valid train neighbors
            train_neighbor_labels = [issues_meta[nbr]["label"] for nbr in train_neighbors]

            # Compute normalized 7D vector
            label_vec = compute_label_distribution(train_neighbor_labels)
            update_records.append((label_vec.tobytes(), issue_id))

        # 4. Save to embeddings table
        cursor.executemany(
            "UPDATE embeddings SET label_aware_vec = ? WHERE issue_id = ?;",
            update_records,
        )
        conn.commit()

        # 5. Summary Statistics
        cursor.execute("SELECT COUNT(*) FROM embeddings WHERE label_aware_vec IS NOT NULL;")
        stored_count = cursor.fetchone()[0]

        print("\n" + "=" * 65)
        print("Label Awareness Feature Generation Complete!")
        print("=" * 65)
        print(f"  - Target Label Ordering            : {TARGET_LABELS}")
        print(f"  - Vector Dimensionality            : {NUM_CLASSES}")
        print(f"  - Total Issues Updated             : {stored_count}")
        print(f"  - Issues with >=1 Train Neighbor   : {nodes_with_train_neighbors}")
        print(f"  - Issues with Zero Train Neighbors : {len(all_issue_ids) - nodes_with_train_neighbors} (Uniform prior)")
        print(f"  - SQLite Target Column             : embeddings.label_aware_vec")
        print("=" * 65)

    finally:
        conn.close()


if __name__ == "__main__":
    generate_and_save_label_awareness()
