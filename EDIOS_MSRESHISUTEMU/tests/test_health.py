# test_health.py - smoke test for /health and /ready (generated)
"""Smoke tests for health check endpoints."""
import pytest


def test_health_ok(client):
    """GET /health returns 200 and status ok."""
    r = client.get("/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data is not None
    assert data.get("status") == "ok"


def test_ready_returns_200_or_503(client):
    """GET /ready returns 200 (DB ok) or 503 (DB unreachable)."""
    r = client.get("/ready")
    assert r.status_code in (200, 503)
