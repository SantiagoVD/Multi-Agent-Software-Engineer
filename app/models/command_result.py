from pydantic import BaseModel, Field


class CommandResult(BaseModel):
    """Safe execution result for a fixed application command."""

    success: bool
    command: str
    exit_code: int | None = None
    available: bool = True
    timed_out: bool = False
    raw_output: str = ""
    issues: list[str] = Field(default_factory=list)
