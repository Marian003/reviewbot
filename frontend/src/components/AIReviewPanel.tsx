import type { ReactNode } from 'react'

interface Props {
  aiReview: string | null
  loading: boolean
  error: string | null
}

function renderInline(text: string): ReactNode {
  const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g)
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i} className="text-white font-semibold">{part.slice(2, -2)}</strong>
    }
    if (part.startsWith('`') && part.endsWith('`')) {
      return (
        <code key={i} className="bg-gray-800 text-purple-300 px-1 py-0.5 rounded font-mono text-xs">
          {part.slice(1, -1)}
        </code>
      )
    }
    return part
  })
}

function renderMarkdown(text: string): ReactNode {
  const lines = text.split('\n')
  const elements: ReactNode[] = []
  let i = 0
  let key = 0

  while (i < lines.length) {
    const line = lines[i]

    // Fenced code block
    if (line.startsWith('```')) {
      const codeLines: string[] = []
      i++
      while (i < lines.length && !lines[i].startsWith('```')) {
        codeLines.push(lines[i])
        i++
      }
      elements.push(
        <pre key={key++} className="bg-gray-950 rounded-lg p-3 my-3 overflow-x-auto border border-gray-800">
          <code className="text-green-400 text-xs font-mono">{codeLines.join('\n')}</code>
        </pre>
      )
      i++ // skip closing ```
      continue
    }

    // Section header
    if (line.startsWith('## ')) {
      elements.push(
        <h3 key={key++} className="text-purple-400 font-semibold text-xs uppercase tracking-widest mt-5 mb-2 pb-1 border-b border-purple-900/40">
          {line.slice(3)}
        </h3>
      )
      i++
      continue
    }

    // Bullet list
    if (line.startsWith('- ') || line.startsWith('* ')) {
      const items: string[] = []
      while (i < lines.length && (lines[i].startsWith('- ') || lines[i].startsWith('* '))) {
        items.push(lines[i].slice(2))
        i++
      }
      elements.push(
        <ul key={key++} className="space-y-1 mb-3">
          {items.map((item, idx) => (
            <li key={idx} className="flex gap-2 text-gray-300 text-sm leading-relaxed">
              <span className="text-purple-500 mt-1 shrink-0">•</span>
              <span>{renderInline(item)}</span>
            </li>
          ))}
        </ul>
      )
      continue
    }

    // Numbered list
    if (/^\d+\. /.test(line)) {
      const items: string[] = []
      while (i < lines.length && /^\d+\. /.test(lines[i])) {
        items.push(lines[i].replace(/^\d+\. /, ''))
        i++
      }
      elements.push(
        <ol key={key++} className="space-y-2 mb-3">
          {items.map((item, idx) => (
            <li key={idx} className="flex gap-2 text-gray-300 text-sm leading-relaxed">
              <span className="text-purple-400 font-mono min-w-[1.25rem] shrink-0">{idx + 1}.</span>
              <span>{renderInline(item)}</span>
            </li>
          ))}
        </ol>
      )
      continue
    }

    // Empty line
    if (line.trim() === '') {
      i++
      continue
    }

    // Plain paragraph
    elements.push(
      <p key={key++} className="text-gray-300 text-sm leading-relaxed mb-2">
        {renderInline(line)}
      </p>
    )
    i++
  }

  return <>{elements}</>
}

function LoadingSkeleton() {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3 mb-6">
        <div className="flex gap-1">
          {[0, 1, 2].map(i => (
            <span
              key={i}
              className="w-2 h-2 rounded-full bg-purple-500 animate-bounce"
              style={{ animationDelay: `${i * 0.15}s` }}
            />
          ))}
        </div>
        <span className="text-purple-300 text-sm">AI is analyzing your code...</span>
      </div>
      {[60, 80, 50, 90, 70].map((w, i) => (
        <div key={i} className="space-y-2">
          <div className="h-3 rounded bg-gray-800 animate-pulse" style={{ width: `${w}%` }} />
          {i % 2 === 0 && (
            <div className="h-3 rounded bg-gray-800 animate-pulse" style={{ width: `${w - 20}%` }} />
          )}
        </div>
      ))}
    </div>
  )
}

export function AIReviewPanel({ aiReview, loading, error }: Props) {
  const isApiKeyError = error?.includes('ANTHROPIC_API_KEY')

  return (
    <div className="bg-gray-900 rounded-xl border border-purple-900/30 p-5 flex flex-col">
      {/* Panel header */}
      <div className="flex items-center gap-2 mb-4 pb-4 border-b border-gray-800">
        <div className="w-2 h-2 rounded-full bg-purple-500" />
        <div>
          <h2 className="text-white font-semibold text-sm">🤖 AI Review</h2>
          <p className="text-gray-500 text-xs">Powered by Claude</p>
        </div>
      </div>

      <div className="flex-1">
        {loading && <LoadingSkeleton />}

        {!loading && error && (
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-red-400 text-sm">
              <span>⚠️</span>
              <span>AI review unavailable</span>
            </div>
            <p className="text-gray-500 text-xs">
              {isApiKeyError
                ? 'Set ANTHROPIC_API_KEY to enable AI reviews'
                : error}
            </p>
          </div>
        )}

        {!loading && !error && aiReview && (
          <div>{renderMarkdown(aiReview)}</div>
        )}

        {!loading && !error && !aiReview && (
          <p className="text-gray-600 text-sm italic">Submit code to get an AI review.</p>
        )}
      </div>
    </div>
  )
}

// v1.1.0 - AI review integration
