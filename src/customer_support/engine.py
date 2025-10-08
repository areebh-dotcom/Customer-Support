"""Core rule-based chatbot engine."""
from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Dict

from .knowledge import KnowledgeBase
from .models import ChatResponse, Intent, Memory, ResponsePayload


@dataclass
class MatchResult:
    intent: Intent
    confidence: float


class ChatbotEngine:
    """Tiny rule-based engine capable of serving MVP chat requests."""

    def __init__(self, knowledge_base: KnowledgeBase, threshold: float = 0.55):
        self.knowledge_base = knowledge_base
        self.threshold = threshold
        self._memory: Dict[str, Memory] = {}

    def _memory_for(self, session_id: str) -> Memory:
        if session_id not in self._memory:
            self._memory[session_id] = Memory(session_id=session_id)
        return self._memory[session_id]

    def _similarity(self, a: str, b: str) -> float:
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    def _match_intent(self, text: str) -> MatchResult:
        best_intent = None
        best_score = 0.0
        normalized = text.strip().lower()

        for intent in self.knowledge_base.intents():
            if not intent.utterances:
                continue
            for utterance in intent.utterances:
                score = self._similarity(normalized, utterance)
                if score > best_score:
                    best_score = score
                    best_intent = intent

        if best_intent and best_score >= self.threshold:
            return MatchResult(intent=best_intent, confidence=best_score)

        fallback = self.knowledge_base.get("fallback")
        return MatchResult(intent=fallback, confidence=best_score)

    def respond(self, session_id: str, message: str) -> ChatResponse:
        memory = self._memory_for(session_id)
        match = self._match_intent(message)

        memory.last_intent = match.intent.name
        response_payload: ResponsePayload = match.intent.response

        return ChatResponse(
            session_id=session_id,
            intent=match.intent.name,
            confidence=round(match.confidence, 3),
            response=response_payload,
            memory=memory.slots,
        )

    def reset_session(self, session_id: str) -> None:
        self._memory.pop(session_id, None)

    def stats(self) -> Dict[str, Dict[str, list]]:
        return self.knowledge_base.to_dict()
