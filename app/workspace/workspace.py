from pydantic import BaseModel


class Workspace(BaseModel):
    task_id: str
    repository_url: str
    path: str
    base_branch: str
    working_branch: str