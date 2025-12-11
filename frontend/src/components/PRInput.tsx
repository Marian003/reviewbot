import { useState } from 'react'
import { GitPullRequest } from 'lucide-react'

interface Props {
  onSubmit: (url: string, token?: string) => void
  loading: boolean
}

export function PRInput({ onSubmit, loading }: Props) {
  const [url, setUrl] = useState('')
  const [token, setToken] = useState('')
  const [showToken, setShowToken] = useState(false)

  const handleSubmit = () => {
    if (!url.trim()) return
    onSubmit(url.trim(), token.trim() || undefined)
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2 text-sm text-gray-400 mb-1">
        <GitPullRequest size={16} />
        <span>Paste a GitHub Pull Request URL</span>
      </div>

      <input
        type="url"
        value={url}
        onChange={e => setUrl(e.target.value)}
        className="w-full bg-gray-900 text-gray-100 rounded-xl border border-gray-700 px-4 py-3 text-sm focus:outline-none focus:border-blue-500 transition-colors"
        placeholder="https://github.com/owner/repo/pull/123"
      />

      <button
        type="button"
        onClick={() => setShowToken(!showToken)}
        className="text-xs text-gray-500 hover:text-gray-300 transition-colors"
      >
        {showToken ? '— Hide' : '+ Add'} GitHub token (for private repos)
      </button>

      {showToken && (
        <input
          type="password"
          value={token}
          onChange={e => setToken(e.target.value)}
          className="w-full bg-gray-900 text-gray-100 rounded-xl border border-gray-700 px-4 py-3 text-sm focus:outline-none focus:border-blue-500 transition-colors"
          placeholder="ghp_your_token_here"
        />
      )}

      <button
        onClick={handleSubmit}
        disabled={loading || !url.trim()}
        className="w-full py-3 rounded-xl font-semibold text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-blue-500/25"
      >
        {loading ? 'Fetching PR...' : 'Review PR'}
      </button>
    </div>
  )
}
