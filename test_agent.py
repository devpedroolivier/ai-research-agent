import pytest
from main import create_research_agent, run_research, WEB_RESEARCHER, REPORT_WRITER


def test_create_agent_returns_instance():
    agent = create_research_agent()
    assert agent is not None


def test_agent_has_invoke_method():
    agent = create_research_agent()
    assert hasattr(agent, "invoke")


def test_subagents_have_required_fields():
    for agent_def in [WEB_RESEARCHER, REPORT_WRITER]:
        assert "name" in agent_def
        assert "description" in agent_def
        assert "system_prompt" in agent_def


def test_web_researcher_has_search_tool():
    tools = WEB_RESEARCHER.get("tools", [])
    assert len(tools) > 0


def test_report_writer_has_no_direct_tools():
    tools = REPORT_WRITER.get("tools", [])
    assert len(tools) == 0


@pytest.mark.skip(reason="Requer chaves de API válidas no .env")
def test_run_research_returns_messages():
    resultado = run_research("O que é LangGraph?")
    assert "messages" in resultado
    assert len(resultado["messages"]) > 0
    last = resultado["messages"][-1]
    assert len(last.content) > 0


@pytest.mark.skip(reason="Requer chaves de API válidas no .env")
def test_run_research_creates_output_file():
    import glob
    run_research("Teste de escrita de arquivo")
    files = glob.glob("research_output/*.md")
    assert len(files) > 0
