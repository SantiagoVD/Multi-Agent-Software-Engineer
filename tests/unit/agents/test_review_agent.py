from pathlib import Path

from app.agents.review_agent import ReviewAgent
from app.memory.task_memory import TaskMemory
from app.models.task import Task
from app.models.test_result import TestResult


def test_review_agent_requires_changes_when_tests_fail(tmp_path: Path) -> None:
    task = Task(id="TASK-1", repository_url="local", task="fix", branch="main")
    result = ReviewAgent().run(task, tmp_path, TaskMemory(task_id="TASK-1"), tests=TestResult(success=False, command="pytest"))
    assert result.status.value == "changes_required"
