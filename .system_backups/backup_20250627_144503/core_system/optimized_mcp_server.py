#!/usr/bin/env python3
"""
🎯 SERVIDOR MCP OTIMIZADO - SISTEMA MULTI-AGENT AI v3.0
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
logger = logging.getLogger("optimized_mcp_server")

class OptimizedMCPServer:
    """Servidor MCP otimizado para integração com sistema central"""
    
    def __init__(self):
        self.server = Server("multi-agent-ai-system-optimized")
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
        """Registra todas as ferramentas MCP otimizadas"""
        
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
                    name="get_agent_details",
                    description="Obtém detalhes completos de um agente específico",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "agent_name": {
                                "type": "string",
                                "description": "Nome do agente"
                            },
                            "domain": {
                                "type": "string",
                                "description": "Domínio do agente"
                            },
                            "include_sub_agents": {
                                "type": "boolean",
                                "description": "Incluir informações dos sub-agentes",
                                "default": True
                            }
                        },
                        "required": ["agent_name"]
                    }
                ),
                Tool(
                    name="generate_mcp_config",
                    description="Gera configuração MCP otimizada para o sistema",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "output_file": {
                                "type": "string",
                                "description": "Arquivo de saída da configuração",
                                "default": "mcp_integration/mcp_config_optimized.json"
                            },
                            "include_metrics": {
                                "type": "boolean",
                                "description": "Incluir métricas de performance",
                                "default": True
                            }
                        }
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
                            },
                            "include_performance": {
                                "type": "boolean",
                                "description": "Incluir métricas de performance",
                                "default": True
                            }
                        }
                    }
                ),
                Tool(
                    name="validate_agent_structure",
                    description="Valida estrutura de agentes específicos ou todos",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "agent_name": {
                                "type": "string",
                                "description": "Nome do agente específico (opcional)"
                            },
                            "domain": {
                                "type": "string",
                                "description": "Domínio específico (opcional)"
                            },
                            "fix_issues": {
                                "type": "boolean",
                                "description": "Tentar corrigir problemas automaticamente",
                                "default": False
                            }
                        }
                    }
                ),
                Tool(
                    name="backup_system",
                    description="Cria backup completo do sistema de agentes",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "include_controllers": {
                                "type": "boolean",
                                "description": "Incluir controllers LangGraph",
                                "default": True
                            },
                            "include_mcp": {
                                "type": "boolean",
                                "description": "Incluir configurações MCP",
                                "default": True
                            },
                            "custom_name": {
                                "type": "string",
                                "description": "Nome customizado para o backup"
                            }
                        }
                    }
                ),
                Tool(
                    name="clear_cache",
                    description="Limpa cache interno do servidor MCP",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "cache_type": {
                                "type": "string",
                                "enum": ["all", "agents", "performance"],
                                "description": "Tipo de cache a limpar",
                                "default": "all"
                            }
                        }
                    }
                ),
                Tool(
                    name="get_performance_metrics",
                    description="Obtém métricas de performance do servidor MCP",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "reset_after": {
                                "type": "boolean",
                                "description": "Resetar métricas após obter",
                                "default": False
                            }
                        }
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Executa ferramentas MCP otimizadas"""
            self.performance_metrics["requests_count"] += 1
            
            try:
                if name == "load_agent_system":
                    return await self._load_agent_system(arguments)
                elif name == "optimize_agents":
                    return await self._optimize_agents(arguments)
                elif name == "deploy_to_platform":
                    return await self._deploy_to_platform(arguments)
                elif name == "get_agent_details":
                    return await self._get_agent_details(arguments)
                elif name == "generate_mcp_config":
                    return await self._generate_mcp_config(arguments)
                elif name == "get_system_status":
                    return await self._get_system_status(arguments)
                elif name == "validate_agent_structure":
                    return await self._validate_agent_structure(arguments)
                elif name == "backup_system":
                    return await self._backup_system(arguments)
                elif name == "clear_cache":
                    return await self._clear_cache(arguments)
                elif name == "get_performance_metrics":
                    return await self._get_performance_metrics(arguments)
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
    
    async def _get_agent_details(self, args: Dict[str, Any]) -> List[TextContent]:
        """Obtém detalhes de agente específico"""
        if not self.registry:
            return [TextContent(type="text", text="❌ Sistema não carregado. Execute load_agent_system primeiro.")]
        
        agent_name = args.get("agent_name")
        domain = args.get("domain")
        include_sub_agents = args.get("include_sub_agents", True)
        
        try:
            found_agent = None
            found_domain = None
            
            # Buscar agente
            for domain_name, agents in self.registry.domains.items():
                if domain and domain_name != domain:
                    continue
                
                for agent in agents:
                    if agent.name == agent_name:
                        found_agent = agent
                        found_domain = domain_name
                        break
                
                if found_agent:
                    break
            
            if not found_agent:
                return [TextContent(type="text", text=f"❌ Agente '{agent_name}' não encontrado")]
            
            # Construir detalhes
            details = {
                "name": found_agent.name,
                "domain": found_domain,
                "specialization": found_agent.metadata.specialization,
                "agent_type": found_agent.metadata.agent_type.value,
                "prompt_length": len(found_agent.system_message),
                "tools_count": len(found_agent.tools),
                "sub_agents_count": len(found_agent.sub_agents),
                "llm_config": {
                    "model": found_agent.llm_config.model,
                    "temperature": found_agent.llm_config.temperature,
                    "max_tokens": found_agent.llm_config.max_tokens
                },
                "tools": [
                    {
                        "name": tool.name,
                        "type": tool.type,
                        "description": tool.description,
                        "enabled": tool.enabled
                    } for tool in found_agent.tools
                ]
            }
            
            if include_sub_agents and found_agent.sub_agents:
                details["sub_agents"] = [
                    {
                        "name": sub.name,
                        "tools_count": len(sub.tools),
                        "prompt_length": len(sub.system_message)
                    } for sub in found_agent.sub_agents
                ]
            
            return [TextContent(type="text", text=json.dumps(details, indent=2, ensure_ascii=False))]
            
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Erro ao obter detalhes: {str(e)}")]
    
    async def _generate_mcp_config(self, args: Dict[str, Any]) -> List[TextContent]:
        """Gera configuração MCP otimizada"""
        if not self.registry:
            return [TextContent(type="text", text="❌ Sistema não carregado. Execute load_agent_system primeiro.")]
        
        output_file = args.get("output_file", "mcp_integration/mcp_config_optimized.json")
        include_metrics = args.get("include_metrics", True)
        
        try:
            success = self.manager.generate_mcp_integration()
            
            if include_metrics:
                # Adicionar métricas ao arquivo
                config_path = Path(output_file)
                if config_path.exists():
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    config["performance_metrics"] = self.performance_metrics
                    config["server_info"] = {
                        "server_name": "optimized_mcp_server",
                        "version": "2.0",
                        "uptime_seconds": (datetime.now() - self.performance_metrics["start_time"]).total_seconds()
                    }
                    
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(config, f, indent=2, ensure_ascii=False)
            
            result = {
                "status": "success",
                "output_file": output_file,
                "file_exists": Path(output_file).exists(),
                "mcp_integration_generated": success
            }
            
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
            
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Erro ao gerar configuração MCP: {str(e)}")]
    
    async def _get_system_status(self, args: Dict[str, Any]) -> List[TextContent]:
        """Obtém status completo do sistema"""
        if not self.registry:
            return [TextContent(type="text", text="❌ Sistema não carregado. Execute load_agent_system primeiro.")]
        
        detailed = args.get("detailed", True)
        include_performance = args.get("include_performance", True)
        
        try:
            report = self.manager.generate_status_report()
            
            if include_performance:
                report["mcp_server_metrics"] = self.performance_metrics
                report["mcp_server_metrics"]["uptime_seconds"] = (
                    datetime.now() - self.performance_metrics["start_time"]
                ).total_seconds()
            
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
    
    async def _validate_agent_structure(self, args: Dict[str, Any]) -> List[TextContent]:
        """Valida estrutura de agentes"""
        if not self.registry:
            return [TextContent(type="text", text="❌ Sistema não carregado. Execute load_agent_system primeiro.")]
        
        agent_name = args.get("agent_name")
        domain = args.get("domain")
        fix_issues = args.get("fix_issues", False)
        
        try:
            validation_results = {
                "timestamp": datetime.now().isoformat(),
                "agents_validated": 0,
                "agents_with_issues": 0,
                "issues_found": [],
                "issues_fixed": []
            }
            
            # Validar agentes específicos ou todos
            for domain_name, agents in self.registry.domains.items():
                if domain and domain_name != domain:
                    continue
                
                for agent in agents:
                    if agent_name and agent.name != agent_name:
                        continue
                    
                    validation_results["agents_validated"] += 1
                    is_valid, issues = self.manager.validate_agent_structure(agent)
                    
                    if not is_valid:
                        validation_results["agents_with_issues"] += 1
                        agent_issues = {
                            "agent": f"{domain_name}/{agent.name}",
                            "issues": issues
                        }
                        validation_results["issues_found"].append(agent_issues)
                        
                        if fix_issues:
                            # Tentar correções básicas
                            fixed = []
                            if "System message muito pequeno" in str(issues):
                                # Não podemos corrigir isso automaticamente
                                pass
                            
                            if fixed:
                                validation_results["issues_fixed"].extend(fixed)
            
            return [TextContent(type="text", text=json.dumps(validation_results, indent=2, ensure_ascii=False))]
            
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Erro na validação: {str(e)}")]
    
    async def _backup_system(self, args: Dict[str, Any]) -> List[TextContent]:
        """Cria backup do sistema"""
        include_controllers = args.get("include_controllers", True)
        include_mcp = args.get("include_mcp", True)
        custom_name = args.get("custom_name")
        
        try:
            backup_path = self.manager.create_backup()
            
            result = {
                "status": "success",
                "backup_path": str(backup_path),
                "timestamp": datetime.now().isoformat(),
                "includes": {
                    "domains": True,
                    "controllers": include_controllers,
                    "mcp_integration": include_mcp
                }
            }
            
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
            
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Erro no backup: {str(e)}")]
    
    async def _clear_cache(self, args: Dict[str, Any]) -> List[TextContent]:
        """Limpa cache do servidor"""
        cache_type = args.get("cache_type", "all")
        
        try:
            if cache_type == "all":
                self.cache.clear()
                self.registry = None
            elif cache_type == "agents":
                self.cache.pop("registry", None)
                self.registry = None
            elif cache_type == "performance":
                self.performance_metrics = {
                    "requests_count": 0,
                    "cache_hits": 0,
                    "errors_count": 0,
                    "start_time": datetime.now()
                }
            
            result = {
                "status": "success",
                "cache_cleared": cache_type,
                "timestamp": datetime.now().isoformat()
            }
            
            return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
            
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Erro ao limpar cache: {str(e)}")]
    
    async def _get_performance_metrics(self, args: Dict[str, Any]) -> List[TextContent]:
        """Obtém métricas de performance"""
        reset_after = args.get("reset_after", False)
        
        try:
            metrics = self.performance_metrics.copy()
            metrics["uptime_seconds"] = (datetime.now() - metrics["start_time"]).total_seconds()
            metrics["cache_hit_rate"] = (
                metrics["cache_hits"] / max(metrics["requests_count"], 1) * 100
            )
            metrics["error_rate"] = (
                metrics["errors_count"] / max(metrics["requests_count"], 1) * 100
            )
            
            if reset_after:
                self.performance_metrics = {
                    "requests_count": 0,
                    "cache_hits": 0,
                    "errors_count": 0,
                    "start_time": datetime.now()
                }
            
            return [TextContent(type="text", text=json.dumps(metrics, indent=2, default=str))]
            
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Erro ao obter métricas: {str(e)}")]

async def main():
    """Função principal do servidor MCP otimizado"""
    logger.info("🚀 Iniciando Servidor MCP Otimizado - Multi-Agent AI System v3.0")
    
    # Criar instância do servidor
    mcp_server = OptimizedMCPServer()
    
    # Carregar sistema automaticamente na inicialização
    logger.info("🔄 Carregando sistema de agentes automaticamente...")
    try:
        mcp_server.registry = mcp_server.manager.load_all_agents()
        logger.info(f"✅ Sistema carregado: {mcp_server.registry.total_agents} agentes disponíveis")
    except Exception as e:
        logger.error(f"❌ Erro ao carregar sistema: {e}")
    
    # Iniciar servidor via stdio
    logger.info("🌐 Servidor MCP pronto para conexões")
    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.server.run(read_stream, write_stream, mcp_server.server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main()) 