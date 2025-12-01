from __future__ import annotations

from pydantic import BaseModel


class ReviewRequest(BaseModel):
    code: str
    language: str | None = None
    filename: str | None = None


class PRRequest(BaseModel):
    url: str
    token: str | None = None


class Issue(BaseModel):
    severity: str  # "critical" | "warning" | "info"
    message: str
    line: int | None = None
    rule: str
    fix: str | None = None


class SecurityResult(BaseModel):
    score: int
    issues: list[Issue]
    passed_checks: int
    total_checks: int


class ComplexityResult(BaseModel):
    score: int
    cyclomatic: int
    cognitive: int
    max_nesting: int
    lines: int
    functions: int


class StyleResult(BaseModel):
    score: int
    issues: list[Issue]


class BugResult(BaseModel):
    score: int
    issues: list[Issue]


class Suggestion(BaseModel):
    category: str
    message: str
    priority: str  # "high" | "medium" | "low"


class ReviewMetadata(BaseModel):
    language: str
    lines_analyzed: int
    time_ms: int


class ReviewResponse(BaseModel):
    overall_score: int
    grade: str
    summary: str
    security: SecurityResult
    complexity: ComplexityResult
    style: StyleResult
    bugs: BugResult
    suggestions: list[Suggestion]
    metadata: ReviewMetadata
