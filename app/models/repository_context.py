from pydantic import BaseModel, Field


class RepositoryContext(BaseModel):
    language: str | None = None

    framework: str | None = None

    architecture: str | None = None

    relevant_files: list[str] = Field(
        default_factory=list
    )

    test_files: list[str] = Field(
        default_factory=list
    )

    dependency_files: list[str] = Field(
        default_factory=list
    )

    summary: str = ""