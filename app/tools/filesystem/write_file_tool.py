"""Overwrite a text file inside a workspace."""

from pathlib import Path

from app.utils.file_utils import resolve_workspace_path


def write_file(
    workspace_root: Path,
    relative_path: str | Path,
    content: str,
) -> Path:
    path = resolve_workspace_path(workspace_root, relative_path)
    if path.is_dir():
        raise IsADirectoryError(f"La ruta es un directorio: {relative_path}")
    path.write_text(content, encoding="utf-8")
    return path
