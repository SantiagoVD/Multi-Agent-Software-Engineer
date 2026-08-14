"""Create and switch to a local Git branch."""

from pathlib import Path

from app.utils.process_utils import require_success, run_git


def create_branch(repository_path: Path, branch_name: str) -> str:
    """Create ``branch_name`` and switch to it."""
    repository_path = Path(repository_path).resolve()
    require_success(
        run_git(repository_path, ["rev-parse", "--is-inside-work-tree"]),
        f"validar el repositorio {repository_path}",
    )
    if not branch_name or branch_name.startswith("-"):
        raise ValueError("El nombre de la branch no es válido")
    result = run_git(repository_path, ["switch", "-c", branch_name])
    require_success(result, f"crear la branch {branch_name}")
    return require_success(
        run_git(repository_path, ["branch", "--show-current"]),
        "consultar la branch activa",
    ).strip()
