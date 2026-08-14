"""Provider abstraction and bounded structured-output parsing."""

from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

from app.llm.llm_response import LLMResponse

T = TypeVar("T", bound=BaseModel)


class LLMProviderError(RuntimeError):
    """Raised when an LLM request cannot be completed or parsed."""


class LLMProvider(ABC):
    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        temperature: float = 0.2,
        json_mode: bool = False,
    ) -> LLMResponse:
        """Generate a provider-independent response."""

    def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
        *,
        temperature: float = 0.2,
        max_attempts: int = 2,
    ) -> T:
        """Generate and validate JSON, retrying once with corrective feedback."""
        if max_attempts < 1:
            raise ValueError("max_attempts debe ser positivo")
        prompt = user_prompt
        last_error: Exception | None = None
        for attempt in range(max_attempts):
            try:
                response = self.generate(
                    system_prompt, prompt, temperature=temperature, json_mode=True
                )
                return response.parse_json(response_model)
            except (ValueError, TypeError) as exc:
                last_error = exc
                prompt = (
                    f"{user_prompt}\n\nLa respuesta anterior no pudo validarse ({exc}). "
                    "Devuelve únicamente un JSON válido compatible con el esquema solicitado."
                )
        raise LLMProviderError(f"No se pudo validar la salida estructurada: {last_error}")
