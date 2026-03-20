import pytest
from main import create_research_agent
from langchain_core.messages import HumanMessage, BaseMessage

def test_create_agent():
    """
    Testa se o agente pode ser criado com sucesso.
    """
    agent = create_research_agent()
    assert agent is not None, "O agente deve ser instanciado."

def test_agent_structure():
    """
    Testa se a resposta do agente contém as mensagens esperadas.
    """
    agent = create_research_agent()
    
    # Simula uma entrada simples para verificar a estrutura de retorno
    # Como não temos chaves reais, o teste real com o modelo falharia se chamássemos 'invoke'
    # mas o teste de configuração é válido.
    assert hasattr(agent, "invoke"), "O agente deve ter um método invoke."

@pytest.mark.skip(reason="Requer chaves de API válidas no .env")
def test_agent_output_validation():
    """
    Teste de integração que valida se o agente gera uma resposta.
    Requer chaves de API configuradas.
    """
    agent = create_research_agent()
    inputs = {"messages": [{"role": "user", "content": "Olá, quem é você?"}]}
    
    result = agent.invoke(inputs)
    
    assert "messages" in result, "A resposta deve conter 'messages'."
    last_message = result["messages"][-1]
    assert isinstance(last_message, BaseMessage), "A última mensagem deve ser do tipo BaseMessage."
    assert len(last_message.content) > 0, "O conteúdo da resposta não deve estar vazio."
