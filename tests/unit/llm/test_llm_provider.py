import json

from pydantic import BaseModel

from app.llm.llm_provider import LLMProvider
from app.llm.llm_response import LLMResponse


class Output(BaseModel):
    value: int


class FakeProvider(LLMProvider):
    def __init__(self) -> None:
        self.calls = 0

    def generate(self, system_prompt: str, user_prompt: str, *, temperature: float = 0.2, json_mode: bool = False) -> LLMResponse:
        self.calls += 1
        return LLMResponse(content=json.dumps({"value": 7}))


def test_structured_output_is_validated() -> None:
    provider = FakeProvider()
    result = provider.generate_structured("system", "user", Output)
    assert result.value == 7
    assert provider.calls == 1
