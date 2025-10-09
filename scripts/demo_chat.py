"""Run a scripted conversation against the chatbot engine."""
from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from customer_support.engine import ChatbotEngine
from customer_support.knowledge import KnowledgeBase


def load_engine() -> ChatbotEngine:
    kb_path = Path(__file__).resolve().parents[1] / "data" / "knowledge_base.json"
    knowledge_base = KnowledgeBase.from_json(kb_path)
    return ChatbotEngine(knowledge_base)


def run_demo() -> None:
    engine = load_engine()
    session_id = "demo"
    script = [
        "hello",
        "I have a billing issue",
        "thank you",
    ]

    print("Running scripted chat demo.\n")
    for turn, message in enumerate(script, start=1):
        response = engine.respond(session_id, message)
        header = f"Turn {turn}: You -> {message}"
        print(header)
        print("Bot ->", response.response.text)
        if response.response.suggestions:
            print("Suggestions:")
            for suggestion in response.response.suggestions:
                print(f"  - {suggestion}")
        if response.response.form:
            print("Form:")
            print(f"  {response.response.form.title}")
            for field in response.response.form.fields:
                required = "*" if field.required else ""
                print(f"   - {field.label} ({field.type}){required}")
        print()

    print("Demo complete.")


if __name__ == "__main__":
    run_demo()
