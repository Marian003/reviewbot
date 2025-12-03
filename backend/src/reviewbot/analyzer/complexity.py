from __future__ import annotations

import re

from reviewbot.models import ComplexityResult
from reviewbot.utils.scoring import clamp_score


class ComplexityAnalyzer:
    def __init__(self, code: str, language: str) -> None:
        self.code = code
        self.language = language.lower()
        self.lines = code.splitlines()

    def _count_functions(self) -> int:
        count = 0
        for line in self.lines:
            stripped = line.strip()
            if self.language == "python":
                if re.match(r"def\s+\w+", stripped):
                    count += 1
            elif self.language in ("javascript", "typescript"):
                if re.search(r"\bfunction\s+\w+|\bconst\s+\w+\s*=\s*(?:async\s*)?\(.*\)\s*=>", stripped):
                    count += 1
            else:
                if re.search(r"\b(function|def|fn|func)\s+\w+", stripped):
                    count += 1
        return max(1, count)

    def _count_cyclomatic(self) -> int:
        count = 1  # base
        keywords = [r"\bif\b", r"\belif\b", r"\belse\b", r"\bfor\b", r"\bwhile\b",
                    r"\band\b", r"\bor\b", r"\bcase\b", r"\bcatch\b", r"\btry\b",
                    r"\?\s*\w"]  # ternary
        for line in self.lines:
            for kw in keywords:
                if re.search(kw, line):
                    count += 1
        return count

    def _count_cognitive(self) -> int:
        """Weighted by nesting depth."""
        total = 0
        depth = 0
        branch_keywords = re.compile(r"\b(if|elif|else|for|while|try|catch|except|case)\b")
        indent_inc = re.compile(r":\s*$|\{\s*$")
        indent_dec = re.compile(r"^\s*(\}|end\b)")

        for line in self.lines:
            stripped = line.strip()
            if indent_dec.match(stripped):
                depth = max(0, depth - 1)
            if branch_keywords.search(stripped):
                total += 1 + depth
            if indent_inc.search(stripped):
                depth += 1
        return total

    def _max_nesting(self) -> int:
        max_depth = 0
        current_depth = 0
        for line in self.lines:
            stripped = line.strip()
            if self.language == "python":
                indent = len(line) - len(line.lstrip())
                current_depth = indent // 4
            else:
                current_depth += stripped.count("{") - stripped.count("}")
                current_depth = max(0, current_depth)
            max_depth = max(max_depth, current_depth)
        return max_depth

    def _count_code_lines(self) -> int:
        count = 0
        for line in self.lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and not stripped.startswith("//") and stripped != '"""' and stripped != "'''":
                count += 1
        return count

    def analyze(self) -> ComplexityResult:
        functions = self._count_functions()
        cyclomatic = self._count_cyclomatic()
        cognitive = self._count_cognitive()
        max_nesting = self._max_nesting()
        lines = self._count_code_lines()

        score = 100

        if cyclomatic > 30:
            score -= 40
        elif cyclomatic > 20:
            score -= 25
        elif cyclomatic > 10:
            score -= 10

        if cognitive > 25:
            score -= 20
        elif cognitive > 15:
            score -= 10

        if max_nesting > 6:
            score -= 20
        elif max_nesting > 4:
            score -= 10

        avg_fn_length = lines / functions if functions else 0
        if avg_fn_length > 30:
            score -= 10

        return ComplexityResult(
            score=clamp_score(score),
            cyclomatic=cyclomatic,
            cognitive=cognitive,
            max_nesting=max_nesting,
            lines=lines,
            functions=functions,
        )
