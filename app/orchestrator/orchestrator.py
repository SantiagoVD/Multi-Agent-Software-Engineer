"""Coordinates infrastructure and agents without owning tool logic."""

from pathlib import Path
from uuid import uuid4

from app.agents.developer_agent import DeveloperAgent
from app.agents.repository_agent import RepositoryAgent
from app.agents.review_agent import ReviewAgent
from app.agents.testing_agent import TestingAgent
from app.core.config import settings
from app.llm.llm_provider import LLMProvider
from app.memory.in_memory_store import InMemoryStore
from app.memory.task_memory import TaskMemory
from app.models.final_result import FinalResult
from app.models.review_result import ReviewStatus
from app.models.task import Task, TaskRequest
from app.models.task_status import TaskStatus
from app.orchestrator.workflow import set_status
from app.orchestrator.workflow_guard import WorkflowError, WorkflowGuard
from app.orchestrator.workflow_state import WorkflowState
from app.workspace.workspace_manager import WorkspaceManager


class Orchestrator:
    def __init__(
        self,
        provider: LLMProvider | None = None,
        workspace_manager: WorkspaceManager | None = None,
        memory_store: InMemoryStore | None = None,
        repository_agent: RepositoryAgent | None = None,
        developer_agent: DeveloperAgent | None = None,
        testing_agent: TestingAgent | None = None,
        review_agent: ReviewAgent | None = None,
    ) -> None:
        self.provider = provider
        self.workspace_manager = workspace_manager or WorkspaceManager()
        self.memory_store = memory_store or InMemoryStore()
        self.repository_agent = repository_agent or RepositoryAgent(provider)
        self.developer_agent = developer_agent or DeveloperAgent(provider)
        self.testing_agent = testing_agent or TestingAgent(provider)
        self.review_agent = review_agent or ReviewAgent(provider)
        self.guard = WorkflowGuard(settings.max_workflow_iterations)

    def run(self, request: TaskRequest | Task) -> FinalResult:
        task = request if isinstance(request, Task) else Task(
            id=f"TASK-{uuid4().hex[:8].upper()}",
            repository_url=request.repository_url,
            task=request.task,
            branch=request.branch or "main",
        )
        memory = TaskMemory(task_id=task.id, task_description=task.task)
        self.memory_store.save(memory)
        state = WorkflowState(task=task, memory=memory)
        try:
            set_status(state, TaskStatus.CLONING_REPOSITORY, self.guard)
            state.workspace = self.workspace_manager.create_workspace(task.id, task.repository_url, task.branch)
            set_status(state, TaskStatus.ANALYZING_REPOSITORY, self.guard)
            repository_path = Path(state.workspace.path)
            state.repository_context = self.repository_agent.run(task, repository_path, memory)
            for iteration in range(settings.max_workflow_iterations):
                state.iterations = iteration + 1
                memory.iteration = state.iterations
                set_status(state, TaskStatus.DEVELOPING, self.guard)
                state.development_result = self.developer_agent.run(task, repository_path, memory)
                if not state.development_result.success:
                    raise WorkflowError(state.development_result.summary)
                set_status(state, TaskStatus.TESTING, self.guard)
                state.test_result = self.testing_agent.run(task, repository_path, memory)
                if not state.test_result.success:
                    if iteration + 1 >= settings.max_workflow_iterations:
                        raise WorkflowError("Los tests no pasan y se agotaron las iteraciones")
                    continue
                set_status(state, TaskStatus.REVIEWING, self.guard)
                state.review_result = self.review_agent.run(
                    task, repository_path, memory, state.development_result,
                    state.test_result, state.repository_context,
                )
                if state.review_result.status == ReviewStatus.APPROVED:
                    set_status(state, TaskStatus.COMPLETED, self.guard)
                    return FinalResult(
                        task_id=task.id, status=state.status, success=True,
                        summary="Tarea completada y aprobada.",
                        files_modified=memory.modified_files,
                        test_result=state.test_result, review_result=state.review_result,
                        iterations=state.iterations,
                    )
                if iteration + 1 >= settings.max_workflow_iterations:
                    raise WorkflowError("La revisión requiere cambios y se agotaron las iteraciones")
            raise WorkflowError("El workflow terminó sin resultado")
        except (OSError, RuntimeError, ValueError, WorkflowError) as exc:
            state.status = TaskStatus.FAILED
            state.errors.append(str(exc))
            return FinalResult(
                task_id=task.id, status=TaskStatus.FAILED, success=False,
                summary=str(exc), files_modified=memory.modified_files,
                test_result=state.test_result, review_result=state.review_result,
                iterations=state.iterations,
            )
