import type { OllamaHealthResult } from '../api/types'
import { StatusBadge } from './StatusBadge'

interface HeaderProps { backendOnline: boolean | null; ollama: OllamaHealthResult | null }

export function Header({ backendOnline, ollama }: HeaderProps) {
  const ollamaTone = ollama?.status === 'online' && ollama.model_available ? 'success' : ollama?.status === 'online' ? 'warning' : 'danger'
  const ollamaLabel = ollama?.status === 'online' && ollama.model_available ? `${ollama.model} listo` : ollama?.status === 'online' ? `${ollama.model} no disponible` : 'Ollama desconectado'
  return <header className="topbar"><a className="brand" href="#top" aria-label="Inicio de Ingeniero de Software Multiagente"><span className="brand-mark"><span>MA</span></span><span className="brand-copy"><strong>Multiagente</strong><small>Ingeniería de software</small></span></a><div className="system-status"><StatusBadge tone={backendOnline ? 'success' : backendOnline === false ? 'danger' : 'neutral'} pulse={backendOnline === true}>{backendOnline ? 'Backend en línea' : backendOnline === false ? 'Backend desconectado' : 'Verificando backend'}</StatusBadge><StatusBadge tone={ollama ? ollamaTone : 'neutral'}>{ollama ? ollamaLabel : 'Verificando modelo'}</StatusBadge><span className="version-pill">V1</span></div></header>
}
