from pydantic import BaseModel, Field

from app.models.branch_publication import BranchPublication
from app.models.review_result import ReviewResult
from app.models.task_status import TaskStatus
from app.models.test_result import TestResult


class FinalResult(BaseModel):
    task_id: str

    status: TaskStatus

    success: bool

    summary: str

    files_modified: list[str] = Field(
        default_factory=list
    )

    test_result: TestResult | None = None

    review_result: ReviewResult | None = None

    publication: BranchPublication | None = None

    iterations: int = 0
