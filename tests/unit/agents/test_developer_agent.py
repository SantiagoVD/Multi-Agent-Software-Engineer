import json
from pathlib import Path

from app.agents.developer_agent import DeveloperAgent
from app.llm.llm_provider import LLMProvider
from app.llm.llm_response import LLMResponse
from app.memory.task_memory import TaskMemory
from app.models.task import Task


class FakeProvider(LLMProvider):
    def generate(self, system_prompt: str, user_prompt: str, *, temperature: float = 0.2, json_mode: bool = False) -> LLMResponse:
        return LLMResponse(content=json.dumps({"summary": "updated", "changes": [{"path": "new.py", "content": "VALUE = 1", "create": True}]}))


def test_developer_agent_applies_structured_plan(tmp_path: Path) -> None:
    task = Task(id="TASK-1", repository_url="local", task="add file", branch="main")
    result = DeveloperAgent(FakeProvider()).run(task, tmp_path, TaskMemory(task_id="TASK-1"))
    assert result.success
    assert (tmp_path / "new.py").exists()


def test_developer_agent_updates_existing_file_when_plan_marks_it_as_new(tmp_path: Path) -> None:
    (tmp_path / "new.py").write_text("VALUE = 0", encoding="utf-8")
    task = Task(id="TASK-2", repository_url="local", task="update file", branch="main")

    result = DeveloperAgent(FakeProvider()).run(task, tmp_path, TaskMemory(task_id="TASK-2"))

    assert result.success
    assert result.files_modified == ["new.py"]
    assert (tmp_path / "new.py").read_text(encoding="utf-8") == "VALUE = 1"
