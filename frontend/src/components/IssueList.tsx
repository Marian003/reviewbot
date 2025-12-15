import { useState } from 'react'
import type { Issue } from '../types'

interface Props {
  issues: Issue[]
}

const severityStyles: Record<string, string> = {
  critical: 'bg-red-900/50 text-red-300 border border-red-700',
  warning: 'bg-yellow-900/50 text-yellow-300 border border-yellow-700',
  info: 'bg-blue-900/50 text-blue-300 border border-blue-700',
}

export function IssueList({ issues }: Props) {
  const [showAll, setShowAll] = useState(false)
  const visible = showAll ? issues : issues.slice(0, 3)
  const remaining = issues.length - 3

  if (issues.length === 0) {
    return <p className="text-green-400 text-sm py-2">No issues found.</p>
  }

  return (
    <div className="space-y-2">
      {visible.map((issue, idx) => (
        <div key={idx} className="rounded-lg bg-gray-900 border border-gray-800 p-3 space-y-1">
          <div className="flex items-start gap-2">
            <span className={`text-xs px-2 py-0.5 rounded-full font-medium shrink-0 ${severityStyles[issue.severity]}`}>
              {issue.severity}
            </span>
            {issue.line !== null && (
              <span className="text-xs text-gray-500 font-mono shrink-0 mt-0.5">L{issue.line}</span>
            )}
            <span className="text-sm text-gray-200">{issue.message}</span>
          </div>
          {issue.fix && (
            <p className="text-xs text-green-400 ml-2 pl-2 border-l border-green-800">
              Fix: {issue.fix}
            </p>
          )}
        </div>
      ))}

      {!showAll && remaining > 0 && (
        <button
          onClick={() => setShowAll(true)}
          className="text-xs text-blue-400 hover:text-blue-300 transition-colors"
        >
          Show {remaining} more issue{remaining !== 1 ? 's' : ''}
        </button>
      )}
    </div>
  )
}
