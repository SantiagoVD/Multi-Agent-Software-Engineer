"""Provider-independent LLM response contract."""

import json
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


class LLMResponse(BaseModel):
    content: str
    raw_response: dict[str, Any] | None = None
    model: str | None = None
    done: bool | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None

    def parse_json(self, response_model: type[T]) -> T:
        text = self.content.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        try:
            payload = json.loads(text)
            return response_model.model_validate(payload)
        except (json.JSONDecodeError, ValidationError, IndexError) as exc:
            raise ValueError(f"La respuesta del LLM no es JSON válido: {exc}") from exc
