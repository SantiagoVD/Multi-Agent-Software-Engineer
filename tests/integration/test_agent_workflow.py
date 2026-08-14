import subprocess
from pathlib import Path

from app.memory.in_memory_store import InMemoryStore
from app.models.development_result import DevelopmentResult
from app.models.repository_context import RepositoryContext
from app.models.review_result import ReviewResult, ReviewStatus
from app.models.task import TaskRequest
from app.models.test_result import TestResult
from app.orchestrator.orchestrator import Orchestrator
from app.workspace.workspace_manager import WorkspaceManager


class FakeRepositoryAgent:
    def run(self, task, repository_path, memory):
        return RepositoryContext(summary="fake context")


class FakeDeveloperAgent:
    def run(self, task, repository_path, memory):
        result = DevelopmentResult(success=True, summary="no-op fake change")
        memory.development_results.append(result)
        return result


class FakeTestingAgent:
    def run(self, task, repository_path, memory):
        result = TestResult(success=True, command="fake pytest", passed=1)
        memory.test_results.append(result)
        return result


class FakeReviewAgent:
    def run(self, *args, **kwargs):
        return ReviewResult(status=ReviewStatus.APPROVED, summary="approved")


def test_task_request_reaches_final_result(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    def git(*args: str) -> None:
        subprocess.run(["git", *args], cwd=source, check=True, capture_output=True, text=True)
    git("init", "-b", "main")
    git("config", "user.name", "E2E")
    git("config", "user.email", "e2e@example.com")
    (source / "README.md").write_text("test\n", encoding="utf-8")
    git("add", ".")
    git("commit", "-m", "initial")
    manager = WorkspaceManager()
    manager.workspace_root = tmp_path / "workspaces"
    result = Orchestrator(
        workspace_manager=manager,
        memory_store=InMemoryStore(),
        repository_agent=FakeRepositoryAgent(),
        developer_agent=FakeDeveloperAgent(),
        testing_agent=FakeTestingAgent(),
        review_agent=FakeReviewAgent(),
    ).run(TaskRequest(repository_url=str(source), task="inspect repository"))
    assert result.success
    assert result.status.value == "completed"
