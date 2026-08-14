"""Shared, security-conscious filesystem helpers."""

from pathlib import Path

from app.exceptions.tool_exceptions import PathSecurityError

IGNORED_DIRECTORIES = {
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache",
}

MAX_BINARY_SUFFIXES = {
    ".7z", ".avi", ".bin", ".bmp", ".class", ".dll", ".exe", ".gif",
    ".ico", ".jpeg", ".jpg", ".mov", ".mp3", ".mp4", ".pdf", ".png",
    ".pyc", ".so", ".tar", ".ttf", ".wav", ".webp", ".woff", ".zip",
}

SENSITIVE_FILENAMES = {
    ".env", ".env.local", ".env.production", ".env.development",
    "id_rsa", "id_ed25519", "credentials.json", "secrets.json",
}


def resolve_workspace_path(root: Path, relative_path: str | Path = ".") -> Path:
    """Resolve a path and ensure it remains inside ``root``."""
    resolved_root = Path(root).resolve()
    resolved = (resolved_root / Path(relative_path)).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise PathSecurityError(
            f"La ruta queda fuera del workspace autorizado: {relative_path}"
        ) from exc
    return resolved


def is_ignored_directory(path: Path) -> bool:
    return path.name in IGNORED_DIRECTORIES


def is_evidently_binary(path: Path) -> bool:
    return path.suffix.lower() in MAX_BINARY_SUFFIXES


def is_sensitive_file(path: Path) -> bool:
    return path.name in SENSITIVE_FILENAMES or path.name.endswith(".pem")
