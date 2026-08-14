"""Conventional text search within a workspace."""

from dataclasses import dataclass
from pathlib import Path

from app.core.constants import MAX_FILE_SIZE_BYTES, MAX_FILES_PER_ANALYSIS
from app.utils.file_utils import (
    is_evidently_binary,
    is_ignored_directory,
    is_sensitive_file,
    resolve_workspace_path,
)


@dataclass(frozen=True)
class SearchMatch:
    file: str
    line: int
    snippet: str


def search_code(
    workspace_root: Path,
    query: str,
    max_results: int = MAX_FILES_PER_ANALYSIS,
) -> list[SearchMatch]:
    if not query:
        raise ValueError("La búsqueda no puede estar vacía")
    if max_results < 1:
        raise ValueError("max_results debe ser positivo")
    root = resolve_workspace_path(workspace_root)
    matches: list[SearchMatch] = []
    for path in sorted(root.rglob("*")):
        if len(matches) >= max_results:
            break
        if (
            not path.is_file()
            or is_evidently_binary(path)
            or is_sensitive_file(path)
            or path.stat().st_size > MAX_FILE_SIZE_BYTES
            or any(is_ignored_directory(parent) for parent in path.relative_to(root).parents)
        ):
            continue
        try:
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if query.casefold() in line.casefold():
                    matches.append(SearchMatch(path.relative_to(root).as_posix(), number, line.strip()))
                    if len(matches) >= max_results:
                        break
        except UnicodeDecodeError:
            continue
    return matches
