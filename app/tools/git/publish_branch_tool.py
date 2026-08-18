"""Commit approved agent changes and publish only its isolated branch."""

from pathlib import Path

from app.core.config import settings
from app.models.branch_publication import BranchPublication
from app.utils.process_utils import require_success, run_git


def publish_branch(
    repository_path: Path,
    branch: str,
    files: list[str],
    task_description: str,
) -> BranchPublication:
    """Create one local commit from agent files and push ``branch`` to origin."""
    repository_path = Path(repository_path).resolve()
    if not branch or branch.startswith("-"):
        return BranchPublication(requested=True, message="La rama a publicar no es vÃ¡lida.")
    if not files:
        return BranchPublication(
            requested=True, branch=branch,
            message="No hay archivos modificados por el agente para publicar.",
        )
    try:
        require_success(
            run_git(repository_path, ["config", "user.name", settings.git_author_name]),
            "configurar la identidad Git local",
        )
        require_success(
            run_git(repository_path, ["config", "user.email", settings.git_author_email]),
            "configurar el correo Git local",
        )
        require_success(
            run_git(repository_path, ["add", "--", *files]),
            "preparar los cambios del agente",
        )
        staged = run_git(repository_path, ["diff", "--cached", "--quiet"])
        if staged.returncode == 0:
            return BranchPublication(
                requested=True, branch=branch,
                message="Los archivos reportados no contienen cambios para publicar.",
            )
        if staged.returncode != 1:
            require_success(staged, "validar los cambios preparados")
        subject = " ".join(task_description.split())[:72] or "agent changes"
        require_success(
            run_git(repository_path, ["commit", "-m", f"agent: {subject}"]),
            "crear el commit del agente",
        )
        commit = require_success(
            run_git(repository_path, ["rev-parse", "HEAD"]),
            "consultar el commit creado",
        ).strip()
        require_success(
            run_git(repository_path, ["push", "--set-upstream", "origin", branch]),
            "publicar la rama del agente",
        )
        return BranchPublication(
            requested=True, published=True, branch=branch, commit=commit,
            message=f"Rama {branch} publicada en origin.",
        )
    except (OSError, RuntimeError, ValueError) as exc:
        return BranchPublication(
            requested=True, branch=branch,
            message=f"No se pudo publicar la rama: {exc}",
        )
