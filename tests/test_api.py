"""Integration-style tests for the FastAPI chatbot service."""
from __future__ import annotations

from fastapi.testclient import TestClient

from customer_support.api import app


client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_intents_includes_billing() -> None:
    response = client.get("/intents")
    payload = response.json()
    assert response.status_code == 200
    assert "billing" in payload
    assert "utterances" in payload["billing"]
    assert "charge on my account" in payload["billing"]["utterances"]


def test_chat_returns_expected_intent() -> None:
    response = client.post(
        "/chat",
        json={"session_id": "test", "message": "hello"},
    )
    body = response.json()
    assert response.status_code == 200
    assert body["intent"] == "greeting"
    assert body["session_id"] == "test"
    assert body["confidence"] >= 0.55
    assert "Hi there" in body["response"]["text"]


def test_chat_handles_blank_message_with_fallback() -> None:
    response = client.post(
        "/chat",
        json={"session_id": "blank", "message": ""},
    )
    body = response.json()
    assert response.status_code == 200
    assert body["intent"] == "fallback"
    assert body["confidence"] == 0.0
    assert "share a bit more detail" in body["response"]["text"]


def test_reset_session_clears_memory() -> None:
    response = client.post(
        "/chat",
        json={"session_id": "reset-me", "message": "billing issue"},
    )
    assert response.status_code == 200
    reset_response = client.post("/sessions/reset-me/reset")
    assert reset_response.status_code == 200
    assert reset_response.json() == {"status": "reset", "session_id": "reset-me"}
