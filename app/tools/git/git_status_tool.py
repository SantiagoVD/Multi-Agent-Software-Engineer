"""Read the current Git status."""

from dataclasses import dataclass
from pathlib import Path

from app.utils.process_utils import require_success, run_git


@dataclass(frozen=True)
class GitStatus:
    branch: str
    has_changes: bool
    staged: bool
    unstaged: bool
    untracked: bool
    raw: str = ""


def git_status(repository_path: Path) -> GitStatus:
    repository_path = Path(repository_path).resolve()
    branch = require_success(
        run_git(repository_path, ["branch", "--show-current"]),
        "consultar la branch activa",
    ).strip()
    raw = require_success(
        run_git(repository_path, ["status", "--porcelain=v1"]),
        f"consultar el status de {repository_path}",
    )
    lines = [line for line in raw.splitlines() if line]
    return GitStatus(
        branch=branch,
        has_changes=bool(lines),
        staged=any(line[0] not in " ?" for line in lines),
        unstaged=any(len(line) > 1 and line[1] not in " ?" for line in lines),
        untracked=any(line.startswith("??") for line in lines),
        raw=raw,
    )
