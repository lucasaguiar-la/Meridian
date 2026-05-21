import { useEffect, useState } from 'react'
import { getTrending, getLanguages } from '../api/client'
import RepoCard from '../components/RepoCard'
import Spinner from '../components/Spinner'
import EmptyState from '../components/EmptyState'

const DAYS_OPTIONS = [
  { value: 7, label: '7 dias' },
  { value: 30, label: '30 dias' },
]

export default function Trending() {
  const [days, setDays] = useState(7)
  const [language, setLanguage] = useState('')
  const [languages, setLanguages] = useState([])
  const [repos, setRepos] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getLanguages().then((r) => setLanguages(r?.data ?? []))
  }, [])

  useEffect(() => {
    setLoading(true)
    getTrending(language || undefined, days, 30)
      .then((r) => setRepos(r?.data ?? []))
      .finally(() => setLoading(false))
  }, [days, language])

  const deltaKey = days <= 7 ? 'stars_delta_7d' : 'stars_delta_30d'

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row gap-4 sm:items-center">
        <div>
          <h1 className="text-lg font-semibold text-[#e5e5e5]">Trending</h1>
          <p className="text-xs text-soft mt-0.5">
            Repositórios com maior crescimento de estrelas
          </p>
        </div>

        <div className="flex flex-wrap gap-2 sm:ml-auto">
          {/* Period selector */}
          <div className="flex gap-0.5 bg-raised border border-edge rounded-lg p-0.5">
            {DAYS_OPTIONS.map((opt) => (
              <button
                key={opt.value}
                onClick={() => setDays(opt.value)}
                className={`px-3 py-1 text-xs rounded transition-all ${
                  days === opt.value
                    ? 'bg-lava text-white'
                    : 'text-soft hover:text-[#e5e5e5]'
                }`}
              >
                {opt.label}
              </button>
            ))}
          </div>

          {/* Language filter */}
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="bg-card border border-edge rounded-lg px-3 py-1 text-sm text-[#e5e5e5] focus:border-lava focus:outline-none transition-colors"
          >
            <option value="">Todas linguagens</option>
            {languages.map((l) => (
              <option key={l.language} value={l.language}>
                {l.language}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Content */}
      {loading ? (
        <div className="flex justify-center py-20">
          <Spinner size="lg" />
        </div>
      ) : repos.length === 0 ? (
        <EmptyState
          message="Nenhum repositório em trending."
          hint="Os deltas de estrelas são calculados após o segundo ciclo de coleta. Aguarde algumas horas."
        />
      ) : (
        <div className="grid gap-3">
          {repos.map((repo, i) => (
            <RepoCard
              key={repo.repository_id}
              repo={repo}
              rank={i + 1}
              deltaKey={deltaKey}
            />
          ))}
        </div>
      )}
    </div>
  )
}
