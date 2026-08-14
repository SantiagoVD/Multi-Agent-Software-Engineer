"""Create a new text file inside a workspace."""

from pathlib import Path

from app.utils.file_utils import resolve_workspace_path


def create_file(
    workspace_root: Path,
    relative_path: str | Path,
    content: str,
    overwrite: bool = False,
) -> Path:
    path = resolve_workspace_path(workspace_root, relative_path)
    if path.exists() and not overwrite:
        raise FileExistsError(f"El archivo ya existe: {relative_path}")
    if path.is_dir():
        raise IsADirectoryError(f"La ruta es un directorio: {relative_path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path
