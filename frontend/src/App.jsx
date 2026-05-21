import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Ranking from './pages/Ranking'
import Trending from './pages/Trending'
import RepoDetail from './pages/RepoDetail'
import Search from './pages/Search'

export default function App() {
  return (
    <div className="min-h-screen bg-canvas text-[#e5e5e5]">
      <Navbar />
      <main className="max-w-6xl mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/ranking/:language" element={<Ranking />} />
          <Route path="/trending" element={<Trending />} />
          <Route path="/repo/:id" element={<RepoDetail />} />
          <Route path="/search" element={<Search />} />
        </Routes>
      </main>
    </div>
  )
}
