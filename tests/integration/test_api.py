import json

from fastapi.testclient import TestClient

from app.api.dependencies import get_orchestrator
from app.core.config import settings
from app.llm.ollama_client import OllamaClient
from app.main import app


def test_health_endpoint() -> None:
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_cors_allows_configured_frontend() -> None:
    response = TestClient(app).options(
        "/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_ollama_health_reports_configured_model(monkeypatch) -> None:
    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def read(self) -> bytes:
            return json.dumps({"models": [{"name": settings.ollama_model}]}).encode()

    monkeypatch.setattr("app.api.routes.health_routes.urlopen", lambda *args, **kwargs: FakeResponse())
    response = TestClient(app).get("/health/ollama")
    assert response.status_code == 200
    assert response.json() == {
        "status": "online",
        "model": settings.ollama_model,
        "model_available": True,
    }


def test_api_orchestrator_uses_ollama_provider() -> None:
    orchestrator = next(get_orchestrator())
    assert isinstance(orchestrator.provider, OllamaClient)
