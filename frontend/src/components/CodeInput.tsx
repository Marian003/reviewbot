import { useState } from 'react'
import { Code2 } from 'lucide-react'

const DEFAULT_CODE = `import os
import pickle

API_KEY = "sk-1234567890abcdef"

def get_user_data(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    data = eval(input("Enter expression: "))
    result = pickle.loads(open("cache.pkl", "rb").read())

    if result == None:
        return []

    items = []
    for i in range(len(result)):
        items = items + [result[i]]

    return items`

const LANGUAGES = [
  'auto-detect', 'python', 'javascript', 'typescript',
  'java', 'go', 'rust', 'cpp', 'ruby', 'php', 'bash', 'sql',
]

interface Props {
  onSubmit: (code: string, language?: string) => void
  loading: boolean
}

export function CodeInput({ onSubmit, loading }: Props) {
  const [code, setCode] = useState(DEFAULT_CODE)
  const [language, setLanguage] = useState('auto-detect')

  const handleSubmit = () => {
    if (!code.trim()) return
    onSubmit(code, language === 'auto-detect' ? undefined : language)
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-sm text-gray-400">
          <Code2 size={16} />
          <span>{code.length.toLocaleString()} chars</span>
        </div>
        <select
          value={language}
          onChange={e => setLanguage(e.target.value)}
          className="bg-gray-800 text-gray-200 text-sm rounded-lg px-3 py-1.5 border border-gray-700 focus:outline-none focus:border-blue-500"
        >
          {LANGUAGES.map(l => (
            <option key={l} value={l}>{l.charAt(0).toUpperCase() + l.slice(1).replace('-', ' ')}</option>
          ))}
        </select>
      </div>

      <textarea
        value={code}
        onChange={e => setCode(e.target.value)}
        className="code-textarea w-full h-72 bg-gray-900 text-gray-100 rounded-xl border border-gray-700 p-4 text-sm focus:outline-none focus:border-blue-500 transition-colors"
        placeholder="Paste your code here..."
        spellCheck={false}
      />

      <button
        onClick={handleSubmit}
        disabled={loading || !code.trim()}
        className="w-full py-3 rounded-xl font-semibold text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-blue-500/25"
      >
        {loading ? 'Analyzing...' : 'Review Code'}
      </button>
    </div>
  )
}
