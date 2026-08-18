# Ingeniero de Software Multiagente

Plataforma local para ejecutar un equipo de agentes de IA sobre repositorios reales. Analiza la estructura de un proyecto, propone e implementa cambios dentro de un workspace aislado, ejecuta verificaciones y revisa el resultado antes de entregarlo.

> Los cambios nunca se aplican directamente a la rama base. De forma opcional, el resultado aprobado se publica en una rama `ai/<task-id>` para su revisión mediante Pull Request.

## Capacidades

- Clonado de repositorios y creación de un workspace aislado por tarea.
- Análisis de arquitectura, dependencias, archivos relevantes e historial Git.
- Planificación e implementación asistida por Ollama.
- Verificaciones controladas con `pytest`, Ruff y mypy para proyectos Python.
- Revisión final basada en resultados de pruebas y diff.
- Commit y push opcional de una rama de trabajo, sin merge automático a `main`.
- Interfaz React para iniciar tareas, consultar el estado del modelo y revisar resultados.

## Arquitectura

```text
Frontend React/Vite
        │ HTTP
        ▼
API FastAPI ──► Orquestador
                   │
      ┌────────────┼────────────┐
      ▼            ▼            ▼
Repositorio   Desarrollo     Pruebas y revisión
   Agent        Agent            Agents
      │            │                 │
      └────────────┴─────────────────┘
                   │
                   ▼
     workspaces/<task-id>/repository
                   │
                   ▼
             Ollama local
```

## Requisitos

- Python 3.13 o superior.
- Node.js 22 o superior.
- Git configurado en el equipo.
- [Ollama](https://ollama.com/) con un modelo Qwen 3 disponible. La configuración de ejemplo usa `qwen3:4b`.

## Inicio rápido

### 1. Configurar el entorno

```powershell
Copy-Item .env.example .env
python -m pip install -e ".[dev]"
```

Instala o descarga el modelo si aún no está disponible:

```powershell
ollama pull qwen3:4b
```

### 2. Iniciar el backend

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

La API queda disponible en `http://localhost:8000` y la documentación interactiva en `http://localhost:8000/docs`.

### 3. Iniciar el frontend

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

Abre `http://localhost:5173` en el navegador.

## Configuración

Las variables principales se definen en `.env`:

| Variable | Descripción |
| --- | --- |
| `OLLAMA_BASE_URL` | URL del servidor Ollama local. |
| `OLLAMA_MODEL` | Modelo utilizado por los agentes. |
| `OLLAMA_TIMEOUT_SECONDS` | Tiempo máximo de espera por una generación. |
| `OLLAMA_NUM_PREDICT` | Límite de tokens de salida por generación. |
| `FRONTEND_ORIGIN` | Origen autorizado por CORS para el frontend. |
| `WORKSPACE_ROOT` | Directorio de workspaces aislados. |
| `GIT_AUTHOR_NAME` / `GIT_AUTHOR_EMAIL` | Identidad usada en commits opcionales del agente. |

## Flujo de una tarea

1. Indica la URL HTTPS del repositorio, la tarea y la rama base.
2. El sistema clona el proyecto y crea la rama local `ai/<task-id>`.
3. Los agentes analizan, implementan, verifican y revisan el cambio.
4. El resultado muestra archivos modificados, verificaciones y revisión.
5. Si activas **Publicar rama aprobada**, se crea un commit y se hace push únicamente de `ai/<task-id>` a `origin`.

Para publicar ramas, Git debe contar con credenciales válidas para el repositorio remoto. La aplicación no publica ni hace merge en `main`.

## Validación

```powershell
python -m pytest -q
python -m ruff check .
python -m mypy app
cd frontend
npm.cmd run lint
npm.cmd run typecheck
npm.cmd run build
```

## Seguridad y límites

- Los workspaces se crean en `workspaces/<task-id>/repository`.
- No se ejecutan comandos indicados por archivos del repositorio analizado.
- Las operaciones Git usan comandos fijos, sin shell.
- Los cambios permanecen aislados hasta una publicación explícita.
- Si expones el backend fuera de tu red local, añade autenticación antes de permitir tareas o publicaciones remotas.

## Próximos pasos

Para un despliegue personal, el frontend puede alojarse en Vercel mientras el backend, Ollama y el agente continúan en tu PC mediante un túnel HTTPS seguro.
