interface StatusBadgeProps {
  tone: 'success' | 'danger' | 'warning' | 'neutral' | 'info'
  children: React.ReactNode
  pulse?: boolean
}

export function StatusBadge({ tone, children, pulse = false }: StatusBadgeProps) {
  return <span className={`status-badge status-${tone}${pulse ? ' status-pulse' : ''}`}><i />{children}</span>
}
