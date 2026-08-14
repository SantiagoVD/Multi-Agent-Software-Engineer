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
      setError(caught instanceof Error ? caught.message : 'An unexpected error occurred.')
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
          <div className="hero-kicker"><span /><span>Autonomous software delivery</span></div>
          <h1>Ship code with an<br /><em>AI engineering team.</em></h1>
          <p>Give the team a repository and a goal. Four specialized agents analyze, implement, test and review every change inside an isolated workspace.</p>
          <div className="hero-proof"><span><i>01</i>Read architecture</span><span><i>02</i>Write safely</span><span><i>03</i>Verify quality</span><span><i>04</i>Review outcome</span></div>
        </section>
        {error && <ErrorPanel message={error} onDismiss={() => setError(null)} />}
        <TaskForm disabled={running} backendOnline={backendOnline} onSubmit={runTask} />
        <AgentWorkflow running={running} result={result} />
        <div id="results">{result && <ResultPanel result={result} />}</div>
      </main>
      <footer><span>Multi-Agent Software Engineer <b>V1</b></span><span>Built for real repositories · No commits · No pushes</span></footer>
    </div>
  )
}
