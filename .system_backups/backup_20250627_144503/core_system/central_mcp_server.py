#!/usr/bin/env python3
"""
🎯 SERVIDOR MCP CENTRAL - SISTEMA MULTI-AGENT AI v3.0
Servidor MCP avançado que integra com o gerenciador central de agentes
Suporte completo para AutoGen, LangSmith e todas as ferramentas
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Importações MCP
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

# Importações do sistema
import sys
sys.path.append('..')
from core.central_agent_manager import CentralAgentManager, manager

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("central_mcp_server")

class CentralMCPServer:
    """Servidor MCP central para integração com sistema de agentes"""
    
    def __init__(self):
        self.server = Server("multi-agent-ai-system-central")
        self.manager = manager
        self.registry = None
        self.cache = {}
        self.performance_metrics = {
            "requests_count": 0,
            "cache_hits": 0,
            "errors_count": 0,
            "start_time": datetime.now()
        }
        
        # Registrar todas as ferramentas MCP
        self._register_tools()
    
    def _register_tools(self):
        """Registra todas as ferramentas MCP centrais"""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """Lista todas as ferramentas disponíveis"""
            return [
                Tool(
                    name="load_agent_system",
                    description="Carrega todo o sistema de agentes do registry central",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "force_reload": {
                                "type": "boolean",
                                "description": "Força recarregamento completo dos agentes",
                                "default": False
                            },
                            "include_backup": {
                                "type": "boolean", 
                                "description": "Cria backup antes do carregamento",
                                "default": True
                            }
                        }
                    }
                ),
                Tool(
                    name="optimize_agents",
                    description="Otimiza estrutura de todos os agentes do sistema",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "domain_filter": {
                                "type": "string",
                                "description": "Filtro por domínio específico (opcional)"
                            },
                            "validation_only": {
                                "type": "boolean",
                                "description": "Apenas validar sem aplicar otimizações",
                                "default": False
                            }
                        }
                    }
                ),
                Tool(
                    name="deploy_to_platform",
                    description="Deploy agentes para plataforma específica (AutoGen/LangSmith)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "platform": {
                                "type": "string",
                                "enum": ["autogen", "langsmith", "all"],
                                "description": "Plataforma de destino"
                            },
                            "force": {
                                "type": "boolean",
                                "description": "Força deploy mesmo se já foi feito",
                                "default": False
                            }
                        },
                        "required": ["platform"]
                    }
                ),
                Tool(
                    name="get_system_status",
                    description="Obtém status completo do sistema de agentes",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "detailed": {
                                "type": "boolean",
                                "description": "Incluir detalhes completos de cada domínio",
                                "default": True
                            }
                        }
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Executa ferramentas MCP centrais"""
            self.performance_metrics["requests_count"] += 1
            
            try:
                if name == "load_agent_system":
                    return await self._load_agent_system(arguments)
                elif name == "optimize_agents":
                    return await self._optimize_agents(arguments)
                elif name == "deploy_to_platform":
                    return await self._deploy_to_platform(arguments)
                elif name == "get_system_status":
                    return await self._get_system_status(arguments)
                else:
                    raise ValueError(f"Ferramenta desconhecida: {name}")
                    
            except Exception as e:
                self.performance_metrics["errors_count"] += 1
                logger.error(f"Erro ao executar {name}: {e}")
                return [TextContent(type="text", text=f"❌ Erro: {str(e)}")]
    
    async def _load_agent_system(self, args: Dict[str, Any]) -> List[TextContent]:
        """Carrega sistema completo de agentes"""
        force_reload = args.get("force_reload", False)
        include_backup = args.get("include_backup", True)
        
        if not force_reload and self.registry:
            self.performance_metrics["cache_hits"] += 1
            return [TextContent(
                type="text",
                text=f"✅ Sistema já carregado (cache). {self.registry.total_agents} agentes disponíveis."
            )]
        
        try:
            # Carregar sistema
            self.registry = self.manager.load_all_agents()
            self.cache["registry"] = self.registry
            
            result = {
                "status": "success",
                "message": "Sistema de agentes carregado com sucesso",
                "statistics": {
                    "total_domains": len(self.registry.domains),
                    "total_agents": self.registry.total_agents,
                    "total_sub_agents": self.registry.total_sub_agents,
                    "total_tools": self.registry.total_tools
                },
                "domains": list(self.registry.domains.keys()),
                "last_updated": self.registry.last_updated
            }
            
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
            
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Erro ao carregar sistema: {str(e)}")]
    
    async def _optimize_agents(self, args: Dict[str, Any]) -> List[TextContent]:
        """Otimiza estrutura de agentes"""
        if not self.registry:
            return [TextContent(type="text", text="❌ Sistema não carregado. Execute load_agent_system primeiro.")]
        
        domain_filter = args.get("domain_filter")
        validation_only = args.get("validation_only", False)
        
        try:
            if validation_only:
                # Apenas validação
                issues_found = []
                for domain_name, agents in self.registry.domains.items():
                    if domain_filter and domain_name != domain_filter:
                        continue
                    
                    for agent in agents:
                        is_valid, issues = self.manager.validate_agent_structure(agent)
                        if not is_valid:
                            issues_found.extend([f"{domain_name}/{agent.name}: {issue}" for issue in issues])
                
                result = {
                    "status": "validation_complete",
                    "issues_found": len(issues_found),
                    "issues": issues_found[:10]  # Primeiros 10
                }
            else:
                # Otimização completa
                optimization_report = self.manager.optimize_agent_structure()
                result = optimization_report
            
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
            
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Erro na otimização: {str(e)}")]
    
    async def _deploy_to_platform(self, args: Dict[str, Any]) -> List[TextContent]:
        """Deploy para plataforma específica"""
        if not self.registry:
            return [TextContent(type="text", text="❌ Sistema não carregado. Execute load_agent_system primeiro.")]
        
        platform = args.get("platform")
        force = args.get("force", False)
        
        try:
            if platform == "all":
                results = self.manager.deploy_all_platforms()
                result = {
                    "status": "deployment_complete",
                    "platforms": results,
                    "successful": sum(1 for success in results.values() if success),
                    "total": len(results)
                }
            else:
                success = self.manager.deploy_to_platform(platform, force)
                result = {
                    "status": "deployment_complete",
                    "platform": platform,
                    "success": success,
                    "message": f"Deploy para {platform} {'bem-sucedido' if success else 'falhou'}"
                }
            
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
            
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Erro no deploy: {str(e)}")]
    
    async def _get_system_status(self, args: Dict[str, Any]) -> List[TextContent]:
        """Obtém status completo do sistema"""
        if not self.registry:
            return [TextContent(type="text", text="❌ Sistema não carregado. Execute load_agent_system primeiro.")]
        
        detailed = args.get("detailed", True)
        
        try:
            report = self.manager.generate_status_report()
            
            if not detailed:
                # Versão simplificada
                simplified_report = {
                    "timestamp": report["timestamp"],
                    "system_overview": report["system_overview"],
                    "deployment_status": {
                        platform: status["status"]
                        for platform, status in report["deployment_status"].items()
                    }
                }
                report = simplified_report
            
            return [TextContent(type="text", text=json.dumps(report, indent=2, ensure_ascii=False))]
            
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Erro ao obter status: {str(e)}")]

async def main():
    """Função principal do servidor MCP central"""
    logger.info("🚀 Iniciando Servidor MCP Central - Multi-Agent AI System v3.0")
    
    # Criar instância do servidor
    mcp_server = CentralMCPServer()
    
    # Carregar sistema automaticamente na inicialização
    logger.info("🔄 Carregando sistema de agentes automaticamente...")
    try:
        mcp_server.registry = mcp_server.manager.load_all_agents()
        logger.info(f"✅ Sistema carregado: {mcp_server.registry.total_agents} agentes disponíveis")
    except Exception as e:
        logger.error(f"❌ Erro ao carregar sistema: {e}")
    
    # Iniciar servidor via stdio
    logger.info("🌐 Servidor MCP Central pronto para conexões")
    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.server.run(read_stream, write_stream, mcp_server.server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main()) 