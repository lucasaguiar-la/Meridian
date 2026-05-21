export default function StarsDelta({ value, className = '' }) {
  if (value == null) return <span className="text-soft text-xs font-mono">—</span>
  const isPos = value >= 0
  const arrow = isPos ? '↑' : '↓'
  const color = isPos ? 'text-up' : 'text-down'
  const formatted = isPos
    ? `+${value.toLocaleString()}`
    : value.toLocaleString()
  return (
    <span className={`text-xs font-mono tabular ${color} ${className}`}>
      {arrow} {formatted}
    </span>
  )
}
