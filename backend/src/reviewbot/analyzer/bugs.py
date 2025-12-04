from __future__ import annotations

import re

from reviewbot.models import Issue, BugResult
from reviewbot.utils.scoring import clamp_score

_DEDUCTIONS = {"critical": 15, "warning": 8, "info": 3}


class BugAnalyzer:
    def __init__(self, code: str, language: str) -> None:
        self.code = code
        self.language = language.lower()
        self.lines = code.splitlines()

    def _check_none_comparison(self) -> list[Issue]:
        if self.language != "python":
            return []
        issues = []
        for num, line in enumerate(self.lines, 1):
            if re.search(r"==\s*None|!=\s*None", line):
                issues.append(Issue(severity="warning", message="Use 'is None' / 'is not None' instead of == None", line=num, rule="none_comparison", fix="Replace '== None' with 'is None' and '!= None' with 'is not None'"))
        return issues

    def _check_loose_equality(self) -> list[Issue]:
        if self.language not in ("javascript", "typescript"):
            return []
        issues = []
        for num, line in enumerate(self.lines, 1):
            if re.search(r"(?<![=!<>])={2}(?!=)|(?<![=!<>])!={1}(?!=)", line):
                if not re.search(r"={3}|!={2}", line):
                    issues.append(Issue(severity="warning", message="Use === and !== instead of == and != in JavaScript", line=num, rule="loose_equality", fix="Replace == with === and != with !== for type-safe comparison"))
        return issues

    def _check_async_without_await(self) -> list[Issue]:
        issues = []
        pattern = re.compile(r"\basync\s+(def|function)\s+(\w+)")
        for num, line in enumerate(self.lines, 1):
            m = pattern.search(line)
            if m:
                fn_name = m.group(2)
                # look for await in next 20 lines
                snippet = "\n".join(self.lines[num: num + 20])
                if "await" not in snippet:
                    issues.append(Issue(severity="warning", message=f"async function '{fn_name}' contains no await — may block event loop", line=num, rule="async_no_await", fix="Add await calls or remove async keyword if not needed"))
        return issues

    def _check_mutable_defaults(self) -> list[Issue]:
        if self.language != "python":
            return []
        issues = []
        for num, line in enumerate(self.lines, 1):
            if re.search(r"def\s+\w+\s*\(.*=\s*(\[\]|\{\})", line):
                issues.append(Issue(severity="critical", message="Mutable default argument ([] or {}) — shared across all calls", line=num, rule="mutable_default", fix="Use None as default and initialize inside the function body"))
        return issues

    def _check_string_concat_in_loop(self) -> list[Issue]:
        issues = []
        in_loop = False
        for num, line in enumerate(self.lines, 1):
            stripped = line.strip()
            if re.match(r"for\s+|while\s+", stripped):
                in_loop = True
            if in_loop and re.search(r"\w+\s*\+=\s*[\"']|\w+\s*=\s*\w+\s*\+\s*[\"']", line):
                issues.append(Issue(severity="info", message="String concatenation inside loop is O(n²)", line=num, rule="string_concat_loop", fix="Use a list and ''.join() outside the loop for O(n) performance"))
                in_loop = False
        return issues

    def _check_range_len(self) -> list[Issue]:
        if self.language != "python":
            return []
        issues = []
        for num, line in enumerate(self.lines, 1):
            if re.search(r"\brange\s*\(\s*len\s*\(", line):
                issues.append(Issue(severity="info", message="range(len(x)) pattern — use enumerate() instead", line=num, rule="range_len", fix="Replace 'for i in range(len(x))' with 'for i, val in enumerate(x)'"))
        return issues

    def _check_while_true(self) -> list[Issue]:
        issues = []
        for num, line in enumerate(self.lines, 1):
            if re.match(r"\s*while\s+True\s*:", line):
                # look for break in next 30 lines
                snippet = "\n".join(self.lines[num: num + 30])
                if "break" not in snippet:
                    issues.append(Issue(severity="info", message="while True loop without visible break — potential infinite loop", line=num, rule="while_true_no_break", fix="Add a break condition or use a sentinel variable"))
        return issues

    def _check_unused_imports(self) -> list[Issue]:
        if self.language != "python":
            return []
        issues = []
        import_names: list[tuple[int, str]] = []
        for num, line in enumerate(self.lines, 1):
            m = re.match(r"^\s*import\s+(\w+)", line)
            if m:
                import_names.append((num, m.group(1)))
            m2 = re.match(r"^\s*from\s+\S+\s+import\s+(\w+)", line)
            if m2:
                import_names.append((num, m2.group(1)))

        code_without_imports = "\n".join(
            line for line in self.lines if not line.strip().startswith("import") and not line.strip().startswith("from")
        )
        for line_num, name in import_names:
            if name not in code_without_imports:
                issues.append(Issue(severity="info", message=f"Unused import: '{name}'", line=line_num, rule="unused_import", fix=f"Remove the unused import of '{name}'"))
        return issues

    def _check_fstring_no_placeholder(self) -> list[Issue]:
        if self.language != "python":
            return []
        issues = []
        for num, line in enumerate(self.lines, 1):
            if re.search(r'\bf"[^"]*"|\bf\'[^\']*\'', line):
                if not re.search(r'\{', line):
                    issues.append(Issue(severity="info", message="f-string with no {} placeholder — unnecessary f-prefix", line=num, rule="fstring_no_placeholder", fix="Remove the f-prefix or add a placeholder expression"))
        return issues

    def analyze(self) -> BugResult:
        issues: list[Issue] = []
        issues.extend(self._check_none_comparison())
        issues.extend(self._check_loose_equality())
        issues.extend(self._check_async_without_await())
        issues.extend(self._check_mutable_defaults())
        issues.extend(self._check_string_concat_in_loop())
        issues.extend(self._check_range_len())
        issues.extend(self._check_while_true())
        issues.extend(self._check_unused_imports())
        issues.extend(self._check_fstring_no_placeholder())

        deduction = sum(_DEDUCTIONS.get(i.severity, 0) for i in issues)
        return BugResult(score=clamp_score(100 - deduction), issues=issues)
