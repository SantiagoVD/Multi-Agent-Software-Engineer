from pydantic import BaseModel, Field


class DevelopmentResult(BaseModel):
    success: bool

    summary: str

    files_created: list[str] = Field(
        default_factory=list
    )

    files_modified: list[str] = Field(
        default_factory=list
    )

    files_deleted: list[str] = Field(
        default_factory=list
    )

    notes: list[str] = Field(
        default_factory=list
    )