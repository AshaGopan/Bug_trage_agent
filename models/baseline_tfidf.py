"""Baseline TF-IDF text classification models for Bug-Report Triage Agent (Phase 6).

Trains Logistic Regression and Linear Support Vector Classifier (LinearSVC)
baselines (representing the BeComE paper benchmark) on TF-IDF unigram features
derived from clean issue bodies. Evaluates Macro-F1 on the chronologically held-out
test set and logs performance to eval/results_comparison.csv.
"""

from pathlib import Path
import sqlite3
import sys

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.svm import LinearSVC

# Support running directly or as module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from features.db import DEFAULT_DB_PATH, get_db_connection

RESULTS_CSV_PATH = Path("eval/results_comparison.csv")


def load_dataset() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load train and test issue data from SQLite database."""
    if not DEFAULT_DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at: {DEFAULT_DB_PATH}")

    conn = get_db_connection(DEFAULT_DB_PATH)
    try:
        train_df = pd.read_sql_query(
            "SELECT body_clean, label FROM issues WHERE split = 'train';",
            conn,
        )
        test_df = pd.read_sql_query(
            "SELECT body_clean, label FROM issues WHERE split = 'test';",
            conn,
        )
    finally:
        conn.close()

    # Handle any potential empty/null text bodies
    train_df["body_clean"] = train_df["body_clean"].fillna("")
    test_df["body_clean"] = test_df["body_clean"].fillna("")

    return train_df, test_df


def save_results_to_csv(results: list[dict]):
    """Save or update baseline model scores in eval/results_comparison.csv."""
    RESULTS_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

    new_results_df = pd.DataFrame(results)

    if RESULTS_CSV_PATH.exists():
        existing_df = pd.read_csv(RESULTS_CSV_PATH)
        # Filter out existing entries with the same model names to ensure idempotency
        model_names = [r["Model"] for r in results]
        filtered_df = existing_df[~existing_df["Model"].isin(model_names)]
        combined_df = pd.concat([filtered_df, new_results_df], ignore_index=True)
    else:
        combined_df = new_results_df

    combined_df.to_csv(RESULTS_CSV_PATH, index=False)
    print(f"\nSaved model evaluation metrics to: {RESULTS_CSV_PATH}")


def run_tfidf_baselines():
    """Extract TF-IDF features, train classifiers, and evaluate Macro-F1."""
    print("=" * 65)
    print("Phase 6: TF-IDF Baseline Models (Logistic Regression & LinearSVC)")
    print("=" * 65)

    # 1. Load train and test splits
    train_df, test_df = load_dataset()
    print(f"Loaded Train set: {len(train_df)} samples")
    print(f"Loaded Test set : {len(test_df)} samples")

    # 2. Extract TF-IDF features (max_features=5000 to conserve RAM)
    print("\nExtracting TF-IDF features (max_features=5000, stop_words='english')...")
    vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
    X_train = vectorizer.fit_transform(train_df["body_clean"])
    X_test = vectorizer.transform(test_df["body_clean"])

    y_train = train_df["label"]
    y_test = test_df["label"]

    print(f"TF-IDF Feature Matrix Shape: Train {X_train.shape}, Test {X_test.shape}")

    # 3. Model 1: Logistic Regression
    print("\n" + "-" * 65)
    print("Training LogisticRegression(max_iter=1000)...")
    lr_model = LogisticRegression(max_iter=1000, random_state=42)
    lr_model.fit(X_train, y_train)

    y_pred_lr = lr_model.predict(X_test)
    lr_macro_f1 = f1_score(y_test, y_pred_lr, average="macro")

    print("\n--- Logistic Regression Classification Report ---")
    print(classification_report(y_test, y_pred_lr, digits=4))
    print(f"Macro-F1 (Logistic Regression): {lr_macro_f1:.4f}")

    # 4. Model 2: LinearSVC (BeComE Baseline)
    print("\n" + "-" * 65)
    print("Training LinearSVC(max_iter=2000) [BeComE Baseline]...")
    svm_model = LinearSVC(max_iter=2000, random_state=42)
    svm_model.fit(X_train, y_train)

    y_pred_svm = svm_model.predict(X_test)
    svm_macro_f1 = f1_score(y_test, y_pred_svm, average="macro")

    print("\n--- LinearSVC (BeComE Baseline) Classification Report ---")
    print(classification_report(y_test, y_pred_svm, digits=4))
    print(f"Macro-F1 (LinearSVC): {svm_macro_f1:.4f}")

    # 5. Save results to CSV
    results_to_log = [
        {"Model": "TF-IDF + Logistic Regression", "Macro-F1": round(lr_macro_f1, 4)},
        {"Model": "TF-IDF + SVM", "Macro-F1": round(svm_macro_f1, 4)},
    ]
    save_results_to_csv(results_to_log)

    print("\n" + "=" * 65)
    print("Baseline Evaluation Summary:")
    print(f"  - TF-IDF + Logistic Regression : Macro-F1 = {lr_macro_f1:.4f}")
    print(f"  - TF-IDF + SVM (LinearSVC)     : Macro-F1 = {svm_macro_f1:.4f}")
    print("=" * 65)


if __name__ == "__main__":
    run_tfidf_baselines()
