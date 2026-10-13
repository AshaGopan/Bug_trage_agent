"""LangGraph workflow node implementations for Bug-Report Triage Agent (Phase 10).

Implements individual agent reasoning nodes:
  - intake_node: cleans text using clean_issue_body
  - missing_info_node: evaluates report completeness via LLM JSON extraction
  - cold_start_node: computes dense text vector, queries ChromaDB, and performs cold-start GraphSAGE & label distribution calculation
  - classifier_node: performs LightGBM inference and confidence estimation
  - writer_high_node / writer_low_node: crafts tailored GitHub triage responses
"""

import json
import os
from pathlib import Path
import re
import sqlite3
import sys
from typing import Any

from dotenv import load_dotenv
import httpx
import joblib
import numpy as np
import torch

# Support running directly or as module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agents.prompts import MISSING_INFO_PROMPT, WRITER_PROMPT
from agents.state import TriageState
from features.clean_text import clean_issue_body
from features.db import DEFAULT_DB_PATH, get_db_connection
from features.embed_graph import GraphSAGE
from features.embed_text import load_model as load_embedding_model
from features.label_awareness import compute_label_distribution
from features.vector_store import query_similar_issues

load_dotenv()

MODEL_SAVED_DIR = Path("models/saved")
GRAPHSAGE_WEIGHTS_PATH = MODEL_SAVED_DIR / "graphsage.pt"
HYBRID_MODEL_PATH = MODEL_SAVED_DIR / "hybrid_model.joblib"

# Global lazy singletons to conserve CPU and RAM
_EMBED_MODEL = None
_GRAPHSAGE_MODEL = None
_LIGHTGBM_MODEL = None


def get_embedding_model():
    global _EMBED_MODEL
    if _EMBED_MODEL is None:
        _EMBED_MODEL = load_embedding_model()
    return _EMBED_MODEL


def get_graphsage_model():
    global _GRAPHSAGE_MODEL
    if _GRAPHSAGE_MODEL is None:
        model = GraphSAGE(in_channels=384, hidden_channels=128, out_channels=7)
        if GRAPHSAGE_WEIGHTS_PATH.exists():
            model.load_state_dict(torch.load(GRAPHSAGE_WEIGHTS_PATH, map_location="cpu"))
        model.eval()
        _GRAPHSAGE_MODEL = model
    return _GRAPHSAGE_MODEL


def get_hybrid_model():
    global _LIGHTGBM_MODEL
    if _LIGHTGBM_MODEL is None:
        if not HYBRID_MODEL_PATH.exists():
            raise FileNotFoundError(f"Hybrid LightGBM model not found at: {HYBRID_MODEL_PATH}")
        _LIGHTGBM_MODEL = joblib.load(HYBRID_MODEL_PATH)
    return _LIGHTGBM_MODEL


