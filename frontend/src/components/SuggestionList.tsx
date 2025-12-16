import type { Suggestion } from '../types'

interface Props {
  suggestions: Suggestion[]
}

const priorityStyles: Record<string, string> = {
  high: 'bg-red-900/50 text-red-300 border border-red-800',
  medium: 'bg-yellow-900/50 text-yellow-300 border border-yellow-800',
  low: 'bg-blue-900/50 text-blue-300 border border-blue-800',
}

export function SuggestionList({ suggestions }: Props) {
  if (suggestions.length === 0) return null

  return (
    <div>
      <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">
        Top Suggestions
      </h3>
      <ol className="space-y-2">
        {suggestions.map((s, idx) => (
          <li key={idx} className="flex items-start gap-3 bg-gray-900 rounded-xl border border-gray-800 p-3">
            <span className="text-gray-600 font-mono text-sm font-bold shrink-0 mt-0.5">
              {String(idx + 1).padStart(2, '0')}
            </span>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1 flex-wrap">
                <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${priorityStyles[s.priority]}`}>
                  {s.priority}
                </span>
                <span className="text-xs text-gray-500">{s.category}</span>
              </div>
              <p className="text-sm text-gray-200">{s.message}</p>
            </div>
          </li>
        ))}
      </ol>
    </div>
  )
}
