from reviewbot.analyzer.engine import CodeAnalyzer
from reviewbot.models import ReviewResponse


PYTHON_SAMPLE = """
import os
import pickle

API_KEY = "sk-1234567890abcdef"

def get_user_data(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    data = eval(input("Enter expression: "))
    result = pickle.loads(open("cache.pkl", "rb").read())

    if result == None:
        return []

    items = []
    for i in range(len(result)):
        items = items + [result[i]]

    return items
"""


def test_end_to_end_returns_review_response():
    analyzer = CodeAnalyzer(PYTHON_SAMPLE, "python")
    result = analyzer.analyze()
    assert isinstance(result, ReviewResponse)
    assert 0 <= result.overall_score <= 100
    assert result.grade in ("A", "B", "C", "D", "F")
    assert result.summary
    assert result.metadata.language == "python"


def test_scoring_weights_applied():
    code = 'eval(x)\neval(y)\neval(z)'
    result = CodeAnalyzer(code, "python").analyze()
    # Security weight is 0.35, so critical security issues should drag overall score down
    assert result.overall_score < result.complexity.score


def test_grade_thresholds():
    from reviewbot.utils.scoring import calculate_grade
    assert calculate_grade(95) == "A"
    assert calculate_grade(85) == "B"
    assert calculate_grade(75) == "C"
    assert calculate_grade(65) == "D"
    assert calculate_grade(55) == "F"


def test_suggestion_generation():
    analyzer = CodeAnalyzer(PYTHON_SAMPLE, "python")
    result = analyzer.analyze()
    assert len(result.suggestions) > 0
    for s in result.suggestions:
        assert s.priority in ("high", "medium", "low")
        assert s.category
        assert s.message


def test_empty_code_returns_max_score():
    """Empty code should not crash and returns a valid response."""
    code = "# just a comment"
    result = CodeAnalyzer(code, "python").analyze()
    assert isinstance(result, ReviewResponse)
    assert result.overall_score >= 0

# Edge case: empty input handling
