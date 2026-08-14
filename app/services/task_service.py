"""Application service for task execution."""

from app.models.final_result import FinalResult
from app.models.task import TaskRequest
from app.orchestrator.orchestrator import Orchestrator


class TaskService:
    def __init__(self, orchestrator: Orchestrator | None = None) -> None:
        self.orchestrator = orchestrator or Orchestrator()

    def execute(self, request: TaskRequest) -> FinalResult:
        return self.orchestrator.run(request)
