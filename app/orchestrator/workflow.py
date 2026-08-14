"""Pure helpers for workflow state changes."""

from app.models.task_status import TaskStatus
from app.orchestrator.workflow_guard import WorkflowGuard
from app.orchestrator.workflow_state import WorkflowState


def set_status(state: WorkflowState, status: TaskStatus, guard: WorkflowGuard) -> None:
    state.status = guard.transition(state.status, status)
    if state.memory:
        state.memory.status = status
