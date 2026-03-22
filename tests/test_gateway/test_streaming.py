"""Gateway stream=true behavior (issue #10)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from agentguard.main import app


def test_stream_true_local_provider_returns_400():
    client = TestClient(app)
    r = client.post(
        "/v1/gateway/complete",
        json={
            "messages": [{"role": "user", "content": "hi"}],
            "model_provider": "local",
            "stream": True,
        },
    )
    assert r.status_code == 400
    body = r.json()
    assert body["detail"]["error"] == "streaming_not_supported"


def test_stream_false_local_still_json():
    client = TestClient(app)
    r = client.post(
        "/v1/gateway/complete",
        json={
            "messages": [{"role": "user", "content": "hi"}],
            "model_provider": "local",
            "stream": False,
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert "output" in data


def test_stream_true_openai_without_key_returns_400(monkeypatch):
    from agentguard.config import settings

    monkeypatch.setattr(settings, "openai_api_key", "")
    client = TestClient(app)
    r = client.post(
        "/v1/gateway/complete",
        json={
            "messages": [{"role": "user", "content": "hi"}],
            "model_provider": "openai",
            "stream": True,
        },
    )
    assert r.status_code == 400
    assert r.json()["detail"]["error"] == "missing_openai_api_key"
