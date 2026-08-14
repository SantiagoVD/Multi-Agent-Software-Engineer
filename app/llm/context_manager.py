"""Small, role-specific context windows for agents."""

from app.memory.task_memory import TaskMemory
from app.models.task import Task


class ContextManager:
    def __init__(self, max_file_chars: int = 12_000, max_history_items: int = 8) -> None:
        self.max_file_chars = max_file_chars
        self.max_history_items = max_history_items

    def build_context(self, agent: str, task: Task, memory: TaskMemory) -> str:
        sections = [f"Tarea: {task.task}", f"Repositorio: {task.repository_url}"]
        if memory.repository_context:
            sections.append(f"Contexto del repositorio:\n{memory.repository_context.model_dump_json()}")
        if agent in {"developer", "testing", "review"}:
            sections.append(self._files(memory))
        latest_test = memory.latest_test()
        if agent in {"developer", "testing", "review"} and latest_test is not None:
            sections.append(f"Último resultado de tests:\n{latest_test.model_dump_json()}")
        latest_review = memory.latest_review()
        if agent == "review" and latest_review is not None:
            sections.append(f"Última revisión:\n{latest_review.model_dump_json()}")
        if memory.tool_calls:
            calls = memory.tool_calls[-self.max_history_items:]
            sections.append("Acciones recientes:\n" + "\n".join(c.result_summary or c.tool_name for c in calls))
        return "\n\n".join(sections)

    def repository_context(self, task: Task, memory: TaskMemory) -> str:
        return self.build_context("repository", task, memory)

    def developer_context(self, task: Task, memory: TaskMemory) -> str:
        return self.build_context("developer", task, memory)

    def testing_context(self, task: Task, memory: TaskMemory) -> str:
        return self.build_context("testing", task, memory)

    def review_context(self, task: Task, memory: TaskMemory) -> str:
        return self.build_context("review", task, memory)

    def _files(self, memory: TaskMemory) -> str:
        chunks = []
        for path, content in list(memory.relevant_files.items())[:10]:
            chunks.append(f"--- {path} ---\n{content[:self.max_file_chars]}")
        return "Archivos relevantes:\n" + "\n".join(chunks)
