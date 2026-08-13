from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    tool_name: str

    arguments: dict[str, Any] = Field(
        default_factory=dict
    )

    success: bool

    result_summary: str | None = None

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )