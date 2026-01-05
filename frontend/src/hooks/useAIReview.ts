import { useState } from 'react'
import { reviewAI } from '../utils/api'

interface UseAIReviewResult {
  aiReview: string | null
  aiLoading: boolean
  aiError: string | null
  submitAIReview: (code: string, language: string) => Promise<void>
  resetAIReview: () => void
}

export function useAIReview(): UseAIReviewResult {
  const [aiReview, setAIReview] = useState<string | null>(null)
  const [aiLoading, setAILoading] = useState(false)
  const [aiError, setAIError] = useState<string | null>(null)

  const submitAIReview = async (code: string, language: string) => {
    setAILoading(true)
    setAIReview(null)
    setAIError(null)
    try {
      const result = await reviewAI(code, language)
      setAIReview(result)
    } catch (e) {
      setAIError(e instanceof Error ? e.message : 'An error occurred')
    } finally {
      setAILoading(false)
    }
  }

  const resetAIReview = () => {
    setAIReview(null)
    setAIError(null)
    setAILoading(false)
  }

  return { aiReview, aiLoading, aiError, submitAIReview, resetAIReview }
}
