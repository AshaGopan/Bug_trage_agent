"""Hybrid and Neighbor-Aware Machine Learning classification models for Bug-Report Triage Agent (Phases 7 & 8).

Trains and compares LightGBM models across four feature modalities:
  1. Text-Only               : Dense text embeddings from SentenceTransformer (all-MiniLM-L6-v2)
  2. Graph-Only              : Dense structural graph embeddings from GraphSAGE
  3. Hybrid                  : Concatenated [Text + Graph] vector representations
  4. Hybrid + Label Awareness: Concatenated [Text + Graph + Training Neighbor Label Distribution]

Evaluates Macro-F1 on the chronologically held-out test split, updates eval/results_comparison.csv,
and outputs a full Confusion Matrix to eval/confusion_matrix.txt.
"""

from pathlib import Path
import sqlite3
import sys

from lightgbm import LGBMClassifier
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, f1_score

# Support running directly or as module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from features.db import DEFAULT_DB_PATH, get_db_connection

RESULTS_CSV_PATH = Path("eval/results_comparison.csv")
CONFUSION_MATRIX_PATH = Path("eval/confusion_matrix.txt")


def load_dataset():
    """Load text_vec, graph_vec, label_aware_vec, and label for train and test splits."""
    if not DEFAULT_DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at: {DEFAULT_DB_PATH}")

    conn = get_db_connection(DEFAULT_DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT i.issue_id, i.label, i.split, e.text_vec, e.graph_vec, e.label_aware_vec
            FROM issues i
            JOIN embeddings e ON i.issue_id = e.issue_id
            WHERE i.split IN ('train', 'test')
              AND e.text_vec IS NOT NULL
              AND e.graph_vec IS NOT NULL
              AND e.label_aware_vec IS NOT NULL
            ORDER BY i.issue_id ASC;
            """
        )
        rows = cursor.fetchall()

        if len(rows) == 0:
            raise ValueError(
                "Incomplete embeddings in database. Run embed_text.py, embed_graph.py, "
                "and label_awareness.py first."
            )

        train_text, train_graph, train_hybrid, train_hybrid_aware, train_labels = [], [], [], [], []
        test_text, test_graph, test_hybrid, test_hybrid_aware, test_labels = [], [], [], [], []

        for row in rows:
            t_vec = np.frombuffer(row["text_vec"], dtype=np.float32)
            g_vec = np.frombuffer(row["graph_vec"], dtype=np.float32)
            l_vec = np.frombuffer(row["label_aware_vec"], dtype=np.float32)

            h_vec = np.concatenate([t_vec, g_vec])
            ha_vec = np.concatenate([t_vec, g_vec, l_vec])

            label = row["label"]
            split = row["split"]

            if split == "train":
                train_text.append(t_vec)
                train_graph.append(g_vec)
                train_hybrid.append(h_vec)
                train_hybrid_aware.append(ha_vec)
                train_labels.append(label)
            elif split == "test":
                test_text.append(t_vec)
                test_graph.append(g_vec)
                test_hybrid.append(h_vec)
                test_hybrid_aware.append(ha_vec)
                test_labels.append(label)

        return {
            "train": {
                "text": np.stack(train_text),
                "graph": np.stack(train_graph),
                "hybrid": np.stack(train_hybrid),
                "hybrid_aware": np.stack(train_hybrid_aware),
                "labels": np.array(train_labels),
            },
            "test": {
                "text": np.stack(test_text),
                "graph": np.stack(test_graph),
                "hybrid": np.stack(test_hybrid),
                "hybrid_aware": np.stack(test_hybrid_aware),
                "labels": np.array(test_labels),
            },
        }

    finally:
        conn.close()


def append_results_to_csv(new_entries: list[dict]):
    """Update or append model evaluation entries in eval/results_comparison.csv."""
    RESULTS_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    new_df = pd.DataFrame(new_entries)

    if RESULTS_CSV_PATH.exists():
        existing_df = pd.read_csv(RESULTS_CSV_PATH)
        model_names = [e["Model"] for e in new_entries]
        filtered_df = existing_df[~existing_df["Model"].isin(model_names)]
        combined_df = pd.concat([filtered_df, new_df], ignore_index=True)
    else:
        combined_df = new_df

    combined_df.to_csv(RESULTS_CSV_PATH, index=False)
    print(f"\nUpdated results saved to: {RESULTS_CSV_PATH}")


def save_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, model_name: str):
    """Format and save a text-based confusion matrix to eval/confusion_matrix.txt."""
    CONFUSION_MATRIX_PATH.parent.mkdir(parents=True, exist_ok=True)
    classes = sorted(list(set(y_true)))
    cm = confusion_matrix(y_true, y_pred, labels=classes)

    lines = [
        "=" * 80,
        f"Confusion Matrix: {model_name}",
        "=" * 80,
        f"Rows = True Labels, Columns = Predicted Labels\n",
    ]

    # Header with abbreviated or spaced class names
    header = f"{'True Label':<22} | " + " | ".join(f"{cls:>18}" for cls in classes)
    lines.append(header)
    lines.append("-" * len(header))

    for idx, true_cls in enumerate(classes):
        row_counts = " | ".join(f"{cm[idx, j]:>18}" for j in range(len(classes)))
        lines.append(f"{true_cls:<22} | {row_counts}")

    lines.append("=" * 80)
    matrix_text = "\n".join(lines) + "\n"

    with open(CONFUSION_MATRIX_PATH, "w", encoding="utf-8") as f:
        f.write(matrix_text)

    print(f"Confusion matrix saved to: {CONFUSION_MATRIX_PATH}")


def train_and_evaluate_models():
    """Train LightGBM on Text, Graph, Hybrid, and Hybrid + Label Awareness features."""
    print("=" * 65)
    print("Phase 8: Training Hybrid & Label-Aware Models (LightGBM)")
    print("=" * 65)

    data = load_dataset()
    train_data = data["train"]
    test_data = data["test"]

    print(f"Train samples         : {len(train_data['labels'])}")
    print(f"Test samples          : {len(test_data['labels'])}")
    print(f"Text Feature Dim      : {train_data['text'].shape[1]}")
    print(f"Graph Feature Dim     : {train_data['graph'].shape[1]}")
    print(f"Hybrid Feature Dim    : {train_data['hybrid'].shape[1]}")
    print(f"Hybrid + Aware Dim    : {train_data['hybrid_aware'].shape[1]}")

    experiments = [
        ("LightGBM (Text-Only)", train_data["text"], test_data["text"]),
        ("LightGBM (Graph-Only)", train_data["graph"], test_data["graph"]),
        ("LightGBM (Hybrid)", train_data["hybrid"], test_data["hybrid"]),
        ("Hybrid + Label Awareness", train_data["hybrid_aware"], test_data["hybrid_aware"]),
    ]

    new_results = []
    final_model_pred = None

    for model_name, X_tr, X_te in experiments:
        print("\n" + "-" * 65)
        print(f"Training: {model_name}...")
        clf = LGBMClassifier(
            n_estimators=100,
            learning_rate=0.05,
            num_leaves=31,
            random_state=42,
            verbosity=-1,
            n_jobs=-1,
        )
        clf.fit(X_tr, train_data["labels"])

        y_pred = clf.predict(X_te)
        macro_f1 = f1_score(test_data["labels"], y_pred, average="macro")

        print(f"\n--- {model_name} Classification Report ---")
        print(classification_report(test_data["labels"], y_pred, digits=4))
        print(f"Macro-F1: {macro_f1:.4f}")

        new_results.append({"Model": model_name, "Macro-F1": round(macro_f1, 4)})

        if model_name == "Hybrid + Label Awareness":
            final_model_pred = y_pred

    # Save results to CSV
    append_results_to_csv(new_results)

    # Save Confusion Matrix for the final model
    if final_model_pred is not None:
        save_confusion_matrix(test_data["labels"], final_model_pred, "Hybrid + Label Awareness")

    # Print entire comparison table
    print("\n" + "=" * 65)
    print("Comprehensive Evaluation Comparison Table:")
    print("=" * 65)
    summary_df = pd.read_csv(RESULTS_CSV_PATH)
    print(summary_df.to_string(index=False))
    print("=" * 65)


if __name__ == "__main__":
    train_and_evaluate_models()
