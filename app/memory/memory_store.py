"""Memory storage abstraction."""

from abc import ABC, abstractmethod

from app.memory.task_memory import TaskMemory


class MemoryStore(ABC):
    @abstractmethod
    def get(self, task_id: str) -> TaskMemory | None:
        pass

    @abstractmethod
    def save(self, memory: TaskMemory) -> None:
        pass

    @abstractmethod
    def delete(self, task_id: str) -> None:
        pass
