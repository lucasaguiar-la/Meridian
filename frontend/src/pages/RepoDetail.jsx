import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getRepository, getRepositoryHistory } from '../api/client'
import LanguageBadge from '../components/LanguageBadge'
import StarsDelta from '../components/StarsDelta'
import HistoryChart from '../components/HistoryChart'
import Spinner from '../components/Spinner'

function MetricCard({ label, value, muted = false }) {
  return (
    <div className="bg-card border border-edge rounded-xl px-5 py-4">
      <p className="text-xs text-soft mb-2 uppercase tracking-wider">{label}</p>
      <p
        className={`text-2xl font-mono font-bold tabular leading-none ${
          muted ? 'text-soft' : 'text-[#e5e5e5]'
        }`}
      >
        {value ?? '—'}
      </p>
    </div>
  )
}

function GitHubIcon() {
  return (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
    </svg>
  )
}

const PERIOD_OPTIONS = [30, 90, 180, 365]

export default function RepoDetail() {
  const { id } = useParams()
  const [repo, setRepo] = useState(null)
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)
  const [historyLoading, setHistoryLoading] = useState(false)
  const [days, setDays] = useState(90)

  useEffect(() => {
    setLoading(true)
    getRepository(id).then(r => setRepo(r)).finally(() => setLoading(false))
  }, [id])

  useEffect(() => {
    setHistoryLoading(true)
    getRepositoryHistory(id, days)
      .then(h => setHistory(h?.data ?? []))
      .finally(() => setHistoryLoading(false))
  }, [id, days])

  if (loading) {
    return (
      <div className="flex justify-center py-20">
        <Spinner size="lg" />
      </div>
    )
  }

  if (!repo) {
    return (
      <div className="text-center py-20 text-soft text-sm">
        Repositório não encontrado.{' '}
        <Link to="/" className="text-lava hover:underline">
          Voltar ao início
        </Link>
      </div>
    )
  }

  const snap = repo.latest_snapshot

  return (
    <div className="space-y-6">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-1.5 text-xs text-soft">
        <Link to="/" className="hover:text-lava transition-colors">
          Home
        </Link>
        {repo.language && (
          <>
            <span className="text-edge">›</span>
            <Link
              to={`/ranking/${repo.language.toLowerCase()}`}
              className="hover:text-lava transition-colors"
            >
              {repo.language}
            </Link>
          </>
        )}
        <span className="text-edge">›</span>
        <span className="text-[#e5e5e5] truncate max-w-xs">{repo.name}</span>
      </nav>

      {/* Repo header */}
      <div className="border-b border-edge pb-6">
        <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <div className="flex flex-wrap items-center gap-2 mb-2">
              <h1 className="text-2xl font-bold text-[#e5e5e5] break-all">
                {repo.full_name}
              </h1>
              <LanguageBadge language={repo.language} />
              {repo.is_fork && (
                <span className="text-xs text-soft border border-edge px-2 py-0.5 rounded-full">
                  fork
                </span>
              )}
            </div>
            {repo.description && (
              <p className="text-soft text-sm leading-relaxed max-w-2xl">
                {repo.description}
              </p>
            )}
          </div>

          {repo.html_url && (
            <a
              href={repo.html_url}
              target="_blank"
              rel="noopener noreferrer"
              className="shrink-0 flex items-center gap-2 px-4 py-2 bg-card border border-edge rounded-lg text-sm text-[#e5e5e5] hover:border-lava/50 hover:text-lava transition-all"
            >
              <GitHubIcon />
              GitHub
            </a>
          )}
        </div>
      </div>

      {/* Metrics */}
      {snap && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <MetricCard label="Estrelas" value={snap.stars_count?.toLocaleString()} />
          <MetricCard label="Forks" value={snap.forks_count?.toLocaleString()} />
          <MetricCard
            label="Issues abertas"
            value={snap.open_issues_count?.toLocaleString()}
            muted
          />
          <MetricCard
            label="Eng. Score"
            value={snap.engagement_score?.toFixed(2)}
          />
        </div>
      )}

      {/* Star deltas */}
      {snap && (snap.stars_delta_7d != null || snap.stars_delta_30d != null) && (
        <div className="flex flex-wrap gap-3">
          {snap.stars_delta_7d != null && (
            <div className="flex items-center gap-3 bg-card border border-edge rounded-lg px-4 py-2.5">
              <span className="text-xs text-soft">Últimos 7 dias</span>
              <StarsDelta value={snap.stars_delta_7d} className="text-sm" />
            </div>
          )}
          {snap.stars_delta_30d != null && (
            <div className="flex items-center gap-3 bg-card border border-edge rounded-lg px-4 py-2.5">
              <span className="text-xs text-soft">Últimos 30 dias</span>
              <StarsDelta value={snap.stars_delta_30d} className="text-sm" />
            </div>
          )}
        </div>
      )}

      {/* History chart */}
      <div className="bg-card border border-edge rounded-xl p-5">
        <div className="flex items-center justify-between mb-5">
          <p className="text-xs uppercase tracking-widest text-soft">
            Histórico de estrelas
          </p>
          <div className="flex gap-1">
            {PERIOD_OPTIONS.map(d => (
              <button
                key={d}
                onClick={() => setDays(d)}
                className={`text-xs px-2.5 py-1 rounded-md transition-colors ${
                  days === d
                    ? 'bg-lava text-white'
                    : 'text-soft border border-edge hover:text-[#e5e5e5] hover:border-lava/50'
                }`}
              >
                {d}d
              </button>
            ))}
          </div>
        </div>
        {historyLoading ? (
          <div className="flex justify-center py-10">
            <Spinner />
          </div>
        ) : history.length > 1 ? (
          <HistoryChart data={history} />
        ) : (
          <p className="text-center text-soft text-xs py-10">
            Sem dados suficientes para o período selecionado.
          </p>
        )}
      </div>

      {/* Meta info */}
      <div className="bg-card border border-edge rounded-xl p-5 text-xs text-soft space-y-2">
        {repo.owner_login && (
          <p>
            Criado por{' '}
            <span className="text-[#e5e5e5] font-medium">@{repo.owner_login}</span>
          </p>
        )}
        {repo.created_at && (
          <p>
            Data de criação:{' '}
            <span className="text-[#e5e5e5]">
              {new Date(repo.created_at).toLocaleDateString('pt-BR', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
            </span>
          </p>
        )}
        <p>
          GitHub ID:{' '}
          <span className="font-mono text-[#e5e5e5]">{repo.id}</span>
        </p>
      </div>
    </div>
  )
}
