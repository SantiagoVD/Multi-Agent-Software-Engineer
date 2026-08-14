"""Developer agent with constrained file-edit tools."""

from pathlib import Path

from app.agents.base_agent import BaseAgent
from app.llm.llm_provider import LLMProviderError
from app.memory.task_memory import TaskMemory
from app.models.agent_plan import DeveloperPlan
from app.models.development_result import DevelopmentResult
from app.models.task import Task
from app.prompts.developer_prompt import SYSTEM_PROMPT, build_developer_prompt
from app.tools.filesystem.create_file_tool import create_file
from app.tools.filesystem.write_file_tool import write_file


class DeveloperAgent(BaseAgent):
    def run(self, task: Task, repository_path: Path, memory: TaskMemory) -> DevelopmentResult:
        if self.provider is None:
            return DevelopmentResult(success=False, summary="No hay un LLM Provider configurado.")
        try:
            plan = self.provider.generate_structured(
                SYSTEM_PROMPT,
                build_developer_prompt(task.task, self.context_manager.developer_context(task, memory)),
                DeveloperPlan,
            )
        except (LLMProviderError, OSError, ValueError) as exc:
            return DevelopmentResult(success=False, summary=f"No se pudo obtener un plan de desarrollo: {exc}")
        modified: list[str] = []
        created: list[str] = []
        try:
            for change in plan.changes:
                if change.create:
                    create_file(repository_path, change.path, change.content)
                    created.append(change.path)
                else:
                    write_file(repository_path, change.path, change.content)
                    modified.append(change.path)
        except (OSError, ValueError) as exc:
            return DevelopmentResult(success=False, summary=f"No se pudo aplicar el cambio: {exc}", files_created=created, files_modified=modified)
        memory.modified_files.extend(path for path in [*created, *modified] if path not in memory.modified_files)
        result = DevelopmentResult(success=True, summary=plan.summary or "Cambios aplicados.", files_created=created, files_modified=modified)
        memory.development_results.append(result)
        return result
