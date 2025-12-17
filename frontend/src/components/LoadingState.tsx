import { Loader2 } from 'lucide-react'

export function LoadingState() {
  return (
    <div className="mt-8 space-y-6">
      <div className="flex flex-col items-center gap-3 py-4">
        <Loader2 size={32} className="animate-spin text-blue-400" />
        <p className="text-gray-400 text-sm">
          Analyzing your code
          <span className="animate-pulse">...</span>
        </p>
      </div>

      {/* Skeleton ScoreCard */}
      <div className="flex justify-center">
        <div className="w-48 h-48 rounded-full bg-gray-800 animate-pulse" />
      </div>

      {/* Skeleton CategoryPanel */}
      <div className="grid grid-cols-2 gap-4">
        {[0, 1, 2, 3].map(i => (
          <div key={i} className="bg-gray-800 rounded-xl p-4 h-24 animate-pulse" />
        ))}
      </div>

      {/* Skeleton suggestions */}
      <div className="space-y-3">
        {[0, 1, 2].map(i => (
          <div key={i} className="bg-gray-800 rounded-xl p-4 h-12 animate-pulse" />
        ))}
      </div>
    </div>
  )
}
