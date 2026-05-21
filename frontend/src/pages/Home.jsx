import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getLanguages } from '../api/client'
import LanguageBadge from '../components/LanguageBadge'
import Spinner from '../components/Spinner'

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

export default function Home() {
  const [languages, setLanguages] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getLanguages()
      .then((d) => setLanguages(d?.data ?? []))
      .finally(() => setLoading(false))
  }, [])

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
            {languages.map(({ language, repository_count }) => (
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
              </Link>
            ))}
          </div>
        )}
      </section>
    </div>
  )
}
