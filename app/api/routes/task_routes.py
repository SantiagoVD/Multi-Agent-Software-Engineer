from fastapi import APIRouter, Depends

from app.api.dependencies import get_orchestrator
from app.models.final_result import FinalResult
from app.models.task import TaskRequest
from app.orchestrator.orchestrator import Orchestrator

router = APIRouter()


@router.post("/tasks", response_model=FinalResult)
def create_task(request: TaskRequest, orchestrator: Orchestrator = Depends(get_orchestrator)) -> FinalResult:  # noqa: B008
    return orchestrator.run(request)
