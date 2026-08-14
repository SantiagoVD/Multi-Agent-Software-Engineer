from app.memory.in_memory_store import InMemoryStore
from app.memory.task_memory import TaskMemory
from app.models.task_status import TaskStatus


def test_memory_is_isolated_by_task() -> None:
    store = InMemoryStore()
    memory = TaskMemory(task_id="TASK-1", task_description="test")
    memory.status = TaskStatus.ANALYZING_REPOSITORY
    store.save(memory)
    assert store.get("TASK-1") is memory
    assert store.get("TASK-2") is None
    store.delete("TASK-1")
    assert store.get("TASK-1") is None
