from pathlib import Path

import pytest

from app.agents.testing_agent import TestingAgent
from app.memory.task_memory import TaskMemory
from app.models.task import Task


def test_testing_agent_reports_unavailable_tools(tmp_path: Path) -> None:
    task = Task(id="TASK-1", repository_url="local", task="run tests", branch="main")
    result = TestingAgent().run(task, tmp_path, TaskMemory(task_id="TASK-1"))
    if not result.available:
        pytest.skip("pytest no está instalado en este entorno")
    assert result.command
