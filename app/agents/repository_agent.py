"""Repository analysis agent using read-only tools."""

from pathlib import Path

from app.agents.base_agent import BaseAgent
from app.memory.task_memory import TaskMemory
from app.models.repository_context import RepositoryContext
from app.models.task import Task
from app.tools.filesystem.list_files_tool import list_files
from app.tools.filesystem.read_file_tool import read_file
from app.tools.git.git_history_tool import git_history


class RepositoryAgent(BaseAgent):
    def run(self, task: Task, repository_path: Path, memory: TaskMemory) -> RepositoryContext:
        files = list_files(repository_path)
        relevant = [path for path in files if self._relevant(path, task.task)]
        if not relevant:
            relevant = [path for path in files if path.endswith((".py", ".js", ".ts", ".go", ".rs"))]
        relevant = relevant[:20]
        tests = [path for path in files if "test" in Path(path).name.lower()][:20]
        dependencies = [path for path in files if Path(path).name.lower() in {
            "pyproject.toml", "requirements.txt", "package.json", "go.mod", "cargo.toml"
        }]
        snippets: list[str] = []
        for path in relevant[:10]:
            try:
                content = read_file(repository_path, path)
                # Preserve enough source for downstream agents without
                # expanding their prompt to the size of the repository.
                memory.remember_file(path, content[:2_000])
                snippets.append(f"{path}: {content[:500]}")
            except (OSError, ValueError):
                continue
        context = RepositoryContext(
            language=self._language(files),
            framework=self._framework(files),
            architecture="; ".join(dependencies) or "Estructura no determinada",
            relevant_files=relevant,
            test_files=tests,
            dependency_files=dependencies,
            summary=f"{len(files)} archivos analizados. " + " | ".join(snippets[:3]),
        )
        memory.repository_context = context
        self.record_tool(memory, "list_files", True, f"{len(files)} archivos")
        try:
            history_count = len(git_history(repository_path, 5))
        except RuntimeError:
            history_count = 0
            self.record_tool(memory, "git_history", False, "No hay historial Git disponible")
        else:
            self.record_tool(memory, "git_history", True, f"{history_count} commits recientes")
        return context

    @staticmethod
    def _relevant(path: str, task: str) -> bool:
        tokens = {token.casefold() for token in task.split() if len(token) > 3}
        name = path.casefold()
        return any(token in name for token in tokens)

    @staticmethod
    def _language(files: list[str]) -> str | None:
        suffixes = {Path(path).suffix for path in files}
        return "Python" if ".py" in suffixes else ("JavaScript/TypeScript" if suffixes & {".js", ".ts"} else None)

    @staticmethod
    def _framework(files: list[str]) -> str | None:
        names = {Path(path).name.lower() for path in files}
        if "pyproject.toml" in names or "requirements.txt" in names:
            return "Python (framework no determinado)"
        return None
