export default function MetricBar({ value, max = 15 }) {
  if (value == null) return <span className="text-xs font-mono text-soft">—</span>
  const pct = Math.min(100, (value / max) * 100)
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1 bg-edge rounded-full overflow-hidden">
        <div
          className="h-full bg-lava rounded-full transition-all"
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="text-xs font-mono text-soft tabular w-9 text-right shrink-0">
        {value.toFixed(1)}
      </span>
    </div>
  )
}
