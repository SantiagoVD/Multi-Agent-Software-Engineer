import type { OllamaHealthResult } from '../api/types'
import { StatusBadge } from './StatusBadge'

interface HeaderProps {
  backendOnline: boolean | null
  ollama: OllamaHealthResult | null
}

export function Header({ backendOnline, ollama }: HeaderProps) {
  const ollamaTone = ollama?.status === 'online' && ollama.model_available
    ? 'success'
    : ollama?.status === 'online' ? 'warning' : 'danger'
  const ollamaLabel = ollama?.status === 'online' && ollama.model_available
    ? `${ollama.model} ready`
    : ollama?.status === 'online' ? `${ollama.model} missing` : 'Ollama offline'

  return (
    <header className="topbar">
      <a className="brand" href="#top" aria-label="Multi-Agent Software Engineer home">
        <span className="brand-mark"><span>MA</span></span>
        <span className="brand-copy"><strong>Multi-Agent</strong><small>Software Engineer</small></span>
      </a>
      <div className="system-status" aria-label="System status">
        <StatusBadge tone={backendOnline ? 'success' : backendOnline === false ? 'danger' : 'neutral'} pulse={backendOnline === true}>
          {backendOnline ? 'Backend online' : backendOnline === false ? 'Backend offline' : 'Checking backend'}
        </StatusBadge>
        <StatusBadge tone={ollama ? ollamaTone : 'neutral'}>
          {ollama ? ollamaLabel : 'Checking model'}
        </StatusBadge>
        <span className="version-pill">V1</span>
      </div>
    </header>
  )
}
