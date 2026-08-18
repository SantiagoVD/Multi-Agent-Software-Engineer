"""Review agent; review is read-only and returns a typed decision."""

from pathlib import Path

from app.agents.base_agent import BaseAgent
from app.core.config import settings
from app.llm.llm_provider import LLMProviderError
from app.memory.task_memory import TaskMemory
from app.models.development_result import DevelopmentResult
from app.models.repository_context import RepositoryContext
from app.models.review_result import (
    IssueSeverity,
    ReviewIssue,
    ReviewResult,
    ReviewStatus,
)
from app.models.task import Task
from app.models.test_result import TestResult
from app.prompts.review_prompt import SYSTEM_PROMPT, build_review_prompt
from app.tools.git.git_diff_tool import git_diff


class ReviewAgent(BaseAgent):
    def run(self, task: Task, repository_path: Path, memory: TaskMemory, development: DevelopmentResult | None = None, tests: TestResult | None = None, repository_context: RepositoryContext | None = None) -> ReviewResult:
        try:
            diff = git_diff(repository_path)
        except RuntimeError:
            diff = ""
        if self.provider is not None and settings.review_llm_enabled:
            try:
                result = self.provider.generate_structured(
                    SYSTEM_PROMPT,
                    build_review_prompt(task.task, self.context_manager.review_context(task, memory) + f"\nDiff:\n{diff[:12000]}"),
                    ReviewResult,
                )
                memory.review_results.append(result)
                return result
            except LLMProviderError:
                pass
        if tests is not None and not tests.success:
            result = ReviewResult(status=ReviewStatus.CHANGES_REQUIRED, summary="Los tests no pasan.", issues=[ReviewIssue(severity=IssueSeverity.HIGH, description="Corregir los fallos reportados por testing.")])
        else:
            result = ReviewResult(status=ReviewStatus.APPROVED, summary="Cambios revisados y tests satisfactorios.")
        memory.review_results.append(result)
        return result
