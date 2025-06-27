#!/usr/bin/env python3
"""
🚀 MCP MARKETPLACE SETUP
Script de configuração inteligente que analisa nossos agentes e sugere/configura
automaticamente as melhores ferramentas MCP para cada um
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Set
import sys
sys.path.append(str(Path(__file__).parent.parent))

try:
    from config.mcp_marketplace import MCPMarketplace, configure_agent_mcp
except ImportError:
    # Adicionar caminho para encontrar o módulo config
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config.mcp_marketplace import MCPMarketplace, configure_agent_mcp

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MCPMarketplaceSetup")

class MCPMarketplaceSetup:
    """
    Setup inteligente do MCP Marketplace
    Analisa agentes existentes e configura automaticamente as melhores ferramentas
    """
    
    def __init__(self):
        self.marketplace = MCPMarketplace()
        self.domains_path = Path("domains")
        
        # Mapeamentos inteligentes baseados na especialização dos agentes
        self.agent_specialization_mapping = {
            # Copywriters - ferramentas de web e análise
            "conversion_catalyst": ["fetch_official", "brave_search", "filesystem_official"],
            "neurohook_ultra": ["fetch_official", "brave_search", "filesystem_official"],
            "pain_detector": ["fetch_official", "brave_search", "filesystem_official"],
            "paradigm_architect": ["fetch_official", "brave_search", "filesystem_official"],
            "metaphor_architect": ["fetch_official", "brave_search", "filesystem_official"],
            "retention_architect": ["fetch_official", "brave_search", "filesystem_official"],
            
            # APIs - integração com databases e GitHub
            "APIUnifyMaster": ["github_official", "postgres_official", "fetch_official"],
            "HotmartAPIMaster": ["fetch_official", "postgres_official", "sqlite_official"],
            "KiwifyAPIMaster": ["fetch_official", "postgres_official", "sqlite_official"],
            "PerfectpayAPIMaster": ["fetch_official", "postgres_official", "sqlite_official"],
            "PaytAPIMaster": ["fetch_official", "postgres_official", "sqlite_official"],
            "APIsImputOutputMapper": ["fetch_official", "postgres_official", "filesystem_official"],
            
            # Analytics - databases e automação web
            "ANALYTICSGPT | Super Track": ["postgres_official", "sqlite_official", "playwright_official", "fetch_official"],
            
            # Knowledge - filesystem e GitHub
            "DocRAGOptimizer": ["filesystem_official", "github_official", "fetch_official"]
        }
        
        # Configurações específicas por domínio
        self.domain_configs = {
            "copywriters": {
                "timeout_multiplier": 1.5,  # Mais tempo para research
                "custom_env": {"RESEARCH_MODE": "creative"}
            },
            "apis": {
                "timeout_multiplier": 1.0,  # Tempo padrão
                "custom_env": {"API_MODE": "production"}
            },
            "analytics": {
                "timeout_multiplier": 2.0,  # Mais tempo para processamento
                "custom_env": {"ANALYTICS_MODE": "batch"}
            },
            "knowledge": {
                "timeout_multiplier": 1.8,  # Tempo para indexação
                "custom_env": {"KNOWLEDGE_MODE": "index"}
            }
        }
    
    async def run_setup(self):
        """Executa setup completo do marketplace"""
        print("🚀 INICIANDO SETUP DO MCP MARKETPLACE")
        print("=" * 50)
        
        # 1. Descobrir agentes existentes
        agents_discovered = await self._discover_agents()
        
        # 2. Configurar agentes automaticamente
        await self._auto_configure_agents(agents_discovered)
        
        # 3. Gerar comandos de instalação
        await self._generate_installation_script()
        
        # 4. Criar exemplos de integração
        await self._create_integration_examples()
        
        # 5. Gerar relatório
        await self._generate_setup_report()
        
        print("\n✅ SETUP CONCLUÍDO COM SUCESSO!")
        print("🌐 Execute: streamlit run config/mcp_marketplace_ui.py")
        print("📋 Para abrir a interface visual do marketplace")
    
    async def _discover_agents(self) -> Dict[str, List[str]]:
        """Descobre todos os agentes do sistema"""
        print("\n🔍 DESCOBRINDO AGENTES...")
        
        agents_data = {}
        total_agents = 0
        
        if not self.domains_path.exists():
            print("❌ Diretório domains/ não encontrado")
            return {}
        
        for domain_path in self.domains_path.iterdir():
            if domain_path.is_dir() and domain_path.name != "__pycache__":
                domain_name = domain_path.name
                agents_path = domain_path / "agents"
                
                if agents_path.exists():
                    agents_data[domain_name] = []
                    
                    for agent_path in agents_path.iterdir():
                        if agent_path.is_dir():
                            manifest_path = agent_path / "agent_manifest.json"
                            if manifest_path.exists():
                                try:
                                    with open(manifest_path, 'r', encoding='utf-8') as f:
                                        manifest = json.load(f)
                                    
                                    agent_name = manifest.get("agent_name", agent_path.name)
                                    agents_data[domain_name].append(agent_name)
                                    total_agents += 1
                                    
                                    print(f"  ✅ {domain_name}/{agent_name}")
                                    
                                except Exception as e:
                                    print(f"  ⚠️  Erro ao ler manifest {agent_path.name}: {e}")
        
        print(f"\n📊 DESCOBERTOS: {total_agents} agentes em {len(agents_data)} domínios")
        return agents_data
    
    async def _auto_configure_agents(self, agents_data: Dict[str, List[str]]):
        """Configura automaticamente agentes com as melhores ferramentas"""
        print("\n🔧 CONFIGURANDO AGENTES AUTOMATICAMENTE...")
        
        configured_count = 0
        
        for domain, agents in agents_data.items():
            print(f"\n📂 Domínio: {domain.upper()}")
            
            # Configuração base do domínio
            domain_config = self.domain_configs.get(domain, {})
            
            for agent_name in agents:
                try:
                    # Determinar ferramentas para este agente
                    recommended_servers = self._get_recommended_servers_for_agent(agent_name, domain)
                    
                    # Configurações customizadas
                    custom_config = {
                        "read_timeout_seconds": int(60 * domain_config.get("timeout_multiplier", 1.0)),
                        "env_overrides": domain_config.get("custom_env", {}),
                        "auto_configured": True,
                        "configuration_date": "2025-01-12",
                        "specialization": self._get_agent_specialization(agent_name)
                    }
                    
                    # Configurar no marketplace
                    configure_agent_mcp(
                        agent_name=agent_name,
                        domain=domain,
                        servers=recommended_servers,
                        custom_config=custom_config
                    )
                    
                    servers_names = [
                        next((s.name for s in self.marketplace.official_servers if s.id == sid), sid)
                        for sid in recommended_servers
                    ]
                    
                    print(f"  ✅ {agent_name}: {', '.join(servers_names)}")
                    configured_count += 1
                    
                except Exception as e:
                    print(f"  ❌ Erro configurando {agent_name}: {e}")
        
        print(f"\n🎯 CONFIGURADOS: {configured_count} agentes com ferramentas MCP")
    
    def _get_recommended_servers_for_agent(self, agent_name: str, domain: str) -> List[str]:
        """Retorna servidores recomendados para um agente específico"""
        
        # Primeiro, verificar mapeamento específico
        if agent_name in self.agent_specialization_mapping:
            return self.agent_specialization_mapping[agent_name]
        
        # Caso contrário, usar recomendações por domínio
        domain_recommendations = {
            "copywriters": ["fetch_official", "brave_search", "filesystem_official"],
            "apis": ["fetch_official", "postgres_official", "filesystem_official"],
            "analytics": ["postgres_official", "sqlite_official", "playwright_official"],
            "knowledge": ["filesystem_official", "github_official", "fetch_official"]
        }
        
        return domain_recommendations.get(domain, ["fetch_official", "filesystem_official"])
    
    def _get_agent_specialization(self, agent_name: str) -> str:
        """Retorna a especialização de um agente baseado no nome"""
        specializations = {
            "conversion_catalyst": "Otimização de conversão e análise de decisão neurológica",
            "neurohook_ultra": "Geração de hooks e otimização de atenção psicológica",
            "pain_detector": "Detecção de dores e mapeamento de necessidades emocionais",
            "paradigm_architect": "Transformação paradigmática e engenharia de linguagem",
            "metaphor_architect": "Criação de metáforas e mapeamento isomórfico",
            "retention_architect": "Estruturas de tensão e engenharia de retenção",
            "APIUnifyMaster": "Unificação e orquestração de múltiplas APIs",
            "HotmartAPIMaster": "Integração completa com API Hotmart",
            "KiwifyAPIMaster": "Integração completa com API Kiwify",
            "PerfectpayAPIMaster": "Integração completa com API Perfectpay",
            "PaytAPIMaster": "Integração completa com API Payt",
            "APIsImputOutputMapper": "Mapeamento e transformação de dados entre APIs",
            "ANALYTICSGPT | Super Track": "Análise de dados e geração de insights avançados",
            "DocRAGOptimizer": "Otimização RAG e processamento de documentos"
        }
        
        return specializations.get(agent_name, "Agente especializado")
    
    async def _generate_installation_script(self):
        """Gera script de instalação para todos os servidores MCP configurados"""
        print("\n📦 GERANDO SCRIPT DE INSTALAÇÃO...")
        
        # Coletar todos os servidores ativos
        active_servers = set()
        for config in self.marketplace.agent_configs.values():
            active_servers.update(config.enabled_servers)
        
        if not active_servers:
            print("  ⚠️  Nenhum servidor ativo encontrado")
            return
        
        # Gerar comandos
        install_commands = self.marketplace.get_installation_commands(list(active_servers))
        
        # Criar script de instalação
        script_content = f"""#!/bin/bash
