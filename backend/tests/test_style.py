from reviewbot.analyzer.style import StyleAnalyzer


def test_long_lines_detected():
    long_line = "x = " + "a" * 130
    result = StyleAnalyzer(long_line, "python").analyze()
    assert any(i.rule == "line_too_long" for i in result.issues)
    assert result.score < 100


def test_mixed_indentation_detected():
    code = "def foo():\n    x = 1\n\ty = 2"
    result = StyleAnalyzer(code, "python").analyze()
    assert any(i.rule == "mixed_indentation" for i in result.issues)


def test_empty_except_detected():
    code = "try:\n    risky()\nexcept Exception:\n    pass"
    result = StyleAnalyzer(code, "python").analyze()
    assert any(i.rule == "empty_except" for i in result.issues)


def test_console_log_detected():
    code = "console.log('debug value:', x);"
    result = StyleAnalyzer(code, "javascript").analyze()
    assert any(i.rule == "debug_print" for i in result.issues)


def test_print_statement_detected():
    code = "print('debugging here')"
    result = StyleAnalyzer(code, "python").analyze()
    assert any(i.rule == "debug_print" for i in result.issues)


def test_clean_code_passes():
    code = """
def calculate_total(items: list) -> float:
    \"\"\"Calculate the total price of all items.\"\"\"
    total = 0.0
    for item in items:
        total += item.price
    return total
"""
    result = StyleAnalyzer(code, "python").analyze()
    assert result.score >= 70
