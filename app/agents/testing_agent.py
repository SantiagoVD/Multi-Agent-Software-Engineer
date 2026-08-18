"""Testing agent backed by the fixed execution tools."""

from pathlib import Path

from app.agents.base_agent import BaseAgent
from app.memory.task_memory import TaskMemory
from app.models.task import Task
from app.models.test_result import TestIssue, TestResult
from app.tools.execution.run_linter_tool import run_linter
from app.tools.execution.run_tests_tool import run_tests
from app.tools.execution.run_typecheck_tool import run_typecheck


class TestingAgent(BaseAgent):
    __test__ = False
    def run(self, task: Task, repository_path: Path, memory: TaskMemory) -> TestResult:
        language = memory.repository_context.language if memory.repository_context else None
        if language is not None and language != "Python":
            result = TestResult(
                success=True,
                command="No fixed Python checks applicable",
                skipped=1,
                raw_output=f"Se omitieron pytest, Ruff y mypy: el repositorio fue detectado como {language}.",
            )
            memory.test_results.append(result)
            self.record_tool(memory, "run_tests", True, result.raw_output or "")
            return result
        tests = run_tests(repository_path)
        lint = run_linter(repository_path)
        typecheck = run_typecheck(repository_path)
        issues = list(tests.issues)
        if not lint.success and lint.available:
            issues.append(TestIssue(message="Ruff: " + " ".join(lint.issues)))
        if not typecheck.success and typecheck.available:
            issues.append(TestIssue(message="mypy: " + " ".join(typecheck.issues)))
        result = tests.model_copy(update={"issues": issues})
        memory.test_results.append(result)
        self.record_tool(memory, "run_tests", tests.success, tests.raw_output or "")
        self.record_tool(memory, "run_linter", lint.success, lint.raw_output)
        self.record_tool(memory, "run_typecheck", typecheck.success, typecheck.raw_output)
        return result
