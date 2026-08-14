"""Shared agent behavior."""

from app.llm.context_manager import ContextManager
from app.llm.llm_provider import LLMProvider
from app.memory.task_memory import TaskMemory
from app.models.tool_call import ToolCall


class BaseAgent:
    def __init__(self, provider: LLMProvider | None = None, context_manager: ContextManager | None = None) -> None:
        self.provider = provider
        self.context_manager = context_manager or ContextManager()

    def record_tool(self, memory: TaskMemory, name: str, success: bool, summary: str) -> None:
        memory.add_tool_call(ToolCall(tool_name=name, success=success, result_summary=summary))
