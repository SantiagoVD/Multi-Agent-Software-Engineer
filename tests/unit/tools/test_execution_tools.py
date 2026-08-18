from pathlib import Path

from app.tools.execution.run_linter_tool import run_linter
from app.tools.execution.run_tests_tool import run_tests
from app.tools.execution.run_typecheck_tool import run_typecheck


def test_run_tests_success_and_failure(tmp_path: Path) -> None:
    (tmp_path / "test_sample.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    result = run_tests(tmp_path)
    assert result.success
    assert result.passed == 1

    (tmp_path / "test_bad.py").write_text("def test_bad():\n    assert False\n", encoding="utf-8")
    failed = run_tests(tmp_path)
    assert not failed.success
    assert failed.failed == 1


def test_optional_tools_return_structured_result(tmp_path: Path) -> None:
    linter = run_linter(tmp_path)
    typecheck = run_typecheck(tmp_path)
    assert linter.command
    assert typecheck.command
    assert isinstance(linter.available, bool)
    assert isinstance(typecheck.available, bool)


def test_run_tests_skips_when_no_python_tests_are_present(tmp_path: Path) -> None:
    result = run_tests(tmp_path)

    assert result.success
    assert result.skipped == 1
