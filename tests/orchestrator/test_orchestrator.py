from app.orchestrator.orchestrator import Orchestrator


def test_orchestrator_echo():
    orch = Orchestrator()
    result = orch.route("echo:hello")
    assert "hello" in result.lower()


def test_orchestrator_classify():
    orch = Orchestrator()
    result = orch.classify("analyze:")
    assert isinstance(result, str)


def test_orchestrator_fallback():
    orch = Orchestrator()
    result = orch.route("hello")
    assert isinstance(result, str)
