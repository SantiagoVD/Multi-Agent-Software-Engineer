from collections.abc import Generator

from app.llm.ollama_client import OllamaClient
from app.orchestrator.orchestrator import Orchestrator
from app.services.task_service import TaskService


def get_orchestrator() -> Generator[Orchestrator]:
    yield Orchestrator(provider=OllamaClient())


def get_task_service(orchestrator: Orchestrator) -> TaskService:
    return TaskService(orchestrator)
