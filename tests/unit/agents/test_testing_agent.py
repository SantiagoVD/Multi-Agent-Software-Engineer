from pathlib import Path

import pytest

from app.agents.testing_agent import TestingAgent
from app.memory.task_memory import TaskMemory
from app.models.repository_context import RepositoryContext
from app.models.task import Task


def test_testing_agent_reports_unavailable_tools(tmp_path: Path) -> None:
    task = Task(id="TASK-1", repository_url="local", task="run tests", branch="main")
    result = TestingAgent().run(task, tmp_path, TaskMemory(task_id="TASK-1"))
    if not result.available:
        pytest.skip("pytest no está instalado en este entorno")
    assert result.command


def test_testing_agent_skips_python_checks_for_javascript_repository(tmp_path: Path) -> None:
    task = Task(id="TASK-2", repository_url="local", task="run tests", branch="main")
    memory = TaskMemory(task_id="TASK-2")
    memory.repository_context = RepositoryContext(language="JavaScript/TypeScript")

    result = TestingAgent().run(task, tmp_path, memory)

    assert result.success
    assert result.skipped == 1
    assert result.command == "No fixed Python checks applicable"
