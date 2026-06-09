from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_orchestrator_search():
    response = client.get("/orchestrator/run", params={"query": "search:hello"})
    assert response.status_code == 200
    assert "response" in response.json()
