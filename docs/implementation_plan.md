# Customer Support Chatbot – MVP Implementation Plan

This document captures the discovery notes, design decisions, and backlog for the first functional release of the customer support chatbot. It distills the broader blueprint into concrete workstreams for the MVP.

## 1. Discovery Highlights
- **Top intents to support first:** billing questions, login help, live event access, general greeting/help, graceful fallbacks.
- **Tone & brand:** friendly, concise, confident. Empathy for sensitive issues (billing, outages).
- **Channels:** Start with a web widget + REST API. CLI provided for quick demos.
- **Success criteria for MVP:** response latency under 500 ms for scripted intents, clear escalation path, ability to capture structured data for billing cases.

## 2. Architecture Snapshot
```
User -> Web Widget / CLI -> FastAPI backend -> Rule-based engine -> JSON knowledge base
```
- **Backend:** Python FastAPI app served via Uvicorn.
- **Knowledge base:** JSON file with canonical utterances, responses, and optional forms.
- **Engine:** Lightweight intent matching via fuzzy similarity (difflib) with fallback handling.
- **State:** In-memory session memory storing last intent and future slot data.

## 3. Functional Scope for First Release
1. **Conversational flows** for greeting, billing, login help, live events, goodbye, and fallback.
2. **Structured responses** including suggestions and forms for data capture.
3. **REST endpoints** for health check, listing intents, chatting, and resetting a session.
4. **Developer tooling**: CLI runner and automated unit tests for billing/fallback coverage.

## 4. Backlog & Next Steps
- Add analytics hooks (event logging per turn).
- Persist session memory to Redis or database for scalability.
- Expand knowledge base and integrate with CMS or external APIs.
- Implement authentication for authenticated user context.
- Build React widget consuming the REST API with quick replies and forms.

## 5. Operational Runbook
- Install dependencies with `pip install -r requirements.txt`.
- Start the API locally: `uvicorn customer_support.api:app --reload`.
- Run tests with `pytest`.
- Monitor logs for slow requests; adjust threshold for intent detection as knowledge base grows.
