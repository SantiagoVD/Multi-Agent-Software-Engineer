# Multi-Agent Software Engineer

Autonomous AI engineering team for real software repositories. The FastAPI backend creates an isolated workspace and coordinates repository, developer, testing, and review agents. The React frontend visualizes the synchronous workflow and its final result.

## Local development

Prerequisites: Python 3.13+, Git, Node.js 22+, and Ollama with `qwen3:8b` available.

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

Copy `.env.example` and `frontend/.env.example` when local overrides are required. Development CORS is restricted to `FRONTEND_ORIGIN` (`http://localhost:5173` by default).

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
