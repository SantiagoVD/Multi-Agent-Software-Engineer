from app.models.task_status import TaskStatus
from app.orchestrator.workflow_guard import WorkflowError, WorkflowGuard


def test_workflow_guard_rejects_invalid_transition() -> None:
    guard = WorkflowGuard(2)
    try:
        guard.transition(TaskStatus.RECEIVED, TaskStatus.COMPLETED)
    except WorkflowError:
        pass
    else:
        raise AssertionError("La transición inválida no fue rechazada")
