# AI Research Agent

Um agente de pesquisa autônomo construído com Python, LangGraph e GPT-4o. Ele busca informações na web em tempo real, analisa fontes e entrega respostas estruturadas — em menos de 60 linhas de código.

## O que ele faz

Dado um tópico ou pergunta, o agente:

1. Recebe a query do usuário
2. Decide autonomamente quando e como usar a busca web (Tavily)
3. Processa e sintetiza os resultados encontrados
4. Entrega uma resposta conclusiva e bem estruturada

```python
resultado = run_research("Quais são as tendências mais recentes em IA Generativa para 2026?")
```

## Stack

| Tecnologia | Papel |
|---|---|
| [deepagents](https://pypi.org/project/deepagents/) | Framework de agents (wrapper LangGraph) |
| [GPT-4o](https://platform.openai.com/docs/models/gpt-4o) | LLM — raciocínio e síntese |
| [Tavily Search](https://tavily.com/) | Busca web em tempo real |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | Agentic loop e gerenciamento de estado |
| Python 3.12+ | Linguagem base |

## Como funciona

O agente opera em um loop agentic:

```
User Query
    ↓
LLM (GPT-4o) raciocina sobre o que pesquisar
    ↓
TavilySearch busca fontes reais na web
    ↓
LLM processa e sintetiza os resultados
    ↓
Resposta estruturada
```

A "personalidade" do agente é definida em texto simples no `system_prompt`:

```python
agent = create_deep_agent(
    model=llm,
    tools=[search_tool],
    system_prompt=(
        "Você é um pesquisador sênior. Sua tarefa é investigar tópicos profundamente, "
        "usando a ferramenta de busca para encontrar informações precisas e organizar "
        "seus achados. Sempre forneça uma resposta conclusiva e bem estruturada."
    )
)
```

## Setup

**Pré-requisitos:** Python 3.12+, [uv](https://docs.astral.sh/uv/) (ou pip)

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/ai-research-agent.git
cd ai-research-agent

# 2. Instale as dependências
uv sync
# ou: pip install -e .

# 3. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas chaves de API

# 4. Execute o agente
python main.py
```

## Variáveis de ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```env
OPENAI_API_KEY=sk-proj-...
TAVILY_API_KEY=tvly-...
```

- **OPENAI_API_KEY**: obtenha em [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **TAVILY_API_KEY**: obtenha em [app.tavily.com](https://app.tavily.com/) (plano gratuito disponível)

## Estrutura do projeto

```
ai-research-agent/
├── main.py          # Agente principal (create + run)
├── test_agent.py    # Testes unitários
├── pyproject.toml   # Dependências e configuração
├── .env.example     # Template de variáveis de ambiente
└── .gitignore
```

## Testes

```bash
pytest test_agent.py -v
```

## Possibilidades de expansão

Este projeto é intencionalmente minimalista. O framework `deepagents` oferece middlewares prontos para expandir:

- **FilesystemMiddleware** — leitura e escrita de arquivos
- **MemoryMiddleware** — memória persistente entre sessões
- **SubAgentMiddleware** — orquestração de múltiplos agentes
- **TodoListMiddleware** — planejamento e execução de tarefas

## Licença

MIT
