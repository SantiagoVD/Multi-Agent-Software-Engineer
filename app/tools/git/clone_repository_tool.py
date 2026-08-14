"""Git repository cloning tool."""

import subprocess
from pathlib import Path


def clone_repository(
    repository_url: str,
    destination: Path
) -> Path:
    """Clone ``repository_url`` into a new destination directory."""

    destination = Path(destination).resolve()

    if destination.exists():
        raise FileExistsError(
            f"El destino ya existe: {destination}"
        )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    result = subprocess.run(
        [
            "git",
            "clone",
            repository_url,
            str(destination),
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"No se pudo clonar el repositorio:\n{result.stderr}"
        )

    return destination
