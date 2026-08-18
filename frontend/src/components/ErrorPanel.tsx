export function ErrorPanel({ message, onDismiss }: { message: string; onDismiss: () => void }) {
  return <aside className="error-panel" role="alert"><div className="error-icon">!</div><div><strong>No se pudo completar la tarea de ingeniería</strong><p>{message}</p></div><button onClick={onDismiss} aria-label="Cerrar error">×</button></aside>
}
