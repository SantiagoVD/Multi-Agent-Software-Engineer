from pydantic import BaseModel, Field


class TaskRequest(BaseModel):
    repository_url: str = Field(
        ...,
        description="URL del repositorio Git que será analizado."
    )

    task: str = Field(
        ...,
        min_length=5,
        description="Descripción de la tarea de desarrollo."
    )

    branch: str | None = Field(
        default=None,
        description="Branch base desde el cual trabajar."
    )


class Task(BaseModel):
    id: str
    repository_url: str
    task: str
    branch: str