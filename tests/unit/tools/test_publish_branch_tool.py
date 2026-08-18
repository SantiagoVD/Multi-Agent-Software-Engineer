import subprocess
from pathlib import Path

from app.tools.git.publish_branch_tool import publish_branch


def _git(path: Path, *arguments: str) -> None:
    subprocess.run(["git", *arguments], cwd=path, check=True, capture_output=True, text=True)


def test_publish_branch_commits_agent_files_to_origin(tmp_path: Path) -> None:
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True, text=True)
    repository = tmp_path / "repository"
    repository.mkdir()
    _git(repository, "init", "-b", "main")
    _git(repository, "config", "user.name", "Test User")
    _git(repository, "config", "user.email", "test@example.com")
    (repository / "sample.py").write_text("VALUE = 1\n", encoding="utf-8")
    _git(repository, "add", "sample.py")
    _git(repository, "commit", "-m", "initial")
    _git(repository, "remote", "add", "origin", str(remote))
    _git(repository, "push", "-u", "origin", "main")
    _git(repository, "switch", "-c", "ai/TASK-TEST")
    (repository / "sample.py").write_text("VALUE = 2\n", encoding="utf-8")

    result = publish_branch(repository, "ai/TASK-TEST", ["sample.py"], "update sample")

    assert result.requested
    assert result.published
    assert result.branch == "ai/TASK-TEST"
    assert result.commit
    remote_branches = subprocess.run(
        ["git", "--git-dir", str(remote), "branch", "--list", "ai/TASK-TEST"],
        check=True, capture_output=True, text=True,
    ).stdout
    assert "ai/TASK-TEST" in remote_branches


def test_publish_branch_requires_agent_changes(tmp_path: Path) -> None:
    result = publish_branch(tmp_path, "ai/TASK-EMPTY", [], "no changes")

    assert result.requested
    assert not result.published
