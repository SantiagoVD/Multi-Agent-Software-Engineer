from pathlib import Path

from app.core.config import settings
from app.workspace.workspace import Workspace


class WorkspaceManager:

    def __init__(self) -> None:
        self.workspace_root = Path(settings.workspace_root).resolve()

    def get_task_directory(self, task_id: str) -> Path:
        return self.workspace_root / task_id

    def ensure_task_directory(self, task_id: str) -> Path:
        task_directory = self.get_task_directory(task_id)

        task_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        return task_directory