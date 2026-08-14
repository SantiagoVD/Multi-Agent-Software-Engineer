"""Read a parseable Git commit history."""

from dataclasses import dataclass
from pathlib import Path

from app.utils.process_utils import require_success, run_git


@dataclass(frozen=True)
class GitCommit:
    hash: str
    author: str
    date: str
    message: str


def git_history(repository_path: Path, limit: int = 10) -> list[GitCommit]:
    if limit < 1:
        raise ValueError("El límite de commits debe ser positivo")
    output = require_success(
        run_git(repository_path, [
            "log", f"-{limit}",
            "--pretty=format:%H%x1f%an%x1f%aI%x1f%s%x1e",
        ]),
        f"consultar el historial de {repository_path}",
    )
    commits: list[GitCommit] = []
    for record in output.split("\x1e"):
        fields = record.strip("\n").split("\x1f")
        if len(fields) == 4 and fields[0]:
            commits.append(GitCommit(*fields))
    return commits
