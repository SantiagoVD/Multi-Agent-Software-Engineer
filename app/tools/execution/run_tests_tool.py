"""Run the project's Python tests using a fixed pytest command."""

import re
import subprocess
import sys
from pathlib import Path

from app.core.config import settings
from app.models.test_result import TestIssue, TestResult


def _output(result: subprocess.CompletedProcess[str]) -> str:
    return "\n".join(part for part in (result.stdout, result.stderr) if part)


def run_tests(repository_path: Path) -> TestResult:
    path = Path(repository_path).resolve()
    command = [sys.executable, "-m", "pytest", "-q"]
    command_text = " ".join(command)
    try:
        result = subprocess.run(
            command, cwd=path, capture_output=True, text=True,
            timeout=settings.test_timeout_seconds, check=False,
        )
        output = _output(result)
        unavailable = "No module named pytest" in output
        passed = _count(output, r"(\d+) passed")
        failed = _count(output, r"(\d+) failed")
        skipped = _count(output, r"(\d+) skipped")
        return TestResult(
            success=result.returncode == 0 and not unavailable,
            available=not unavailable,
            command=command_text,
            passed=passed,
            failed=failed,
            skipped=skipped,
            exit_code=result.returncode,
            raw_output=output,
            issues=[] if result.returncode == 0 else [TestIssue(message=output[-2000:] or "pytest falló")],
        )
    except subprocess.TimeoutExpired as exc:
        output = "\n".join(str(part) for part in (exc.stdout, exc.stderr) if part)
        return TestResult(
            success=False, command=command_text, timed_out=True,
            raw_output=output, issues=[TestIssue(message="pytest excedió el timeout")],
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return TestResult(
            success=False, command=command_text, raw_output=str(exc),
            issues=[TestIssue(message=f"No fue posible ejecutar pytest: {exc}")],
        )


def _count(output: str, pattern: str) -> int:
    match = re.search(pattern, output)
    return int(match.group(1)) if match else 0
