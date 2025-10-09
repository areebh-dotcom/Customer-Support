from fastapi.testclient import TestClient

from customer_support.api import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_index_serves_frontend():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    body = response.text
    assert "Customer Care Assistant" in body
    assert "quick-actions" in body


def test_links_endpoint_provides_docs_link():
    response = client.get("/links")
    assert response.status_code == 200
    payload = response.json()
    assert payload["docs_url"].endswith("/docs")
    assert payload["chat_endpoint"].endswith("/chat")


def test_chat_endpoint_handles_known_intent():
    response = client.post(
        "/chat",
        json={"session_id": "pytest", "message": "Need help with billing"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "billing"
    assert "billing" in payload["response"]["text"].lower()
    assert len(payload["history"]) == 2
    assert payload["history"][0] == {"role": "user", "text": "Need help with billing"}
    assert payload["history"][1]["intent"] == "billing"


def test_chat_endpoint_handles_empty_message():
    response = client.post(
        "/chat",
        json={"session_id": "pytest", "message": "   "},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "fallback"
    assert payload["confidence"] == 0.0
    assert payload["history"] == []


def test_session_state_endpoint_tracks_history():
    session_id = "pytest-history"

    initial = client.get(f"/sessions/{session_id}")
    assert initial.status_code == 200
    assert initial.json()["history"] == []

    client.post(
        "/chat",
        json={"session_id": session_id, "message": "hi"},
    )

    response = client.get(f"/sessions/{session_id}")
    assert response.status_code == 200
    payload = response.json()
    assert payload["session_id"] == session_id
    assert payload["history"][0] == {"role": "user", "text": "hi"}
    assert payload["history"][1]["intent"] == "greeting"
