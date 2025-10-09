"""Domain models for the customer support chatbot."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class FormField:
    """Schema for a dynamic form field shown to the user."""

    name: str
    label: str
    type: str
    required: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "FormField":
        return cls(
            name=str(data["name"]),
            label=str(data.get("label", "")),
            type=str(data.get("type", "text")),
            required=bool(data.get("required", False)),
        )


@dataclass
class FormSchema:
    """Dynamic form attached to an intent response."""

    title: str
    fields: List[FormField] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "FormSchema":
        fields = [FormField.from_dict(f) for f in data.get("fields", [])]
        return cls(title=str(data.get("title", "")), fields=fields)


@dataclass
class ResponsePayload:
    """Response payload returned for a resolved intent."""

    text: str
    suggestions: List[str] = field(default_factory=list)
    form: Optional[FormSchema] = None

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "ResponsePayload":
        form_data = data.get("form")
        form = FormSchema.from_dict(form_data) if isinstance(form_data, dict) else None
        return cls(
            text=str(data.get("text", "")),
            suggestions=[str(item) for item in data.get("suggestions", [])],
            form=form,
        )

    def to_dict(self) -> Dict[str, object]:
        payload: Dict[str, object] = {
            "text": self.text,
            "suggestions": list(self.suggestions),
        }
        if self.form:
            payload["form"] = {
                "title": self.form.title,
                "fields": [field.__dict__ for field in self.form.fields],
            }
        return payload


@dataclass
class Intent:
    """Canonical intent description loaded from the knowledge base."""

    name: str
    utterances: List[str]
    response: ResponsePayload


@dataclass
class Memory:
    """Conversation state tracked across user turns."""

    session_id: str
    last_intent: Optional[str] = None
    slots: Dict[str, str] = field(default_factory=dict)


@dataclass
class ChatRequest:
    """Incoming message payload for the API."""

    message: str
    session_id: str = "anon"


@dataclass
class ChatResponse:
    """Response returned by the chatbot engine via the API."""

    session_id: str
    intent: str
    confidence: float
    response: ResponsePayload
    memory: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, object]:
        return {
            "session_id": self.session_id,
            "intent": self.intent,
            "confidence": self.confidence,
            "response": self.response.to_dict(),
            "memory": dict(self.memory),
        }
