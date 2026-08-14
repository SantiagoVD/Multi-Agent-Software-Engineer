from pydantic import BaseModel, Field


class FileChange(BaseModel):
    path: str
    content: str
    create: bool = False


class DeveloperPlan(BaseModel):
    summary: str = ""
    changes: list[FileChange] = Field(default_factory=list)
