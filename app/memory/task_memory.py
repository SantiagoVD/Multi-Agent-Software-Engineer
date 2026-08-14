"""Bounded memory for one workflow task."""

from pydantic import BaseModel, Field

from app.models.development_result import DevelopmentResult
from app.models.repository_context import RepositoryContext
from app.models.review_result import ReviewResult
from app.models.task_status import TaskStatus
from app.models.test_result import TestResult
from app.models.tool_call import ToolCall


class TaskMemory(BaseModel):
    task_id: str
    task_description: str = ""
    repository_context: RepositoryContext | None = None
    relevant_files: dict[str, str] = Field(default_factory=dict)
    modified_files: list[str] = Field(default_factory=list)
    tool_calls: list[ToolCall] = Field(default_factory=list)
    development_results: list[DevelopmentResult] = Field(default_factory=list)
    test_results: list[TestResult] = Field(default_factory=list)
    review_results: list[ReviewResult] = Field(default_factory=list)
    iteration: int = 0
    status: TaskStatus = TaskStatus.RECEIVED

    def add_tool_call(self, call: ToolCall, limit: int = 50) -> None:
        self.tool_calls.append(call)
        del self.tool_calls[:-limit]

    def remember_file(self, path: str, content: str, limit: int = 20) -> None:
        self.relevant_files[path] = content
        while len(self.relevant_files) > limit:
            self.relevant_files.pop(next(iter(self.relevant_files)))

    def latest_test(self) -> TestResult | None:
        return self.test_results[-1] if self.test_results else None

    def latest_review(self) -> ReviewResult | None:
        return self.review_results[-1] if self.review_results else None
