from pathlib import Path

from customer_support.engine import ChatbotEngine
from customer_support.knowledge import KnowledgeBase


def load_engine() -> ChatbotEngine:
    kb_path = Path(__file__).resolve().parents[1] / "data" / "knowledge_base.json"
    kb = KnowledgeBase.from_json(kb_path)
    return ChatbotEngine(kb)


def test_engine_matches_billing_intent():
    engine = load_engine()

    response = engine.respond("test", "I have a billing issue")

    assert response.intent == "billing"
    assert "billing" in response.response.text.lower()
    assert response.history[0] == {"role": "user", "text": "I have a billing issue"}
    assert response.history[1]["intent"] == "billing"


def test_engine_falls_back_for_unknown():
    engine = load_engine()

    response = engine.respond("test", "Tell me about space rockets")

    assert response.intent == "fallback"
    assert "not sure" in response.response.text.lower()


def test_session_state_reports_history():
    engine = load_engine()
    session_id = "stateful"

    empty_state = engine.session_state(session_id)
    assert empty_state["history"] == []

    engine.respond(session_id, "hi")

    state = engine.session_state(session_id)
    assert state["history"][0] == {"role": "user", "text": "hi"}
    assert state["history"][1]["intent"] == "greeting"
