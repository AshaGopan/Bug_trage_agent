"""Tests for temporal split validity and data leakage prevention (Phases 5 & 8).

Verifies:
  1. Chronological split ordering (zero temporal leakage).
  2. Training-neighbor label awareness isolation (zero val/test label leakage).
"""

from collections import defaultdict
from pathlib import Path
import sqlite3

import numpy as np
import pytest

from features.db import DEFAULT_DB_PATH, get_db_connection
from features.label_awareness import (
    LABEL_TO_IDX,
    NUM_CLASSES,
    compute_label_distribution,
)


def test_temporal_split_validity():
    """Verify chronological split ordering to prevent future-to-past data leakage.

    Asserts:
      1. max(train.created_at) <= min(val.created_at)
      2. max(val.created_at) <= min(test.created_at)
    """
    assert DEFAULT_DB_PATH.exists(), f"Database not found at {DEFAULT_DB_PATH}"

    conn = get_db_connection(DEFAULT_DB_PATH)
    try:
        cursor = conn.cursor()

        # 1. Fetch max created_at for train
        cursor.execute("SELECT MAX(created_at) FROM issues WHERE split = 'train';")
        train_max = cursor.fetchone()[0]

        # 2. Fetch min and max created_at for val
        cursor.execute("SELECT MIN(created_at), MAX(created_at) FROM issues WHERE split = 'val';")
        val_min, val_max = cursor.fetchone()

        # 3. Fetch min created_at for test
        cursor.execute("SELECT MIN(created_at) FROM issues WHERE split = 'test';")
        test_min = cursor.fetchone()[0]

        # Verify all split values exist
        assert train_max is not None, "Train split has no records or created_at is NULL"
        assert val_min is not None, "Val split has no records or created_at is NULL"
        assert val_max is not None, "Val split has no records or created_at is NULL"
        assert test_min is not None, "Test split has no records or created_at is NULL"

        # 4. Verify train_max <= val_min
        assert train_max <= val_min, (
            f"Data leakage detected! Train maximum created_at ({train_max}) "
            f"is greater than Val minimum created_at ({val_min})."
        )

        # 5. Verify val_max <= test_min
        assert val_max <= test_min, (
            f"Data leakage detected! Val maximum created_at ({val_max}) "
            f"is greater than Test minimum created_at ({test_min})."
        )

    finally:
        conn.close()


def test_label_awareness_leakage():
    """Verify that NO node's label_aware_vec is influenced by a val or test neighbor's label.

    Asserts:
      1. Every stored label_aware_vec matches the distribution computed using ONLY train neighbors.
      2. Mutating any test node's label has zero effect on the computed vectors of all other nodes.
    """
    assert DEFAULT_DB_PATH.exists(), f"Database not found at {DEFAULT_DB_PATH}"

    conn = get_db_connection(DEFAULT_DB_PATH)
    try:
        cursor = conn.cursor()

        # 1. Fetch all issues and their split / label metadata
        cursor.execute("SELECT issue_id, label, split FROM issues;")
        issues = {row["issue_id"]: {"label": row["label"], "split": row["split"]} for row in cursor.fetchall()}

        # 2. Fetch all edges
        cursor.execute("SELECT src_issue, dst_issue FROM edges;")
        adjacency = defaultdict(set)
        for row in cursor.fetchall():
            s, d = row["src_issue"], row["dst_issue"]
            if s in issues and d in issues:
                adjacency[s].add(d)
                adjacency[d].add(s)

        # 3. Fetch stored label_aware_vec
        cursor.execute(
            """
            SELECT issue_id, label_aware_vec
            FROM embeddings
            WHERE label_aware_vec IS NOT NULL;
            """
        )
        stored_vectors = {
            row["issue_id"]: np.frombuffer(row["label_aware_vec"], dtype=np.float32)
            for row in cursor.fetchall()
        }

        assert len(stored_vectors) == len(issues), (
            f"Mismatch in count: {len(stored_vectors)} vectors vs {len(issues)} issues."
        )

        # 4. Verify every node strictly equals train-only neighbor distribution
        for issue_id, stored_vec in stored_vectors.items():
            neighbors = adjacency[issue_id] - {issue_id}

            # Only train neighbors are allowed
            train_neighbor_labels = [
                issues[nbr]["label"] for nbr in neighbors
                if issues[nbr]["split"] == "train"
            ]

            expected_vec = compute_label_distribution(train_neighbor_labels)
            assert np.allclose(stored_vec, expected_vec, atol=1e-5), (
                f"Label leakage detected for issue {issue_id}! Stored vector does not match train-only neighbors."
            )

        # 5. Sensitivity Test: Mutate a test node's label and verify zero impact on any other node
        test_issues = [iid for iid, data in issues.items() if data["split"] == "test" and adjacency[iid]]
        if test_issues:
            target_test_id = test_issues[0]
            original_label = issues[target_test_id]["label"]
            fake_label = "sig/storage" if original_label != "sig/storage" else "sig/auth"

            # Recompute all vectors with fake test label
            mutated_issues = {
                iid: {"label": fake_label if iid == target_test_id else d["label"], "split": d["split"]}
                for iid, d in issues.items()
            }

            for issue_id, stored_vec in stored_vectors.items():
                if issue_id == target_test_id:
                    continue
                neighbors = adjacency[issue_id] - {issue_id}
                train_labels = [
                    mutated_issues[nbr]["label"] for nbr in neighbors
                    if mutated_issues[nbr]["split"] == "train"
                ]
                recomputed_vec = compute_label_distribution(train_labels)
                assert np.allclose(stored_vec, recomputed_vec, atol=1e-5), (
                    f"Leakage detected! Mutating test issue {target_test_id} affected neighbor issue {issue_id}."
                )

    finally:
        conn.close()
