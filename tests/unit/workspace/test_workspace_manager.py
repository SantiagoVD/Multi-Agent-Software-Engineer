from pathlib import Path
import subprocess

from app.workspace.workspace_manager import WorkspaceManager


def _source_repo(tmp_path: Path) -> Path:
    path = tmp_path / "source"
    path.mkdir()
    def git(*args: str) -> None:
        subprocess.run(["git", *args], cwd=path, check=True, capture_output=True, text=True)
    git("init", "-b", "main")
    git("config", "user.name", "Test User")
    git("config", "user.email", "test@example.com")
    (path / "app.py").write_text("print('ok')\n", encoding="utf-8")
    git("add", ".")
    git("commit", "-m", "initial")
    return path


def test_create_workspace_clones_and_creates_working_branch(tmp_path: Path) -> None:
    manager = WorkspaceManager()
    manager.workspace_root = tmp_path / "workspaces"
    workspace = manager.create_workspace("TASK-TEST", str(_source_repo(tmp_path)))
    assert workspace.base_branch == "main"
    assert workspace.working_branch == "ai/TASK-TEST"
    assert Path(workspace.path, "app.py").exists()