def call_llm_api(system_prompt: str, user_prompt: str) -> str:
    """Call an LLM API securely using environment keys with robust local fallback."""
    api_key = os.getenv("LLM_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("HF_TOKEN")

    if api_key and not api_key.startswith("hf_your"):
        # 1. Google Gemini endpoint
        if api_key.startswith("AIza"):
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                payload = {
                    "contents": [{"parts": [{"text": f"{system_prompt}\n\n{user_prompt}"}]}],
                    "generationConfig": {"temperature": 0.2, "maxOutputTokens": 800},
                }
                with httpx.Client(timeout=15.0) as client:
                    resp = client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        return candidates[0]["content"]["parts"][0]["text"].strip()
            except Exception as e:
                print(f"[Notice] Gemini API call skipped ({e}). Using robust fallback.")

        # 2. HuggingFace Serverless Inference Router endpoint
        else:
            try:
                url = "https://router.huggingface.co/hf-inference/models/meta-llama/Llama-3.2-3B-Instruct/v1/chat/completions"
                headers = {"Authorization": f"Bearer {api_key.strip()}"}
                payload = {
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "max_tokens": 600,
                    "temperature": 0.2,
                }
                with httpx.Client(timeout=15.0) as client:
                    resp = client.post(url, json=payload, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    return data["choices"][0]["message"]["content"].strip()
            except Exception as e:
                print(f"[Notice] HuggingFace API call skipped ({e}). Using robust fallback.")

    return ""


# ---------------------------------------------------------------------------
# Node 1: Intake
# ---------------------------------------------------------------------------
def intake_node(state: TriageState) -> dict[str, Any]:
    """Clean the raw issue body and normalize the text."""
    raw_body = state.get("raw_body", "") or ""
    clean_body = clean_issue_body(raw_body)
    return {"clean_body": clean_body}


# ---------------------------------------------------------------------------
# Node 2: Missing Information Assessment
# ---------------------------------------------------------------------------
def missing_info_node(state: TriageState) -> dict[str, Any]:
    """Call the LLM with MISSING_INFO_PROMPT to identify diagnostic omissions."""
    title = state.get("raw_title", "")
    body = state.get("clean_body", "")
    user_prompt = f"Bug Report Title: {title}\n\nBug Report Body:\n{body}"

    llm_output = call_llm_api(MISSING_INFO_PROMPT, user_prompt)

    parsed_info = None
    if llm_output:
        try:
            # Extract JSON block using regex
            json_match = re.search(r"\{.*?\}", llm_output, re.DOTALL)
            if json_match:
                parsed_info = json.loads(json_match.group(0))
        except Exception:
            pass

    # Heuristic fallback if API key is unset or output is non-JSON
    if not parsed_info or not isinstance(parsed_info, dict):
        text_lower = f"{title}\n{body}".lower()
        has_repro = bool(re.search(r"(reproduc|steps to|repro|how to repro|to repro)", text_lower))
        has_logs = bool(re.search(r"(error|exception|panic|fatal|traceback|stderr|failed with|status:)", text_lower))
        has_version = bool(re.search(r"(kubernetes version|k8s version|v1\.\d+|client version|server version)", text_lower))

        missing_fields = []
        if not has_repro:
            missing_fields.append("step-by-step reproduction instructions")
        if not has_logs:
            missing_fields.append("component log excerpts or terminal error output")
        if not has_version:
            missing_fields.append("Kubernetes version and operating environment")

        parsed_info = {
            "has_repro": has_repro,
            "has_logs": has_logs,
            "missing_fields": missing_fields,
        }

    return {"missing_info": parsed_info}


# ---------------------------------------------------------------------------
# Node 3: Cold-Start Vector & Graph Representation
# ---------------------------------------------------------------------------
def cold_start_node(state: TriageState) -> dict[str, Any]:
    """Compute text embedding, retrieve top 5 Chroma neighbors, and compute graph & label vectors."""
    title = state.get("raw_title", "")
    body = state.get("clean_body", "")
    full_text = f"{title} {body}".strip()

    # 1. Generate text embedding on CPU
    embed_model = get_embedding_model()
    text_vec = embed_model.encode([full_text], convert_to_numpy=True)[0].astype(np.float32)

    # 2. Retrieve top 5 similar historical issues from ChromaDB
    chroma_results = query_similar_issues(text_vec, n_results=5)
    similar_issues = []

    if chroma_results and chroma_results.get("ids") and len(chroma_results["ids"][0]) > 0:
        retrieved_ids = chroma_results["ids"][0]
        metadatas = chroma_results["metadatas"][0]
        distances = chroma_results.get("distances", [[]])[0]

        for i, iid in enumerate(retrieved_ids):
            similar_issues.append({
                "issue_id": int(iid),
                "title": metadatas[i].get("title", ""),
                "label": metadatas[i].get("label", ""),
                "distance": distances[i] if i < len(distances) else None,
            })

    # 3. Compute label_aware_vec from retrieved training neighbors
    neighbor_labels = [s["label"] for s in similar_issues if s.get("label")]
    label_aware_vec = compute_label_distribution(neighbor_labels)

    # 4. Compute cold-start graph_vec using temporary edges to the 5 neighbors
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        neighbor_vecs = []
        valid_neighbor_count = 0

        for s in similar_issues:
            cursor.execute("SELECT text_vec FROM embeddings WHERE issue_id = ?;", (s["issue_id"],))
            row = cursor.fetchone()
            if row and row["text_vec"]:
                neighbor_vecs.append(np.frombuffer(row["text_vec"], dtype=np.float32))
                valid_neighbor_count += 1
    finally:
        conn.close()

    if valid_neighbor_count > 0:
        # Construct temporary subgraph: Node 0 = new issue, Nodes 1..K = retrieved neighbors
        all_vecs = [text_vec] + neighbor_vecs
        x_subgraph = torch.tensor(np.stack(all_vecs), dtype=torch.float32)

        src_edges = [0] * valid_neighbor_count + list(range(1, valid_neighbor_count + 1))
        dst_edges = list(range(1, valid_neighbor_count + 1)) + [0] * valid_neighbor_count
        edge_index_subgraph = torch.tensor([src_edges, dst_edges], dtype=torch.long)

        gnn_model = get_graphsage_model()
        with torch.no_grad():
            _, out_graph_vecs = gnn_model(x_subgraph, edge_index_subgraph)
        graph_vec = out_graph_vecs[0].numpy().astype(np.float32)
    else:
        # Zero-edge fallback
        gnn_model = get_graphsage_model()
        x_single = torch.tensor(text_vec.reshape(1, -1), dtype=torch.float32)
        edge_empty = torch.empty((2, 0), dtype=torch.long)
        with torch.no_grad():
            _, out_graph_vecs = gnn_model(x_single, edge_empty)
        graph_vec = out_graph_vecs[0].numpy().astype(np.float32)

    return {
        "similar_issues": similar_issues,
        "text_vec": text_vec,
        "graph_vec": graph_vec,
        "label_aware_vec": label_aware_vec,
    }


# ---------------------------------------------------------------------------
# Node 4: LightGBM Classifier
# ---------------------------------------------------------------------------
def classifier_node(state: TriageState) -> dict[str, Any]:
    """Combine modalities and predict SIG category and prediction confidence."""
    text_vec = state.get("text_vec")
    graph_vec = state.get("graph_vec")
    label_aware_vec = state.get("label_aware_vec")

    if text_vec is None or graph_vec is None or label_aware_vec is None:
        raise ValueError("Missing feature vectors in TriageState for classification.")

    features = np.concatenate([text_vec, graph_vec, label_aware_vec]).reshape(1, -1)
    clf = get_hybrid_model()

    probabilities = clf.predict_proba(features)[0]
    best_idx = int(np.argmax(probabilities))
    confidence = float(probabilities[best_idx])
    predicted_label = str(clf.classes_[best_idx])

    return {
        "predicted_label": predicted_label,
        "confidence": confidence,
    }


# ---------------------------------------------------------------------------
# Node 5a: Writer Node (High Confidence >= 0.60)
# ---------------------------------------------------------------------------
def writer_high_node(state: TriageState) -> dict[str, Any]:
    """Draft a response recommending the predicted SIG label with high confidence."""
    title = state.get("raw_title", "")
    pred_label = state.get("predicted_label", "sig/node")
    confidence = state.get("confidence", 0.0)
    missing = state.get("missing_info", {}).get("missing_fields", [])
    similar = state.get("similar_issues", [])

    sim_text = "\n".join([f"- #{s['issue_id']}: {s['title']} ({s['label']})" for s in similar[:3]])
    missing_text = ", ".join(missing) if missing else "None"

    context = (
        f"Mode: HIGH CONFIDENCE\n"
        f"Predicted SIG Label: {pred_label} (Confidence: {confidence*100:.1f}%)\n"
        f"Issue Title: {title}\n"
        f"Missing Fields: {missing_text}\n"
        f"Similar Issues Found:\n{sim_text}\n"
    )

    comment = call_llm_api(WRITER_PROMPT, context)

    if not comment:
        # High quality template fallback
        sig_name = pred_label.replace("sig/", "").upper()
        similar_bullets = "\n".join([f"- **#{s['issue_id']}**: {s['title']}" for s in similar[:3]])
        missing_section = ""
        if missing:
            missing_items = "\n".join([f"- {field}" for field in missing])
            missing_section = (
                f"\n### 📋 Requested Diagnostic Details\n"
                f"To help maintainers reproduce and troubleshoot the issue efficiently, please provide:\n"
                f"{missing_items}\n"
            )

        similar_section = ""
        if similar:
            similar_section = (
                f"\n### 🔍 Potentially Related Issues\n"
                f"Our triage system identified the following similar historical reports:\n"
                f"{similar_bullets}\n"
            )

        comment = (
            f"Thanks for opening this issue!\n\n"
            f"### SIG Assignment Recommendation\n"
            f"Based on our automated classification model (**{confidence*100:.1f}% confidence**), "
            f"this report has been triaged for **`{pred_label}`** (SIG {sig_name}).\n"
            f"{missing_section}"
            f"{similar_section}\n"
            f"*/sig {pred_label.replace('sig/', '')}*"
        )

    return {"draft_comment": comment}


# ---------------------------------------------------------------------------
# Node 5b: Writer Node (Low Confidence < 0.60)
# ---------------------------------------------------------------------------
def writer_low_node(state: TriageState) -> dict[str, Any]:
    """Draft a response asking for clarification without suggesting a specific SIG label."""
    title = state.get("raw_title", "")
    confidence = state.get("confidence", 0.0)
    missing = state.get("missing_info", {}).get("missing_fields", [])
    similar = state.get("similar_issues", [])

    sim_text = "\n".join([f"- #{s['issue_id']}: {s['title']} ({s['label']})" for s in similar[:3]])
    missing_text = ", ".join(missing) if missing else "None"

    context = (
        f"Mode: LOW CONFIDENCE\n"
        f"Confidence Score: {confidence*100:.1f}% (Under 60% threshold - DO NOT suggest a label!)\n"
        f"Issue Title: {title}\n"
        f"Missing Fields: {missing_text}\n"
        f"Similar Issues Found:\n{sim_text}\n"
    )

    comment = call_llm_api(WRITER_PROMPT, context)

    if not comment:
        # High quality template fallback (STRICTLY NO SIG ASSIGNMENT)
        similar_bullets = "\n".join([f"- **#{s['issue_id']}**: {s['title']} (`{s['label']}`)" for s in similar[:3]])
        missing_section = ""
        if missing:
            missing_items = "\n".join([f"- {field}" for field in missing])
            missing_section = (
                f"\n### 📋 Requested Diagnostic Details\n"
                f"To help us identify the affected subsystem, could you please provide:\n"
                f"{missing_items}\n"
            )

        similar_section = ""
        if similar:
            similar_section = (
                f"\n### 🔍 Potentially Related Issues\n"
                f"These existing reports might share relevant symptoms across components:\n"
                f"{similar_bullets}\n"
            )

        comment = (
            f"Thanks for opening this issue!\n\n"
            f"### Triage Notice: Clarification Needed\n"
            f"This bug report appears to touch multiple Kubernetes areas or requires additional "
            f"context before assigning a specific Special Interest Group (SIG) label "
            f"(confidence score: **{confidence*100:.1f}%**).\n"
            f"{missing_section}"
            f"{similar_section}\n"
            f"Once more diagnostic information is shared, a maintainer will route this issue to the appropriate team."
        )

    return {"draft_comment": comment}
