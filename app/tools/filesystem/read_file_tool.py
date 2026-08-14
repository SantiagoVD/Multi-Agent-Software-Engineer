"""Read a bounded UTF-8 text file inside a workspace."""

from pathlib import Path

from app.core.constants import DEFAULT_FILE_ENCODING, MAX_FILE_SIZE_BYTES
from app.utils.file_utils import is_sensitive_file, resolve_workspace_path


def read_file(
    workspace_root: Path,
    relative_path: str | Path,
    encoding: str = DEFAULT_FILE_ENCODING,
) -> str:
    path = resolve_workspace_path(workspace_root, relative_path)
    if not path.is_file():
        raise FileNotFoundError(f"El archivo no existe: {relative_path}")
    if is_sensitive_file(path):
        raise PermissionError(f"Lectura bloqueada para archivo sensible: {relative_path}")
    if path.stat().st_size > MAX_FILE_SIZE_BYTES:
        raise ValueError(f"El archivo excede el límite permitido: {relative_path}")
    try:
        return path.read_text(encoding=encoding)
    except UnicodeDecodeError as exc:
        raise ValueError(f"El archivo no es texto {encoding}: {relative_path}") from exc
