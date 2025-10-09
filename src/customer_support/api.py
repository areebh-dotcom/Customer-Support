"""FastAPI application exposing the chatbot engine."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

from fastapi import Body, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .engine import ChatbotEngine
from .knowledge import KnowledgeBase

app = FastAPI(title="Customer Support Chatbot", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"]
)


def kb_path() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "knowledge_base.json"


@lru_cache()
def knowledge_base() -> KnowledgeBase:
    return KnowledgeBase.from_json(kb_path())


@lru_cache()
def engine() -> ChatbotEngine:
    return ChatbotEngine(knowledge_base())


@app.get("/health")
def healthcheck() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/intents")
def list_intents(kb: KnowledgeBase = Depends(knowledge_base)) -> Dict[str, Dict[str, Any]]:
    return kb.to_dict()


@app.post("/chat")
def chat(payload: Dict[str, Any] = Body(...), bot: ChatbotEngine = Depends(engine)) -> Dict[str, Any]:
    session_id = str(payload.get("session_id", "anon"))
    message = str(payload.get("message", "")).strip()
    if not message:
        return {
            "session_id": session_id,
            "intent": "fallback",
            "confidence": 0.0,
            "response": {
                "text": "Could you share a bit more detail so I can assist you?",
                "suggestions": ["Billing question", "Trouble logging in", "Talk to an agent"],
            },
            "memory": {},
        }

    response = bot.respond(session_id, message)
    return response.to_dict()


@app.post("/sessions/{session_id}/reset")
def reset_session(session_id: str, bot: ChatbotEngine = Depends(engine)) -> Dict[str, str]:
    bot.reset_session(session_id)
    return {"status": "reset", "session_id": session_id}
