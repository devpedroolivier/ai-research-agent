import os
from dotenv import load_dotenv
from deepagents import create_deep_agent
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def create_research_agent():
    """
    Cria um Deep Agent configurado com OpenAI e Tavily.
    """
    # 1. Configurar ferramentas (Tavily para busca)
    search_tool = TavilySearch(max_results=3)

    # 2. Inicializar o LLM (OpenAI gpt-4o)
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # 3. Criar o Deep Agent
    # Nota: A função create_deep_agent usa 'system_prompt' em vez de 'instructions'
    agent = create_deep_agent(
        model=llm,
        tools=[search_tool],
        system_prompt=(
            "Você é um pesquisador sênior. Sua tarefa é investigar tópicos profundamente, "
            "usando a ferramenta de busca para encontrar informações precisas e o "
            "sistema de arquivos para organizar seus achados. "
            "Sempre forneça uma resposta conclusiva e bem estruturada."
        )
    )
    
    return agent

def run_research(query: str):
    """
    Executa uma pesquisa usando o agente.
    """
    agent = create_research_agent()
    
    inputs = {"messages": [{"role": "user", "content": query}]}
    
    print(f"Iniciando pesquisa: {query}")
    
    # Execução do agente
    # O deepagents usa LangGraph por baixo, retornamos o estado final
    result = agent.invoke(inputs)
    
    return result

if __name__ == "__main__":
    # Exemplo de uso
    query = "Quais são as tendências mais recentes em IA Generativa para 2026?"
    try:
        resultado = run_research(query)
        # Imprime a última mensagem do agente
        if "messages" in resultado and len(resultado["messages"]) > 0:
            print("\n--- RESPOSTA DO AGENTE ---")
            print(resultado["messages"][-1].content)
    except Exception as e:
        print(f"Erro ao executar o agente: {e}")
        print("Verifique se as chaves de API no arquivo .env estão corretas.")
