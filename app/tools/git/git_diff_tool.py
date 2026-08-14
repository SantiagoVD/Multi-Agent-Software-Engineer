"""Read current Git changes as text."""

from pathlib import Path

from app.utils.process_utils import require_success, run_git


def git_diff(repository_path: Path) -> str:
    repository_path = Path(repository_path).resolve()
    return require_success(
        run_git(repository_path, ["diff", "HEAD"]),
        f"consultar el diff de {repository_path}",
    )
