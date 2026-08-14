"""In-memory task memory implementation."""

from app.memory.memory_store import MemoryStore
from app.memory.task_memory import TaskMemory


class InMemoryStore(MemoryStore):
    def __init__(self) -> None:
        self._items: dict[str, TaskMemory] = {}

    def get(self, task_id: str) -> TaskMemory | None:
        return self._items.get(task_id)

    def save(self, memory: TaskMemory) -> None:
        self._items[memory.task_id] = memory

    def delete(self, task_id: str) -> None:
        self._items.pop(task_id, None)

    def clear(self) -> None:
        self._items.clear()
