# Multi-Agent Software Engineer

Autonomous AI engineering team for real software repositories. The FastAPI backend creates an isolated workspace and coordinates repository, developer, testing, and review agents. The React frontend visualizes the synchronous workflow and its final result.

## Local development

Prerequisites: Python 3.13+, Git, Node.js 22+, and Ollama with a Qwen 3 model available. The provided configuration uses `qwen3:4b`; set `OLLAMA_MODEL` to another installed model when needed.

Backend:

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend:

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

Open `http://localhost:5173`. The API and interactive documentation are available at `http://localhost:8000` and `http://localhost:8000/docs`.

Copy `.env.example` and `frontend/.env.example` when local overrides are required. The Ollama client disables Qwen's thinking mode, bounds generated tokens, and uses a compact repository context so the synchronous workflow returns reliably. Development CORS is restricted to `FRONTEND_ORIGIN` (`http://localhost:5173` by default).

The review agent uses deterministic test and diff checks by default so a task cannot be held up by an optional second LLM generation. Set `REVIEW_LLM_ENABLED=true` to enable LLM-based review as an additional decision step.

To publish an approved result, select **Publish approved branch** in the UI. The agent commits only its reported changed files and pushes `ai/<task-id>` to `origin`; it never pushes or merges the base branch. Git uses the credentials already configured on the machine and the optional `GIT_AUTHOR_NAME` / `GIT_AUTHOR_EMAIL` values from `.env`.

## Validation

```powershell
python -m pytest
ruff check .
mypy app
python -m compileall -q app tests
cd frontend
npm.cmd run lint
npm.cmd run typecheck
npm.cmd run build
```

The application never commits, pushes, or merges generated changes. All repository modifications remain inside `workspaces/<task_id>/repository`.
