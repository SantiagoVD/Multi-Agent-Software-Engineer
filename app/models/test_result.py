from pydantic import BaseModel, Field


class TestIssue(BaseModel):
    __test__ = False
    test_name: str | None = None
    message: str
    file: str | None = None


class TestResult(BaseModel):
    __test__ = False
    success: bool

    available: bool = True

    command: str

    passed: int = 0

    failed: int = 0

    skipped: int = 0

    exit_code: int | None = None

    timed_out: bool = False

    issues: list[TestIssue] = Field(
        default_factory=list
    )

    raw_output: str | None = None
