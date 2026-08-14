from pathlib import Path
import subprocess

from app.tools.filesystem.list_files_tool import list_files
from app.tools.filesystem.read_file_tool import read_file
from app.tools.filesystem.search_code_tool import search_code
from app.tools.git.git_status_tool import git_status
from app.workspace.workspace_manager import WorkspaceManager


def test_infrastructure_layers_work_together(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    def git(*args: str) -> None:
        subprocess.run(["git", *args], cwd=source, check=True, capture_output=True, text=True)
    git("init", "-b", "main")
    git("config", "user.name", "Integration Test")
    git("config", "user.email", "integration@example.com")
    (source / "module.py").write_text("VALUE = 42\n", encoding="utf-8")
    git("add", ".")
    git("commit", "-m", "initial")

    manager = WorkspaceManager()
    manager.workspace_root = tmp_path / "workspaces"
    workspace = manager.create_workspace("TASK-INTEGRATION", str(source))
    repository = Path(workspace.path)
    assert "module.py" in list_files(repository)
    assert "VALUE = 42" in read_file(repository, "module.py")
    assert search_code(repository, "VALUE")[0].line == 1
    assert git_status(repository).branch == "ai/TASK-INTEGRATION"
