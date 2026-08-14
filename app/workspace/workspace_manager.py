from pathlib import Path

from app.core.config import settings
from app.core.constants import AI_BRANCH_PREFIX, DEFAULT_BRANCH
from app.tools.git.clone_repository_tool import clone_repository
from app.tools.git.create_branch_tool import create_branch
from app.utils.file_utils import resolve_workspace_path
from app.utils.process_utils import require_success, run_git
from app.workspace.workspace import Workspace


class WorkspaceManager:
    def __init__(self) -> None:
        self.workspace_root = Path(settings.workspace_root).resolve()

    def get_task_directory(self, task_id: str) -> Path:
        return resolve_workspace_path(self.workspace_root, task_id)

    def ensure_task_directory(self, task_id: str) -> Path:
        task_directory = self.get_task_directory(task_id)
        task_directory.mkdir(parents=True, exist_ok=True)
        return task_directory

    def create_workspace(
        self,
        task_id: str,
        repository_url: str,
        base_branch: str | None = None,
    ) -> Workspace:
        """Create an isolated clone and its local AI working branch."""
        task_directory = self.ensure_task_directory(task_id)
        repository_path = task_directory / "repository"
        cloned_path = clone_repository(repository_url, repository_path)

        detected_branch = require_success(
            run_git(cloned_path, ["branch", "--show-current"]),
            "determinar la branch base",
        ).strip()
        selected_base = base_branch or detected_branch or DEFAULT_BRANCH
        if selected_base != detected_branch:
            require_success(
                run_git(cloned_path, ["switch", selected_base]),
                f"cambiar a la branch base {selected_base}",
            )

        working_branch = f"{AI_BRANCH_PREFIX}/{task_id}"
        active_branch = create_branch(cloned_path, working_branch)
        return Workspace(
            task_id=task_id,
            repository_url=repository_url,
            path=str(cloned_path),
            base_branch=selected_base,
            working_branch=active_branch,
        )
