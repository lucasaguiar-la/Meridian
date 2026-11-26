import { Link, NavLink } from 'react-router-dom'

const linkClass = ({ isActive }) =>
  `text-sm transition-colors ${isActive ? 'text-lava' : 'text-soft hover:text-paper'}`

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b border-edge bg-card">
      <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link
          to="/"
          className="flex items-center hover:opacity-80 transition-opacity"
          aria-label="Meridian - Home"
        >
          <img
            src="/logo/svg/horizontal/meridian-horizontal-reverse.svg"
            alt="Meridian"
            className="h-8 w-auto"
          />
        </Link>

        <nav className="flex items-center gap-6">
          <NavLink to="/" end className={linkClass}>Home</NavLink>
          <NavLink to="/trending" className={linkClass}>Trending</NavLink>
          <NavLink to="/reports" className={linkClass}>Relatórios</NavLink>
          <NavLink to="/search" className={linkClass}>Search</NavLink>
        </nav>
      </div>
    </header>
  )
}
