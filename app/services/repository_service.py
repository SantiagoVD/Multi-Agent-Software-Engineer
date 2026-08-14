"""Repository-facing service kept deliberately small for V1."""

from pathlib import Path

from app.tools.git.git_status_tool import GitStatus, git_status


class RepositoryService:
    def status(self, repository_path: Path) -> GitStatus:
        return git_status(repository_path)
