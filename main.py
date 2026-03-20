import os
from dotenv import load_dotenv
from deepagents import create_deep_agent, SubAgent
from deepagents.backends import FilesystemBackend
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI

load_dotenv()

# --- Subagentes especializados ---

WEB_RESEARCHER: SubAgent = {
    "name": "web_researcher",
    "description": (
        "Especialista em busca web. Use para encontrar informações "
        "atualizadas, dados recentes e fontes confiáveis sobre qualquer tópico."
    ),
    "system_prompt": (
        "Você é um especialista em pesquisa web. Sua única responsabilidade "
        "é buscar informações precisas e atualizadas usando a ferramenta de busca. "
        "Retorne sempre os dados brutos encontrados, com as fontes citadas."
    ),
    "tools": [TavilySearch(max_results=5)],
    "model": ChatOpenAI(model="gpt-4o", temperature=0),
}

REPORT_WRITER: SubAgent = {
    "name": "report_writer",
    "description": (
        "Especialista em estruturar e escrever relatórios. Use para transformar "
        "dados brutos de pesquisa em um relatório claro e bem estruturado."
    ),
    "system_prompt": (
        "Você é um especialista em redação de relatórios técnicos. "
        "Receba os dados de pesquisa e produza um relatório com: "
        "1) Resumo executivo, 2) Achados principais, 3) Análise, 4) Conclusão. "
        "Salve o relatório em research_output/ usando as ferramentas de "
        "sistema de arquivos disponíveis."
    ),
    "tools": [],
    "model": ChatOpenAI(model="gpt-4o", temperature=0),
}

# --- Backend de arquivos ---

FILESYSTEM_BACKEND = FilesystemBackend(
    root_dir="./",
    virtual_mode=True,  # Bloqueia traversal (../) — seguro para produção
)

# --- Agente orquestrador ---

def create_research_agent():
    """
    Cria o Deep Agent orquestrador com 4 middlewares ativos:
    - FilesystemMiddleware (via backend=): leitura/escrita de arquivos
    - MemoryMiddleware (via memory=): instruções persistentes do AGENTS.md
    - SubAgentMiddleware (via subagents=): delega para web_researcher e report_writer
    - TodoListMiddleware (built-in): planejamento de etapas com write_todos
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    agent = create_deep_agent(
        name="research_orchestrator",
        model=llm,
        tools=[],
        system_prompt=(
            "Você é um orquestrador de pesquisa sênior. Coordene agentes "
            "especializados para produzir pesquisas completas.\n\n"
            "PROCESSO OBRIGATÓRIO:\n"
            "1. Use write_todos para listar as etapas do plano\n"
            "2. Delegue a busca de dados ao agente 'web_researcher'\n"
            "3. Delegue a escrita do relatório ao agente 'report_writer'\n"
            "4. Consolide e apresente o resultado final ao usuário\n\n"
            "Siga as instruções persistentes do arquivo AGENTS.md."
        ),
        backend=FILESYSTEM_BACKEND,
        memory=[".deepagents/AGENTS.md"],
        subagents=[WEB_RESEARCHER, REPORT_WRITER],
        debug=False,
    )

    return agent


def run_research(query: str) -> dict:
    """Executa uma pesquisa orquestrada com todos os middlewares ativos."""
    agent = create_research_agent()
    inputs = {"messages": [{"role": "user", "content": query}]}
    print(f"\nIniciando pesquisa orquestrada: {query}\n")
    result = agent.invoke(inputs)
    return result


if __name__ == "__main__":
    query = "Quais são as tendências mais recentes em IA Generativa para 2026?"
    try:
        resultado = run_research(query)
        if "messages" in resultado and len(resultado["messages"]) > 0:
            print("\n--- RESPOSTA DO AGENTE ---")
            print(resultado["messages"][-1].content)
    except Exception as e:
        print(f"Erro ao executar o agente: {e}")
        print("Verifique se as chaves de API no arquivo .env estão corretas.")
