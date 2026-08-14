"""Small helpers for invoking fixed external tools."""

import subprocess
from pathlib import Path


def run_git(repository: Path, arguments: list[str]) -> subprocess.CompletedProcess[str]:
    """Run Git in a validated repository without invoking a shell."""
    repository = Path(repository).resolve()
    if not repository.is_dir():
        raise FileNotFoundError(f"El repositorio no existe: {repository}")
    return subprocess.run(
        ["git", *arguments],
        cwd=repository,
        capture_output=True,
        text=True,
        check=False,
    )


def require_success(result: subprocess.CompletedProcess[str], operation: str) -> str:
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"{operation} falló: {detail}")
    return result.stdout
