"""Optional X-AgentGuard-Latency-Ms header (issue #9)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from agentguard.config import settings
from agentguard.main import app


@pytest.fixture
def expose_latency_header():
    prev = settings.expose_guardrail_latency_header
    settings.expose_guardrail_latency_header = True
    yield
    settings.expose_guardrail_latency_header = prev


def test_latency_header_on_evaluate_input(expose_latency_header):
    client = TestClient(app)
    r = client.post("/v1/guardrails/evaluate-input", json={"text": "hello"})
    assert r.status_code == 200
    assert "X-AgentGuard-Latency-Ms" in r.headers
    assert "input_guardrails=" in r.headers["X-AgentGuard-Latency-Ms"]


def test_latency_header_absent_when_disabled():
    settings.expose_guardrail_latency_header = False
    client = TestClient(app)
    r = client.post("/v1/guardrails/evaluate-input", json={"text": "hello"})
    assert r.status_code == 200
    assert "X-AgentGuard-Latency-Ms" not in r.headers
