from __future__ import annotations

import re

from reviewbot.models import Issue, StyleResult
from reviewbot.utils.scoring import clamp_score

_DEDUCTIONS = {"warning": 5, "info": 2}

_ALLOWED_SHORT_VARS = {"i", "j", "k", "x", "y", "n", "e", "f", "t", "v"}


class StyleAnalyzer:
    def __init__(self, code: str, language: str) -> None:
        self.code = code
        self.language = language.lower()
        self.lines = code.splitlines()

    def _check_line_length(self) -> list[Issue]:
        issues = []
        for num, line in enumerate(self.lines, 1):
            if len(line) > 120:
                issues.append(Issue(severity="warning", message=f"Line too long ({len(line)} chars > 120)", line=num, rule="line_too_long", fix="Break the line into multiple shorter lines"))
        return issues

    def _check_mixed_indentation(self) -> list[Issue]:
        has_tabs = any("\t" in line for line in self.lines)
        has_spaces = any(line.startswith("  ") for line in self.lines)
        if has_tabs and has_spaces:
            return [Issue(severity="warning", message="Mixed tabs and spaces detected", line=None, rule="mixed_indentation", fix="Standardize on spaces (PEP 8) or tabs throughout the file")]
        return []

    def _check_missing_docstrings(self) -> list[Issue]:
        issues = []
        if self.language not in ("python", "javascript", "typescript"):
            return issues
        for num, line in enumerate(self.lines, 1):
            stripped = line.strip()
            is_fn = re.match(r"def\s+\w+|function\s+\w+|const\s+\w+\s*=\s*\(", stripped)
            if is_fn:
                prev = self.lines[num - 2].strip() if num >= 2 else ""
                nxt = self.lines[num].strip() if num < len(self.lines) else ""
                has_doc = nxt.startswith('"""') or nxt.startswith("'''") or nxt.startswith("/**") or prev.startswith("#") or prev.startswith("//")
                if not has_doc:
                    issues.append(Issue(severity="info", message="Function missing docstring/comment", line=num, rule="missing_docstring", fix="Add a docstring or comment describing the function's purpose"))
        return issues

    def _check_magic_numbers(self) -> list[Issue]:
        issues = []
        allowed = {"0", "1", "-1", "2", "100"}
        pattern = re.compile(r'\b(\d{2,})\b')
        for num, line in enumerate(self.lines, 1):
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("//"):
                continue
            for match in pattern.finditer(line):
                val = match.group(1)
                if val not in allowed:
                    issues.append(Issue(severity="info", message=f"Magic number {val} — consider a named constant", line=num, rule="magic_number", fix=f"Replace {val} with a descriptive named constant"))
                    break  # one per line
        return issues

    def _check_dead_code(self) -> list[Issue]:
        issues = []
        for num, line in enumerate(self.lines, 1):
            stripped = line.strip()
            if re.match(r"^(return|break|continue)\b", stripped) and num < len(self.lines):
                next_line = self.lines[num].strip()
                if next_line and not next_line.startswith("#") and not next_line.startswith("//") and next_line not in ("}", "else:", "elif"):
                    issues.append(Issue(severity="warning", message="Unreachable code after return/break/continue", line=num + 1, rule="dead_code", fix="Remove the unreachable code block"))
        return issues

    def _check_short_vars(self) -> list[Issue]:
        issues = []
        pattern = re.compile(r'\b([a-zA-Z])\s*=\s*')
        for num, line in enumerate(self.lines, 1):
            for m in pattern.finditer(line):
                name = m.group(1).lower()
                if name not in _ALLOWED_SHORT_VARS:
                    issues.append(Issue(severity="info", message=f"Single-letter variable '{m.group(1)}' reduces readability", line=num, rule="short_var_name", fix="Use a descriptive variable name"))
                    break
        return issues

    def _check_empty_except(self) -> list[Issue]:
        issues = []
        for num, line in enumerate(self.lines, 1):
            stripped = line.strip()
            if re.match(r"except(\s+\w+)?:$|catch\s*\(", stripped):
                if num < len(self.lines):
                    body = self.lines[num].strip()
                    if body in ("pass", "{}", ""):
                        issues.append(Issue(severity="warning", message="Empty except/catch block silently swallows errors", line=num, rule="empty_except", fix="Log the exception or re-raise it with context"))
        return issues

    def _check_print_statements(self) -> list[Issue]:
        issues = []
        for num, line in enumerate(self.lines, 1):
            stripped = line.strip()
            if re.match(r"print\s*\(|console\.log\s*\(", stripped):
                issues.append(Issue(severity="info", message="Debug print/console.log statement found", line=num, rule="debug_print", fix="Remove debug statements or replace with a proper logging framework"))
        return issues

    def _check_quote_consistency(self) -> list[Issue]:
        if self.language not in ("javascript", "typescript"):
            return []
        has_single = bool(re.search(r"'[^']*'", self.code))
        has_double = bool(re.search(r'"[^"]*"', self.code))
        if has_single and has_double:
            return [Issue(severity="info", message="Inconsistent quote style (mixed single and double quotes)", line=None, rule="quote_style", fix="Standardize on single quotes or configure a formatter like Prettier")]
        return []

    def analyze(self) -> StyleResult:
        issues: list[Issue] = []
        issues.extend(self._check_line_length())
        issues.extend(self._check_mixed_indentation())
        issues.extend(self._check_missing_docstrings())
        issues.extend(self._check_magic_numbers())
        issues.extend(self._check_dead_code())
        issues.extend(self._check_short_vars())
        issues.extend(self._check_empty_except())
        issues.extend(self._check_print_statements())
        issues.extend(self._check_quote_consistency())

        deduction = sum(_DEDUCTIONS.get(i.severity, 0) for i in issues)
        return StyleResult(score=clamp_score(100 - deduction), issues=issues)
