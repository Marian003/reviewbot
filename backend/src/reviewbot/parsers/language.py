from __future__ import annotations

import re


_EXT_MAP: dict[str, str] = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".go": "go",
    ".rs": "rust",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".rb": "ruby",
    ".php": "php",
    ".sh": "bash",
    ".bash": "bash",
    ".sql": "sql",
}


def detect_language(code: str, filename: str | None = None) -> str:
    if filename:
        for ext, lang in _EXT_MAP.items():
            if filename.lower().endswith(ext):
                return lang

    first_line = code.splitlines()[0] if code.strip() else ""

    if first_line.startswith("#!") and "python" in first_line:
        return "python"
    if first_line.startswith("#!") and ("node" in first_line or "js" in first_line):
        return "javascript"
    if first_line.startswith("#!") and "bash" in first_line:
        return "bash"

    # Heuristics
    py_score = sum([
        bool(re.search(r"^(import|from)\s+\w+", code, re.MULTILINE)),
        bool(re.search(r"\bdef\s+\w+\s*\(", code)),
        bool(re.search(r"\bclass\s+\w+.*:", code)),
        bool(re.search(r":\s*$", code, re.MULTILINE)),
        bool(re.search(r"\bprint\s*\(", code)),
        bool(re.search(r"\bself\b", code)),
    ])

    js_score = sum([
        bool(re.search(r"\bconst\s+\w+\s*=", code)),
        bool(re.search(r"\blet\s+\w+\s*=", code)),
        bool(re.search(r"\bfunction\s+\w+\s*\(", code)),
        bool(re.search(r"=>\s*\{", code)),
        bool(re.search(r"console\.(log|error)", code)),
        bool(re.search(r"require\s*\(|import\s+.*from\s+['\"]", code)),
    ])

    ts_score = js_score + sum([
        bool(re.search(r":\s*(string|number|boolean|any|void|never)\b", code)),
        bool(re.search(r"\binterface\s+\w+", code)),
        bool(re.search(r"\btype\s+\w+\s*=", code)),
    ])

    java_score = sum([
        bool(re.search(r"\bpublic\s+(class|interface|enum)\s+\w+", code)),
        bool(re.search(r"\bSystem\.out\.print", code)),
        bool(re.search(r"@Override", code)),
    ])

    go_score = sum([
        bool(re.search(r"\bfunc\s+\w+\s*\(", code)),
        bool(re.search(r"\bpackage\s+\w+", code)),
        bool(re.search(r":=", code)),
    ])

    scores = {
        "python": py_score,
        "typescript": ts_score,
        "javascript": js_score,
        "java": java_score,
        "go": go_score,
    }
    best = max(scores, key=lambda k: scores[k])
    return best if scores[best] > 0 else "python"