# 🛠️ MCP MARKETPLACE - Script de Instalação Automática
# Gerado automaticamente em {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

echo "🚀 Instalando servidores MCP..."
echo "================================"

# Verificar dependências
echo "🔍 Verificando dependências..."
which node >/dev/null 2>&1 || {{ echo "❌ Node.js não encontrado. Instale Node.js 16+"; exit 1; }}
which python3 >/dev/null 2>&1 || {{ echo "❌ Python3 não encontrado"; exit 1; }}
which docker >/dev/null 2>&1 || {{ echo "⚠️  Docker não encontrado (necessário para alguns servidores)"; }}

echo "✅ Dependências verificadas"
echo ""

# Comandos de instalação
{chr(10).join(install_commands)}

echo ""
echo "✅ Instalação concluída!"
echo "🌐 Execute: streamlit run config/mcp_marketplace_ui.py"
echo "📋 Para gerenciar as ferramentas MCP"
"""
        
        script_path = Path("scripts/install_mcp_servers.sh")
        script_path.write_text(script_content)
        script_path.chmod(0o755)  # Tornar executável
        
        print(f"  ✅ Script criado: {script_path}")
        print(f"  🚀 Execute: chmod +x {script_path} && ./{script_path}")
    
    async def _create_integration_examples(self):
        """Cria exemplos de integração para cada agente configurado"""
        print("\n📋 CRIANDO EXEMPLOS DE INTEGRAÇÃO...")
        
        examples_dir = Path("examples/mcp_integration")
        examples_dir.mkdir(parents=True, exist_ok=True)
        
        # Exemplo geral
        general_example = '''
# 🛒 EXEMPLO DE INTEGRAÇÃO MCP - Template Geral
# Como usar ferramentas MCP em qualquer agente

import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.mcp_marketplace import get_agent_mcp_tools

async def create_agent_with_mcp_tools(agent_name: str):
    """Cria um agente com ferramentas MCP configuradas"""
    
    # 1. Buscar ferramentas MCP configuradas para este agente
    tools = await get_agent_mcp_tools(agent_name)
    
    # 2. Configurar modelo
    model_client = OpenAIChatCompletionClient(model="gpt-4o")
    
    # 3. Criar agente com ferramentas MCP
    agent = AssistantAgent(
        name=agent_name,
        model_client=model_client,
        tools=tools,  # ← Ferramentas MCP automaticamente carregadas!
        system_message=f"Você é {agent_name} com acesso a ferramentas MCP avançadas.",
        reflect_on_tool_use=True,
        model_client_stream=True
    )
    
    return agent

# Exemplo de uso
async def main():
    # Substituir por qualquer agente configurado no marketplace
    agent = await create_agent_with_mcp_tools("neurohook_ultra")
    
    # O agente agora tem acesso a todas as ferramentas MCP configuradas!
    result = await agent.run("Pesquise sobre neurociência da atenção e gere um hook persuasivo")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
'''
        
        (examples_dir / "general_integration_example.py").write_text(general_example)
        
        # Exemplos específicos por agente configurado
        examples_created = 0
        for agent_name, config in self.marketplace.agent_configs.items():
            
            # Determinar ferramentas específicas
            enabled_tools = []
            for server_id in config.enabled_servers:
                server = next((s for s in self.marketplace.official_servers if s.id == server_id), None)
                if server:
                    enabled_tools.extend(server.tools_preview[:3])  # Primeiras 3 ferramentas
            
            agent_example = f'''
# 🤖 EXEMPLO MCP - {agent_name.upper()}
# Especialização: {self._get_agent_specialization(agent_name)}
# Domínio: {config.domain}

import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.mcp_marketplace import get_agent_mcp_tools

async def create_{agent_name.lower().replace(' ', '_')}_with_mcp():
    """Cria {agent_name} com ferramentas MCP otimizadas"""
    
    # Carregar ferramentas MCP configuradas especificamente para {agent_name}
    tools = await get_agent_mcp_tools("{agent_name}")
    
    # Configurar modelo otimizado para {config.domain}
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        temperature=0.7,
        max_tokens=2000
    )
    
    # Criar agente especializado
    agent = AssistantAgent(
        name="{agent_name}",
        model_client=model_client,
        tools=tools,
        system_message="""
        Você é {agent_name}, especializado em: {self._get_agent_specialization(agent_name)}
        
        Você tem acesso às seguintes ferramentas MCP:
        {', '.join(enabled_tools[:5])}
        
        Use essas ferramentas para oferecer insights profundos e acionáveis.
        """,
        reflect_on_tool_use=True
    )
    
    return agent

# Exemplo de uso específico para {agent_name}
async def test_{agent_name.lower().replace(' ', '_')}():
    agent = await create_{agent_name.lower().replace(' ', '_')}_with_mcp()
    
    # Prompt específico para testar as capacidades do agente
    prompt = "{"Demonstre suas capacidades usando as ferramentas MCP disponíveis" if config.domain == "copywriters" else "Analise dados de exemplo usando suas ferramentas MCP" if config.domain == "analytics" else "Execute operações de API usando ferramentas MCP" if config.domain == "apis" else "Processe documentos usando ferramentas MCP"}"
    
    result = await agent.run(prompt)
    print(f"Resultado de {agent_name}:")
    print(result)

if __name__ == "__main__":
    asyncio.run(test_{agent_name.lower().replace(' ', '_')}())
'''
            
            filename = f"{agent_name.lower().replace(' ', '_').replace('|', '')}_mcp_example.py"
            (examples_dir / filename).write_text(agent_example)
            examples_created += 1
        
        print(f"  ✅ {examples_created + 1} exemplos criados em {examples_dir}")
    
    async def _generate_setup_report(self):
        """Gera relatório completo do setup"""
        print("\n📊 GERANDO RELATÓRIO DE SETUP...")
        
        # Estatísticas
        total_agents = len(self.marketplace.agent_configs)
        total_servers = len(set(
            server_id 
            for config in self.marketplace.agent_configs.values() 
            for server_id in config.enabled_servers
        ))
        
        # Contar por domínio
        domain_stats = {}
        for config in self.marketplace.agent_configs.values():
            domain = config.domain
            if domain not in domain_stats:
                domain_stats[domain] = {"agents": 0, "servers": set()}
            domain_stats[domain]["agents"] += 1
            domain_stats[domain]["servers"].update(config.enabled_servers)
        
        # Formatear estatísticas por domínio
        domain_breakdown = []
        for domain, stats in domain_stats.items():
            domain_breakdown.append(f"  • {domain}: {stats['agents']} agentes, {len(stats['servers'])} servidores únicos")
        
        report = f"""
