"""Simple command line interface for manual testing of the chatbot engine."""
from __future__ import annotations

import uuid
from pathlib import Path

from .engine import ChatbotEngine
from .knowledge import KnowledgeBase


def run_cli() -> None:
    kb_path = Path(__file__).resolve().parents[2] / "data" / "knowledge_base.json"
    engine = ChatbotEngine(KnowledgeBase.from_json(kb_path))
    session_id = str(uuid.uuid4())
    print("Customer Support Assistant (type 'exit' to quit)")

    while True:
        message = input("You: ").strip()
        if message.lower() in {"exit", "quit"}:
            break
        if not message:
            continue
        response = engine.respond(session_id, message)
        print(f"Bot [{response.intent} @ {response.confidence:.2f}]: {response.response.text}")
        if response.response.suggestions:
            print("Suggestions:")
            for suggestion in response.response.suggestions:
                print(f"  - {suggestion}")
    print("Goodbye!")


if __name__ == "__main__":
    run_cli()
