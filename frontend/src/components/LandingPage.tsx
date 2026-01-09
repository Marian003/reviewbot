import { useEffect, useRef, useState } from 'react'
import { Shield, BarChart2, Paintbrush, Bug, Code, Zap, Bot } from 'lucide-react'

function useCountUp(target: number, trigger: boolean) {
  const [count, setCount] = useState(0)
  useEffect(() => {
    if (!trigger) return
    const duration = 1400
    const startTime = performance.now()
    const step = (now: number) => {
      const elapsed = now - startTime
      const progress = Math.min(elapsed / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      setCount(Math.floor(eased * target))
      if (progress < 1) requestAnimationFrame(step)
      else setCount(target)
    }
    requestAnimationFrame(step)
  }, [target, trigger])
  return count
}

function StatCard({ value, label, suffix = '' }: { value: number; label: string; suffix?: string }) {
  const ref = useRef<HTMLDivElement>(null)
  const [visible, setVisible] = useState(false)
  const count = useCountUp(value, visible)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setVisible(true) },
      { threshold: 0.5 }
    )
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [])

  return (
    <div ref={ref} className="bg-gray-900 rounded-xl border border-gray-800 px-8 py-6 text-center hover:border-gray-700 transition-colors">
      <div className="text-4xl font-bold mb-1" style={{ background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
        {count}{suffix}
      </div>
      <div className="text-gray-400 text-sm">{label}</div>
    </div>
  )
}

const HOW_IT_WORKS = [
  {
    icon: <Code className="w-6 h-6" />,
    title: 'Paste Your Code',
    description: 'Drop in any code snippet or GitHub PR link',
  },
  {
    icon: <Zap className="w-6 h-6" />,
    title: 'Instant Analysis',
    description: 'Static analysis scans for bugs, security issues, and style problems in milliseconds',
  },
  {
    icon: <Bot className="w-6 h-6" />,
    title: 'AI Deep Review',
    description: 'Claude AI provides contextual feedback with specific improvement suggestions',
  },
]

const FEATURES = [
  {
    icon: <Shield className="w-5 h-5" />,
    title: 'Security Analysis',
    description: 'Detects hardcoded secrets, SQL injection, XSS vulnerabilities, and unsafe function calls',
    accent: '#3b82f6',
  },
  {
    icon: <BarChart2 className="w-5 h-5" />,
    title: 'Complexity Metrics',
    description: 'Cyclomatic and cognitive complexity scoring with function-level breakdown',
    accent: '#8b5cf6',
  },
  {
    icon: <Paintbrush className="w-5 h-5" />,
    title: 'Code Style',
    description: 'Enforces clean code practices, formatting rules, and naming conventions',
    accent: '#06b6d4',
  },
  {
    icon: <Bug className="w-5 h-5" />,
    title: 'Bug Detection',
    description: 'Catches common mistakes like off-by-one errors, null reference issues, and async pitfalls',
    accent: '#f59e0b',
  },
]

const TECH_STACK = ['Python', 'FastAPI', 'React', 'TypeScript', 'Claude AI']

export function LandingPage() {
  const scrollToReview = () => {
    document.getElementById('review')?.scrollIntoView({ behavior: 'smooth' })
  }

  return (
    <>
      {/* Hero */}
      <section
        className="relative flex flex-col items-center justify-center text-center px-4 overflow-hidden"
        style={{ minHeight: 'calc(100vh - 60px)' }}
      >
        {/* Animated grid background */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            backgroundImage:
              'linear-gradient(rgba(59,130,246,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(59,130,246,0.04) 1px, transparent 1px)',
            backgroundSize: '50px 50px',
            animation: 'gridScroll 25s linear infinite',
          }}
        />
        {/* Radial fade overlay */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{ background: 'radial-gradient(ellipse 70% 60% at 50% 50%, transparent 0%, #0a0a0f 100%)' }}
        />

        <div className="relative z-10 max-w-3xl mx-auto">
          {/* Title */}
          <h1 className="text-6xl sm:text-7xl font-bold mb-5 leading-tight tracking-tight">
            <span
              style={{
                background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}
            >
              ReviewBot AI
            </span>
          </h1>

          {/* Subtitle */}
          <p className="text-gray-400 text-xl sm:text-2xl mb-8 font-light">
            Your code, reviewed by machines and intelligence.
          </p>

          {/* Badges */}
          <div className="flex flex-wrap gap-3 justify-center mb-10">
            <span className="px-4 py-2 rounded-full border text-sm bg-blue-500/5 text-blue-400" style={{ borderColor: 'rgba(59,130,246,0.35)' }}>
              ⚡ Static Analysis
            </span>
            <span className="px-4 py-2 rounded-full border text-sm bg-purple-500/5 text-purple-400" style={{ borderColor: 'rgba(139,92,246,0.35)' }}>
              🤖 AI-Powered Review
            </span>
          </div>

          {/* CTA */}
          <button
            onClick={scrollToReview}
            className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl font-semibold text-white transition-all duration-200 hover:scale-105 hover:shadow-lg active:scale-100"
            style={{ background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)', boxShadow: '0 0 30px rgba(139,92,246,0.25)' }}
          >
            Start Reviewing →
          </button>
        </div>
      </section>

      {/* Stats */}
      <section className="max-w-3xl mx-auto px-4 py-16">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <StatCard value={15} suffix="+" label="Rules" />
          <StatCard value={11} label="Languages" />
          <StatCard value={1} suffix="s" label="Analysis Time" />
        </div>
      </section>

      {/* How it works */}
      <section className="max-w-5xl mx-auto px-4 py-10 pb-16">
        <h2 className="text-center text-2xl font-bold text-white mb-2">How It Works</h2>
        <p className="text-center text-gray-500 text-sm mb-10">Three steps to better code</p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          {HOW_IT_WORKS.map((step, i) => (
            <div
              key={i}
              className="bg-gray-900 rounded-xl border border-gray-800 p-6 text-center transition-transform duration-200 hover:scale-105 hover:border-gray-700"
            >
              <div
                className="w-12 h-12 rounded-xl flex items-center justify-center mx-auto mb-4"
                style={{ background: 'linear-gradient(135deg, rgba(59,130,246,0.15), rgba(139,92,246,0.15))', border: '1px solid rgba(139,92,246,0.2)' }}
              >
                <span className="text-purple-400">{step.icon}</span>
              </div>
              <div className="text-gray-400 text-xs font-mono mb-2" style={{ color: 'rgba(139,92,246,0.7)' }}>
                0{i + 1}
              </div>
              <h3 className="text-white font-semibold mb-2">{step.title}</h3>
              <p className="text-gray-500 text-sm leading-relaxed">{step.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Feature cards */}
      <section className="max-w-5xl mx-auto px-4 pb-16">
        <h2 className="text-center text-2xl font-bold text-white mb-2">What We Check</h2>
        <p className="text-center text-gray-500 text-sm mb-10">Comprehensive analysis across four dimensions</p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {FEATURES.map((f, i) => (
            <div
              key={i}
              className="bg-gray-900 rounded-xl border border-gray-800 p-5 flex gap-4 transition-all duration-200 hover:border-gray-700 hover:scale-[1.01]"
              style={{ borderLeft: `3px solid ${f.accent}` }}
            >
              <div className="shrink-0 mt-0.5" style={{ color: f.accent }}>{f.icon}</div>
              <div>
                <h3 className="text-white font-semibold mb-1">{f.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{f.description}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Tech stack strip */}
      <section className="max-w-5xl mx-auto px-4 pb-16">
        <div className="flex flex-wrap gap-3 justify-center">
          {TECH_STACK.map(tech => (
            <span key={tech} className="px-3 py-1.5 rounded-lg bg-gray-900 border border-gray-800 text-gray-600 text-xs font-mono">
              {tech}
            </span>
          ))}
        </div>
      </section>
    </>
  )
}

// Hero section with animated CSS grid background
