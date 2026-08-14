"""Mutable state carried through one workflow."""

from pydantic import BaseModel, Field

from app.memory.task_memory import TaskMemory
from app.models.development_result import DevelopmentResult
from app.models.repository_context import RepositoryContext
from app.models.review_result import ReviewResult
from app.models.task import Task
from app.models.task_status import TaskStatus
from app.models.test_result import TestResult
from app.workspace.workspace import Workspace


class WorkflowState(BaseModel):
    task: Task
    status: TaskStatus = TaskStatus.RECEIVED
    workspace: Workspace | None = None
    memory: TaskMemory | None = None
    repository_context: RepositoryContext | None = None
    development_result: DevelopmentResult | None = None
    test_result: TestResult | None = None
    review_result: ReviewResult | None = None
    iterations: int = 0
    errors: list[str] = Field(default_factory=list)
