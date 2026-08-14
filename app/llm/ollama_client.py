"""HTTP client for a local Ollama server."""

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.core.config import settings
from app.llm.llm_provider import LLMProvider, LLMProviderError
from app.llm.llm_response import LLMResponse


class OllamaClient(LLMProvider):
    def __init__(self, base_url: str | None = None, model: str | None = None, timeout: int | None = None) -> None:
        self.base_url = (base_url or settings.ollama_base_url).rstrip("/")
        self.model = model or settings.ollama_model
        self.timeout = timeout or settings.ollama_timeout_seconds

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        temperature: float = 0.2,
        json_mode: bool = False,
    ) -> LLMResponse:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "options": {"temperature": temperature},
        }
        if settings.ollama_num_gpu is not None:
            payload["options"]["num_gpu"] = settings.ollama_num_gpu
        if json_mode:
            payload["format"] = "json"
        request = Request(
            f"{self.base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                raw = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            raise LLMProviderError(f"No se pudo conectar con Ollama: {exc}") from exc
        if not isinstance(raw, dict):
            raise LLMProviderError("Ollama devolvió una respuesta inválida")
        message = raw.get("message")
        content = message.get("content") if isinstance(message, dict) else raw.get("response")
        if not isinstance(content, str):
            raise LLMProviderError("La respuesta de Ollama no contiene contenido textual")
        return LLMResponse(
            content=content,
            raw_response=raw,
            model=raw.get("model", self.model),
            done=raw.get("done"),
            prompt_tokens=raw.get("prompt_eval_count"),
            completion_tokens=raw.get("eval_count"),
        )
