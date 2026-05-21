export default function Spinner({ size = 'md' }) {
  const s = { sm: 'w-4 h-4', md: 'w-7 h-7', lg: 'w-10 h-10' }[size] ?? 'w-7 h-7'
  return (
    <div className={`${s} border-2 border-edge border-t-lava rounded-full animate-spin`} />
  )
}
