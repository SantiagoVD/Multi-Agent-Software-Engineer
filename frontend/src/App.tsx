import { useCallback, useEffect, useState } from 'react'
import { api } from './api/client'
import type { FinalResult, OllamaHealthResult, TaskRequest } from './api/types'
import { AgentWorkflow } from './components/AgentWorkflow'
import { ErrorPanel } from './components/ErrorPanel'
import { Header } from './components/Header'
import { ResultPanel } from './components/ResultPanel'
import { TaskForm } from './components/TaskForm'

export default function App() {
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null)
  const [ollama, setOllama] = useState<OllamaHealthResult | null>(null)
  const [running, setRunning] = useState(false)
  const [result, setResult] = useState<FinalResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const checkServices = useCallback(async () => {
    try {
      const health = await api.health()
      setBackendOnline(health.status === 'ok')
      setOllama(await api.ollamaHealth())
    } catch {
      setBackendOnline(false)
      setOllama(null)
    }
  }, [])

  useEffect(() => {
    void checkServices()
    const timer = window.setInterval(() => void checkServices(), 15_000)
    return () => window.clearInterval(timer)
  }, [checkServices])

  async function runTask(request: TaskRequest) {
    setRunning(true)
    setResult(null)
    setError(null)
    try {
      const finalResult = await api.runTask(request)
      setResult(finalResult)
      if (!finalResult.success) setError(finalResult.summary)
      window.setTimeout(() => document.getElementById('results')?.scrollIntoView({ behavior: 'smooth' }), 100)
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'Ocurrió un error inesperado.')
    } finally {
      setRunning(false)
    }
  }

  return (
    <div id="top" className="app-shell">
      <div className="ambient ambient-one" /><div className="ambient ambient-two" /><div className="grid-overlay" />
      <Header backendOnline={backendOnline} ollama={ollama} />
      <main>
        <section className="hero">
          <div className="hero-kicker"><span /><span>Entrega de software autónoma</span></div>
          <h1>Desarrolla software con un<br /><em>equipo de IA.</em></h1>
          <p>Indica un repositorio y un objetivo. Cuatro agentes especializados analizan, implementan, verifican y revisan cada cambio dentro de un workspace aislado.</p>
          <div className="hero-proof"><span><i>01</i>Analizar arquitectura</span><span><i>02</i>Implementar con seguridad</span><span><i>03</i>Verificar calidad</span><span><i>04</i>Revisar resultado</span></div>
        </section>
        {error && <ErrorPanel message={error} onDismiss={() => setError(null)} />}
        <TaskForm disabled={running} backendOnline={backendOnline} onSubmit={runTask} />
        <AgentWorkflow running={running} result={result} />
        <div id="results">{result && <ResultPanel result={result} />}</div>
      </main>
      <footer><span>Ingeniero de Software Multiagente <b>V1</b></span><span>Diseñado para repositorios reales · Sin cambios en la rama base</span></footer>
    </div>
  )
}
