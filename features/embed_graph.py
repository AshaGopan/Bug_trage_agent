"""Graph embedding generation using GraphSAGE for Bug-Report Triage Agent (Phase 7).

Constructs a graph from issue relationships, trains a 2-layer GraphSAGE (SAGEConv)
model strictly on training nodes and train-only edges (preventing test set leakage),
extracts graph embeddings (graph_vec) for all issues, and persists them into SQLite.
"""

from pathlib import Path
import sqlite3
import sys
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv

# Support running directly or as module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from features.db import DEFAULT_DB_PATH, get_db_connection

MODEL_SAVE_DIR = Path("models/saved")
MODEL_SAVE_PATH = MODEL_SAVE_DIR / "graphsage.pt"


class GraphSAGE(nn.Module):
    """2-layer GraphSAGE neural network for node representation learning."""

    def __init__(self, in_channels: int, hidden_channels: int, out_channels: int):
        super().__init__()
        self.conv1 = SAGEConv(in_channels, hidden_channels)
        self.conv2 = SAGEConv(hidden_channels, hidden_channels)
        self.classifier = nn.Linear(hidden_channels, out_channels)

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        # Layer 1
        h = self.conv1(x, edge_index)
        h = F.relu(h)
        h = F.dropout(h, p=0.2, training=self.training)

        # Layer 2 -> graph embedding representation
        graph_vec = self.conv2(h, edge_index)
        graph_vec = F.relu(graph_vec)

        # Classifier logits
        logits = self.classifier(graph_vec)
        return logits, graph_vec


def load_graph_data(conn: sqlite3.Connection):
    """Load node features (text_vec), labels, split masks, and graph edges."""
    cursor = conn.cursor()

    # 1. Fetch nodes: issue_id, label, split, text_vec
    cursor.execute(
        """
        SELECT i.issue_id, i.label, i.split, e.text_vec
        FROM issues i
        JOIN embeddings e ON i.issue_id = e.issue_id
        WHERE e.text_vec IS NOT NULL
        ORDER BY i.issue_id ASC;
        """
    )
    rows = cursor.fetchall()
    total_nodes = len(rows)

    if total_nodes == 0:
        raise ValueError("No embeddings found in the database. Run features/embed_text.py first.")

    issue_ids = []
    labels = []
    splits = []
    text_vecs = []

    for row in rows:
        issue_ids.append(row["issue_id"])
        labels.append(row["label"])
        splits.append(row["split"])
        text_vecs.append(np.frombuffer(row["text_vec"], dtype=np.float32))

    issue_to_idx = {issue_id: idx for idx, issue_id in enumerate(issue_ids)}

    # Map target labels to integer indices
    unique_labels = sorted(list(set(labels)))
    label_to_idx = {l: i for i, l in enumerate(unique_labels)}
    y = torch.tensor([label_to_idx[l] for l in labels], dtype=torch.long)

    # Node features: [N, D]
    x = torch.tensor(np.stack(text_vecs), dtype=torch.float32)

    # Split masks
    train_mask = torch.tensor([s == "train" for s in splits], dtype=torch.bool)
    val_mask = torch.tensor([s == "val" for s in splits], dtype=torch.bool)
    test_mask = torch.tensor([s == "test" for s in splits], dtype=torch.bool)

    # 2. Fetch all edges from the database
    cursor.execute("SELECT src_issue, dst_issue FROM edges;")
    raw_edges = cursor.fetchall()

    all_src = []
    all_dst = []
    train_src = []
    train_dst = []

    train_indices = set(np.where(train_mask.numpy())[0])

    for src, dst in raw_edges:
        if src in issue_to_idx and dst in issue_to_idx:
            s_idx = issue_to_idx[src]
            d_idx = issue_to_idx[dst]

            # All edges (for full inference)
            all_src.append(s_idx)
            all_dst.append(d_idx)

            # Strictly train-only edges (both source and destination in train set)
            if s_idx in train_indices and d_idx in train_indices:
                train_src.append(s_idx)
                train_dst.append(d_idx)

    # Convert to PyG edge_index tensors [2, num_edges]
    if len(all_src) > 0:
        edge_index_all = torch.tensor([all_src, all_dst], dtype=torch.long)
    else:
        edge_index_all = torch.empty((2, 0), dtype=torch.long)

    if len(train_src) > 0:
        edge_index_train = torch.tensor([train_src, train_dst], dtype=torch.long)
    else:
        edge_index_train = torch.empty((2, 0), dtype=torch.long)

    return {
        "issue_ids": issue_ids,
        "x": x,
        "y": y,
        "train_mask": train_mask,
        "val_mask": val_mask,
        "test_mask": test_mask,
        "edge_index_all": edge_index_all,
        "edge_index_train": edge_index_train,
        "num_classes": len(unique_labels),
    }


