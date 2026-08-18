"""Run Ruff without allowing automatic code modifications."""

import importlib.util
import subprocess
import sys
from pathlib import Path

from app.core.config import settings
from app.models.command_result import CommandResult


def run_linter(repository_path: Path) -> CommandResult:
    command = [sys.executable, "-m", "ruff", "check", "."]
    command_text = " ".join(command)
    if importlib.util.find_spec("ruff") is None:
        return CommandResult(
            success=False, available=False, command=command_text,
            issues=["Ruff no está disponible en el entorno"],
        )
    try:
        result = subprocess.run(
            command, cwd=Path(repository_path).resolve(), capture_output=True,
            text=True, timeout=settings.command_timeout_seconds, check=False,
        )
        output = "\n".join(part for part in (result.stdout, result.stderr) if part)
        return CommandResult(
            success=result.returncode == 0, command=command_text,
            exit_code=result.returncode, raw_output=output,
            issues=[] if result.returncode == 0 else [output[-2000:] or "Ruff encontró errores"],
        )
    except subprocess.TimeoutExpired as exc:
        return CommandResult(
            success=False, command=command_text, timed_out=True,
            raw_output=str(exc), issues=["Ruff excedió el timeout"],
        )
    except OSError as exc:
        return CommandResult(
            success=False, command=command_text, raw_output=str(exc),
            issues=[f"No fue posible ejecutar Ruff: {exc}"],
        )
