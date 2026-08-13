from enum import Enum

from pydantic import BaseModel, Field


class ReviewStatus(str, Enum):
    APPROVED = "approved"
    CHANGES_REQUIRED = "changes_required"


class IssueSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ReviewIssue(BaseModel):
    severity: IssueSeverity
    description: str
    file: str | None = None
    line: int | None = None
    recommendation: str | None = None


class ReviewResult(BaseModel):
    status: ReviewStatus

    summary: str

    issues: list[ReviewIssue] = Field(
        default_factory=list
    )