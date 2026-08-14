from pathlib import Path

from app.agents.repository_agent import RepositoryAgent
from app.memory.task_memory import TaskMemory
from app.models.task import Task


def test_repository_agent_uses_read_only_analysis_tools(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text("print('ok')\n", encoding="utf-8")
    task = Task(id="TASK-1", repository_url="local", task="inspect python", branch="main")
    context = RepositoryAgent().run(task, tmp_path, TaskMemory(task_id="TASK-1"))
    assert context.language == "Python"
    assert "main.py" in context.relevant_files
