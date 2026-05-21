import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts'

function formatDate(str) {
  return new Date(str).toLocaleDateString('pt-BR', { month: 'short', day: 'numeric' })
}

function formatK(n) {
  if (n >= 1000) return `${(n / 1000).toFixed(1)}k`
  return String(n)
}

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null
  return (
    <div className="bg-raised border border-edge rounded px-3 py-2 text-xs shadow-lg">
      <p className="text-soft mb-1">{formatDate(label)}</p>
      {payload.map((p) => (
        <p key={p.dataKey} style={{ color: p.color }}>
          {p.name}:{' '}
          <span className="font-mono font-semibold">
            {p.value?.toLocaleString()}
          </span>
        </p>
      ))}
    </div>
  )
}

export default function HistoryChart({ data }) {
  if (!data?.length) return null
  return (
    <ResponsiveContainer width="100%" height={220}>
      <LineChart data={data} margin={{ top: 4, right: 4, bottom: 0, left: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#2a2a2a" vertical={false} />
        <XAxis
          dataKey="snapshot_date"
          tickFormatter={formatDate}
          tick={{ fill: '#737373', fontSize: 11 }}
          axisLine={false}
          tickLine={false}
          interval="preserveStartEnd"
        />
        <YAxis
          tickFormatter={formatK}
          tick={{ fill: '#737373', fontSize: 11 }}
          axisLine={false}
          tickLine={false}
          width={44}
        />
        <Tooltip content={<CustomTooltip />} />
        <Line
          type="monotone"
          dataKey="stars_count"
          name="Estrelas"
          stroke="#ff4500"
          strokeWidth={2}
          dot={false}
          activeDot={{ r: 4, fill: '#ff4500', strokeWidth: 0 }}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}
