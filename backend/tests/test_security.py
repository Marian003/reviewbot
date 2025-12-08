import pytest
from reviewbot.analyzer.security import SecurityAnalyzer


def test_python_eval_detected():
    code = 'result = eval(input("Enter:"))'
    result = SecurityAnalyzer(code, "python").analyze()
    assert any(i.severity == "critical" and "eval" in i.message.lower() for i in result.issues)
    assert result.score < 100


def test_python_exec_detected():
    code = "exec(user_input)"
    result = SecurityAnalyzer(code, "python").analyze()
    assert any("exec" in i.message.lower() for i in result.issues)


def test_python_os_system_detected():
    code = "import os\nos.system('ls -la')"
    result = SecurityAnalyzer(code, "python").analyze()
    assert any("os.system" in i.message for i in result.issues)


def test_python_sql_injection_detected():
    code = 'query = f"SELECT * FROM users WHERE id = {user_id}"'
    result = SecurityAnalyzer(code, "python").analyze()
    assert any(i.severity == "critical" for i in result.issues)


def test_python_hardcoded_secret_detected():
    code = 'API_KEY = "sk-supersecretkey1234"'
    result = SecurityAnalyzer(code, "python").analyze()
    assert any(i.severity == "critical" for i in result.issues)


def test_js_eval_detected():
    code = "const result = eval(userInput);"
    result = SecurityAnalyzer(code, "javascript").analyze()
    assert any("eval" in i.message.lower() for i in result.issues)


def test_js_inner_html_detected():
    code = 'element.innerHTML = userContent;'
    result = SecurityAnalyzer(code, "javascript").analyze()
    assert any("innerHTML" in i.message for i in result.issues)


def test_js_dangerous_set_inner_html():
    code = '<div dangerouslySetInnerHTML={{ __html: data }} />'
    result = SecurityAnalyzer(code, "javascript").analyze()
    assert any("dangerouslySetInnerHTML" in i.message for i in result.issues)


def test_js_proto_access():
    code = "obj.__proto__.admin = true;"
    result = SecurityAnalyzer(code, "javascript").analyze()
    assert any("proto" in i.message.lower() for i in result.issues)


def test_clean_python_scores_100():
    code = """
def add(a, b):
    return a + b

def greet(name):
    return f"Hello, {name}"
"""
    result = SecurityAnalyzer(code, "python").analyze()
    assert result.score == 100
    assert len(result.issues) == 0


def test_multiple_issues_stack_deductions():
    code = """
API_KEY = "sk-12345"
eval(user_input)
exec(code)
"""
    result = SecurityAnalyzer(code, "python").analyze()
    assert result.score < 60
