import { useEffect, useState } from 'react'
import {
  generateReport,
  getLanguages,
  getMonthlyReport,
  getWeeklyReport,
} from '../api/client'
import RepoCard from '../components/RepoCard'
import Spinner from '../components/Spinner'
import EmptyState from '../components/EmptyState'

const TYPE_OPTIONS = [
  { value: 'weekly', label: 'Semanal' },
  { value: 'monthly', label: 'Mensal' },
]

const SECTIONS = [
  { key: 'top_by_stars', title: 'Top por estrelas' },
  { key: 'top_by_engagement', title: 'Top por engajamento' },
  { key: 'top_by_growth', title: 'Top por crescimento' },
]

export default function Reports() {
  const [reportType, setReportType] = useState('weekly')
  const [language, setLanguage] = useState('')
  const [languages, setLanguages] = useState([])
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)

  useEffect(() => {
    getLanguages().then((r) => setLanguages(r?.data ?? []))
  }, [])

  function fetchReport() {
    setLoading(true)
    const fetcher = reportType === 'weekly' ? getWeeklyReport : getMonthlyReport
    return fetcher(language || undefined)
      .then(setReport)
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    fetchReport()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [reportType, language])

  function handleGenerate() {
    setGenerating(true)
    generateReport(reportType, language || undefined)
      .then(fetchReport)
      .finally(() => setGenerating(false))
  }

  const deltaKey = reportType === 'weekly' ? 'stars_delta_7d' : 'stars_delta_30d'
  const content = report?.content_json

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row gap-4 sm:items-center">
        <div>
          <h1 className="text-lg font-semibold text-[#e5e5e5]">Relatórios</h1>
          <p className="text-xs text-soft mt-0.5">
            Resumo periódico dos repositórios monitorados
          </p>
        </div>

        <div className="flex flex-wrap gap-2 sm:ml-auto">
          {/* Type selector */}
          <div className="flex gap-0.5 bg-raised border border-edge rounded-lg p-0.5">
            {TYPE_OPTIONS.map((opt) => (
              <button
                key={opt.value}
                onClick={() => setReportType(opt.value)}
                className={`px-3 py-1 text-xs rounded transition-all ${
                  reportType === opt.value
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
      ) : !content ? (
        <div className="space-y-4">
          <EmptyState
            message="Nenhum relatório gerado ainda."
            hint="Relatórios são gerados automaticamente às segundas-feiras (semanal) e no dia 1 de cada mês (mensal). Você também pode gerar um agora."
          />
          <div className="flex justify-center">
            <button
              onClick={handleGenerate}
              disabled={generating}
              className="px-4 py-2 bg-lava text-white text-sm rounded-lg font-medium hover:bg-lava-hover transition-colors disabled:opacity-50 flex items-center gap-2"
            >
              {generating && <Spinner size="sm" />}
              Gerar relatório agora
            </button>
          </div>
        </div>
      ) : (
        <div className="space-y-8">
          <div className="flex flex-wrap gap-4 text-xs text-soft">
            <span>
              Período: {content.period_start} a {content.period_end}
            </span>
            <span>Repositórios monitorados: {content.repos_tracked}</span>
          </div>

          {SECTIONS.map((section) => {
            const repos = content[section.key] ?? []
            return (
              <div key={section.key} className="space-y-3">
                <h2 className="text-sm font-semibold text-[#e5e5e5]">
                  {section.title}
                </h2>
                {repos.length === 0 ? (
                  <p className="text-xs text-soft">Sem dados para este período.</p>
                ) : (
                  <div className="grid gap-3">
                    {repos.map((repo) => (
                      <RepoCard
                        key={`${section.key}-${repo.repository_id}`}
                        repo={repo}
                        rank={repo.rank}
                        deltaKey={deltaKey}
                      />
                    ))}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
