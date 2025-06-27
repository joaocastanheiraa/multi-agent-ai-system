#!/usr/bin/env python3
"""
🛒 MCP MARKETPLACE - Pacote de Configuração
Módulo principal para marketplace de ferramentas MCP
"""

# Imports principais para facilitar uso
try:
    from .mcp_marketplace import (
        MCPMarketplace,
        MCPServer, 
        AgentToolConfig,
        configure_agent_mcp,
        get_agent_mcp_tools
    )
    
    # Instância global do marketplace
    marketplace = MCPMarketplace()
    
    __all__ = [
        'MCPMarketplace',
        'MCPServer',
        'AgentToolConfig', 
        'configure_agent_mcp',
        'get_agent_mcp_tools',
        'marketplace'
    ]
    
except ImportError as e:
    print(f"⚠️  Erro ao importar módulos MCP: {e}")
    print("💡 Certifique-se de que as dependências estão instaladas")
    
    # Fallbacks para evitar crashes
    class MCPMarketplace:
        def __init__(self):
            pass
    
    class MCPServer:
        def __init__(self, **kwargs):
            pass
    
    class AgentToolConfig:
        def __init__(self, **kwargs):
            pass
    
    def configure_agent_mcp(*args, **kwargs):
        print("⚠️  MCP não disponível - modo fallback")
        return None
    
    async def get_agent_mcp_tools(agent_name):
        print(f"⚠️  MCP não disponível para {agent_name} - modo fallback")
        return []
    
    marketplace = MCPMarketplace()
    
    __all__ = [
        'MCPMarketplace',
        'MCPServer', 
        'AgentToolConfig',
        'configure_agent_mcp',
        'get_agent_mcp_tools',
        'marketplace'
    ] 