import { useEffect, useState } from 'react'

interface Props {
  score: number
  grade: string
  summary: string
}

function gradeColor(grade: string): string {
  if (grade === 'A' || grade === 'B') return '#22c55e'
  if (grade === 'C') return '#eab308'
  if (grade === 'D') return '#f97316'
  return '#ef4444'
}

export function ScoreCard({ score, grade, summary }: Props) {
  const [animatedScore, setAnimatedScore] = useState(0)
  const radius = 54
  const circumference = 2 * Math.PI * radius
  const color = gradeColor(grade)

  useEffect(() => {
    const timer = setTimeout(() => setAnimatedScore(score), 100)
    return () => clearTimeout(timer)
  }, [score])

  const offset = circumference - (animatedScore / 100) * circumference

  return (
    <div className="flex flex-col items-center gap-4">
      <div className="relative" style={{ filter: `drop-shadow(0 0 20px ${color}44)` }}>
        <svg width="140" height="140" viewBox="0 0 140 140">
          {/* Background circle */}
          <circle cx="70" cy="70" r={radius} fill="none" stroke="#1f2937" strokeWidth="10" />
          {/* Animated progress */}
          <circle
            cx="70"
            cy="70"
            r={radius}
            fill="none"
            stroke={color}
            strokeWidth="10"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            transform="rotate(-90 70 70)"
            style={{ transition: 'stroke-dashoffset 1s ease-out' }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-4xl font-bold text-white" style={{ color }}>
            {animatedScore}
          </span>
          <span className="text-lg font-semibold" style={{ color }}>
            {grade}
          </span>
        </div>
      </div>

      <p className="text-center text-gray-300 text-sm max-w-md leading-relaxed">{summary}</p>
    </div>
  )
}

// Animation timing adjusted for slow connections
