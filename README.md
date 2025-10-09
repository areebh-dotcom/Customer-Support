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
   Or, use the Make target to bootstrap the environment in one step:
   ```bash
   make install
   ```
3. **Run the API locally**:
   ```bash
   uvicorn --app-dir src customer_support.api:app --reload
   ```
   Or, using the provided shortcut (which sets the same flag for you):
   ```bash
   make run
   ```
   Once running, visit the fully featured web chat at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) for a guided UI that mirrors
   the reference designs. The browser client offers quick-reply chips, dynamic billing forms, typing indicators, and automatic
   transcript recovery so you can watch the experience update in real time. The interactive API docs remain available at
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) if you prefer to exercise the endpoints directly.
4. **Interact with the chatbot**:
   - Send REST requests to `POST /chat` with JSON `{ "session_id": "demo", "message": "I have a billing issue" }`. Each response now echoes the running conversation history so you can render transcripts on the client side.
   - Retrieve the active session memory and transcript with `GET /sessions/{session_id}` or reset it via `POST /sessions/{session_id}/reset`.
   - Use the CLI helper for a quick terminal experience:
     ```bash
     python -m customer_support.cli
     ```
   - Replay the scripted smoke test conversation without starting the API:
     ```bash
     python scripts/demo_chat.py
     ```
5. **Run tests**:
   ```bash
   pytest
   ```
   Or run the full suite via Make:
   ```bash
   make test
   ```

## Containerized Deployment

Build and run the chatbot in a self-contained Docker image:

```bash
make docker-build
make docker-run
```

Or perform both steps in one go:

```bash
make deploy
```

To publish the image to your container registry, override the image reference and push:

```bash
make docker-build IMAGE_NAME=registry.example.com/my-team/customer-support IMAGE_TAG=v1
make docker-push IMAGE_NAME=registry.example.com/my-team/customer-support IMAGE_TAG=v1
```

The defaults (`customer-support-chatbot:latest`) remain suitable for local testing.

The API will be available on [http://127.0.0.1:8000](http://127.0.0.1:8000); visit `/docs` for the interactive interface. To stop the container, press <kbd>Ctrl</kbd>+<kbd>C</kbd> (or run `docker ps` and `docker stop` if launched in detached mode).

## Continuous Integration

This repository includes a GitHub Actions workflow that installs dependencies, executes the test suite, and builds the Docker image on every push and pull request. The workflow lives in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) and keeps the chatbot deployable by catching regressions before they reach production.

## Publishing to GitHub

To link a freshly cloned workspace to the public repository and push your commits, configure the remote and publish the `main` branch:

```bash
git remote add origin https://github.com/areebh-dotcom/Customer-Support.git
git branch -m main
git push -u origin main
```

If the branch already exists remotely, run `git fetch origin` beforehand so the local branch can track the upstream history.

### Using a Personal Access Token (PAT)

When authenticating with GitHub from CI or a restricted environment, set a personal access token in the `GITHUB_PAT` environment variable and run the helper script:

```bash
export GITHUB_PAT=github_pat_xxx   # token with repo scope
./scripts/push_with_pat.sh areebh-dotcom/Customer-Support main
```

The script safely configures (or updates) the `origin` remote with the tokenized URL and performs `git push -u origin <branch>`. Override `REMOTE_NAME` or the branch argument if you need to publish to a different remote or branch.

## Next Steps
The MVP focuses on scripted flows for top intents. Future iterations will integrate a richer knowledge base, analytics instrumentation, multilingual support, and web/mobile chat widgets.
