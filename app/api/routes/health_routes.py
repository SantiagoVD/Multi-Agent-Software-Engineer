import json
from urllib.error import URLError
from urllib.request import urlopen

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/ollama")
def ollama_health() -> dict[str, str | bool]:
    try:
        with urlopen(f"{settings.ollama_base_url.rstrip('/')}/api/tags", timeout=2) as response:
            payload = json.loads(response.read().decode("utf-8"))
        models = payload.get("models", []) if isinstance(payload, dict) else []
        names = {
            model.get("name", "").split(":latest")[0]
            for model in models
            if isinstance(model, dict)
        }
        available = settings.ollama_model in names
        return {
            "status": "online",
            "model": settings.ollama_model,
            "model_available": available,
        }
    except (OSError, URLError, TimeoutError, json.JSONDecodeError):
        return {
            "status": "offline",
            "model": settings.ollama_model,
            "model_available": False,
        }
