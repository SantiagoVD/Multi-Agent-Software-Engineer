import type { FinalResult } from '../api/types'

type AgentState = 'waiting' | 'running' | 'completed' | 'failed' | 'changes'
interface AgentCardData { key: string; number: string; title: string; role: string; detail: string }

const agents: AgentCardData[] = [
  { key: 'repository', number: '01', title: 'Agente de repositorio', role: 'Inteligencia de arquitectura', detail: 'Identifica estructura, dependencias, pruebas y código relevante.' },
  { key: 'developer', number: '02', title: 'Agente de desarrollo', role: 'Motor de implementación', detail: 'Aplica un plan validado dentro del workspace aislado.' },
  { key: 'testing', number: '03', title: 'Agente de pruebas', role: 'Verificación de calidad', detail: 'Ejecuta pytest, Ruff y mypy con herramientas controladas.' },
  { key: 'review', number: '04', title: 'Agente de revisión', role: 'Revisión final de código', detail: 'Evalúa requisitos, diff, seguridad y mantenibilidad.' },
]

function stateFor(agent: AgentCardData, running: boolean, result: FinalResult | null): AgentState {
  if (running) return 'running'
  if (!result) return 'waiting'
  if (result.success) return 'completed'
  if (agent.key === 'testing' && result.test_result) return result.test_result.success ? 'completed' : 'failed'
  if (agent.key === 'review' && result.review_result) return result.review_result.status === 'approved' ? 'completed' : 'changes'
  return 'waiting'
}

const stateLabel: Record<AgentState, string> = { waiting: 'En espera', running: 'En ejecución', completed: 'Completado', failed: 'Falló', changes: 'Requiere cambios' }

export function AgentWorkflow({ running, result }: { running: boolean; result: FinalResult | null }) {
  return <section className={`workflow-section${running ? ' workflow-active' : ''}`}><div className="section-heading workflow-heading"><div><span className="eyebrow">FLUJO ORQUESTADO</span><h2>Cuatro especialistas. Un resultado.</h2></div>{running && <span className="sync-note"><i />Ejecución síncrona · el resultado llega al finalizar</span>}</div><div className="agent-grid">{agents.map((agent, index) => { const state = stateFor(agent, running, result); return <div className={`agent-card agent-${state}`} key={agent.key}><div className="agent-top"><span className="agent-number">{agent.number}</span><span className="agent-state"><i />{stateLabel[state]}</span></div><div className="agent-orb"><span>{agent.number}</span></div><h3>{agent.title}</h3><p className="agent-role">{agent.role}</p><p>{agent.detail}</p>{index < agents.length - 1 && <span className="flow-arrow" aria-hidden="true">→</span>}</div> })}</div></section>
}
