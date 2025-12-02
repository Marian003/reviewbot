from __future__ import annotations


def clamp_score(score: int | float) -> int:
    return max(0, min(100, int(score)))


def calculate_grade(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def weighted_average(scores_weights: list[tuple[int, float]]) -> int:
    total_weight = sum(w for _, w in scores_weights)
    if total_weight == 0:
        return 0
    result = sum(score * weight for score, weight in scores_weights) / total_weight
    return int(round(result))
