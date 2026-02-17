# 🤖 ReviewBot AI

> **AI-powered code review — instant security analysis, complexity scoring, and improvement suggestions**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178c6?logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/React-18-61dafb?logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?logo=fastapi&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![CI](https://img.shields.io/github/actions/workflow/status/your-org/reviewbot/ci.yml?label=CI)

---

## Features

| | Feature | Description |
|---|---|---|
| 🛡️ | **Security Analysis** | Detects vulnerabilities, hardcoded secrets, injection risks, and insecure API usage |
| 📊 | **Complexity Scoring** | Cyclomatic and cognitive complexity metrics with nesting depth analysis |
| 🎨 | **Style Checker** | Enforces best practices: line length, dead code, magic numbers, naming conventions |
| 🐛 | **Bug Detection** | Finds common bugs, anti-patterns, mutable defaults, and code smells |
| 💡 | **Smart Suggestions** | Prioritized, actionable improvement recommendations ranked by severity |
| 🔗 | **GitHub PR Support** | Review pull requests directly by pasting a GitHub PR URL |

### Supported Languages

Python · JavaScript · TypeScript · Java · Go · Rust · C++ · Ruby · PHP · Bash · SQL

---

## How It Works

1. **Paste code** or enter a GitHub PR URL
2. ReviewBot analyzes security, complexity, style, and bugs in parallel
3. Get instant results with scores (0–100), issues, line numbers, and fix suggestions

---

## Tech Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python 3.10+, FastAPI, Pydantic v2, Uvicorn, HTTPX |
| **Frontend** | React 18, TypeScript 5, Tailwind CSS v3, Vite 5, Lucide React |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+

### Backend

```bash
cd backend
pip install -e ".[dev]"
uvicorn reviewbot.main:app --reload
# API available at http://localhost:8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# UI available at http://localhost:5173
```

### Run Both

```bash
make install
# Then open two terminals:
make dev-backend   # Terminal 1
make dev-frontend  # Terminal 2
```

### Docker

```bash
docker-compose up --build
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
```

---

## API Reference

### `POST /api/review`

Analyze a code snippet.

```bash
curl -X POST http://localhost:8000/api/review \
  -H "Content-Type: application/json" \
  -d '{
    "code": "eval(user_input)",
    "language": "python"
  }'
```

**Response:**
```json
{
  "overall_score": 55,
  "grade": "F",
  "summary": "This code scores 55/100 (grade F). The main concerns are: 1 critical security issue (eval).",
  "security": { "score": 85, "issues": [...], "passed_checks": 7, "total_checks": 8 },
  "complexity": { "score": 100, "cyclomatic": 1, "cognitive": 0, "max_nesting": 0, "lines": 1, "functions": 1 },
  "style": { "score": 100, "issues": [] },
  "bugs": { "score": 100, "issues": [] },
  "suggestions": [{ "category": "Security", "message": "Replace eval() with ...", "priority": "high" }],
  "metadata": { "language": "python", "lines_analyzed": 1, "time_ms": 3 }
}
```

### `POST /api/review/pr`

Analyze a GitHub Pull Request.

```bash
curl -X POST http://localhost:8000/api/review/pr \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://github.com/owner/repo/pull/42",
    "token": "ghp_optional_for_private_repos"
  }'
```

### `GET /api/health`

```bash
curl http://localhost:8000/api/health
# {"status":"ok","version":"0.1.0"}
```

### `GET /api/languages`

```bash
curl http://localhost:8000/api/languages
# {"languages":["python","javascript","typescript","java","go","rust","cpp","ruby","php","bash","sql"]}
```

---

## Architecture

ReviewBot uses a 4-analyzer pipeline:

```
Code Input
    │
    ├─→ SecurityAnalyzer  (weight 35%) — regex-based vulnerability scanning
    ├─→ ComplexityAnalyzer (weight 20%) — cyclomatic + cognitive complexity
    ├─→ StyleAnalyzer     (weight 20%) — line length, naming, dead code
    └─→ BugAnalyzer       (weight 25%) — anti-patterns, type errors, smells
              │
              └─→ Engine aggregates → weighted score → grade → suggestions → summary
```

Each analyzer returns a 0–100 score. The engine computes a weighted average, assigns a letter grade (A–F), generates up to 5 prioritized suggestions, and produces a human-readable summary.

---

## Running Tests

```bash
# Backend
cd backend && pytest -v

# Frontend type check
cd frontend && npx tsc --noEmit
```

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Commit your changes: `git commit -m 'feat: add my feature'`
4. Push and open a PR

Please run `ruff check src/` (backend) before submitting.

---

## License

MIT — see [LICENSE](./LICENSE) for details.

<!-- API reference updated with AI review endpoint -->
