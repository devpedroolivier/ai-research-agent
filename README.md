# AI Research Agent

Um agente de pesquisa autônomo construído com Python, LangGraph e GPT-4o. Ele busca informações na web em tempo real, analisa fontes e entrega respostas estruturadas — em menos de 60 linhas de código.

## O que ele faz

Dado um tópico ou pergunta, o sistema orquestrado:

1. O orquestrador planeja as etapas com **TodoListMiddleware**
2. Delega a busca de dados para `web_researcher` (Tavily)
3. Delega a estruturação do relatório para `report_writer`
4. Salva o relatório em `research_output/` via **FilesystemMiddleware**
5. Lê instruções persistentes de `.deepagents/AGENTS.md` via **MemoryMiddleware**

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
| `FilesystemBackend` | Acesso seguro ao sistema de arquivos |
| Python 3.12+ | Linguagem base |

## Como funciona

O sistema opera com um orquestrador que coordena 2 sub-agentes especializados:

```
User Query
    ↓
Orquestrador (GPT-4o) — planeja etapas com write_todos
        ↓                           ↓
web_researcher              report_writer
(Tavily Search)         (estrutura + salva .md)
        ↓                           ↓
   Dados brutos          research_output/*.md
        ↓
Resposta consolidada ao usuário
```

Middlewares ativos e como são ativados:

| Middleware | Como ativar | O que faz |
|---|---|---|
| `FilesystemMiddleware` | `backend=FilesystemBackend(...)` | Agente lê/escreve arquivos |
| `MemoryMiddleware` | `memory=[".deepagents/AGENTS.md"]` | Instruções persistentes |
| `SubAgentMiddleware` | `subagents=[...]` | Orquestração de especialistas |
| `TodoListMiddleware` | Built-in automático | Planejamento de tarefas |

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
├── main.py                    # Orquestrador + subagentes + todos os middlewares
├── test_agent.py              # Testes unitários e de integração
├── pyproject.toml             # Dependências e configuração
├── .deepagents/
│   └── AGENTS.md              # Instruções persistentes (MemoryMiddleware)
├── research_output/           # Relatórios gerados (FilesystemMiddleware)
│   └── .gitkeep
├── .env.example               # Template de variáveis de ambiente
└── .gitignore
```

## Testes

```bash
pytest test_agent.py -v
```

## Expandindo o sistema

Para adicionar um novo especialista, defina um `SubAgent` e inclua em `subagents=`:

```python
NOVO_ESPECIALISTA: SubAgent = {
    "name": "data_analyst",
    "description": "Analisa dados numéricos e gera insights.",
    "system_prompt": "Você é um analista de dados especializado...",
    "tools": [...],
    "model": ChatOpenAI(model="gpt-4o", temperature=0),
}
```

## Licença

MIT
