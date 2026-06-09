from app.agents.refactor_agent import RefactorAgent


def test_refactor_syntax_validation():
    agent = RefactorAgent()
    ok, msg = agent.validate_syntax("print('ok')")
    assert ok is True


def test_refactor_diff():
    agent = RefactorAgent()
    diff = agent.generate_diff("a = 1", "a = 2")
    assert "a = 1" in diff
    assert "a = 2" in diff
