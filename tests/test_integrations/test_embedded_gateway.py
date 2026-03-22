"""In-process FastAPI integration: embedded gateway router."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from agentguard.integrations import include_gateway_router, register_agentguard_middleware


def test_embedded_gateway_complete_local_provider():
    app = FastAPI()
    register_agentguard_middleware(app)
    include_gateway_router(app)
    client = TestClient(app)
    resp = client.post(
        "/v1/gateway/complete",
        json={
            "messages": [{"role": "user", "content": "hello"}],
            "model_provider": "local",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["tenant_id"] == "default"
    assert "choices" in data["output"]
