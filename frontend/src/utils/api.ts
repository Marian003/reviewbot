import type { ReviewResponse } from '../types'

const API_BASE = (import.meta.env.VITE_API_URL as string | undefined) || 'http://localhost:8000'

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let message = `Request failed: ${res.status} ${res.statusText}`
    try {
      const body = await res.json()
      if (body?.detail) message = body.detail
    } catch {
      // ignore parse error
    }
    throw new Error(message)
  }
  return res.json() as Promise<T>
}

export async function reviewCode(code: string, language?: string): Promise<ReviewResponse> {
  const res = await fetch(`${API_BASE}/api/review`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code, language }),
  })
  return handleResponse<ReviewResponse>(res)
}

export async function reviewPR(url: string, token?: string): Promise<ReviewResponse> {
  const res = await fetch(`${API_BASE}/api/review/pr`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, token }),
  })
  return handleResponse<ReviewResponse>(res)
}

export async function reviewAI(code: string, language: string): Promise<string> {
  const res = await fetch(`${API_BASE}/api/review/ai`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code, language }),
  })
  const data = await handleResponse<{ review: string }>(res)
  return data.review
}
