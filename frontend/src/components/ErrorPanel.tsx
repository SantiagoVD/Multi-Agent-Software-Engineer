export function ErrorPanel({ message, onDismiss }: { message: string; onDismiss: () => void }) {
  return <aside className="error-panel" role="alert"><div className="error-icon">!</div><div><strong>Engineering run could not complete</strong><p>{message}</p></div><button onClick={onDismiss} aria-label="Dismiss error">×</button></aside>
}
