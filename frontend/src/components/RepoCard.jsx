import { Link } from 'react-router-dom'
import LanguageBadge from './LanguageBadge'
import StarsDelta from './StarsDelta'

export default function RepoCard({ repo, deltaKey = 'stars_delta_7d', rank }) {
  const repoId = repo.repository_id ?? repo.id
  const stars = repo.stars_count ?? repo.latest_snapshot?.stars_count
  const delta = repo[deltaKey] ?? repo.stars_delta_7d

  return (
    <Link
      to={`/repo/${repoId}`}
      className="block bg-card border border-edge rounded-lg p-4 hover:border-lava/40 hover:bg-raised transition-all"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            {rank != null && (
              <span className="text-lava font-mono text-xs shrink-0">#{rank}</span>
            )}
            <span className="font-medium text-[#e5e5e5] text-sm truncate">
              {repo.full_name}
            </span>
            <LanguageBadge language={repo.language} />
          </div>
          {repo.description && (
            <p className="text-soft text-xs line-clamp-2 leading-relaxed">
              {repo.description}
            </p>
          )}
        </div>

        <div className="flex flex-col items-end gap-1 shrink-0">
          {stars != null && (
            <span className="font-mono text-sm text-[#e5e5e5] tabular">
              ★ {stars.toLocaleString()}
            </span>
          )}
          <StarsDelta value={delta} />
        </div>
      </div>
    </Link>
  )
}
