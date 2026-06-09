import tempfile

from app.agents.tests_agent import TestsAgent


def test_generate_tests_for_file():
    agent = TestsAgent()
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write("def add(a, b): return a + b")
        path = f.name

    result = agent.generate_tests_for_file(path)
    assert "def test" in result.lower()
