import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getCollectorStatus, getLanguages, getTrending } from '../api/client'
import LanguageBadge from '../components/LanguageBadge'
import Spinner from '../components/Spinner'
import StarsDelta from '../components/StarsDelta'

function HeroFlame() {
  return (
    <svg width="40" height="40" viewBox="0 0 32 32" fill="none">
      <path
        d="M16 2C16 2 7 10 7 19a9 9 0 0 0 18 0c0-3-1.5-6-3.5-8 0 0 .5 4.5-3.5 6.5 0-3-2.5-5.5-2-10z"
        fill="#ff4500"
      />
      <path
        d="M16 19c0 1.7-1.3 3-3 3s-3-1.3-3-3c0-3 3-6 3-6s3 3 3 6z"
        fill="#ff6b35"
      />
    </svg>
  )
}

function StatCard({ label, value, valueClass = 'text-[#e5e5e5]' }) {
  return (
    <div className="bg-card border border-edge rounded-xl px-5 py-4">
      <p className="text-xs text-soft mb-2 uppercase tracking-wider">{label}</p>
      <p className={`text-2xl font-mono font-bold tabular leading-none ${valueClass}`}>
        {value ?? '—'}
      </p>
    </div>
  )
}

function timeAgo(isoString) {
  if (!isoString) return '—'
  const diff = (Date.now() - new Date(isoString).getTime()) / 1000
  if (diff < 60) return 'agora'
  if (diff < 3600) return `há ${Math.floor(diff / 60)} min`
  if (diff < 86400) return `há ${Math.floor(diff / 3600)} h`
  return `há ${Math.floor(diff / 86400)} dias`
}

const STATUS_CLASS = {
  success: 'text-emerald-400',
  error: 'text-lava',
  running: 'text-amber-400',
}

export default function Home() {
  const [languages, setLanguages] = useState([])
  const [loading, setLoading] = useState(true)
  const [collector, setCollector] = useState(null)
  const [trending, setTrending] = useState([])

  useEffect(() => {
    getLanguages()
      .then((d) => setLanguages(d?.data ?? []))
      .finally(() => setLoading(false))
    getCollectorStatus().then(setCollector)
    getTrending(undefined, 7, 5).then((d) => setTrending(d?.data ?? []))
  }, [])

  const totalRepos = languages.reduce((sum, l) => sum + l.repository_count, 0)
  const lastRun = collector?.last_run

  return (
    <div className="space-y-14">
      {/* Hero */}
      <section className="pt-8 pb-4">
        <div className="flex items-center gap-3 mb-5">
          <HeroFlame />
          <h1 className="text-4xl font-bold tracking-tight text-[#e5e5e5]">
            Meridian
          </h1>
        </div>
        <p className="text-soft text-base max-w-xl leading-relaxed">
          Insights sobre repositórios do GitHub por linguagem. Rankings, tendências e métricas atualizadas automaticamente.
        </p>
        <div className="flex gap-3 mt-6">
          <Link
            to="/trending"
            className="px-4 py-2 bg-lava text-white text-sm rounded-lg font-medium hover:bg-lava-hover transition-colors"
          >
            Ver trending
          </Link>
          <Link
            to="/search"
            className="px-4 py-2 bg-card border border-edge text-sm rounded-lg font-medium text-[#e5e5e5] hover:border-lava/50 hover:text-lava transition-colors"
          >
            Buscar repositórios
          </Link>
        </div>
      </section>

      {/* Stats row */}
      <section>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <StatCard
            label="Repositórios monitorados"
            value={totalRepos > 0 ? totalRepos.toLocaleString() : '—'}
          />
          <StatCard
            label="Linguagens ativas"
            value={languages.length > 0 ? languages.length : '—'}
          />
          <StatCard
            label="Última coleta"
            value={timeAgo(lastRun?.finished_at)}
          />
          <StatCard
            label="Status"
            value={lastRun?.status ?? '—'}
            valueClass={STATUS_CLASS[lastRun?.status] ?? 'text-soft'}
          />
        </div>
      </section>

      {/* Trending this week */}
      {trending.length > 0 && (
        <section>
          <div className="flex items-center justify-between mb-4">
            <p className="text-xs uppercase tracking-widest text-soft">
              Em alta esta semana
            </p>
            <Link
              to="/trending"
              className="text-xs text-soft hover:text-lava transition-colors"
            >
              Ver todos
            </Link>
          </div>
          <div className="space-y-2">
            {trending.map((repo, i) => (
              <Link
                key={repo.repository_id}
                to={`/repo/${repo.repository_id}`}
                className="flex items-center gap-4 bg-card border border-edge rounded-xl px-5 py-3.5 hover:border-lava/40 hover:bg-raised transition-all"
              >
                <span className="text-xs font-mono text-soft w-4 shrink-0">
                  {i + 1}
                </span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-[#e5e5e5] truncate">
                    {repo.full_name}
                  </p>
                </div>
                <LanguageBadge language={repo.language} />
                <span className="font-mono text-sm text-soft shrink-0">
                  {repo.stars_count?.toLocaleString()}
                </span>
                <StarsDelta value={repo.stars_delta_7d} className="text-xs shrink-0" />
              </Link>
            ))}
          </div>
        </section>
      )}

      {/* Divider */}
      <div className="border-t border-edge" />

      {/* Languages grid */}
      <section>
        <p className="text-xs uppercase tracking-widest text-soft mb-6">
          Linguagens coletadas
        </p>

        {loading ? (
          <div className="flex justify-center py-20">
            <Spinner size="lg" />
          </div>
        ) : languages.length === 0 ? (
          <div className="text-center py-20 text-soft text-sm">
            Nenhuma linguagem coletada ainda.
            <br />
            <span className="text-xs text-edge mt-1 block">
              Aguarde o primeiro ciclo do collector ou configure a variável LANGUAGES.
            </span>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
            {languages.map(({ language, repository_count, open_positions_count }) => (
              <Link
                key={language}
                to={`/ranking/${language}`}
                className="group bg-card border border-edge rounded-xl p-5 hover:border-lava/40 hover:bg-raised transition-all"
              >
                <div className="mb-4">
                  <LanguageBadge language={language} />
                </div>
                <p className="font-mono text-2xl font-bold text-[#e5e5e5] tabular leading-none">
                  {repository_count.toLocaleString()}
                </p>
                <p className="text-xs text-soft mt-1.5">repos</p>

                <div className="mt-3 pt-3 border-t border-edge">
                  <p className="font-mono text-sm font-semibold text-[#e5e5e5] tabular leading-none">
                    {open_positions_count != null ? open_positions_count.toLocaleString() : '—'}
                  </p>
                  <p className="text-xs text-soft mt-1">vagas abertas</p>
                </div>
              </Link>
            ))}
          </div>
        )}
      </section>
    </div>
  )
}