# 🛒 MCP MARKETPLACE - Relatório de Setup
**Data:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Estatísticas Gerais
- **Agentes Configurados:** {total_agents}
- **Servidores MCP Únicos:** {total_servers}
- **Domínios Ativos:** {len(domain_stats)}

## 📂 Breakdown por Domínio
{chr(10).join(domain_breakdown)}

## 🛠️ Servidores MCP Ativos
{chr(10).join([f"  • {server.name} ({server.category})" for server in self.marketplace.official_servers if server.id in set(sid for config in self.marketplace.agent_configs.values() for sid in config.enabled_servers)])}

## 🚀 Próximos Passos

### 1. Instalar Servidores MCP
```bash
chmod +x scripts/install_mcp_servers.sh
./scripts/install_mcp_servers.sh
```

### 2. Abrir Interface Visual
```bash
streamlit run config/mcp_marketplace_ui.py
```

### 3. Testar Integração
```bash
cd examples/mcp_integration
python general_integration_example.py
```

## 📋 Configuração por Agente

{chr(10).join([f"### {agent_name} ({config.domain}){chr(10)}**Servidores:** {', '.join(config.enabled_servers)}{chr(10)}**Especialização:** {self._get_agent_specialization(agent_name)}{chr(10)}" for agent_name, config in self.marketplace.agent_configs.items()])}

## 🔧 Comandos Úteis

### Reconfigurar um agente específico:
```python
from config.mcp_marketplace import configure_agent_mcp
configure_agent_mcp("agent_name", "domain", ["server1", "server2"])
```

### Listar ferramentas disponíveis:
```python
from config.mcp_marketplace import marketplace
catalog = marketplace.get_marketplace_catalog()
```

### Buscar ferramentas por domínio:
```python
tools = marketplace.get_recommended_tools_for_domain("copywriters")
```

---
✅ **Setup concluído com sucesso!** O MCP Marketplace está pronto para uso.
"""
        
        report_path = Path("docs/MCP_MARKETPLACE_SETUP_REPORT.md")
        report_path.write_text(report)
        
        print(f"  ✅ Relatório salvo: {report_path}")

async def main():
    """Função principal"""
    setup = MCPMarketplaceSetup()
    await setup.run_setup()

if __name__ == "__main__":
    # Adicionar pandas import
    import pandas as pd
    asyncio.run(main()) 