import { useEffect, useState } from 'react'
import { searchRepositories, getLanguages } from '../api/client'
import RepoCard from '../components/RepoCard'
import Spinner from '../components/Spinner'
import EmptyState from '../components/EmptyState'

const LIMIT = 20

function SearchIcon() {
  return (
    <svg
      className="absolute left-3 top-1/2 -translate-y-1/2 text-soft pointer-events-none"
      width="15"
      height="15"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="11" cy="11" r="8" />
      <path d="m21 21-4.35-4.35" />
    </svg>
  )
}

export default function Search() {
  const [query, setQuery] = useState('')
  const [language, setLanguage] = useState('')
  const [languages, setLanguages] = useState([])
  const [data, setData] = useState(null)
  const [offset, setOffset] = useState(0)
  const [loading, setLoading] = useState(false)
  const [searched, setSearched] = useState(false)

  useEffect(() => {
    getLanguages().then((r) => setLanguages(r?.data ?? []))
  }, [])

  useEffect(() => {
    if (query.length < 2) {
      setData(null)
      setSearched(false)
      return
    }
    setOffset(0)
    const timer = setTimeout(() => doSearch(query, language, 0), 400)
    return () => clearTimeout(timer)
  }, [query, language])

  useEffect(() => {
    if (query.length >= 2 && searched) doSearch(query, language, offset)
  }, [offset])

  function doSearch(q, lang, off) {
    setLoading(true)
    setSearched(true)
    searchRepositories(q, lang || undefined, LIMIT, off)
      .then((r) => setData(r))
      .finally(() => setLoading(false))
  }

  const repos = data?.data ?? []
  const total = data?.meta?.total ?? 0
  const hasNext = offset + LIMIT < total
  const hasPrev = offset > 0

  return (
    <div className="space-y-6">
      <h1 className="text-lg font-semibold text-[#e5e5e5]">Buscar Repositórios</h1>

      {/* Search controls */}
      <div className="flex gap-3 flex-wrap">
        <div className="relative flex-1 min-w-56">
          <SearchIcon />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Buscar por nome ou descrição..."
            className="w-full bg-card border border-edge rounded-lg pl-9 pr-4 py-2.5 text-sm text-[#e5e5e5] placeholder:text-soft focus:border-lava focus:outline-none transition-colors"
          />
        </div>

        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="bg-card border border-edge rounded-lg px-3 py-2.5 text-sm text-[#e5e5e5] focus:border-lava focus:outline-none transition-colors"
        >
          <option value="">Todas linguagens</option>
          {languages.map((l) => (
            <option key={l.language} value={l.language}>
              {l.language}
            </option>
          ))}
        </select>
      </div>

      {/* Results */}
      {loading ? (
        <div className="flex justify-center py-20">
          <Spinner size="lg" />
        </div>
      ) : !searched ? (
        <p className="text-center py-20 text-soft text-sm">
          Digite pelo menos 2 caracteres para buscar.
        </p>
      ) : repos.length === 0 ? (
        <EmptyState message={`Nenhum resultado para "${query}".`} />
      ) : (
        <>
          <p className="text-xs text-soft">
            {total.toLocaleString()} resultado{total !== 1 ? 's' : ''}
          </p>

          <div className="grid gap-3">
            {repos.map((repo) => (
              <RepoCard key={repo.id} repo={repo} />
            ))}
          </div>

          {/* Pagination */}
          {(hasPrev || hasNext) && (
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
          )}
        </>
      )}
    </div>
  )
}
