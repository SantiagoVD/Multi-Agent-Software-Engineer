import { useState } from 'react'
import type { FormEvent } from 'react'
import type { TaskRequest } from '../api/types'

interface TaskFormProps {
  disabled: boolean
  backendOnline: boolean | null
  onSubmit: (request: TaskRequest) => Promise<void>
}

const initialForm = {
  repository_url: '',
  task: '',
  branch: 'main',
  publish_branch: false,
}

export function TaskForm({ disabled, backendOnline, onSubmit }: TaskFormProps) {
  const [form, setForm] = useState(initialForm)
  const [validation, setValidation] = useState<string | null>(null)

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    try {
      const url = new URL(form.repository_url)
      if (!['http:', 'https:'].includes(url.protocol)) throw new Error()
    } catch {
      setValidation('Enter a valid HTTP or HTTPS Git repository URL.')
      return
    }
    if (form.task.trim().length < 5) {
      setValidation('Describe the engineering task in at least 5 characters.')
      return
    }
    if (form.branch && !/^[\w./-]+$/.test(form.branch)) {
      setValidation('The branch name contains unsupported characters.')
      return
    }
    setValidation(null)
    await onSubmit({
      repository_url: form.repository_url.trim(),
      task: form.task.trim(),
      branch: form.branch.trim() || null,
      publish_branch: form.publish_branch,
    })
  }

  return (
    <section className="composer-card" id="compose">
      <div className="section-heading">
        <div><span className="eyebrow">NEW ENGINEERING RUN</span><h2>What should the team build?</h2></div>
        <span className="secure-label"><svg viewBox="0 0 24 24"><path d="M12 3 5 6v5c0 4.6 2.9 8.8 7 10 4.1-1.2 7-5.4 7-10V6l-7-3Z"/><path d="m9.5 12 1.7 1.7 3.6-4"/></svg>Isolated workspace</span>
      </div>
      <form onSubmit={submit} noValidate>
        <label className="field field-wide">
          <span>Repository URL</span>
          <div className="input-shell"><svg viewBox="0 0 24 24"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.9c0-1.1-.4-2-1-2.6 3.3-.4 6.8-1.6 6.8-7.4 0-1.7-.6-3-1.6-4.1.2-.4.7-2-.2-4 0 0-1.3-.4-4.4 1.6a15.4 15.4 0 0 0-8 0C4.5-1.4 3.2-1 3.2-1c-.9 2-.4 3.6-.2 4C2 4.1 1.4 5.4 1.4 7.1c0 5.8 3.5 7 6.8 7.4-.5.5-.8 1.2-.9 2"/></svg><input value={form.repository_url} onChange={(e) => setForm({ ...form, repository_url: e.target.value })} placeholder="https://github.com/your-org/customer-api" disabled={disabled} /></div>
        </label>
        <label className="field field-wide">
          <span>Engineering task</span>
          <textarea value={form.task} onChange={(e) => setForm({ ...form, task: e.target.value })} placeholder="Add cursor-based pagination to GET /customers and cover it with tests" rows={4} disabled={disabled} />
          <small>{form.task.length} characters · Be specific about the expected outcome</small>
        </label>
        <label className="field branch-field">
          <span>Base branch <em>optional</em></span>
          <div className="input-shell"><svg viewBox="0 0 24 24"><circle cx="6" cy="5" r="2"/><circle cx="18" cy="6" r="2"/><circle cx="6" cy="19" r="2"/><path d="M6 7v10M18 8c0 5-12 3-12 8"/></svg><input value={form.branch} onChange={(e) => setForm({ ...form, branch: e.target.value })} placeholder="main" disabled={disabled} /></div>
        </label>
        <label className="publish-field">
          <input type="checkbox" checked={form.publish_branch} onChange={(e) => setForm({ ...form, publish_branch: e.target.checked })} disabled={disabled} />
          <span><strong>Publish approved branch</strong><small>Commits and pushes only <code>ai/&lt;task-id&gt;</code>; never main.</small></span>
        </label>
        <div className="submit-area">
          {validation && <p className="validation-message">{validation}</p>}
          <button className="run-button" type="submit" disabled={disabled || backendOnline === false}>
            {disabled ? <><span className="button-spinner" />Engineering run in progress</> : <><svg viewBox="0 0 24 24"><path d="m13 2-1 7h7l-9 13 1-8H5l8-12Z"/></svg>Run AI Engineering Team<span>⌘ ↵</span></>}
          </button>
        </div>
      </form>
    </section>
  )
}
