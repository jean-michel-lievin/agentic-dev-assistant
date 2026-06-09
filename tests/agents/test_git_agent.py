from app.agents.git_agent import GitAgent


def test_git_agent_init():
    agent = GitAgent()
    assert agent.base_path is not None


def test_git_agent_list_files_empty(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    agent = GitAgent(base_path=str(tmp_path))
    result = agent.list_files("repo")
    assert result == "No files found in repo."
