"""Tests for Bug-Report Triage API endpoints (Phase 12: Testing and Manual Review)."""

from fastapi.testclient import TestClient
import pytest

from backend.main import app

client = TestClient(app)


def test_triage_endpoint_valid():
    """Verify that /triage accepts a valid bug report and returns required fields."""
    payload = {
        "title": "Crash on startup",
        "body": "It crashes when I run kubectl",
    }
    response = client.post("/triage", json=payload)

    # Assert response status code is 200 OK
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}: {response.text}"

    data = response.json()

    # Assert essential response fields exist
    assert "predicted_label" in data, "Response missing 'predicted_label'"
    assert "confidence" in data, "Response missing 'confidence'"
    assert "draft_comment" in data, "Response missing 'draft_comment'"

    # Verify types and content
    assert isinstance(data["predicted_label"], str) and data["predicted_label"]
    assert isinstance(data["confidence"], (float, int)) and 0.0 <= data["confidence"] <= 1.0
    assert isinstance(data["draft_comment"], str) and len(data["draft_comment"]) > 0


def test_triage_endpoint_empty():
    """Verify that /triage gracefully handles empty inputs without a 500 crash."""
    payload = {
        "title": "",
        "body": "",
    }
    response = client.post("/triage", json=payload)

    # Must NOT crash with a 500 internal server error
    assert response.status_code != 500, f"API crashed with 500 Internal Server Error: {response.text}"

    # Handled gracefully: either 400 Bad Request, 422 Validation Error, or 200 with polite fallback
    assert response.status_code in [200, 400, 422], (
        f"Unexpected status code {response.status_code}: expected 200, 400, or 422."
    )
