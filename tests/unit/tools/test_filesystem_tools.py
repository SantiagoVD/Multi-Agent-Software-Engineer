from pathlib import Path

import pytest

from app.exceptions.tool_exceptions import PathSecurityError
from app.tools.filesystem.create_file_tool import create_file
from app.tools.filesystem.list_files_tool import list_files
from app.tools.filesystem.read_file_tool import read_file
from app.tools.filesystem.search_code_tool import search_code
from app.tools.filesystem.write_file_tool import write_file


def test_filesystem_tools_and_security(tmp_path: Path) -> None:
    create_file(tmp_path, "src/example.py", "needle = 1\n")
    assert "src/example.py" in list_files(tmp_path)
    assert read_file(tmp_path, "src/example.py") == "needle = 1\n"
    write_file(tmp_path, "src/example.py", "needle = 2\n")
    assert read_file(tmp_path, "src/example.py") == "needle = 2\n"
    matches = search_code(tmp_path, "needle")
    assert matches[0].file == "src/example.py"
    assert matches[0].line == 1
    with pytest.raises(FileExistsError):
        create_file(tmp_path, "src/example.py", "no overwrite")
    with pytest.raises(PathSecurityError):
        read_file(tmp_path, "../outside.txt")
    with pytest.raises(PathSecurityError):
        write_file(tmp_path, str(tmp_path.parent / "outside.txt"), "blocked")


def test_large_file_is_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import app.tools.filesystem.read_file_tool as reader
    monkeypatch.setattr(reader, "MAX_FILE_SIZE_BYTES", 2)
    create_file(tmp_path, "large.txt", "123")
    with pytest.raises(ValueError):
        read_file(tmp_path, "large.txt")
