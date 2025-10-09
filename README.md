# Customer Support Chatbot

This repository houses the source code and planning artifacts for a customer support virtual assistant. The goal is to deliver a guided, trustworthy, and insight-driven experience that resolves the majority of subscriber issues without human intervention.

## Project Structure
- `docs/chatbot_blueprint.md` – Strategic blueprint covering product vision, capabilities, and roadmap.
- `docs/implementation_plan.md` – Discovery notes and MVP delivery plan for the first functional release.
- `data/knowledge_base.json` – Canonical intents and scripted responses for the MVP chatbot.
- `src/customer_support/` – FastAPI application, rule-based engine, and CLI utilities.
- `tests/` – Automated unit tests covering core chatbot behavior.

## Getting Started
1. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the API locally**:
   ```bash
   uvicorn customer_support.api:app --reload
   ```
   or use the provided shortcuts:
   ```bash
   make run   # start the FastAPI server on http://127.0.0.1:8000
   make chat  # launch the interactive CLI tester
   ```
4. **Interact with the chatbot**:
   - Send REST requests to `POST /chat` with JSON `{ "session_id": "demo", "message": "I have a billing issue" }`.
   - Exercise the automated smoke tests to confirm the endpoints function end-to-end:
     ```bash
     make test
     ```
   - Use the CLI helper for a quick terminal experience:
     ```bash
     python -m customer_support.cli
     ```

## Next Steps
The MVP focuses on scripted flows for top intents. Future iterations will integrate a richer knowledge base, analytics instrumentation, multilingual support, and web/mobile chat widgets.
