from pydantic import BaseModel, Field


class TestIssue(BaseModel):
    test_name: str | None = None
    message: str
    file: str | None = None


class TestResult(BaseModel):
    success: bool

    command: str

    passed: int = 0

    failed: int = 0

    skipped: int = 0

    issues: list[TestIssue] = Field(
        default_factory=list
    )

    raw_output: str | None = None