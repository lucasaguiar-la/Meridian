const LANG_STYLES = {
  python:     { bg: '#1e3a5f', color: '#4da8da', border: '#2a5280' },
  javascript: { bg: '#3d3000', color: '#f0db4f', border: '#5a4600' },
  typescript: { bg: '#1a2d4a', color: '#5aa3f5', border: '#243e66' },
  go:         { bg: '#003333', color: '#00add8', border: '#005566' },
  rust:       { bg: '#3d1a0a', color: '#f4740b', border: '#5a2910' },
  java:       { bg: '#3d2000', color: '#e76f00', border: '#5a3200' },
  ruby:       { bg: '#3d0a0a', color: '#cc342d', border: '#5a1010' },
  swift:      { bg: '#3d1500', color: '#f05214', border: '#5a2200' },
  kotlin:     { bg: '#2a1a40', color: '#9b72ff', border: '#3d2860' },
  'c++':      { bg: '#001a33', color: '#4d9ecf', border: '#002b52' },
  'c#':       { bg: '#1a2e1a', color: '#5fb85f', border: '#263d26' },
  php:        { bg: '#1e1a3d', color: '#8892be', border: '#2a2552' },
  scala:      { bg: '#3d0a0a', color: '#dc322f', border: '#5a1010' },
  dart:       { bg: '#003340', color: '#0175c2', border: '#00506a' },
  elixir:     { bg: '#2a0a3d', color: '#9b4fc3', border: '#3d1560' },
  haskell:    { bg: '#2a1a40', color: '#5e5086', border: '#3d2860' },
}

const DEFAULT = { bg: '#2a1a0a', color: '#ff4500', border: '#3d2710' }

export default function LanguageBadge({ language, className = '' }) {
  if (!language) return null
  const key = language.toLowerCase()
  const s = LANG_STYLES[key] ?? DEFAULT
  return (
    <span
      className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${className}`}
      style={{ backgroundColor: s.bg, color: s.color, border: `1px solid ${s.border}` }}
    >
      {language}
    </span>
  )
}
