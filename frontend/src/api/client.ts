import type { FinalResult, HealthResult, OllamaHealthResult, TaskRequest } from './types'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000').replace(/\/$/, '')

class ApiError extends Error {
  constructor(message: string, readonly status?: number) {
    super(message)
    this.name = 'ApiError'
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...init,
      headers: { 'Content-Type': 'application/json', ...init?.headers },
    })
  } catch {
    throw new ApiError('The backend is offline or unreachable. Check that FastAPI is running on port 8000.')
  }
  if (!response.ok) {
    const payload: unknown = await response.json().catch(() => null)
    const detail = typeof payload === 'object' && payload !== null && 'detail' in payload
      ? String((payload as { detail: unknown }).detail)
      : `Request failed with status ${response.status}`
    throw new ApiError(detail, response.status)
  }
  return response.json() as Promise<T>
}

export const api = {
  health: () => request<HealthResult>('/health'),
  ollamaHealth: () => request<OllamaHealthResult>('/health/ollama'),
  runTask: (task: TaskRequest) => request<FinalResult>('/tasks', {
    method: 'POST',
    body: JSON.stringify(task),
  }),
}

export { API_BASE_URL, ApiError }
