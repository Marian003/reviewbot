export interface Issue {
  severity: 'critical' | 'warning' | 'info'
  message: string
  line: number | null
  rule: string
  fix: string | null
}

export interface SecurityResult {
  score: number
  issues: Issue[]
  passed_checks: number
  total_checks: number
}

export interface ComplexityResult {
  score: number
  cyclomatic: number
  cognitive: number
  max_nesting: number
  lines: number
  functions: number
}

export interface StyleResult {
  score: number
  issues: Issue[]
}

export interface BugResult {
  score: number
  issues: Issue[]
}

export interface Suggestion {
  category: string
  message: string
  priority: 'high' | 'medium' | 'low'
}

export interface ReviewMetadata {
  language: string
  lines_analyzed: number
  time_ms: number
}

export interface ReviewResponse {
  overall_score: number
  grade: string
  summary: string
  security: SecurityResult
  complexity: ComplexityResult
  style: StyleResult
  bugs: BugResult
  suggestions: Suggestion[]
  metadata: ReviewMetadata
}
