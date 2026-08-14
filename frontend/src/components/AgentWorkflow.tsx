import type { FinalResult } from '../api/types'

type AgentState = 'waiting' | 'running' | 'completed' | 'failed' | 'changes'

interface AgentCardData {
  key: string
  number: string
  title: string
  role: string
  detail: string
}

const agents: AgentCardData[] = [
  { key: 'repository', number: '01', title: 'Repository Agent', role: 'Architecture intelligence', detail: 'Maps structure, dependencies, tests and relevant code.' },
  { key: 'developer', number: '02', title: 'Developer Agent', role: 'Implementation engine', detail: 'Applies a validated plan inside the isolated workspace.' },
  { key: 'testing', number: '03', title: 'Testing Agent', role: 'Quality verification', detail: 'Runs pytest, Ruff and mypy through controlled tools.' },
  { key: 'review', number: '04', title: 'Review Agent', role: 'Final code review', detail: 'Evaluates requirements, diff, safety and maintainability.' },
]

function stateFor(agent: AgentCardData, running: boolean, result: FinalResult | null): AgentState {
  if (running) return 'running'
  if (!result) return 'waiting'
  if (result.success) return 'completed'
  if (agent.key === 'testing' && result.test_result) return result.test_result.success ? 'completed' : 'failed'
  if (agent.key === 'review' && result.review_result) return result.review_result.status === 'approved' ? 'completed' : 'changes'
  return 'waiting'
}

const stateLabel: Record<AgentState, string> = {
  waiting: 'Waiting', running: 'In workflow', completed: 'Completed', failed: 'Failed', changes: 'Changes required',
}

export function AgentWorkflow({ running, result }: { running: boolean; result: FinalResult | null }) {
  return (
    <section className={`workflow-section${running ? ' workflow-active' : ''}`}>
      <div className="section-heading workflow-heading">
        <div><span className="eyebrow">ORCHESTRATED PIPELINE</span><h2>Four specialists. One outcome.</h2></div>
        {running && <span className="sync-note"><i />Synchronous run · final status returns on completion</span>}
      </div>
      <div className="agent-grid">
        {agents.map((agent, index) => {
          const state = stateFor(agent, running, result)
          return (
            <div className={`agent-card agent-${state}`} key={agent.key}>
              <div className="agent-top"><span className="agent-number">{agent.number}</span><span className="agent-state"><i />{stateLabel[state]}</span></div>
              <div className="agent-orb"><span>{agent.title.split(' ')[0][0]}{agent.title.split(' ')[1][0]}</span></div>
              <h3>{agent.title}</h3><p className="agent-role">{agent.role}</p><p>{agent.detail}</p>
              {index < agents.length - 1 && <span className="flow-arrow" aria-hidden="true">→</span>}
            </div>
          )
        })}
      </div>
    </section>
  )
}
