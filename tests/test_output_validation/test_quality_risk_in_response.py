"""Optional quality_risk_score in POST /v1/outputs/validate metadata."""

from __future__ import annotations

from fastapi.testclient import TestClient

from agentguard.main import app


def test_validate_without_score_flag_empty_metadata_keys():
    client = TestClient(app)
    r = client.post(
        "/v1/outputs/validate",
        json={"output_text": "Hello world.", "context_text": ""},
    )
    assert r.status_code == 200
    data = r.json()
    assert "quality_risk_score" not in data.get("metadata", {})


def test_validate_with_score_flag_populates_metadata():
    client = TestClient(app)
    r = client.post(
        "/v1/outputs/validate",
        json={
            "output_text": "Hello world.",
            "context_text": "Hello world.",
            "include_quality_risk_score": True,
        },
    )
    assert r.status_code == 200
    data = r.json()
    meta = data["metadata"]
    assert "quality_risk_score" in meta
    assert "quality_risk_decision" in meta
    assert 0.0 <= meta["quality_risk_score"] <= 1.0
