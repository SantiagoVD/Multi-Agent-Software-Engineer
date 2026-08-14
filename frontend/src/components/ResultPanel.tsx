import type { FinalResult, IssueSeverity } from '../api/types'
import { StatusBadge } from './StatusBadge'

const severityTone: Record<IssueSeverity, string> = { low: 'sev-low', medium: 'sev-medium', high: 'sev-high', critical: 'sev-critical' }

export function ResultPanel({ result }: { result: FinalResult }) {
  const tests = result.test_result
  const review = result.review_result
  return (
    <section className="result-section" aria-live="polite">
      <div className="result-hero">
        <div className={`result-symbol ${result.success ? 'result-success' : 'result-failed'}`}>{result.success ? '✓' : '×'}</div>
        <div className="result-copy"><span className="eyebrow">RUN COMPLETE · {result.task_id}</span><h2>{result.success ? 'Engineering task completed' : 'Workflow ended with an issue'}</h2><p>{result.summary}</p></div>
        <div className="result-meta"><StatusBadge tone={result.success ? 'success' : 'danger'}>{result.status.replaceAll('_', ' ')}</StatusBadge><span><strong>{result.iterations}</strong> iteration{result.iterations === 1 ? '' : 's'}</span></div>
      </div>

      <div className="result-grid">
        <article className="result-card files-card">
          <div className="result-card-title"><span>⌘</span><div><h3>Files modified</h3><p>{result.files_modified.length} reported by the workflow</p></div></div>
          {result.files_modified.length ? <ul className="file-list">{result.files_modified.map((file) => <li key={file}><span>M</span><code>{file}</code></li>)}</ul> : <p className="empty-state">No modified files were reported.</p>}
        </article>

        <article className="result-card tests-card">
          <div className="result-card-title"><span>✓</span><div><h3>Test results</h3><p>{tests ? tests.command : 'No test result returned'}</p></div></div>
          {tests ? <>
            <div className="test-stats"><div><strong>{tests.passed}</strong><span>Passed</span></div><div><strong>{tests.failed}</strong><span>Failed</span></div><div><strong>{tests.skipped}</strong><span>Skipped</span></div></div>
            <div className="test-footer"><StatusBadge tone={tests.success ? 'success' : tests.timed_out ? 'warning' : 'danger'}>{tests.timed_out ? 'Timed out' : tests.success ? 'All checks passed' : tests.available ? 'Checks failed' : 'Tool unavailable'}</StatusBadge></div>
            {tests.issues.length > 0 && <ul className="issue-list">{tests.issues.map((issue, index) => <li key={`${issue.message}-${index}`}><strong>{issue.test_name ?? 'Test issue'}</strong><span>{issue.message}</span></li>)}</ul>}
          </> : <p className="empty-state">The workflow did not reach or report the testing phase.</p>}
        </article>
      </div>

      <article className="result-card review-card">
        <div className="result-card-title"><span>◇</span><div><h3>Code review</h3><p>{review?.summary ?? 'No review result returned'}</p></div>{review && <StatusBadge tone={review.status === 'approved' ? 'success' : 'warning'}>{review.status.replace('_', ' ')}</StatusBadge>}</div>
        {review?.issues.length ? <div className="review-issues">{review.issues.map((issue, index) => <div className="review-issue" key={`${issue.description}-${index}`}><span className={`severity ${severityTone[issue.severity]}`}>{issue.severity}</span><div><strong>{issue.file ? `${issue.file}${issue.line ? `:${issue.line}` : ''}` : 'General finding'}</strong><p>{issue.description}</p>{issue.recommendation && <small>Recommendation · {issue.recommendation}</small>}</div></div>)}</div> : review ? <p className="empty-state review-clean">No review issues were reported.</p> : null}
      </article>

      {result.iterations > 1 && <div className="iteration-note"><strong>{result.iterations} workflow iterations</strong><span>The backend returned the final result only; per-agent retry events are not available in V1.</span></div>}
    </section>
  )
}
