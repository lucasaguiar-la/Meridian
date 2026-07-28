const BASE = import.meta.env.VITE_API_URL ?? '/api'

async function request(path, params = {}) {
  const url = new URL(BASE + path, window.location.origin)
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') url.searchParams.set(k, v)
  })
  const res = await fetch(url.toString())
  if (!res.ok) {
    if (res.status === 404) return null
    throw new Error(`API error ${res.status}: ${path}`)
  }
  return res.json()
}

async function requestPost(path, body = {}) {
  const url = new URL(BASE + path, window.location.origin)
  const res = await fetch(url.toString(), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) throw new Error(`API error ${res.status}: ${path}`)
  return res.json()
}

export const getLanguages = () =>
  request('/languages')

export const getRanking = (lang, metric = 'stars', limit = 20, offset = 0) =>
  request(`/languages/${lang}/ranking`, { metric, limit, offset })

export const getRepository = (id) =>
  request(`/repositories/${id}`)

export const getRepositoryHistory = (id, days = 90) =>
  request(`/repositories/${id}/history`, { days })

export const searchRepositories = (q, language, limit = 20, offset = 0) =>
  request('/repositories/search/', { q, language, limit, offset })

export const getTrending = (language, days = 7, limit = 30) =>
  request('/reports/trending', { language, days, limit })

export const getHealth = () =>
  request('/health')

export const getCollectorStatus = () =>
  request('/collector/status')

export const getWeeklyReport = (language, period) =>
  request('/reports/weekly', { language, period })

export const getMonthlyReport = (language, period) =>
  request('/reports/monthly', { language, period })

export const generateReport = (reportType, language, allLanguages = false) =>
  requestPost('/reports/generate', {
    report_type: reportType,
    language: language || null,
    all_languages: allLanguages,
  })
