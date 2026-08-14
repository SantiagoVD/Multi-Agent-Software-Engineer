"""List project files without reading their contents."""

from pathlib import Path

from app.utils.file_utils import (
    is_evidently_binary,
    is_ignored_directory,
    resolve_workspace_path,
)


def list_files(workspace_root: Path, recursive: bool = True) -> list[str]:
    root = resolve_workspace_path(workspace_root)
    if not root.is_dir():
        raise NotADirectoryError(f"El workspace no existe: {root}")
    iterator = root.rglob("*") if recursive else root.glob("*")
    files = [
        path.relative_to(root).as_posix()
        for path in iterator
        if path.is_file()
        and not any(is_ignored_directory(parent) for parent in path.relative_to(root).parents)
        and not is_evidently_binary(path)
    ]
    return sorted(files)
