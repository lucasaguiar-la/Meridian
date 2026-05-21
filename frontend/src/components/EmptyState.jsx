export default function EmptyState({ message = 'Nenhum dado encontrado.', hint }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 gap-3 text-center">
      <div className="w-12 h-12 rounded-full border-2 border-edge flex items-center justify-center">
        <span className="text-edge text-xl">○</span>
      </div>
      <p className="text-soft text-sm">{message}</p>
      {hint && <p className="text-xs text-edge max-w-xs leading-relaxed">{hint}</p>}
    </div>
  )
}
