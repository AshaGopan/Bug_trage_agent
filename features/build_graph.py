"""Graph construction and dataset splitting for Bug-Report Triage Agent (Phase 5).

Reads raw issues from data/raw/issues.jsonl, cleans the text using clean_issue_body,
populates the SQLite database (data/processed/triage.db), extracts cross-reference
edges between issues, and applies a chronological 70/15/15 train/val/test split.
"""

import json
from pathlib import Path
import re
import sqlite3
import sys

# Support running directly or as a module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from features.clean_text import clean_issue_body
from features.db import get_db_connection, init_db

ISSUES_JSONL_PATH = Path("data/raw/issues.jsonl")


def assign_splits(conn: sqlite3.Connection):
    """Assign chronological dataset splits (70% train, 15% val, 15% test).

    Fetches all issues ordered by created_at ascending (oldest first)
    to ensure temporal ordering and avoid data leakage.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT issue_id, created_at FROM issues ORDER BY created_at ASC;")
    rows = cursor.fetchall()

    total_count = len(rows)
    if total_count == 0:
        print("Warning: No issues found to assign splits.")
        return

    # Calculate partition boundaries
    train_end = int(total_count * 0.70)
    val_end = int(total_count * 0.85)

    split_updates = []
    for idx, row in enumerate(rows):
        issue_id = row["issue_id"]
        if idx < train_end:
            split_label = "train"
        elif idx < val_end:
            split_label = "val"
        else:
            split_label = "test"
        split_updates.append((split_label, issue_id))

    cursor.executemany("UPDATE issues SET split = ? WHERE issue_id = ?;", split_updates)
    conn.commit()


def build_graph_and_populate_db():
    """Main workflow to populate issues and edges tables, then assign time splits."""
    if not ISSUES_JSONL_PATH.exists():
        raise FileNotFoundError(f"Input file not found at: {ISSUES_JSONL_PATH}")

    print("=" * 60)
    print("Starting Graph Building & Database Ingestion (Phase 5)")
    print(f"Reading from: {ISSUES_JSONL_PATH}")
    print("=" * 60)

    # Initialize tables and open connection
    conn = init_db()
    cursor = conn.cursor()

    # Clear old data from previous runs to ensure idempotency
    cursor.execute("DELETE FROM edges;")
    cursor.execute("DELETE FROM issues;")
    conn.commit()

    total_issues = 0
    total_edges = 0

    with open(ISSUES_JSONL_PATH, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line_str = line.strip()
            if not line_str:
                continue

            try:
                issue_data = json.loads(line_str)
            except json.JSONDecodeError as e:
                print(f"Warning: Skipping malformed JSON on line {line_num}: {e}")
                continue

            issue_id = issue_data.get("number")
            title = issue_data.get("title", "")
            raw_body = issue_data.get("body", "") or ""
            body_clean = clean_issue_body(raw_body)
            created_at = issue_data.get("created_at", "")
            state = issue_data.get("state", "")

            # Extract the single SIG label
            label = ""
            for lbl in issue_data.get("labels", []):
                lname = lbl.get("name", "") if isinstance(lbl, dict) else str(lbl)
                if lname.startswith("sig/"):
                    label = lname
                    break

            # 1. Insert issue into database (split is initially NULL)
            cursor.execute(
                """
                INSERT INTO issues (issue_id, title, body_clean, created_at, state, label, linked_pr_ids, split)
                VALUES (?, ?, ?, ?, ?, ?, NULL, NULL);
                """,
                (issue_id, title, body_clean, created_at, state, label),
            )
            total_issues += 1

            # 2. Extract cross-references (#\d+) from clean body
            # Using set to avoid inserting duplicate edges for repeated mentions in the same body
            ref_matches = set(int(m) for m in re.findall(r"#(\d+)", body_clean))

            # 3. For every number found that matches an issue_id already in the database, insert edge
            for ref_id in ref_matches:
                cursor.execute("SELECT 1 FROM issues WHERE issue_id = ? LIMIT 1;", (ref_id,))
                if cursor.fetchone():
                    cursor.execute(
                        """
                        INSERT INTO edges (src_issue, dst_issue, edge_type)
                        VALUES (?, ?, 'cross_ref');
                        """,
                        (issue_id, ref_id),
                    )
                    total_edges += 1

    conn.commit()
    print(f"Inserted {total_issues} issues into 'issues' table.")
    print(f"Inserted {total_edges} cross-reference edges into 'edges' table.")

    # 4. Assign time-based train / val / test splits
    print("\nAssigning chronological 70/15/15 time splits...")
    assign_splits(conn)

    # 5. Query and print final statistics
    cursor.execute(
        """
        SELECT split, COUNT(*) as cnt
        FROM issues
        GROUP BY split
        ORDER BY 
            CASE split
                WHEN 'train' THEN 1
                WHEN 'val' THEN 2
                WHEN 'test' THEN 3
                ELSE 4
            END;
        """
    )
    split_counts = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM edges;")
    final_edge_count = cursor.fetchone()[0]

    print("\n" + "=" * 60)
    print("Database Population & Graph Construction Complete!")
    print("=" * 60)
    print("Issue Counts by Split:")
    for row in split_counts:
        print(f"  - {row['split']:<6}: {row['cnt']:>5} issues")
    print("-" * 60)
    print(f"  Total Issues Processed: {total_issues}")
    print(f"  Total Edges Created   : {final_edge_count}")
    print("=" * 60)

    conn.close()


if __name__ == "__main__":
    build_graph_and_populate_db()
