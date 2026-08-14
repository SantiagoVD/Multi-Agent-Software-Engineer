"""Workflow transition and iteration safety checks."""

from typing import ClassVar

from app.models.task_status import TaskStatus


class WorkflowError(RuntimeError):
    pass


class WorkflowGuard:
    transitions: ClassVar[dict[TaskStatus, set[TaskStatus]]] = {
        TaskStatus.RECEIVED: {TaskStatus.CLONING_REPOSITORY, TaskStatus.FAILED},
        TaskStatus.CLONING_REPOSITORY: {TaskStatus.ANALYZING_REPOSITORY, TaskStatus.FAILED},
        TaskStatus.ANALYZING_REPOSITORY: {TaskStatus.DEVELOPING, TaskStatus.FAILED},
        TaskStatus.DEVELOPING: {TaskStatus.TESTING, TaskStatus.FAILED},
        TaskStatus.TESTING: {TaskStatus.DEVELOPING, TaskStatus.REVIEWING, TaskStatus.FAILED},
        TaskStatus.REVIEWING: {TaskStatus.DEVELOPING, TaskStatus.COMPLETED, TaskStatus.FAILED},
        TaskStatus.COMPLETED: set(),
        TaskStatus.FAILED: set(),
    }

    def __init__(self, max_iterations: int) -> None:
        self.max_iterations = max_iterations

    def transition(self, current: TaskStatus, target: TaskStatus) -> TaskStatus:
        if target not in self.transitions.get(current, set()):
            raise WorkflowError(f"Transición inválida: {current.value} -> {target.value}")
        return target

    def check_iteration(self, iteration: int) -> None:
        if iteration >= self.max_iterations:
            raise WorkflowError("Se alcanzó el máximo de iteraciones del workflow")

    def require_workspace(self, workspace: object | None) -> None:
        if workspace is None:
            raise WorkflowError("No existe un workspace válido")
