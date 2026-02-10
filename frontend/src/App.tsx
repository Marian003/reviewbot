import { useState } from 'react'
import { Header } from './components/Header'
import { CodeInput } from './components/CodeInput'
import { PRInput } from './components/PRInput'
import { ReviewResults } from './components/ReviewResults'
import { LoadingState } from './components/LoadingState'
import { LandingPage } from './components/LandingPage'
import { useReview } from './hooks/useReview'
import { useAIReview } from './hooks/useAIReview'

type Tab = 'code' | 'pr'

export default function App() {
  const [activeTab, setActiveTab] = useState<Tab>('code')
  const { review, loading, error, submitCode, submitPR } = useReview()
  const { aiReview, aiLoading, aiError, submitAIReview, resetAIReview } = useAIReview()

  const handleCodeSubmit = (code: string, language?: string) => {
    void submitCode(code, language)
    void submitAIReview(code, language ?? 'unknown')
  }

  const handlePRSubmit = (url: string, token?: string) => {
    resetAIReview()
    void submitPR(url, token)
  }

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#0a0a0f' }}>
      <Header />

      <LandingPage />

      <main id="review" className="max-w-6xl mx-auto px-4 py-8">
        {/* Input panel — kept narrow */}
        <div className="max-w-3xl mx-auto">
          {/* Tab switcher */}
          <div className="flex gap-1 bg-gray-900 rounded-xl p-1 mb-6 w-fit">
            {(['code', 'pr'] as Tab[]).map(tab => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-5 py-2 rounded-lg text-sm font-medium transition-all duration-150 ${
                  activeTab === tab
                    ? 'bg-blue-600 text-white shadow'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                {tab === 'code' ? 'Paste Code' : 'GitHub PR'}
              </button>
            ))}
          </div>

          {/* Input */}
          <div className="bg-gray-900/60 rounded-2xl border border-gray-800 p-5">
            {activeTab === 'code' ? (
              <CodeInput onSubmit={handleCodeSubmit} loading={loading} />
            ) : (
              <PRInput onSubmit={handlePRSubmit} loading={loading} />
            )}
          </div>

          {/* Error */}
          {error && (
            <div className="mt-4 bg-red-900/30 border border-red-700 rounded-xl p-4 text-red-300 text-sm">
              {error}
            </div>
          )}
        </div>

        {/* Results — full width of container */}
        {loading && <LoadingState />}
        {!loading && review && (
          <ReviewResults
            review={review}
            aiReview={aiReview}
            aiLoading={aiLoading}
            aiError={aiError}
          />
        )}
      </main>
    </div>
  )
}

// Graceful empty input handling
