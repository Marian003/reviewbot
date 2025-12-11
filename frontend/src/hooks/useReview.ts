import { useState } from 'react'
import type { ReviewResponse } from '../types'
import { reviewCode, reviewPR } from '../utils/api'

interface UseReviewResult {
  review: ReviewResponse | null
  loading: boolean
  error: string | null
  submitCode: (code: string, language?: string) => Promise<void>
  submitPR: (url: string, token?: string) => Promise<void>
}

export function useReview(): UseReviewResult {
  const [review, setReview] = useState<ReviewResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const submitCode = async (code: string, language?: string) => {
    setLoading(true)
    setError(null)
    try {
      const result = await reviewCode(code, language)
      setReview(result)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const submitPR = async (url: string, token?: string) => {
    setLoading(true)
    setError(null)
    try {
      const result = await reviewPR(url, token)
      setReview(result)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return { review, loading, error, submitCode, submitPR }
}
