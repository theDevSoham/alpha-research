# tests/unit/test_agent.py
from app.agent.research_agent import run_serp_agent

def test_serp_agent_output():
    result = run_serp_agent("Alice Alpha", "alice@alpha.com", "alpha.com")
    assert isinstance(result["logs"], list)
    assert "company_value_prop" in result["data"]
