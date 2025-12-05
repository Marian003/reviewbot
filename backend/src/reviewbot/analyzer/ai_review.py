from __future__ import annotations

from reviewbot.models import BugResult, ComplexityResult, SecurityResult, StyleResult


def generate_summary(
    code: str,
    security: SecurityResult,
    complexity: ComplexityResult,
    style: StyleResult,
    bugs: BugResult,
    overall_score: int,
    grade: str,
) -> str:
    parts: list[str] = []

    critical_security = [i for i in security.issues if i.severity == "critical"]
    critical_bugs = [i for i in bugs.issues if i.severity == "critical"]
    all_warnings = [i for i in security.issues + bugs.issues + style.issues if i.severity == "warning"]

    parts.append(f"This code scores {overall_score}/100 (grade {grade}).")

    concerns: list[str] = []

    if critical_security:
        names = ", ".join(i.rule.split(r"\\")[0][:30] for i in critical_security[:2])
        concerns.append(f"{len(critical_security)} critical security issue(s) ({names})")

    if critical_bugs:
        concerns.append(f"{len(critical_bugs)} critical bug(s) including mutable default arguments")

    if complexity.cyclomatic > 20:
        concerns.append(f"very high cyclomatic complexity ({complexity.cyclomatic})")
    elif complexity.cyclomatic > 10:
        concerns.append(f"moderate complexity (cyclomatic={complexity.cyclomatic})")

    if len(all_warnings) > 5:
        concerns.append(f"{len(all_warnings)} warnings across security, style, and bug categories")

    if concerns:
        parts.append("The main concerns are: " + "; ".join(concerns) + ".")

    if overall_score >= 90:
        parts.append("Overall the code is in excellent shape with only minor improvements needed.")
    elif overall_score >= 80:
        parts.append("The code is generally solid; addressing the listed issues will improve reliability and security.")
    elif overall_score >= 70:
        parts.append("Consider prioritizing the high-severity issues before deploying to production.")
    else:
        parts.append("Significant refactoring and security hardening are recommended before this code goes to production.")

    return " ".join(parts)
