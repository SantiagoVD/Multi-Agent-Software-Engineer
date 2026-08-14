from pathlib import Path
import subprocess

from app.tools.git.create_branch_tool import create_branch
from app.tools.git.git_diff_tool import git_diff
from app.tools.git.git_history_tool import git_history
from app.tools.git.git_status_tool import git_status


def _git(path: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=path, check=True, capture_output=True, text=True)


def _repo(tmp_path: Path) -> Path:
    path = tmp_path / "repo"
    path.mkdir()
    _git(path, "init", "-b", "main")
    _git(path, "config", "user.name", "Test User")
    _git(path, "config", "user.email", "test@example.com")
    (path / "README.md").write_text("hello\n", encoding="utf-8")
    _git(path, "add", "README.md")
    _git(path, "commit", "-m", "initial commit")
    return path


def test_branch_status_diff_and_history(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    assert create_branch(repo, "ai/TASK-TEST") == "ai/TASK-TEST"
    clean = git_status(repo)
    assert clean.branch == "ai/TASK-TEST"
    assert not clean.has_changes

    (repo / "README.md").write_text("changed\n", encoding="utf-8")
    dirty = git_status(repo)
    assert dirty.has_changes and dirty.unstaged
    assert "changed" in git_diff(repo)
    history = git_history(repo, limit=5)
    assert len(history) == 1
    assert history[0].message == "initial commit"
