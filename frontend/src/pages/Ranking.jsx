import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { getRanking, getLanguages } from '../api/client'
import LanguageBadge from '../components/LanguageBadge'
import StarsDelta from '../components/StarsDelta'
import MetricBar from '../components/MetricBar'
import Spinner from '../components/Spinner'
import EmptyState from '../components/EmptyState'

const METRICS = [
  { key: 'stars', label: 'Estrelas' },
  { key: 'engagement', label: 'Engajamento' },
  { key: 'growth', label: 'Crescimento' },
]

const LIMIT = 20

export default function Ranking() {
  const { language } = useParams()
  const navigate = useNavigate()
  const [metric, setMetric] = useState('stars')
  const [offset, setOffset] = useState(0)
  const [data, setData] = useState(null)
  const [languages, setLanguages] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getLanguages().then((r) => setLanguages(r?.data ?? []))
  }, [])

  useEffect(() => {
    setOffset(0)
  }, [language, metric])

  useEffect(() => {
    setLoading(true)
    getRanking(language, metric, LIMIT, offset)
      .then((r) => setData(r))
      .finally(() => setLoading(false))
  }, [language, metric, offset])

  const repos = data?.data ?? []
  const total = data?.meta?.total ?? 0
  const hasNext = offset + LIMIT < total
  const hasPrev = offset > 0

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row gap-4 sm:items-center">
        <div className="flex items-center gap-3">
          <LanguageBadge language={language} className="text-sm px-3 py-1" />
          <h1 className="text-lg font-semibold text-[#e5e5e5]">Ranking</h1>
        </div>

        <div className="flex flex-wrap gap-3 sm:ml-auto">
          {/* Language selector */}
          <select
            value={language}
            onChange={(e) => navigate(`/ranking/${e.target.value}`)}
            className="bg-card border border-edge rounded-lg px-3 py-1.5 text-sm text-[#e5e5e5] focus:border-lava focus:outline-none transition-colors"
          >
            {languages.map((l) => (
              <option key={l.language} value={l.language}>
                {l.language}
              </option>
            ))}
          </select>

          {/* Metric tabs */}
          <div className="flex gap-0.5 bg-raised border border-edge rounded-lg p-0.5">
            {METRICS.map((m) => (
              <button
                key={m.key}
                onClick={() => setMetric(m.key)}
                className={`px-3 py-1 text-xs rounded transition-all ${
                  metric === m.key
                    ? 'bg-lava text-white'
                    : 'text-soft hover:text-[#e5e5e5]'
                }`}
              >
                {m.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Content */}
      {loading ? (
        <div className="flex justify-center py-20">
          <Spinner size="lg" />
        </div>
      ) : repos.length === 0 ? (
        <EmptyState
          message={`Nenhum repositório coletado para ${language} ainda.`}
          hint="Verifique se a linguagem está na lista LANGUAGES e aguarde um ciclo de coleta."
        />
      ) : (
        <>
          <div className="overflow-x-auto">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="border-b border-edge">
                  <th className="text-left py-3 pr-4 text-xs uppercase tracking-wider text-soft font-medium w-8">
                    #
                  </th>
                  <th className="text-left py-3 pr-4 text-xs uppercase tracking-wider text-soft font-medium">
                    Repositório
                  </th>
                  <th className="text-right py-3 pr-4 text-xs uppercase tracking-wider text-soft font-medium hidden sm:table-cell">
                    Estrelas
                  </th>
                  <th className="text-right py-3 pr-4 text-xs uppercase tracking-wider text-soft font-medium hidden md:table-cell">
                    Forks
                  </th>
                  <th className="text-right py-3 pr-4 text-xs uppercase tracking-wider text-soft font-medium hidden lg:table-cell">
                    Issues
                  </th>
                  <th className="py-3 pr-4 text-xs uppercase tracking-wider text-soft font-medium hidden md:table-cell w-36">
                    Score
                  </th>
                  <th className="text-right py-3 text-xs uppercase tracking-wider text-soft font-medium hidden sm:table-cell">
                    30d
                  </th>
                </tr>
              </thead>
              <tbody>
                {repos.map((repo, i) => {
                  const snap = repo.latest_snapshot
                  return (
                    <tr
                      key={repo.id}
                      className="border-b border-edge hover:bg-raised transition-colors"
                    >
                      <td className="py-3 pr-4">
                        <span className="text-xs font-mono text-soft tabular">
                          {offset + i + 1}
                        </span>
                      </td>
                      <td className="py-3 pr-4">
                        <Link to={`/repo/${repo.id}`}>
                          <span className="font-medium text-[#e5e5e5] hover:text-lava transition-colors">
                            {repo.full_name}
                          </span>
                          {repo.description && (
                            <p className="text-xs text-soft mt-0.5 line-clamp-1">
                              {repo.description}
                            </p>
                          )}
                        </Link>
                      </td>
                      <td className="py-3 pr-4 text-right hidden sm:table-cell">
                        <span className="font-mono text-[#e5e5e5] tabular">
                          {snap?.stars_count?.toLocaleString() ?? '—'}
                        </span>
                      </td>
                      <td className="py-3 pr-4 text-right hidden md:table-cell">
                        <span className="font-mono text-soft tabular">
                          {snap?.forks_count?.toLocaleString() ?? '—'}
                        </span>
                      </td>
                      <td className="py-3 pr-4 text-right hidden lg:table-cell">
                        <span className="font-mono text-soft tabular">
                          {snap?.open_issues_count?.toLocaleString() ?? '—'}
                        </span>
                      </td>
                      <td className="py-3 pr-4 hidden md:table-cell">
                        <MetricBar value={snap?.engagement_score} />
                      </td>
                      <td className="py-3 text-right hidden sm:table-cell">
                        <StarsDelta value={snap?.stars_delta_30d} />
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-between pt-1">
            <p className="text-xs text-soft">
              {offset + 1}–{Math.min(offset + LIMIT, total)} de {total.toLocaleString()}
            </p>
            <div className="flex gap-2">
              <button
                disabled={!hasPrev}
                onClick={() => setOffset((o) => Math.max(0, o - LIMIT))}
                className="px-3 py-1.5 text-xs border border-edge rounded-lg disabled:opacity-30 hover:border-lava/50 hover:text-lava transition-all disabled:cursor-not-allowed"
              >
                ← Anterior
              </button>
              <button
                disabled={!hasNext}
                onClick={() => setOffset((o) => o + LIMIT)}
                className="px-3 py-1.5 text-xs border border-edge rounded-lg disabled:opacity-30 hover:border-lava/50 hover:text-lava transition-all disabled:cursor-not-allowed"
              >
                Próximo →
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
