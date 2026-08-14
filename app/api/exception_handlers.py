from fastapi import Request
from fastapi.responses import JSONResponse


async def workflow_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})


async def llm_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=503, content={"detail": "El proveedor LLM no está disponible."})
