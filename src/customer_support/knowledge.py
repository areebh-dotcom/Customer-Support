"""Knowledge base loader for the customer support chatbot."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List

from .models import Intent, ResponsePayload


class KnowledgeBase:
    """Loads and stores intents defined in a JSON file."""

    def __init__(self, intents: List[Intent]):
        self._intents = {intent.name: intent for intent in intents}

    @classmethod
    def from_json(cls, path: Path) -> "KnowledgeBase":
        raw = json.loads(path.read_text())
        intents: List[Intent] = []
        for entry in raw:
            response = ResponsePayload.from_dict(entry["response"])
            intents.append(
                Intent(
                    name=entry["intent"],
                    utterances=[u.lower() for u in entry.get("utterances", [])],
                    response=response,
                )
            )
        return cls(intents)

    def intents(self) -> Iterable[Intent]:
        return self._intents.values()

    def get(self, name: str) -> Intent:
        return self._intents[name]

    def to_dict(self) -> Dict[str, Dict[str, List[str]]]:
        return {
            intent.name: {
                "utterances": intent.utterances,
                "suggestions": intent.response.suggestions,
            }
            for intent in self._intents.values()
        }
