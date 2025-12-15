import { useState } from 'react'
import { Shield, Activity, Paintbrush, Bug } from 'lucide-react'
import type { SecurityResult, ComplexityResult, StyleResult, BugResult, Issue } from '../types'
import { IssueList } from './IssueList'

interface CategoryCard {
  name: string
  icon: React.ReactNode
  score: number
  issues: Issue[]
  color: string
  extraInfo?: React.ReactNode
}

interface Props {
  security: SecurityResult
  complexity: ComplexityResult
  style: StyleResult
  bugs: BugResult
}

function scoreColor(score: number): string {
  if (score >= 80) return '#22c55e'
  if (score >= 60) return '#eab308'
  if (score >= 40) return '#f97316'
  return '#ef4444'
}

export function CategoryPanel({ security, complexity, style, bugs }: Props) {
  const [expanded, setExpanded] = useState<string | null>(null)

  const cards: CategoryCard[] = [
    {
      name: 'Security',
      icon: <Shield size={20} />,
      score: security.score,
      issues: security.issues,
      color: scoreColor(security.score),
      extraInfo: (
        <span className="text-xs text-gray-500">
          {security.passed_checks}/{security.total_checks} checks passed
        </span>
      ),
    },
    {
      name: 'Complexity',
      icon: <Activity size={20} />,
      score: complexity.score,
      issues: [],
      color: scoreColor(complexity.score),
      extraInfo: (
        <span className="text-xs text-gray-500">
          CC={complexity.cyclomatic} · Nest={complexity.max_nesting} · {complexity.functions} fn
        </span>
      ),
    },
    {
      name: 'Style',
      icon: <Paintbrush size={20} />,
      score: style.score,
      issues: style.issues,
      color: scoreColor(style.score),
    },
    {
      name: 'Bugs',
      icon: <Bug size={20} />,
      score: bugs.score,
      issues: bugs.issues,
      color: scoreColor(bugs.score),
    },
  ]

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
      {cards.map(card => {
        const isExpanded = expanded === card.name
        const criticalCount = card.issues.filter(i => i.severity === 'critical').length
        const totalIssues = card.issues.length

        return (
          <div
            key={card.name}
            className={`bg-gray-900 rounded-xl border transition-all duration-200 cursor-pointer ${
              isExpanded ? 'border-blue-500/50' : 'border-gray-800 hover:border-gray-600'
            }`}
            onClick={() => setExpanded(isExpanded ? null : card.name)}
          >
            <div className="p-4">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2" style={{ color: card.color }}>
                  {card.icon}
                  <span className="font-semibold text-white">{card.name}</span>
                </div>
                <div className="flex items-center gap-2">
                  {totalIssues > 0 && (
                    <span className={`text-xs px-2 py-0.5 rounded-full ${
                      criticalCount > 0 ? 'bg-red-900/50 text-red-300' : 'bg-yellow-900/50 text-yellow-300'
                    }`}>
                      {totalIssues} issue{totalIssues !== 1 ? 's' : ''}
                    </span>
                  )}
                  <span className="text-2xl font-bold" style={{ color: card.color }}>
                    {card.score}
                  </span>
                </div>
              </div>

              {/* Progress bar */}
              <div className="w-full bg-gray-800 rounded-full h-1.5 mb-2">
                <div
                  className="h-1.5 rounded-full transition-all duration-500"
                  style={{ width: `${card.score}%`, backgroundColor: card.color }}
                />
              </div>

              {card.extraInfo}
            </div>

            {isExpanded && (card.name === 'Complexity' ? (
              <div className="px-4 pb-4 border-t border-gray-800 pt-3">
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div className="bg-gray-800 rounded-lg p-2">
                    <p className="text-gray-400 text-xs">Cyclomatic</p>
                    <p className="text-white font-bold">{complexity.cyclomatic}</p>
                  </div>
                  <div className="bg-gray-800 rounded-lg p-2">
                    <p className="text-gray-400 text-xs">Cognitive</p>
                    <p className="text-white font-bold">{complexity.cognitive}</p>
                  </div>
                  <div className="bg-gray-800 rounded-lg p-2">
                    <p className="text-gray-400 text-xs">Max Nesting</p>
                    <p className="text-white font-bold">{complexity.max_nesting}</p>
                  </div>
                  <div className="bg-gray-800 rounded-lg p-2">
                    <p className="text-gray-400 text-xs">Code Lines</p>
                    <p className="text-white font-bold">{complexity.lines}</p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="px-4 pb-4 border-t border-gray-800 pt-3">
                <IssueList issues={card.issues} />
              </div>
            ))}
          </div>
        )
      })}
    </div>
  )
}
