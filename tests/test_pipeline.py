"""Unit and integration tests for API, agent routing, and preprocessing utilities."""

from fastapi.testclient import TestClient
import numpy as np
import pytest

from agents.graph import route_confidence
from backend.main import app
from features.clean_text import clean_issue_body
from features.label_awareness import NUM_CLASSES, compute_label_distribution


def test_clean_issue_body():
    """Verify that clean_issue_body strips markdown comments and normalizes whitespace."""
    raw = (
        "<!-- This is a comment that must be stripped -->\n"
        "### What happened?\n"
        "The kubelet crashed with OOM on node-1.\n"
        "```go\n"
        "func main() { panic(\"oom\") }\n"
        "```"
    )
    cleaned = clean_issue_body(raw)
    assert "This is a comment" not in cleaned
    assert "kubelet crashed with OOM" in cleaned


def test_compute_label_distribution():
    """Verify compute_label_distribution returns normalized vector or uniform fallback."""
    # Test uniform fallback for empty list
    uniform_vec = compute_label_distribution([])
    assert len(uniform_vec) == NUM_CLASSES
    assert np.isclose(np.sum(uniform_vec), 1.0)
    assert np.allclose(uniform_vec, 1.0 / NUM_CLASSES)

    # Test single label
    single_vec = compute_label_distribution(["sig/node"])
    assert np.isclose(np.sum(single_vec), 1.0)
    assert single_vec[4] == 1.0  # LABEL_TO_IDX["sig/node"] == 4


def test_agent_route_confidence():
    """Verify agent route_confidence conditional router branching."""
    high_state = {"confidence": 0.85}
    assert route_confidence(high_state) == "writer_high_node"

    threshold_state = {"confidence": 0.60}
    assert route_confidence(threshold_state) == "writer_high_node"

    low_state = {"confidence": 0.59}
    assert route_confidence(low_state) == "writer_low_node"

    zero_state = {"confidence": 0.0}
    assert route_confidence(zero_state) == "writer_low_node"


def test_api_root_endpoint():
    """Verify FastAPI GET / health check endpoint."""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["service"] == "Bug Triage API"


def test_api_triage_empty_title_validation():
    """Verify FastAPI POST /triage rejects empty issue title with HTTP 400."""
    client = TestClient(app)
    payload = {"title": "   ", "body": "Some body content"}
    response = client.post("/triage", json=payload)
    assert response.status_code == 400
    assert "cannot be empty" in response.json()["detail"].lower()
