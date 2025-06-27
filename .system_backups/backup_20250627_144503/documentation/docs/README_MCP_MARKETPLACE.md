# 🛒 MCP MARKETPLACE - Sistema Inteligente de Ferramentas

> **Marketplace visual para descobrir, configurar e gerenciar ferramentas MCP (Model Context Protocol) para todos os seus agentes AutoGen**

Baseado na [documentação oficial do AutoGen MCP](https://microsoft.github.io/autogen/stable/reference/python/autogen_ext.tools.mcp.html) e no excelente [artigo do Victor Dibia](https://newsletter.victordibia.com/p/how-to-use-mcp-anthropic-mcp-tools).

## 🎯 O Que É?

O MCP Marketplace resolve o problema de **"Como facilmente ativar e desativar ferramentas MCP para qualquer agente"** criando:

- **🛒 Interface visual** para descobrir ferramentas MCP oficiais
- **⚡ Configuração em 2 cliques** para qualquer agente
- **🔧 Auto-configuração inteligente** baseada no domínio do agente
- **📋 Geração automática** de código de integração
- **🎯 Recomendações personalizadas** por especialização

## 🚀 Início Rápido

### 1. Lançar o Sistema

```bash
# Execute o lançador interativo
./launch_mcp_marketplace.sh
```

### 2. Setup Automático (Primeira vez)

No menu do lançador, escolha:
- **Opção 2**: 🔧 Executar Setup Automático

Isso irá:
- ✅ Descobrir todos os seus agentes automaticamente
- ⚡ Configurar ferramentas MCP recomendadas para cada domínio
- 📋 Gerar exemplos de integração
- 🛠️ Criar scripts de instalação

### 3. Abrir Interface Visual

No menu do lançador, escolha:
- **Opção 1**: 🌐 Abrir Interface Visual

Ou diretamente:
```bash
streamlit run config/mcp_marketplace_ui.py
```

## 🛠️ Ferramentas MCP Disponíveis

### 🏆 **Servidores Oficiais Top-Tier**

| Servidor | Descrição | Domínios Recomendados | Rating |
|----------|-----------|----------------------|--------|
| **GitHub MCP** | Gestão de repositórios, PRs, issues | APIs, Analytics, Knowledge | ⭐⭐⭐⭐⭐ |
| **Fetch MCP** | Web scraping e fetching de conteúdo | Copywriters, APIs, Analytics | ⭐⭐⭐⭐ |
| **Filesystem MCP** | Operações de sistema de arquivos | Copywriters, Analytics, Knowledge | ⭐⭐⭐⭐⭐ |
| **Playwright MCP** | Automação web avançada | Analytics, Copywriters | ⭐⭐⭐⭐ |

### 🛢️ **Servidores de Database**

| Servidor | Descrição | Domínios Recomendados |
|----------|-----------|----------------------|
| **PostgreSQL MCP** | Integração PostgreSQL completa | Analytics, APIs |
| **SQLite MCP** | Database SQLite local | Analytics, APIs |

### 🔍 **Servidores de Search**

| Servidor | Descrição | Domínios Recomendados |
|----------|-----------|----------------------|
| **Brave Search MCP** | Search web usando Brave API | Copywriters, Analytics |

## 🤖 Integração com Agentes

### Modo 1: Automático (Recomendado)

```python
# Apenas 2 linhas para carregar todas as ferramentas MCP configuradas!
from config.mcp_marketplace import get_agent_mcp_tools

tools = await get_agent_mcp_tools("neurohook_ultra")
agent = AssistantAgent(name="neurohook_ultra", tools=tools, ...)
```

### Modo 2: Configuração Manual

```python
from config.mcp_marketplace import configure_agent_mcp

# Configurar ferramentas específicas
configure_agent_mcp(
    agent_name="pain_detector",
    domain="copywriters", 
    servers=["fetch_official", "brave_search", "filesystem_official"]
)
```

## 📋 Exemplos Práticos

### 🧠 NeuroHook Ultra com MCP

```bash
# Testar NeuroHook Ultra com ferramentas MCP
python3 examples/mcp_integration/neurohook_ultra_mcp_controller.py
```

### 📊 Analytics Agent com Database

```python
# Automático: agente com PostgreSQL + SQLite + Playwright
tools = await get_agent_mcp_tools("ANALYTICSGPT | Super Track")
agent = AssistantAgent(name="analytics", tools=tools, ...)
```

### 🔗 API Agent com GitHub Integration

```python
# Automático: agente com GitHub + PostgreSQL + Fetch
tools = await get_agent_mcp_tools("APIUnifyMaster")
agent = AssistantAgent(name="api_master", tools=tools, ...)
```

## 🎯 Configurações por Domínio

### 📝 **Copywriters** 
**Ferramentas:** Web Fetch + Search + Filesystem  
**Timeout:** 1.5x (mais tempo para research)  
**Agentes:** `neurohook_ultra`, `pain_detector`, `conversion_catalyst`, etc.

### 🔗 **APIs**
**Ferramentas:** GitHub + Database + Fetch  
**Timeout:** 1.0x (tempo padrão)  
**Agentes:** `APIUnifyMaster`, `HotmartAPIMaster`, `KiwifyAPIMaster`, etc.

### 📊 **Analytics**
**Ferramentas:** Databases + Web Automation + Fetch  
**Timeout:** 2.0x (mais tempo para processamento)  
**Agentes:** `ANALYTICSGPT | Super Track`

### 📚 **Knowledge**
**Ferramentas:** Filesystem + GitHub + Fetch  
**Timeout:** 1.8x (tempo para indexação)  
**Agentes:** `DocRAGOptimizer`

## 🛠️ Instalação de Servidores MCP

### Automática

```bash
# Via lançador - Opção 6: Instalar Servidores MCP
./launch_mcp_marketplace.sh

# Ou diretamente
chmod +x scripts/install_mcp_servers.sh
./scripts/install_mcp_servers.sh
```

### Manual

```bash
# GitHub MCP Server
docker pull ghcr.io/github/github-mcp-server

# Fetch MCP Server  
pip install mcp-server-fetch

# Filesystem MCP Server
npm install -g @modelcontextprotocol/server-filesystem

# Playwright MCP Server
npm install -g @playwright/mcp@latest
```

## 📊 Interface Visual - Funcionalidades

### 🛒 **Catálogo de Ferramentas**
- Navegar por categoria (Development, Web, Database, etc.)
- Filtrar por domínio e rating
- Ver preview de ferramentas disponíveis
- Links para documentação oficial

### 🤖 **Configurar Agentes**
- Descoberta automática de agentes existentes
- Recomendações inteligentes por domínio
- Configuração visual com checkboxes
- Editor JSON para configurações avançadas

### 📊 **Status dos Agentes**
- Tabela com status de configuração
- Gráficos de uso por domínio
- Estatísticas de popularidade dos servidores

### ⚙️ **Configurações Avançadas**
- Exportar/importar configurações
- Comandos de instalação automáticos
- Reset e limpeza de cache

## 🔧 API de Programação

### Marketplace Core

```python
from config.mcp_marketplace import marketplace

# Listar catálogo
catalog = marketplace.get_marketplace_catalog()

# Recomendações para domínio
tools = marketplace.get_recommended_tools_for_domain("copywriters")

# Configurar agente
config = marketplace.configure_agent_tools(
    agent_name="agent_name",
    domain="domain",
    enabled_servers=["server1", "server2"]
)
```

### Funções de Conveniência

```python
# Carregar ferramentas para agente específico
tools = await get_agent_mcp_tools("agent_name")

# Configuração rápida
configure_agent_mcp("agent_name", "domain", ["server1", "server2"])
```

## 🏗️ Arquitetura

```
config/
├── mcp_marketplace.py          # Core do marketplace
├── mcp_marketplace_ui.py       # Interface Streamlit
└── mcp_marketplace_config.json # Configurações salvas

scripts/
├── setup_mcp_marketplace.py    # Setup automático
└── install_mcp_servers.sh      # Instalação de servidores

examples/mcp_integration/
├── general_integration_example.py
├── neurohook_ultra_mcp_controller.py
└── [outros exemplos por agente]

launch_mcp_marketplace.sh       # Lançador principal
```

## 🎯 Casos de Uso

### 1. **Copywriter com Research em Tempo Real**
```python
# NeuroHook Ultra pesquisa tendências e gera hooks baseados em dados atuais
tools = await get_agent_mcp_tools("neurohook_ultra")
# Agente tem acesso a: Fetch, Brave Search, Filesystem
```

### 2. **API Master com Integração GitHub**
```python
# APIUnifyMaster gerencia repositórios e databases simultaneamente
tools = await get_agent_mcp_tools("APIUnifyMaster") 
# Agente tem acesso a: GitHub, PostgreSQL, Fetch
```

### 3. **Analytics com Automação Web**
```python
# Analytics coleta dados via web scraping + database
tools = await get_agent_mcp_tools("ANALYTICSGPT | Super Track")
# Agente tem acesso a: PostgreSQL, SQLite, Playwright, Fetch
```

## 🚀 Próximos Passos

1. **Execute**: `./launch_mcp_marketplace.sh`
2. **Configure**: Opção 2 (Setup Automático)
3. **Explore**: Opção 1 (Interface Visual)
4. **Teste**: Opção 3 (NeuroHook Demo)
5. **Integre**: Use `get_agent_mcp_tools()` nos seus controllers

## 📚 Recursos Adicionais

- 📖 [Documentação AutoGen MCP](https://microsoft.github.io/autogen/stable/reference/python/autogen_ext.tools.mcp.html)
- 📝 [Artigo Victor Dibia](https://newsletter.victordibia.com/p/how-to-use-mcp-anthropic-mcp-tools)
- 🔧 [Repositório MCP](https://github.com/modelcontextprotocol)
- 🛠️ [Servidores MCP Oficiais](https://github.com/modelcontextprotocol/servers)

---

✅ **O MCP Marketplace transforma a complexidade das ferramentas MCP em simplicidade visual!**

> 💡 **Dica**: Comece com o setup automático e depois personalize via interface visual conforme necessário. 