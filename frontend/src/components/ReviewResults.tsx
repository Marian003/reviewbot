import type { ReviewResponse } from '../types'
import { ScoreCard } from './ScoreCard'
import { CategoryPanel } from './CategoryPanel'
import { SuggestionList } from './SuggestionList'
import { AIReviewPanel } from './AIReviewPanel'

interface Props {
  review: ReviewResponse
  aiReview: string | null
  aiLoading: boolean
  aiError: string | null
}

export function ReviewResults({ review, aiReview, aiLoading, aiError }: Props) {
  return (
    <div className="mt-8 space-y-6">
      {/* Two-panel grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
        {/* LEFT — Static Analysis */}
        <div className="bg-gray-900 rounded-xl border border-blue-900/30 p-5 space-y-6">
          {/* Panel header */}
          <div className="flex items-center gap-2 pb-4 border-b border-gray-800">
            <div className="w-2 h-2 rounded-full bg-blue-500" />
            <div>
              <h2 className="text-white font-semibold text-sm">⚡ Static Analysis</h2>
              <p className="text-gray-500 text-xs">Pattern-based code scanning</p>
            </div>
          </div>

          <ScoreCard score={review.overall_score} grade={review.grade} summary={review.summary} />

          <div className="flex justify-center gap-4 text-xs text-gray-500 flex-wrap">
            <span>Language: <span className="text-gray-300">{review.metadata.language}</span></span>
            <span>Lines: <span className="text-gray-300">{review.metadata.lines_analyzed}</span></span>
            <span>Time: <span className="text-gray-300">{review.metadata.time_ms}ms</span></span>
          </div>

          <CategoryPanel
            security={review.security}
            complexity={review.complexity}
            style={review.style}
            bugs={review.bugs}
          />

          <SuggestionList suggestions={review.suggestions} />
        </div>

        {/* RIGHT — AI Review */}
        <AIReviewPanel aiReview={aiReview} loading={aiLoading} error={aiError} />
      </div>
    </div>
  )
}

// Two-panel layout: static analysis + AI review
