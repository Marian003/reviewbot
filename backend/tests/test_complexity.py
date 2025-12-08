from reviewbot.analyzer.complexity import ComplexityAnalyzer


def test_simple_function_scores_high():
    code = """
def greet(name):
    return f"Hello, {name}"
"""
    result = ComplexityAnalyzer(code, "python").analyze()
    assert result.score >= 80


def test_deeply_nested_function_scores_low():
    code = """
def process(data):
    for item in data:
        if item:
            for sub in item:
                if sub:
                    for x in sub:
                        if x:
                            print(x)
"""
    result = ComplexityAnalyzer(code, "python").analyze()
    assert result.max_nesting >= 4


def test_function_counting():
    code = """
def foo():
    pass

def bar():
    pass

def baz():
    pass
"""
    result = ComplexityAnalyzer(code, "python").analyze()
    assert result.functions == 3


def test_line_counting_ignores_blanks_and_comments():
    code = """
# This is a comment
def foo():
    # Another comment

    x = 1
    return x
"""
    result = ComplexityAnalyzer(code, "python").analyze()
    assert result.lines <= 3


def test_high_cyclomatic_reduces_score():
    code = "\n".join(
        ["def complex():"] +
        [f"    if x == {i}: pass" for i in range(35)]
    )
    result = ComplexityAnalyzer(code, "python").analyze()
    assert result.cyclomatic > 20
    assert result.score < 80
