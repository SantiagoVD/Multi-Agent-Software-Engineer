from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.exception_handlers import llm_exception_handler, workflow_exception_handler
from app.api.routes.health_routes import router as health_router
from app.api.routes.task_routes import router as task_router
from app.core.config import settings
from app.llm.llm_provider import LLMProviderError
from app.orchestrator.workflow_guard import WorkflowError


def create_app() -> FastAPI:
    application = FastAPI(title=settings.app_name)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_origin, "http://127.0.0.1:5173"],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )
    application.include_router(health_router)
    application.include_router(task_router)
    application.add_exception_handler(WorkflowError, workflow_exception_handler)
    application.add_exception_handler(LLMProviderError, llm_exception_handler)
    return application


app = create_app()
