import tempfile

from app.agents.documentation_agent import DocumentationAgent


def test_document_file():
    agent = DocumentationAgent()
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        f.write("def hello(): pass")
        path = f.name

    result = agent.document_file(path)
    assert isinstance(result, str)
