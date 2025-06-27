#!/usr/bin/env python3
"""
🎯 GERENCIADOR CENTRAL DE AGENTES - SISTEMA MULTI-AGENT AI v3.0
Orquestra todas as estruturas centrais de agentes, sub-agentes, prompts, modelos e tools
Permite deploy organizado para AutoGen, LangSmith, OpenAI e outras plataformas
"""

import json
import yaml
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

from .agent_structure import AgentCore, AgentLoader, Tool, LLMConfig, AgentMetadata, AgentType
from .adapters.autogen_adapter import AutoGenAdapter
from .adapters.langsmith_adapter import LangSmithAdapter

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DeploymentConfig:
    """Configuração de deployment para cada plataforma"""
    platform: str
    enabled: bool = True
    endpoint: Optional[str] = None
    config: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.config is None:
            self.config = {}

@dataclass
class CentralRegistry:
    """Registro central de todos os agentes do sistema"""
    domains: Dict[str, List[AgentCore]]
    total_agents: int
    total_sub_agents: int
    total_tools: int
    last_updated: str
    deployment_configs: Dict[str, DeploymentConfig]
    
    def __post_init__(self):
        if self.deployment_configs is None:
            self.deployment_configs = {}

class CentralAgentManager:
    """Gerenciador central de toda a estrutura de agentes"""
    
    def __init__(self, domains_path: str = "domains", backup_enabled: bool = True):
        self.domains_path = Path(domains_path)
        self.backup_enabled = backup_enabled
        self.agent_loader = AgentLoader(str(self.domains_path))
        self.registry: Optional[CentralRegistry] = None
        
        # Adaptadores para diferentes plataformas
        self.adapters = {
            "autogen": AutoGenAdapter(),
            "langsmith": LangSmithAdapter(),
        }
        
        # Configurações de deployment padrão
        self.default_deployments = {
            "autogen": DeploymentConfig(
                platform="autogen",
                enabled=True,
                endpoint="http://localhost:8081",
                config={
                    "db_path": str(Path.home() / ".autogenstudio" / "autogen04202.db"),
                    "ui_port": 8081
                }
            ),
            "langsmith": DeploymentConfig(
                platform="langsmith",
                enabled=True,
                endpoint="http://127.0.0.1:8082",
                config={
                    "output_dir": "langgraph_controllers",
                    "project_name": "multi-agent-ai-system",
                    "tracing": True
                }
            ),
            "mcp": DeploymentConfig(
                platform="mcp",
                enabled=True,
                endpoint="http://localhost:8000",
                config={
                    "server_count": 3,
                    "tools_enabled": True,
                    "config_file": "mcp_integration/mcp_config.json"
                }
            )
        }
    
    def create_backup(self) -> Path:
        """Cria backup completo da estrutura atual"""
        if not self.backup_enabled:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = Path(f"backups/agents_backup_{timestamp}")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup dos domains
        if self.domains_path.exists():
            shutil.copytree(self.domains_path, backup_dir / "domains")
        
        # Backup dos controllers
        controllers_dir = Path("langgraph_controllers")
        if controllers_dir.exists():
            shutil.copytree(controllers_dir, backup_dir / "langgraph_controllers")
        
        # Backup da integração MCP
        mcp_dir = Path("mcp_integration")
        if mcp_dir.exists():
            shutil.copytree(mcp_dir, backup_dir / "mcp_integration")
        
        logger.info(f"✅ Backup criado: {backup_dir}")
        return backup_dir
    
    def load_all_agents(self) -> CentralRegistry:
        """Carrega todos os agentes de todos os domínios"""
        logger.info("🔄 Carregando todos os agentes do sistema...")
        
        # Criar backup antes de qualquer operação
        backup_path = self.create_backup()
        
        domains = {}
        total_agents = 0
        total_sub_agents = 0
        total_tools = 0
        
        # Verificar se existe índice de domínios
        domains_index_file = self.domains_path / "domains_index.json"
        if domains_index_file.exists():
            with open(domains_index_file, 'r', encoding='utf-8') as f:
                domains_index = json.load(f)
            logger.info(f"📋 Índice encontrado: {domains_index['domains_index']['total_domains']} domínios")
        
        # Processar cada domínio
        for domain_dir in self.domains_path.iterdir():
            if domain_dir.is_dir() and domain_dir.name != "__pycache__":
                domain_name = domain_dir.name
                logger.info(f"📁 Processando domínio: {domain_name}")
                
                domain_agents = []
                agents_dir = domain_dir / "agents"
                
                if agents_dir.exists():
                    for agent_dir in agents_dir.iterdir():
                        if agent_dir.is_dir():
                            try:
                                agent = self.agent_loader.load_agent_from_directory(agent_dir, domain_name)
                                domain_agents.append(agent)
                                total_agents += 1
                                total_sub_agents += len(agent.sub_agents)
                                total_tools += len(agent.tools)
                                
                                # Contabilizar ferramentas dos sub-agentes
                                for sub_agent in agent.sub_agents:
                                    total_tools += len(sub_agent.tools)
                                
                                logger.info(f"  ✅ {agent.name}: {len(agent.sub_agents)} sub-agentes, {len(agent.tools)} ferramentas")
                                
                            except Exception as e:
                                logger.error(f"  ❌ Erro ao carregar {agent_dir.name}: {e}")
                
                domains[domain_name] = domain_agents
                logger.info(f"  📊 {domain_name}: {len(domain_agents)} agentes carregados")
        
        # Criar registro central
        self.registry = CentralRegistry(
            domains=domains,
            total_agents=total_agents,
            total_sub_agents=total_sub_agents,
            total_tools=total_tools,
            last_updated=datetime.now().isoformat(),
            deployment_configs=self.default_deployments
        )
        
        logger.info(f"🎉 CARREGAMENTO CONCLUÍDO!")
        logger.info(f"📊 ESTATÍSTICAS GLOBAIS:")
        logger.info(f"   • Domínios: {len(domains)}")
        logger.info(f"   • Agentes principais: {total_agents}")
        logger.info(f"   • Sub-agentes: {total_sub_agents}")
        logger.info(f"   • Total de ferramentas: {total_tools}")
        logger.info(f"   • Backup: {backup_path}")
        
        return self.registry
    
    def validate_agent_structure(self, agent: AgentCore) -> Tuple[bool, List[str]]:
        """Valida a estrutura de um agente"""
        issues = []
        
        # Validar campos obrigatórios
        if not agent.name or len(agent.name.strip()) == 0:
            issues.append("Nome do agente está vazio")
        
        if not agent.system_message or len(agent.system_message.strip()) < 50:
            issues.append(f"System message muito pequeno: {len(agent.system_message)} chars")
        
        if not agent.metadata.domain:
            issues.append("Domínio não especificado")
        
        # Validar ferramentas
        for tool in agent.tools:
            if not tool.name or not tool.description:
                issues.append(f"Ferramenta incompleta: {tool.name}")
        
        # Validar sub-agentes
        for sub_agent in agent.sub_agents:
            sub_valid, sub_issues = self.validate_agent_structure(sub_agent)
            if not sub_valid:
                issues.extend([f"Sub-agente {sub_agent.name}: {issue}" for issue in sub_issues])
        
        return len(issues) == 0, issues
    
    def optimize_agent_structure(self) -> Dict[str, Any]:
        """Otimiza a estrutura de todos os agentes"""
        if not self.registry:
            raise ValueError("Registry não carregado. Execute load_all_agents() primeiro.")
        
        logger.info("🔧 Iniciando otimização da estrutura de agentes...")
        
        optimization_report = {
            "timestamp": datetime.now().isoformat(),
            "agents_analyzed": 0,
            "agents_optimized": 0,
            "issues_found": [],
            "optimizations_applied": [],
            "performance_improvements": []
        }
        
        for domain_name, agents in self.registry.domains.items():
            logger.info(f"🔍 Otimizando domínio: {domain_name}")
            
            for agent in agents:
                optimization_report["agents_analyzed"] += 1
                
                # Validar estrutura
                is_valid, issues = self.validate_agent_structure(agent)
                if not is_valid:
                    optimization_report["issues_found"].extend(
                        [f"{domain_name}/{agent.name}: {issue}" for issue in issues]
                    )
                
                # Otimizações automáticas
                optimizations = []
                
                # 1. Otimizar configuração LLM
                if agent.llm_config.temperature > 0.9:
                    agent.llm_config.temperature = 0.8
                    optimizations.append("Temperatura ajustada para melhor consistência")
                
                # 2. Otimizar tamanho do prompt
                if len(agent.system_message) > 8000:
                    logger.warning(f"Prompt muito longo em {agent.name}: {len(agent.system_message)} chars")
                
                # 3. Otimizar ferramentas duplicadas
                unique_tools = {}
                for tool in agent.tools:
                    if tool.name not in unique_tools:
                        unique_tools[tool.name] = tool
                
                if len(unique_tools) < len(agent.tools):
                    agent.tools = list(unique_tools.values())
                    optimizations.append(f"Removidas {len(agent.tools) - len(unique_tools)} ferramentas duplicadas")
                
                if optimizations:
                    optimization_report["agents_optimized"] += 1
                    optimization_report["optimizations_applied"].extend(
                        [f"{domain_name}/{agent.name}: {opt}" for opt in optimizations]
                    )
        
        logger.info(f"✅ Otimização concluída: {optimization_report['agents_optimized']}/{optimization_report['agents_analyzed']} agentes otimizados")
        return optimization_report
    
    def deploy_to_platform(self, platform: str, force: bool = False) -> bool:
        """Deploy para uma plataforma específica"""
        if not self.registry:
            raise ValueError("Registry não carregado. Execute load_all_agents() primeiro.")
        
        if platform not in self.adapters:
            raise ValueError(f"Plataforma não suportada: {platform}")
        
        config = self.registry.deployment_configs.get(platform)
        if not config or not config.enabled:
            logger.warning(f"Deploy para {platform} está desabilitado")
            return False
        
        logger.info(f"🚀 Iniciando deploy para {platform}...")
        
        try:
            adapter = self.adapters[platform]
            success = adapter.deploy_agents(self.registry.domains)
            
            if success:
                logger.info(f"✅ Deploy para {platform} concluído com sucesso!")
                
                # Atualizar registro de deploy
                config.config["last_deployed"] = datetime.now().isoformat()
                config.config["deployment_status"] = "success"
            else:
                logger.error(f"❌ Falha no deploy para {platform}")
                config.config["deployment_status"] = "failed"
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Erro durante deploy para {platform}: {e}")
            return False
    
    def deploy_all_platforms(self) -> Dict[str, bool]:
        """Deploy para todas as plataformas habilitadas"""
        results = {}
        
        for platform_name in self.adapters.keys():
            try:
                results[platform_name] = self.deploy_to_platform(platform_name)
            except Exception as e:
                logger.error(f"Erro no deploy para {platform_name}: {e}")
                results[platform_name] = False
        
        return results
    
    def generate_mcp_integration(self) -> bool:
        """Gera integração MCP otimizada"""
        if not self.registry:
            raise ValueError("Registry não carregado.")
        
        logger.info("🔧 Gerando integração MCP otimizada...")
        
        mcp_config = {
            "version": "2.0",
            "name": "multi-agent-ai-system-mcp-optimized",
            "description": "MCP Integration Optimized for Multi-Agent AI System v3.0",
            "created_at": datetime.now().isoformat(),
            "agents": {
                "langgraph_controllers": [],
                "autogen_agents": [],
                "mcp_tools": []
            },
            "optimization_features": {
                "caching_enabled": True,
                "batch_processing": True,
                "async_execution": True,
                "monitoring": True
            }
        }
        
        # Processar agentes para MCP
        for domain_name, agents in self.registry.domains.items():
            for agent in agents:
                # Adicionar controller LangGraph
                mcp_config["agents"]["langgraph_controllers"].append({
                    "name": agent.name,
                    "type": "langgraph",
                    "domain": domain_name,
                    "file": f"langgraph_controllers/{domain_name}/{agent.name.lower().replace(' ', '_')}_controller.py",
                    "endpoint": f"/langgraph/{agent.name}",
                    "tools_count": len(agent.tools),
                    "sub_agents_count": len(agent.sub_agents)
                })
                
                # Adicionar sub-agentes como agentes AutoGen
                for sub_agent in agent.sub_agents:
                    mcp_config["agents"]["autogen_agents"].append({
                        "name": sub_agent.name,
                        "type": "autogen",
                        "domain": domain_name,
                        "parent": agent.name,
                        "file": f"domains/{domain_name}/agents/{agent.name}/sub_agents/{sub_agent.name}/autogen/{sub_agent.name}_agent.py",
                        "endpoint": f"/autogen/{domain_name}/{sub_agent.name}"
                    })
                
                # Adicionar ferramentas como MCP tools
                for tool in agent.tools:
                    mcp_config["agents"]["mcp_tools"].append({
                        "name": tool.name,
                        "type": tool.type,
                        "description": tool.description,
                        "enabled": tool.enabled,
                        "parent_agent": agent.name,
                        "domain": domain_name,
                        "config": tool.config
                    })
        
        # Salvar configuração MCP otimizada
        mcp_config_file = Path("mcp_integration/mcp_config_optimized.json")
        with open(mcp_config_file, 'w', encoding='utf-8') as f:
            json.dump(mcp_config, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Configuração MCP otimizada salva: {mcp_config_file}")
        return True
    
    def generate_status_report(self) -> Dict[str, Any]:
        """Gera relatório completo do status do sistema"""
        if not self.registry:
            return {"error": "Registry não carregado"}
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "system_overview": {
                "total_domains": len(self.registry.domains),
                "total_agents": self.registry.total_agents,
                "total_sub_agents": self.registry.total_sub_agents,
                "total_tools": self.registry.total_tools
            },
            "domains_detail": {},
            "deployment_status": {},
            "optimization_status": "pending",
            "recommendations": []
        }
        
        # Detalhar cada domínio
        for domain_name, agents in self.registry.domains.items():
            report["domains_detail"][domain_name] = {
                "agents_count": len(agents),
                "agents": []
            }
            
            for agent in agents:
                agent_info = {
                    "name": agent.name,
                    "sub_agents_count": len(agent.sub_agents),
                    "tools_count": len(agent.tools),
                    "prompt_length": len(agent.system_message),
                    "specialization": agent.metadata.specialization
                }
                report["domains_detail"][domain_name]["agents"].append(agent_info)
        
        # Status de deployment
        for platform, config in self.registry.deployment_configs.items():
            report["deployment_status"][platform] = {
                "enabled": config.enabled,
                "endpoint": config.endpoint,
                "last_deployed": config.config.get("last_deployed", "never"),
                "status": config.config.get("deployment_status", "pending")
            }
        
        # Recomendações
        if self.registry.total_agents > 50:
            report["recommendations"].append("Sistema com muitos agentes - considere otimização de performance")
        
        if self.registry.total_tools > 200:
            report["recommendations"].append("Muitas ferramentas - considere consolidação")
        
        return report
    
    def save_registry(self, file_path: str = "core/central_registry.json") -> bool:
        """Salva o registry central em arquivo"""
        if not self.registry:
            return False
        
        try:
            # Converter para formato serializável
            registry_data = {
                "domains": {
                    domain: [asdict(agent) for agent in agents]
                    for domain, agents in self.registry.domains.items()
                },
                "total_agents": self.registry.total_agents,
                "total_sub_agents": self.registry.total_sub_agents,
                "total_tools": self.registry.total_tools,
                "last_updated": self.registry.last_updated,
                "deployment_configs": {
                    platform: asdict(config)
                    for platform, config in self.registry.deployment_configs.items()
                }
            }
            
            registry_file = Path(file_path)
            registry_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(registry_file, 'w', encoding='utf-8') as f:
                json.dump(registry_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Registry salvo: {registry_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar registry: {e}")
            return False

# Instância global do gerenciador
manager = CentralAgentManager()

if __name__ == "__main__":
    # Teste completo do sistema
    print("🚀 INICIANDO SISTEMA CENTRAL DE GERENCIAMENTO DE AGENTES")
    print("=" * 60)
    
    # 1. Carregar todos os agentes
    registry = manager.load_all_agents()
    
    # 2. Otimizar estruturas
    optimization_report = manager.optimize_agent_structure()
    print(f"📈 Otimizações aplicadas: {len(optimization_report['optimizations_applied'])}")
    
    # 3. Gerar integração MCP
    manager.generate_mcp_integration()
    
    # 4. Salvar registry
    manager.save_registry()
    
    # 5. Gerar relatório
    report = manager.generate_status_report()
    print(f"📊 Relatório gerado com {report['system_overview']['total_agents']} agentes")
    
    print("\n✅ SISTEMA CENTRAL PRONTO PARA DEPLOYMENT!") 