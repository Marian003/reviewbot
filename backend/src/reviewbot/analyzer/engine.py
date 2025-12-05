from __future__ import annotations

import time

from reviewbot.analyzer.ai_review import generate_summary
from reviewbot.analyzer.bugs import BugAnalyzer
from reviewbot.analyzer.complexity import ComplexityAnalyzer
from reviewbot.analyzer.security import SecurityAnalyzer
from reviewbot.analyzer.style import StyleAnalyzer
from reviewbot.models import Issue, ReviewMetadata, ReviewResponse, Suggestion
from reviewbot.utils.scoring import calculate_grade, clamp_score, weighted_average


class CodeAnalyzer:
    def __init__(self, code: str, language: str) -> None:
        self.code = code
        self.language = language

    def _build_suggestions(self, all_issues: list[Issue]) -> list[Suggestion]:
        priority_map = {"critical": "high", "warning": "medium", "info": "low"}
        severity_order = {"critical": 0, "warning": 1, "info": 2}

        seen_rules: set[str] = set()
        suggestions: list[Suggestion] = []

        for issue in sorted(all_issues, key=lambda i: severity_order.get(i.severity, 9)):
            if issue.rule in seen_rules:
                continue
            seen_rules.add(issue.rule)
            if issue.fix:
                suggestions.append(
                    Suggestion(
                        category=_guess_category(issue.rule),
                        message=issue.fix,
                        priority=priority_map.get(issue.severity, "low"),
                    )
                )
            if len(suggestions) >= 5:
                break

        return suggestions

    def analyze(self) -> ReviewResponse:
        start = time.monotonic()

        security = SecurityAnalyzer(self.code, self.language).analyze()
        complexity = ComplexityAnalyzer(self.code, self.language).analyze()
        style = StyleAnalyzer(self.code, self.language).analyze()
        bugs = BugAnalyzer(self.code, self.language).analyze()

        overall_score = clamp_score(
            weighted_average([
                (security.score, 0.35),
                (bugs.score, 0.25),
                (complexity.score, 0.20),
                (style.score, 0.20),
            ])
        )
        grade = calculate_grade(overall_score)

        all_issues = security.issues + bugs.issues + style.issues
        suggestions = self._build_suggestions(all_issues)

        summary = generate_summary(self.code, security, complexity, style, bugs, overall_score, grade)

        elapsed_ms = int((time.monotonic() - start) * 1000)
        lines = len([l for l in self.code.splitlines() if l.strip()])

        return ReviewResponse(
            overall_score=overall_score,
            grade=grade,
            summary=summary,
            security=security,
            complexity=complexity,
            style=style,
            bugs=bugs,
            suggestions=suggestions,
            metadata=ReviewMetadata(language=self.language, lines_analyzed=lines, time_ms=elapsed_ms),
        )


def _guess_category(rule: str) -> str:
    security_rules = {"eval", "exec", "sql", "secret", "pickle", "yaml", "shell", "xss", "proto", "redirect", "innerHTML", "document", "verify"}
    bug_rules = {"none_comparison", "loose_equality", "mutable_default", "async_no_await", "string_concat", "range_len", "unused_import", "fstring"}
    complexity_rules = {"complexity", "nesting", "cognitive"}

    rule_lower = rule.lower()
    if any(k in rule_lower for k in security_rules):
        return "Security"
    if any(k in rule_lower for k in bug_rules):
        return "Bugs"
    if any(k in rule_lower for k in complexity_rules):
        return "Complexity"
    return "Style"
