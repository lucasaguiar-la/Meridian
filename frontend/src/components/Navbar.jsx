import { Link, NavLink } from 'react-router-dom'

function FlameIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
      <path
        d="M12 2C12 2 5 9 5 15a7 7 0 0 0 14 0c0-2.5-1-4.5-2.5-6 0 0 .5 3.5-2.5 5C14 12 12 9 12 2z"
        fill="#ff4500"
      />
      <path
        d="M12 15c0 1.4-1.1 2.5-2.5 2.5S7 16.4 7 15c0-2.5 2.5-5 2.5-5s2.5 2.5 2.5 5z"
        fill="#ff6b35"
      />
    </svg>
  )
}

const linkClass = ({ isActive }) =>
  `text-sm transition-colors ${isActive ? 'text-lava' : 'text-soft hover:text-[#e5e5e5]'}`

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b border-edge bg-card">
      <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link
          to="/"
          className="flex items-center gap-2 hover:opacity-80 transition-opacity"
        >
          <FlameIcon />
          <span className="font-bold text-[#e5e5e5] tracking-widest text-sm uppercase">
            Meridian
          </span>
        </Link>

        <nav className="flex items-center gap-6">
          <NavLink to="/" end className={linkClass}>Home</NavLink>
          <NavLink to="/trending" className={linkClass}>Trending</NavLink>
          <NavLink to="/search" className={linkClass}>Search</NavLink>
        </nav>
      </div>
    </header>
  )
}
