#!/usr/bin/env python3
"""
🛒 MCP MARKETPLACE - Sistema Inteligente de Ferramentas
Sistema central para descobrir, ativar e gerenciar ferramentas MCP para todos os agentes
Baseado na documentação oficial do AutoGen e artigo do Victor Dibia
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime

# AutoGen MCP imports
try:
    from autogen_ext.tools.mcp import (
        StdioServerParams, 
        SseServerParams, 
        StreamableHttpServerParams,
        mcp_server_tools,
        create_mcp_server_session,
        McpWorkbench
    )
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("⚠️  AutoGen MCP não disponível. Execute: pip install -U 'autogen-ext[mcp]'")

@dataclass
class MCPServer:
    """Definição de um servidor MCP disponível no marketplace"""
    id: str
    name: str
    description: str
    category: str
    install_command: str
    server_params: Dict[str, Any]
    tools_preview: List[str]
    requirements: List[str] = field(default_factory=list)
    documentation_url: str = ""
    supported_domains: List[str] = field(default_factory=list)
    performance_rating: int = 5  # 1-5 estrelas
    security_level: str = "official"  # official, community, experimental
    last_updated: str = ""
    status: str = "available"  # available, installing, installed, error

@dataclass
class AgentToolConfig:
    """Configuração de ferramentas para um agente específico"""
    agent_name: str
    domain: str
    enabled_servers: List[str] = field(default_factory=list)
    disabled_tools: List[str] = field(default_factory=list)
    custom_config: Dict[str, Any] = field(default_factory=dict)
    last_updated: str = ""

class MCPMarketplace:
    """
    🛒 Sistema Central de Marketplace de Ferramentas MCP
    
    Funcionalidades:
    - Descoberta automática de servidores MCP oficiais
    - Interface visual para ativar/desativar ferramentas
    - Configuração por agente/domínio
    - Cache inteligente de sessões
    - Monitoramento de performance
    """
    
    def __init__(self, config_path: str = "config/mcp_marketplace_config.json"):
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(exist_ok=True)
        self.logger = logging.getLogger("MCPMarketplace")
        
        # Catálogo oficial de servidores MCP (baseado na documentação)
        self.official_servers = self._load_official_catalog()
        
        # Configurações salvas
        self.agent_configs: Dict[str, AgentToolConfig] = {}
        self.server_cache: Dict[str, Any] = {}
        
        # Carregar configurações existentes
        self._load_configs()
    
    def _load_official_catalog(self) -> List[MCPServer]:
        """Catálogo oficial baseado na documentação do AutoGen MCP"""
        return [
            # 🏆 SERVIDORES OFICIAIS TOP-TIER
            MCPServer(
                id="github_official",
                name="GitHub MCP Server",
                description="Integração oficial GitHub - gestão de repositórios, PRs, issues",
                category="Development",
                install_command="docker pull ghcr.io/github/github-mcp-server",
                server_params={
                    "type": "stdio",
                    "command": "docker",
                    "args": [
                        "run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
                        "ghcr.io/github/github-mcp-server"
                    ],
                    "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"}
                },
                tools_preview=[
                    "create_repository", "list_repositories", "create_issue", 
                    "list_issues", "create_pr", "merge_pr", "search_code"
                ],
                requirements=["GITHUB_TOKEN"],
                documentation_url="https://github.com/github/github-mcp-server",
                supported_domains=["apis", "analytics", "copywriters", "knowledge"],
                performance_rating=5,
                security_level="official"
            ),
            
            MCPServer(
                id="filesystem_official",
                name="Filesystem MCP Server",
                description="Operações de sistema de arquivos - ler, escrever, listar",
                category="System",
                install_command="npm install -g @modelcontextprotocol/server-filesystem",
                server_params={
                    "type": "stdio",
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-filesystem", "{workspace_path}"]
                },
                tools_preview=[
                    "read_file", "write_file", "list_directory", 
                    "create_directory", "delete_file", "search_files"
                ],
                requirements=["Node.js 16+"],
                documentation_url="https://github.com/modelcontextprotocol/servers",
                supported_domains=["copywriters", "analytics", "knowledge"],
                performance_rating=5,
                security_level="official"
            ),
            
            MCPServer(
                id="fetch_official",
                name="Fetch MCP Server",
                description="Web scraping e fetching de conteúdo - APIs, páginas web",
                category="Web",
                install_command="pip install mcp-server-fetch",
                server_params={
                    "type": "stdio",
                    "command": "uvx",
                    "args": ["mcp-server-fetch"],
                    "read_timeout_seconds": 100
                },
                tools_preview=[
                    "fetch", "fetch_with_headers", "analyze_page", 
                    "extract_content", "download_file"
                ],
                requirements=["Python 3.8+"],
                documentation_url="https://github.com/anthropics/mcp-server-fetch",
                supported_domains=["copywriters", "apis", "analytics"],
                performance_rating=4,
                security_level="official"
            ),
            
            MCPServer(
                id="playwright_official",
                name="Playwright MCP Server",
                description="Automação web avançada - browser automation, screenshots",
                category="Web Automation",
                install_command="npm install -g @playwright/mcp@latest",
                server_params={
                    "type": "stdio",
                    "command": "npx",
                    "args": ["@playwright/mcp@latest", "--headless"],
                    "read_timeout_seconds": 60
                },
                tools_preview=[
                    "navigate", "click", "type", "screenshot", 
                    "extract_text", "wait_for_element", "scroll"
                ],
                requirements=["Node.js 16+", "Playwright browsers"],
                documentation_url="https://github.com/microsoft/playwright-mcp",
                supported_domains=["analytics", "copywriters"],
                performance_rating=4,
                security_level="official"
            ),
            
            # 🛠️ SERVIDORES ESPECIALIZADOS
            MCPServer(
                id="sqlite_official",
                name="SQLite MCP Server",
                description="Integração com bases de dados SQLite",
                category="Database",
                install_command="npm install -g @modelcontextprotocol/server-sqlite",
                server_params={
                    "type": "stdio",
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-sqlite", "{database_path}"]
                },
                tools_preview=[
                    "query", "execute", "list_tables", "describe_table",
                    "create_table", "insert_data", "backup"
                ],
                requirements=["Node.js 16+"],
                documentation_url="https://github.com/modelcontextprotocol/servers",
                supported_domains=["analytics", "apis"],
                performance_rating=4,
                security_level="official"
            ),
            
            MCPServer(
                id="postgres_official",
                name="PostgreSQL MCP Server",
                description="Integração com PostgreSQL - queries, schemas, data",
                category="Database",
                install_command="npm install -g @modelcontextprotocol/server-postgres",
                server_params={
                    "type": "stdio",
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-postgres"],
                    "env": {"DATABASE_URL": "${POSTGRES_URL}"}
                },
                tools_preview=[
                    "query", "execute", "list_schemas", "describe_table",
                    "analyze_performance", "backup", "migrate"
                ],
                requirements=["Node.js 16+", "POSTGRES_URL"],
                documentation_url="https://github.com/modelcontextprotocol/servers",
                supported_domains=["analytics", "apis"],
                performance_rating=4,
                security_level="official"
            ),
            
            MCPServer(
                id="brave_search",
                name="Brave Search MCP Server",
                description="Search web usando Brave Search API",
                category="Search",
                install_command="npm install -g @modelcontextprotocol/server-brave-search",
                server_params={
                    "type": "stdio",
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-brave-search"],
                    "env": {"BRAVE_API_KEY": "${BRAVE_API_KEY}"}
                },
                tools_preview=[
                    "web_search", "news_search", "image_search",
                    "local_search", "trending_topics"
                ],
                requirements=["Node.js 16+", "BRAVE_API_KEY"],
                documentation_url="https://github.com/modelcontextprotocol/servers",
                supported_domains=["copywriters", "analytics"],
                performance_rating=4,
                security_level="official"
            )
        ]
    
    def _load_configs(self):
        """Carrega configurações salvas dos agentes"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for agent_name, config_data in data.get('agent_configs', {}).items():
                    self.agent_configs[agent_name] = AgentToolConfig(**config_data)
                    
                self.logger.info(f"✅ Configurações carregadas para {len(self.agent_configs)} agentes")
            except Exception as e:
                self.logger.error(f"❌ Erro ao carregar configurações: {e}")
    
    def _save_configs(self):
        """Salva configurações dos agentes"""
        try:
            data = {
                'agent_configs': {
                    name: {
                        'agent_name': config.agent_name,
                        'domain': config.domain,
                        'enabled_servers': config.enabled_servers,
                        'disabled_tools': config.disabled_tools,
                        'custom_config': config.custom_config,
                        'last_updated': datetime.now().isoformat()
                    }
                    for name, config in self.agent_configs.items()
                },
                'last_save': datetime.now().isoformat()
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            self.logger.info("✅ Configurações salvas com sucesso")
        except Exception as e:
            self.logger.error(f"❌ Erro ao salvar configurações: {e}")
    
    def get_marketplace_catalog(self) -> Dict[str, List[MCPServer]]:
        """Retorna catálogo organizado por categorias"""
        catalog = {}
        for server in self.official_servers:
            if server.category not in catalog:
                catalog[server.category] = []
            catalog[server.category].append(server)
        return catalog
    
    def get_recommended_tools_for_domain(self, domain: str) -> List[MCPServer]:
        """Retorna ferramentas recomendadas para um domínio específico"""
        return [
            server for server in self.official_servers
            if domain in server.supported_domains
        ]
    
    def configure_agent_tools(self, agent_name: str, domain: str, 
                            enabled_servers: List[str],
                            custom_config: Dict[str, Any] = None) -> AgentToolConfig:
        """Configura ferramentas para um agente específico"""
        config = AgentToolConfig(
            agent_name=agent_name,
            domain=domain,
            enabled_servers=enabled_servers,
            custom_config=custom_config or {},
            last_updated=datetime.now().isoformat()
        )
        
        self.agent_configs[agent_name] = config
        self._save_configs()
        
        self.logger.info(f"🔧 Configurado {agent_name} com {len(enabled_servers)} servidores MCP")
        return config
    
    async def get_tools_for_agent(self, agent_name: str) -> List[Any]:
        """
        Retorna ferramentas MCP configuradas para um agente específico
        Esta é a função que será chamada pelos controllers dos agentes
        """
        if not MCP_AVAILABLE:
            self.logger.warning("⚠️  AutoGen MCP não disponível")
            return []
        
        if agent_name not in self.agent_configs:
            self.logger.warning(f"⚠️  Agente {agent_name} não tem configuração MCP")
            return []
        
        config = self.agent_configs[agent_name]
        all_tools = []
        
        for server_id in config.enabled_servers:
            try:
                server = next((s for s in self.official_servers if s.id == server_id), None)
                if not server:
                    self.logger.warning(f"⚠️  Servidor {server_id} não encontrado")
                    continue
                
                # Criar parâmetros do servidor
                server_params = self._create_server_params(server, config.custom_config)
                
                # Buscar ferramentas do servidor MCP
                tools = await mcp_server_tools(server_params)
                all_tools.extend(tools)
                
                self.logger.info(f"✅ {len(tools)} ferramentas carregadas de {server.name}")
                
            except Exception as e:
                self.logger.error(f"❌ Erro ao carregar servidor {server_id}: {e}")
        
        self.logger.info(f"🔧 Total: {len(all_tools)} ferramentas para {agent_name}")
        return all_tools
    
    def _create_server_params(self, server: MCPServer, custom_config: Dict[str, Any]):
        """Cria parâmetros do servidor com configurações personalizadas"""
        params = server.server_params.copy()
        
        # Aplicar configurações customizadas
        if custom_config:
            params.update(custom_config)
        
        # Expandir variáveis de ambiente
        workspace_path = str(Path.cwd())
        if 'args' in params:
            params['args'] = [
                arg.replace('{workspace_path}', workspace_path)
                for arg in params['args']
            ]
        
        # Criar objeto de parâmetros baseado no tipo
        if params.get('type') == 'stdio':
            return StdioServerParams(
                command=params['command'],
                args=params['args'],
                env=params.get('env', {}),
                read_timeout_seconds=params.get('read_timeout_seconds', 60)
            )
        elif params.get('type') == 'sse':
            return SseServerParams(
                url=params['url'],
                headers=params.get('headers', {}),
                timeout=params.get('timeout', 30)
            )
        elif params.get('type') == 'streamable_http':
            return StreamableHttpServerParams(
                url=params['url'],
                headers=params.get('headers', {}),
                timeout=params.get('timeout', 30)
            )
    
    def get_installation_commands(self, server_ids: List[str]) -> List[str]:
        """Retorna comandos de instalação para servidores específicos"""
        commands = []
        for server_id in server_ids:
            server = next((s for s in self.official_servers if s.id == server_id), None)
            if server:
                commands.append(f"# {server.name}")
                commands.append(server.install_command)
                commands.append("")
        return commands
    
    def generate_agent_integration_code(self, agent_name: str) -> str:
        """Gera código de integração para um agente específico"""
        if agent_name not in self.agent_configs:
            return "# Agente não configurado no marketplace MCP"
        
        config = self.agent_configs[agent_name]
        
        code = f'''
# 🛒 MCP Tools Integration para {agent_name}
# Gerado automaticamente pelo MCP Marketplace

from config.mcp_marketplace import MCPMarketplace

async def setup_mcp_tools():
    """Configura ferramentas MCP para {agent_name}"""
    marketplace = MCPMarketplace()
    tools = await marketplace.get_tools_for_agent("{agent_name}")
    return tools

# No seu controller, use:
# tools = await setup_mcp_tools()
# agent = AssistantAgent(name="{agent_name}", tools=tools, ...)
'''
        return code
    
    def get_usage_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas de uso do marketplace"""
        domain_usage = {}
        for agent_name, config in self.agent_configs.items():
            domain = config.domain
            if domain not in domain_usage:
                domain_usage[domain] = 0
            domain_usage[domain] += 1
        
        # Servidores mais populares
        server_usage = {}
        for config in self.agent_configs.values():
            for server_id in config.enabled_servers:
                if server_id not in server_usage:
                    server_usage[server_id] = 0
                server_usage[server_id] += 1
        
        most_popular = sorted(server_usage.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            'total_servers': len(self.official_servers),
            'configured_agents': len(self.agent_configs),
            'usage_by_domain': domain_usage,
            'most_popular_servers': [server_id for server_id, _ in most_popular],
            'total_tools_available': sum(len(server.tools_preview) for server in self.official_servers)
        }
    
    def export_domain_configuration(self, domain: str) -> Dict[str, Any]:
        """Exporta configuração de todos os agentes de um domínio"""
        domain_agents = {
            name: config for name, config in self.agent_configs.items()
            if config.domain == domain
        }
        
        return {
            'domain': domain,
            'agents_count': len(domain_agents),
            'agents': domain_agents,
            'recommended_servers': [
                server.id for server in self.get_recommended_tools_for_domain(domain)
            ],
            'export_date': datetime.now().isoformat()
        }

# 🌟 INSTANCE GLOBAL
marketplace = MCPMarketplace()

# 🚀 FUNÇÕES DE CONVENIÊNCIA PARA OS AGENTES
async def get_agent_mcp_tools(agent_name: str) -> List[Any]:
    """Função de conveniência para controllers de agentes"""
    return await marketplace.get_tools_for_agent(agent_name)

def configure_agent_mcp(agent_name: str, domain: str, servers: List[str], 
                       custom_config: Dict[str, Any] = None) -> AgentToolConfig:
    """Função de conveniência para configurar MCP de um agente"""
    return marketplace.configure_agent_tools(agent_name, domain, servers, custom_config) 