def train_and_embed_graph():
    """Train GraphSAGE and compute graph embeddings for all issues."""
    if not DEFAULT_DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at: {DEFAULT_DB_PATH}")

    print("=" * 65)
    print("Phase 7: Graph Embeddings Generation (GraphSAGE / PyG)")
    print("=" * 65)

    conn = get_db_connection(DEFAULT_DB_PATH)
    try:
        data = load_graph_data(conn)
        x = data["x"]
        y = data["y"]
        train_mask = data["train_mask"]
        val_mask = data["val_mask"]
        edge_index_all = data["edge_index_all"]
        edge_index_train = data["edge_index_train"]
        issue_ids = data["issue_ids"]
        num_classes = data["num_classes"]

        print(f"Total Nodes               : {x.size(0)}")
        print(f"Input Feature Dimension   : {x.size(1)}")
        print(f"Train Nodes Count         : {train_mask.sum().item()}")
        print(f"All Graph Edges           : {edge_index_all.size(1)}")
        print(f"Train-Only Edges (Strict) : {edge_index_train.size(1)} (Zero test leakage)")

        # Initialize GraphSAGE
        hidden_dim = 128
        model = GraphSAGE(in_channels=x.size(1), hidden_channels=hidden_dim, out_channels=num_classes)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
        criterion = nn.CrossEntropyLoss()

        print("\nTraining GraphSAGE on CPU...")
        epochs = 80
        best_val_loss = float("inf")

        for epoch in range(1, epochs + 1):
            model.train()
            optimizer.zero_grad()

            # Forward pass using ONLY train-to-train edges
            logits, _ = model(x, edge_index_train)
            loss = criterion(logits[train_mask], y[train_mask])
            loss.backward()
            optimizer.step()

            # Validation evaluation
            model.eval()
            with torch.no_grad():
                val_logits, _ = model(x, edge_index_train)
                val_loss = criterion(val_logits[val_mask], y[val_mask]).item()
                val_acc = (val_logits[val_mask].argmax(dim=1) == y[val_mask]).float().mean().item()

            if epoch % 20 == 0 or epoch == epochs:
                train_acc = (logits[train_mask].argmax(dim=1) == y[train_mask]).float().mean().item()
                print(
                    f"  Epoch {epoch:02d}/{epochs:02d} | "
                    f"Train Loss: {loss.item():.4f} | Train Acc: {train_acc*100:.2f}% | "
                    f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc*100:.2f}%"
                )

        # Save model weights to models/saved/graphsage.pt
        MODEL_SAVE_DIR.mkdir(parents=True, exist_ok=True)
        torch.save(model.state_dict(), MODEL_SAVE_PATH)
        print(f"\nSaved trained model weights to: {MODEL_SAVE_PATH}")

        # Forward pass on the ENTIRE graph (all nodes and all edges) to extract graph_vec
        print("\nExtracting final graph embeddings (graph_vec) for ALL nodes...")
        model.eval()
        with torch.no_grad():
            _, graph_vecs = model(x, edge_index_all)

        graph_vecs_np = graph_vecs.numpy().astype(np.float32)
        print(f"Generated graph_vec shape: {graph_vecs_np.shape}")

        # Update SQLite embeddings table with graph_vec BLOBs
        cursor = conn.cursor()
        update_data = [
            (vec.tobytes(), issue_id)
            for vec, issue_id in zip(graph_vecs_np, issue_ids)
        ]

        cursor.executemany(
            "UPDATE embeddings SET graph_vec = ? WHERE issue_id = ?;",
            update_data,
        )
        conn.commit()

        # Verification
        cursor.execute("SELECT COUNT(*) FROM embeddings WHERE graph_vec IS NOT NULL;")
        stored_graph_count = cursor.fetchone()[0]

        print("\n" + "=" * 65)
        print("Graph Embedding Generation Completed Successfully!")
        print("=" * 65)
        print(f"  - Total Issues with Graph Vectors : {stored_graph_count}")
        print(f"  - Graph Vector Length             : {hidden_dim} dimensions")
        print(f"  - SQLite Column Updated           : embeddings.graph_vec")
        print(f"  - PyTorch Checkpoint              : {MODEL_SAVE_PATH}")
        print("=" * 65)

    finally:
        conn.close()


if __name__ == "__main__":
    train_and_embed_graph()
