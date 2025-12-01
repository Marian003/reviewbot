from __future__ import annotations

import os

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from reviewbot.analyzer.engine import CodeAnalyzer
from reviewbot.models import PRRequest, ReviewRequest, ReviewResponse
from reviewbot.parsers.github_pr import fetch_pr_diff
from reviewbot.parsers.language import detect_language

app = FastAPI(title="ReviewBot AI", version="0.1.0")

_AI_SYSTEM_PROMPT = """You are a senior code reviewer. Analyze the provided code and give a \
concise, actionable review. Structure your response exactly like this:

## Overall Assessment
2-3 sentences summarizing code quality.

## Security
List any security concerns. If none, say "No security issues found."

## Code Quality
Key observations about structure, readability, and best practices.

## Suggestions
Numbered list of specific improvements. Include short code snippets where helpful. \
Focus on the most impactful changes.

## Verdict
One line: use ✅ for good code, ⚠️ for needs improvement, or 🚨 for critical issues. \
Include a brief reason."""


class AIReviewRequest(BaseModel):
    code: str
    language: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPPORTED_LANGUAGES = [
    "python", "javascript", "typescript", "java", "go",
    "rust", "cpp", "ruby", "php", "bash", "sql",
]


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}


@app.get("/api/languages")
async def languages():
    return {"languages": SUPPORTED_LANGUAGES}


@app.post("/api/review", response_model=ReviewResponse)
async def review_code(request: ReviewRequest) -> ReviewResponse:
    if not request.code or not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")

    language = request.language or detect_language(request.code, request.filename)
    analyzer = CodeAnalyzer(request.code, language)
    return analyzer.analyze()


@app.post("/api/review/pr", response_model=ReviewResponse)
async def review_pr(request: PRRequest) -> ReviewResponse:
    try:
        diff = await fetch_pr_diff(request.url, request.token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch PR: {e}")

    language = detect_language(diff, filename="diff.py")
    analyzer = CodeAnalyzer(diff, language)
    return analyzer.analyze()


@app.post("/api/review/ai")
async def review_ai(request: AIReviewRequest) -> dict:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="AI review requires ANTHROPIC_API_KEY")

    user_message = (
        f"Review this {request.language} code:\n\n"
        f"```{request.language}\n{request.code}\n```"
    )

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 1500,
                    "temperature": 0.3,
                    "system": _AI_SYSTEM_PROMPT,
                    "messages": [{"role": "user", "content": user_message}],
                },
            )
    except httpx.TimeoutException as e:
        raise HTTPException(status_code=504, detail="AI review timed out") from e
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI review failed: {e}") from e

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=f"AI API error: {response.text}")

    data = response.json()
    return {"review": data["content"][0]["text"]}


def run() -> None:
    uvicorn.run("reviewbot.main:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    run()
