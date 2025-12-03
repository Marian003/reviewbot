from __future__ import annotations

import re

from reviewbot.models import Issue, SecurityResult
from reviewbot.utils.scoring import clamp_score

_DEDUCTIONS = {"critical": 15, "warning": 8, "info": 3}

_PYTHON_PATTERNS: list[tuple[str, str, str, str | None]] = [
    (r"\beval\s*\(", "critical", "Use of eval() is dangerous — it executes arbitrary code", "Replace eval() with a safe parser or ast.literal_eval()"),
    (r"\bexec\s*\(", "critical", "Use of exec() executes arbitrary code", "Avoid exec(); use explicit function calls instead"),
    (r"\bos\.system\s*\(", "critical", "os.system() is vulnerable to shell injection", "Use subprocess.run() with a list argument and shell=False"),
    (r'subprocess\.[a-z_]+\(.*shell\s*=\s*True', "critical", "subprocess with shell=True is vulnerable to injection", "Pass a list of arguments and use shell=False"),
    (r'(f"|f\')SELECT.*\{', "critical", "SQL query built with f-string — SQL injection risk", "Use parameterized queries or an ORM"),
    (r'"SELECT.*%s|\'SELECT.*%s', "critical", "SQL query with % formatting — SQL injection risk", "Use parameterized queries"),
    (r'(password|passwd|secret|api_key|apikey|token)\s*=\s*["\'][^"\']{4,}', "critical", "Hardcoded secret or credential detected", "Store secrets in environment variables or a secrets manager"),
    (r'\bpickle\.loads?\s*\(', "warning", "pickle.loads() can execute arbitrary code when deserializing untrusted data", "Use json or another safe serialization format for untrusted data"),
    (r'\byaml\.load\s*\((?!.*Loader\s*=\s*yaml\.SafeLoader)', "warning", "yaml.load() without SafeLoader can execute arbitrary code", "Use yaml.safe_load() instead"),
    (r'\bassert\b', "info", "assert statements are disabled with -O flag and should not be used for validation", "Replace with explicit if/raise checks"),
    (r'requests\.(get|post|put|delete|patch)\s*\((?!.*verify\s*=\s*True)', "warning", "requests call without verify=True — SSL verification may be disabled", "Explicitly pass verify=True or configure SSL properly"),
]

_JS_PATTERNS: list[tuple[str, str, str, str | None]] = [
    (r'\beval\s*\(', "critical", "Use of eval() executes arbitrary code", "Remove eval(); use JSON.parse() or explicit logic"),
    (r'\.innerHTML\s*=', "warning", "innerHTML assignment is an XSS risk", "Use textContent or sanitize with DOMPurify"),
    (r'\bdocument\.write\s*\(', "warning", "document.write() is an XSS risk and blocks parsing", "Use DOM manipulation methods instead"),
    (r'dangerouslySetInnerHTML', "warning", "dangerouslySetInnerHTML can lead to XSS", "Sanitize content with DOMPurify before setting"),
    (r'(password|passwd|secret|api_key|apikey|token)\s*=\s*["\'][^"\']{4,}', "critical", "Hardcoded secret or credential detected", "Store secrets in environment variables"),
    (r'__proto__', "warning", "Accessing __proto__ can lead to prototype pollution", "Use Object.create(null) or Object.getPrototypeOf()"),
    (r'window\.location\s*=\s*[a-zA-Z_$]', "warning", "Unvalidated redirect via window.location assignment", "Validate the URL before redirecting"),
]

_GENERAL_PATTERNS: list[tuple[str, str, str, str | None]] = [
    (r'\b(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b', "info", "Hardcoded IP address detected", "Use configuration or DNS names instead of hardcoded IPs"),
    (r'(TODO|FIXME).*(?:security|vuln|hack|injection|xss|auth)', "info", "Security-related TODO/FIXME comment found", "Address this security concern before deploying"),
]


class SecurityAnalyzer:
    def __init__(self, code: str, language: str) -> None:
        self.code = code
        self.language = language.lower()
        self.lines = code.splitlines()

    def analyze(self) -> SecurityResult:
        issues: list[Issue] = []
        total_checks = 0

        if self.language == "python":
            patterns = _PYTHON_PATTERNS + _GENERAL_PATTERNS
        elif self.language in ("javascript", "typescript"):
            patterns = _JS_PATTERNS + _GENERAL_PATTERNS
        else:
            patterns = _GENERAL_PATTERNS

        total_checks = len(patterns)

        for line_num, line in enumerate(self.lines, 1):
            for pattern, severity, message, fix in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(Issue(severity=severity, message=message, line=line_num, rule=pattern[:40], fix=fix))

        # Check for large commented-out blocks
        consecutive_comments = 0
        for line_num, line in enumerate(self.lines, 1):
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("*"):
                consecutive_comments += 1
                if consecutive_comments > 5:
                    issues.append(Issue(severity="info", message="Large block of commented-out code detected", line=line_num, rule="commented_code", fix="Remove dead code; rely on version control for history"))
                    consecutive_comments = 0  # reset to avoid duplicate
            else:
                consecutive_comments = 0

        deduction = sum(_DEDUCTIONS.get(i.severity, 0) for i in issues)
        score = clamp_score(100 - deduction)
        passed = total_checks - len({i.rule for i in issues})

        return SecurityResult(score=score, issues=issues, passed_checks=max(0, passed), total_checks=total_checks)
