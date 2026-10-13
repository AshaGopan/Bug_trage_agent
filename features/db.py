"""SQLite database management for Bug-Report Triage Agent (Phase 5).

Manages connection lifecycle and schema initialization for the clean issue
data, relationship graph edges, linked PR modified files, and embedding vectors.
"""

from pathlib import Path
import sqlite3
from typing import Union

# Default path to the SQLite database
DEFAULT_DB_PATH = Path("data/processed/triage.db")


def get_db_connection(db_path: Union[Path, str] = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Open and return a connection to the SQLite database.

    Ensures the parent directory exists and configures the connection
    with sqlite3.Row for convenient column-name access.
    """
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Union[Path, str] = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Initialize database tables defined in the project architecture.

    Creates the following 4 tables if they do not exist:
      1. issues: Cleaned issue texts, labels, PR links, and dataset splits.
      2. edges: Graph edges between issues (references, duplicate links, etc.).
      3. pr_files: Files modified by PRs linked to issues.
      4. embeddings: Precomputed dense vector embeddings (text and graph).

    Returns:
        The active sqlite3.Connection object.
    """
    conn = get_db_connection(db_path)
    try:
        with conn:
            # 1. issues table
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS issues (
                    issue_id INTEGER PRIMARY KEY,
                    title TEXT,
                    body_clean TEXT,
                    created_at TEXT,
                    state TEXT,
                    label TEXT,
                    linked_pr_ids TEXT,
                    split TEXT
                );
                """
            )

            # 2. edges table
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS edges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    src_issue INTEGER,
                    dst_issue INTEGER,
                    edge_type TEXT
                );
                """
            )

            # 3. pr_files table
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS pr_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pr_id INTEGER,
                    file_path TEXT
                );
                """
            )

            # 4. embeddings table
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS embeddings (
                    issue_id INTEGER PRIMARY KEY,
                    text_vec BLOB,
                    graph_vec BLOB,
                    label_aware_vec BLOB
                );
                """
            )
        return conn
    except sqlite3.Error as e:
        conn.close()
        raise RuntimeError(f"Failed to initialize SQLite database at {db_path}: {e}") from e


if __name__ == "__main__":
    print(f"Initializing database at: {DEFAULT_DB_PATH}...")
    connection = init_db()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [row["name"] for row in cursor.fetchall() if not row["name"].startswith("sqlite_")]
    print(f"Successfully initialized tables: {tables}")
    connection.close()
