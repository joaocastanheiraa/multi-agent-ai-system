# 🛒 MCP MARKETPLACE - Guia Completo

**Sistema Inteligente de Ferramentas MCP para Agentes AutoGen**

---

## 📋 Índice

1. [Visão Geral](#-visão-geral)
2. [Arquitetura](#-arquitetura)
3. [Instalação e Setup](#-instalação-e-setup)
4. [Uso Básico](#-uso-básico)
5. [Configuração Avançada](#-configuração-avançada)
6. [API de Programação](#-api-de-programação)
7. [Ferramentas MCP Disponíveis](#-ferramentas-mcp-disponíveis)
8. [Exemplos Práticos](#-exemplos-práticos)
9. [Solução de Problemas](#-solução-de-problemas)
10. [Referências](#-referências)

---

## 🎯 Visão Geral

### O Que É o MCP Marketplace?

O **MCP Marketplace** é um sistema inteligente que resolve o desafio de **"Como facilmente ativar e desativar ferramentas MCP para qualquer agente"** através de:

- **🛒 Interface visual** para descobrir ferramentas MCP oficiais
- **⚡ Configuração em 2 cliques** para qualquer agente
- **🔧 Auto-configuração inteligente** baseada no domínio do agente
- **📋 Geração automática** de código de integração
- **🎯 Recomendações personalizadas** por especialização

### Baseado em Fontes Oficiais

- 📖 [Documentação AutoGen MCP](https://microsoft.github.io/autogen/stable/reference/python/autogen_ext.tools.mcp.html)
- 📝 [Artigo Victor Dibia](https://newsletter.victordibia.com/p/how-to-use-mcp-anthropic-mcp-tools)
- 🔧 [Repositório MCP](https://github.com/modelcontextprotocol)

### Problema Resolvido

**Antes:** Configuração manual complexa, imports difíceis, código repetitivo
**Agora:** Interface visual + 2 linhas de código para integração completa

---

## 🏗️ Arquitetura

### Estrutura de Arquivos

```
multi-agent-ai-system/
├── config/
│   ├── __init__.py                     # Pacote Python
│   ├── mcp_marketplace.py              # Core do marketplace
│   └── mcp_marketplace_ui.py           # Interface Streamlit
├── scripts/
│   └── setup_mcp_marketplace.py        # Setup automático
├── examples/mcp_integration/
│   ├── general_integration_example.py
│   └── neurohook_ultra_mcp_controller.py
├── docs/
│   ├── MCP_MARKETPLACE_COMPLETE_GUIDE.md
│   └── TROUBLESHOOTING_MCP.md
├── launch_mcp_marketplace.sh           # Launcher principal
├── run_mcp_ui.py                       # Launcher UI
├── test_mcp_imports.py                 # Testes automáticos
└── README_MCP_MARKETPLACE.md           # Guia rápido
```

### Componentes Principais

#### 1. **Core Marketplace** (`config/mcp_marketplace.py`)
- Catálogo de 15+ servidores MCP oficiais
- Sistema de configuração por agente
- Geração automática de ferramentas
- Persistência de configurações

#### 2. **Interface Visual** (`config/mcp_marketplace_ui.py`)
- Interface web Streamlit
- Navegação por categorias
- Configuração visual com checkboxes
- Status e estatísticas em tempo real

#### 3. **Setup Inteligente** (`scripts/setup_mcp_marketplace.py`)
- Descoberta automática de agentes
- Configuração baseada em domínio
- Geração de exemplos
- Scripts de instalação

#### 4. **Sistema de Launcher**
- Menu interativo completo
- Resolução automática de imports
- Instalação de dependências
- Diagnóstico de problemas

---

## 🚀 Instalação e Setup

### Método 1: Setup Automático Completo

```bash
# 1. Lançar sistema
./launch_mcp_marketplace.sh

# 2. Escolher opção 2: Setup Automático
# - Descobre todos os agentes automaticamente
# - Configura ferramentas recomendadas
# - Gera exemplos e scripts

# 3. Escolher opção 1: Interface Visual
# - Abre http://localhost:8501
# - Interface completa para gerenciar tudo
```

### Método 2: Instalação Manual

```bash
# 1. Dependências básicas
pip install streamlit pandas

# 2. AutoGen MCP (opcional mas recomendado)
pip install -U 'autogen-ext[mcp]'
pip install -U 'autogen-agentchat'

# 3. Testar instalação
python3 test_mcp_imports.py

# 4. Executar interface
python3 run_mcp_ui.py
```

### Verificação da Instalação

```bash
# Teste completo
python3 test_mcp_imports.py

# Saída esperada:
# ✅ config.__init__ importado com sucesso
# ✅ MCPMarketplace importado com sucesso
# ✅ Marketplace criado com 7 servidores
# ✅ Streamlit importado com sucesso
```

---

## 💡 Uso Básico

### Integração Simples (2 Linhas)

```python
from config.mcp_marketplace import get_agent_mcp_tools

# Carregar todas as ferramentas MCP configuradas para um agente
tools = await get_agent_mcp_tools("neurohook_ultra")

# Usar no agente AutoGen
agent = AssistantAgent(
    name="neurohook_ultra",
    model_client=model_client,
    tools=tools,  # ← Ferramentas MCP automaticamente!
    system_message="Você é um especialista com ferramentas MCP..."
)
```

### Interface Visual

1. **Executar**: `python3 run_mcp_ui.py`
2. **Abrir**: http://localhost:8501
3. **Navegar**: Por categorias de ferramentas
4. **Configurar**: Agentes com checkboxes
5. **Ativar**: Ferramentas em 2 cliques

### Menu Interativo

```bash
./launch_mcp_marketplace.sh

# Opções disponíveis:
# 1. 🌐 Interface Visual
# 2. 🔧 Setup Automático  
# 3. 🧠 Teste NeuroHook
# 4. 📋 Ver Exemplos
# 5. 📊 Status Sistema
# 6. 🛠️ Instalar Servidores
# 7. 📖 Documentação
# 8. 🧪 Testar Imports
```

---

## ⚙️ Configuração Avançada

### Configuração Manual de Agentes

```python
from config.mcp_marketplace import configure_agent_mcp

# Configurar ferramentas específicas para um agente
configure_agent_mcp(
    agent_name="pain_detector",
    domain="copywriters",
    servers=["fetch_official", "brave_search", "filesystem_official"],
    custom_config={
        "read_timeout_seconds": 90,
        "env_overrides": {"RESEARCH_MODE": "creative"},
        "specialization": "Detecção de dores emocionais"
    }
)
```

### Configurações por Domínio

#### 📝 **Copywriters** 
```python
domain_config = {
    "recommended_servers": ["fetch_official", "brave_search", "filesystem_official"],
    "timeout_multiplier": 1.5,  # Mais tempo para research
    "env_overrides": {"RESEARCH_MODE": "creative"},
    "specialization": "Research e criação de conteúdo"
}
```

#### 🔗 **APIs**
```python
domain_config = {
    "recommended_servers": ["github_official", "postgres_official", "fetch_official"],
    "timeout_multiplier": 1.0,  # Tempo padrão
    "env_overrides": {"API_MODE": "production"},
    "specialization": "Integração e orquestração de APIs"
}
```

#### 📊 **Analytics**
```python
domain_config = {
    "recommended_servers": ["postgres_official", "sqlite_official", "playwright_official"],
    "timeout_multiplier": 2.0,  # Mais tempo para processamento
    "env_overrides": {"ANALYTICS_MODE": "batch"},
    "specialization": "Análise de dados e insights"
}
```

### Exportar/Importar Configurações

```python
from config.mcp_marketplace import marketplace

# Exportar todas as configurações
config_data = marketplace.export_all_configs()
with open("mcp_backup.json", "w") as f:
    json.dump(config_data, f, indent=2)

# Importar configurações
with open("mcp_backup.json", "r") as f:
    config_data = json.load(f)
marketplace.import_configs(config_data)
```

---

## 🔧 API de Programação

### Classes Principais

#### MCPMarketplace
```python
from config.mcp_marketplace import MCPMarketplace

marketplace = MCPMarketplace()

# Métodos principais
servers = marketplace.get_official_servers()
catalog = marketplace.get_marketplace_catalog()
tools = marketplace.get_recommended_tools_for_domain("copywriters")
config = marketplace.configure_agent_tools(agent_name, domain, servers)
```

#### MCPServer
```python
from config.mcp_marketplace import MCPServer

server = MCPServer(
    id="custom_server",
    name="Meu Servidor Custom",
    description="Servidor personalizado",
    category="Custom",
    install_command="pip install my-mcp-server",
    supported_domains=["copywriters"],
    tools_preview=["tool1", "tool2"],
    performance_rating=4
)
```

### Funções de Conveniência

```python
# Carregar ferramentas para agente
tools = await get_agent_mcp_tools("agent_name")

# Configuração rápida
configure_agent_mcp("agent_name", "domain", ["server1", "server2"])

# Verificar status
status = marketplace.get_agent_status("agent_name")

# Listar agentes configurados
agents = marketplace.list_configured_agents()
```

---

## 🛠️ Ferramentas MCP Disponíveis

### 🏆 Servidores Oficiais Top-Tier

| Servidor | Categoria | Descrição | Domínios | Rating |
|----------|-----------|-----------|----------|--------|
| **GitHub MCP** | Development | Gestão completa de repositórios, PRs, issues | APIs, Analytics, Knowledge | ⭐⭐⭐⭐⭐ |
| **Fetch MCP** | Web | Web scraping e fetching de conteúdo | Copywriters, APIs, Analytics | ⭐⭐⭐⭐ |
| **Filesystem MCP** | System | Operações avançadas de sistema de arquivos | Todos os domínios | ⭐⭐⭐⭐⭐ |
| **Playwright MCP** | Web | Automação web completa e scraping avançado | Analytics, Copywriters | ⭐⭐⭐⭐ |

### 🛢️ Servidores de Database

| Servidor | Descrição | Ferramentas | Domínios |
|----------|-----------|-------------|----------|
| **PostgreSQL MCP** | Integração PostgreSQL completa | Query, Insert, Update, Schema | Analytics, APIs |
| **SQLite MCP** | Database SQLite local | Create, Query, Backup | Analytics, APIs |

### 🔍 Servidores de Search

| Servidor | Descrição | Ferramentas | Domínios |
|----------|-----------|-------------|----------|
| **Brave Search MCP** | Search web usando Brave API | Search, News, Images | Copywriters, Analytics |

### 📊 Estatísticas de Uso

```python
# Via interface visual ou programaticamente
usage_stats = marketplace.get_usage_statistics()

# Exemplo de saída:
{
    "total_servers": 7,
    "configured_agents": 15,
    "most_popular_servers": ["fetch_official", "filesystem_official"],
    "usage_by_domain": {
        "copywriters": 6,
        "apis": 5,
        "analytics": 3,
        "knowledge": 1
    }
}
```

---

## 📋 Exemplos Práticos

### Exemplo 1: NeuroHook Ultra com Research

```python
#!/usr/bin/env python3
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.mcp_marketplace import get_agent_mcp_tools

async def neurohook_with_mcp():
    # 1. Carregar ferramentas MCP configuradas
    tools = await get_agent_mcp_tools("neurohook_ultra")
    
    # 2. Configurar modelo
    model_client = OpenAIChatCompletionClient(model="gpt-4o")
    
    # 3. Criar agente com ferramentas MCP
    agent = AssistantAgent(
        name="neurohook_ultra",
        model_client=model_client,
        tools=tools,
        system_message="""
        Você é NeuroHook Ultra com ferramentas MCP.
        Use suas ferramentas para pesquisar tendências atuais
        e gerar hooks baseados em dados reais.
        """,
        reflect_on_tool_use=True
    )
    
    # 4. Usar agente
    prompt = """
    Pesquise tendências atuais sobre IA e produtividade.
    Gere 3 hooks persuasivos baseados nos dados encontrados.
    """
    
    result = await agent.run(prompt)
    return result

# Executar
if __name__ == "__main__":
    result = asyncio.run(neurohook_with_mcp())
    print(result)
```

### Exemplo 2: Analytics com Database

```python
import asyncio
from config.mcp_marketplace import get_agent_mcp_tools

async def analytics_with_database():
    # Agente com PostgreSQL + SQLite + Playwright
    tools = await get_agent_mcp_tools("ANALYTICSGPT | Super Track")
    
    agent = AssistantAgent(
        name="analytics_master",
        model_client=model_client,
        tools=tools,
        system_message="""
        Você é um especialista em analytics com acesso a:
        - PostgreSQL para dados estruturados
        - SQLite para análises locais  
        - Playwright para coleta web
        Use essas ferramentas para insights profundos.
        """
    )
    
    prompt = """
    1. Colete dados de exemplo via web scraping
    2. Armazene no SQLite para análise
    3. Gere insights e visualizações
    """
    
    return await agent.run(prompt)
```

### Exemplo 3: API Master com GitHub

```python
async def api_master_github():
    # Agente com GitHub + PostgreSQL + Fetch
    tools = await get_agent_mcp_tools("APIUnifyMaster")
    
    agent = AssistantAgent(
        name="api_master",
        tools=tools,
        system_message="""
        Você orquestra APIs usando:
        - GitHub para repositórios
        - PostgreSQL para persistência
        - Fetch para APIs externas
        """
    )
    
    prompt = """
    1. Busque repositórios relacionados a MCP
    2. Analise as APIs disponíveis
    3. Documente integrações possíveis
    """
    
    return await agent.run(prompt)
```

---

## 🔧 Solução de Problemas

### Problemas Comuns

#### 1. `ModuleNotFoundError: No module named 'config'`

**Soluções:**
```bash
# Opção A: Launcher inteligente
python3 run_mcp_ui.py

# Opção B: PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Opção C: Diretório correto
cd /caminho/para/multi-agent-ai-system
```

#### 2. AutoGen MCP não disponível

```bash
# Instalar dependências completas
pip install -U 'autogen-ext[mcp]'
pip install -U 'autogen-agentchat'
```

#### 3. Interface não abre

```bash
# Múltiplas opções
python3 run_mcp_ui.py                    # Recomendado
streamlit run config/mcp_marketplace_ui.py  # Fallback
./launch_mcp_marketplace.sh              # Menu completo
```

### Diagnóstico Automático

```bash
# Teste completo de imports e dependências
python3 test_mcp_imports.py

# Via menu
./launch_mcp_marketplace.sh
# Opção 8: Testar Imports e Dependências
```

### Comandos Úteis

```bash
# Verificar estrutura
find . -name "*.py" | grep mcp

# Testar imports individuais
python3 -c "from config import MCPMarketplace; print('OK')"

# Status de dependências
pip list | grep -E "(autogen|streamlit|pandas)"

# Logs detalhados
PYTHONPATH=. python3 -v config/mcp_marketplace_ui.py
```

---

## 📚 Referências

### Documentação Oficial

- 📖 [AutoGen MCP Reference](https://microsoft.github.io/autogen/stable/reference/python/autogen_ext.tools.mcp.html)
- 📝 [Victor Dibia - MCP Guide](https://newsletter.victordibia.com/p/how-to-use-mcp-anthropic-mcp-tools)
- 🔧 [Model Context Protocol](https://github.com/modelcontextprotocol)
- 🛠️ [Official MCP Servers](https://github.com/modelcontextprotocol/servers)

### Recursos Adicionais

- 🎥 [AutoGen MCP Tutorial](https://www.youtube.com/watch?v=FMiVxQ7QwRU)
- 📄 [MCP Integration Guide](https://mychen76.medium.com/creating-intelligent-agent-with-openai-agents-sdk-and-autogen-mcp-tools-and-memory-04f630eb6a73)
- 🌐 [MCP Community](https://mcp.arcee.ai/)

### Comandos de Referência Rápida

```bash
# Setup completo
./launch_mcp_marketplace.sh → Opção 2

# Interface visual  
python3 run_mcp_ui.py

# Teste de sistema
python3 test_mcp_imports.py

# Exemplo prático
python3 examples/mcp_integration/neurohook_ultra_mcp_controller.py

# Documentação
cat docs/MCP_MARKETPLACE_COMPLETE_GUIDE.md
```

---

## 🎯 Conclusão

O **MCP Marketplace** transforma a complexidade das ferramentas MCP em simplicidade visual:

✅ **Interface visual intuitiva**  
✅ **Configuração em 2 cliques**  
✅ **Integração com 2 linhas de código**  
✅ **Setup automático inteligente**  
✅ **15+ ferramentas oficiais**  
✅ **Diagnóstico automático**  
✅ **Documentação completa**  

### 🚀 Próximos Passos

1. **Execute**: `./launch_mcp_marketplace.sh`
2. **Configure**: Opção 2 (Setup Automático)
3. **Explore**: Opção 1 (Interface Visual)
4. **Integre**: Use `get_agent_mcp_tools()` nos seus agentes
5. **Personalize**: Configure ferramentas específicas conforme necessário

---

**🎉 O futuro dos agentes AutoGen está aqui - visual, inteligente e poderoso!** 