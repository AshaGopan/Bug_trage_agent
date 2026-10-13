"""Duplicate and related issue retrieval evaluation (Recall@5) for Bug-Report Triage Agent (Phase 9).

Evaluates the vector store retrieval capabilities against historical cross-reference edges:
Queries ChromaDB with test issue embeddings and assesses whether the ground-truth
train reference issue appears in the top 5 retrieved neighbors (Recall@5).
"""

from collections import defaultdict
from pathlib import Path
import sqlite3
import sys

import numpy as np

# Support running directly or as module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from features.db import DEFAULT_DB_PATH, get_db_connection
from features.vector_store import query_similar_issues


def evaluate_recall_at_5():
    """Evaluate Recall@5 on test-to-train ground truth cross-reference edges."""
    if not DEFAULT_DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at: {DEFAULT_DB_PATH}")

    print("=" * 70)
    print("Phase 9: Evaluating Duplicate & Related Issue Retrieval (Recall@5)")
    print("=" * 70)

    conn = get_db_connection(DEFAULT_DB_PATH)
    try:
        cursor = conn.cursor()

        # 1. Fetch cross-reference edges where src_issue in test and dst_issue in train
        cursor.execute(
            """
            SELECT 
                e.src_issue AS test_id,
                s.title AS test_title,
                e.dst_issue AS train_id,
                d.title AS train_title,
                e.text_vec AS test_vec
            FROM edges e
            JOIN issues s ON e.src_issue = s.issue_id
            JOIN issues d ON e.dst_issue = d.issue_id
            JOIN embeddings e ON s.issue_id = e.issue_id
            WHERE s.split = 'test'
              AND d.split = 'train'
              AND e.text_vec IS NOT NULL
            ORDER BY e.src_issue ASC;
            """
        )
        rows = cursor.fetchall()
        total_targets = len(rows)

        if total_targets == 0:
            print("Warning: No ground truth cross-reference edges found connecting 'test' to 'train'.")
            return 0.0

        print(f"Found {total_targets} ground truth (test -> train) duplicate/reference target pairs.")
        print("-" * 70)

        # Group targets by unique test issue
        test_queries = defaultdict(lambda: {"title": "", "test_vec": None, "targets": []})
        for r in rows:
            test_id = r["test_id"]
            test_queries[test_id]["title"] = r["test_title"]
            test_queries[test_id]["test_vec"] = np.frombuffer(r["test_vec"], dtype=np.float32)
            test_queries[test_id]["targets"].append({
                "train_id": r["train_id"],
                "train_title": r["train_title"],
            })

        print(f"Evaluating across {len(test_queries)} unique test issues with known train references:\n")

        hits = 0
        total_queries = len(test_queries)

        for query_idx, (test_id, q_data) in enumerate(test_queries.items(), 1):
            target_ids = {t["train_id"] for t in q_data["targets"]}
            target_id_list = list(target_ids)

            # Query ChromaDB for top 5 most similar train issues
            results = query_similar_issues(q_data["test_vec"], n_results=5)
            retrieved_ids = [int(i) for i in results["ids"][0]] if results and results["ids"] else []

            # Check if any ground truth target is in the top 5
            found_targets = [t for t in target_id_list if t in retrieved_ids]
            is_hit = len(found_targets) > 0

            if is_hit:
                hits += 1
                status = "[HIT]"
                rank_str = f"Rank: {retrieved_ids.index(found_targets[0]) + 1}"
            else:
                status = "[MISS]"
                rank_str = "Not in Top 5"

            print(f"[{query_idx:02d}/{total_queries:02d}] {status} Test Issue #{test_id} ({rank_str})")
            print(f"       Title  : {q_data['title'][:60]}...")
            print(f"       Targets: {target_id_list}")
            print(f"       Top 5  : {retrieved_ids}\n")

        recall_at_5 = (hits / total_queries) * 100.0

        print("=" * 70)
        print("Duplicate Retrieval Evaluation Summary:")
        print("=" * 70)
        print(f"  - Total Test Queries Evaluated : {total_queries}")
        print(f"  - Successful Top-5 Hits        : {hits}")
        print(f"  - Misses                       : {total_queries - hits}")
        print(f"  - Overall Recall@5             : {recall_at_5:.2f}% ({hits}/{total_queries})")
        print("=" * 70)

        return recall_at_5

    finally:
        conn.close()


if __name__ == "__main__":
    evaluate_recall_at_5()
