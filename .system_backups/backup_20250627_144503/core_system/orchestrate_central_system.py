#!/usr/bin/env python3
"""
🎯 ORQUESTRADOR CENTRAL DO SISTEMA MULTI-AGENT AI v3.0
Script principal para coordenar todas as estruturas centrais:
- Carregamento e validação de agentes
- Otimização e sincronização
- Deploy para AutoGen e LangSmith
- Integração MCP completa
- Backup automático
"""

import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime
import logging

# Adicionar paths necessários
sys.path.append('.')
sys.path.append('core')

from core.central_agent_manager import CentralAgentManager
from core.adapters.autogen_adapter import AutoGenAdapter
from core.adapters.langsmith_adapter import LangSmithAdapter

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("orchestrator")

class CentralOrchestrator:
    """Orquestrador central do sistema completo"""
    
    def __init__(self):
        self.manager = CentralAgentManager()
        self.registry = None
        self.session_log = []
        
    def log_action(self, action: str, status: str, details: str = ""):
        """Registra ação no log da sessão"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "status": status,
            "details": details
        }
        self.session_log.append(entry)
        logger.info(f"{status.upper()}: {action} - {details}")
    
    async def initialize_system(self, force_reload: bool = False) -> bool:
        """Inicializa o sistema completo"""
        self.log_action("INICIALIZAÇÃO DO SISTEMA", "iniciando", "Carregando estrutura central")
        
        try:
            # 1. Carregar todos os agentes
            self.log_action("CARREGAMENTO DE AGENTES", "processando", "Lendo estrutura de domínios")
            self.registry = self.manager.load_all_agents()
            
            # 2. Validar estruturas
            self.log_action("VALIDAÇÃO", "processando", "Verificando integridade dos agentes")
            total_issues = 0
            for domain_name, agents in self.registry.domains.items():
                for agent in agents:
                    is_valid, issues = self.manager.validate_agent_structure(agent)
                    if not is_valid:
                        total_issues += len(issues)
                        self.log_action("VALIDAÇÃO", "aviso", f"{domain_name}/{agent.name}: {len(issues)} problemas")
            
            # 3. Aplicar otimizações
            self.log_action("OTIMIZAÇÃO", "processando", "Aplicando melhorias automáticas")
            optimization_report = self.manager.optimize_agent_structure()
            
            # 4. Salvar registry
            self.log_action("PERSISTÊNCIA", "processando", "Salvando registry central")
            self.manager.save_registry()
            
            self.log_action("INICIALIZAÇÃO DO SISTEMA", "sucesso", 
                          f"{self.registry.total_agents} agentes, {total_issues} problemas, "
                          f"{optimization_report['agents_optimized']} otimizações")
            
            return True
            
        except Exception as e:
            self.log_action("INICIALIZAÇÃO DO SISTEMA", "erro", str(e))
            return False
    
    async def setup_mcp_integration(self) -> bool:
        """Configura integração MCP completa"""
        if not self.registry:
            self.log_action("MCP SETUP", "erro", "Sistema não inicializado")
            return False
        
        self.log_action("MCP SETUP", "processando", "Configurando integração MCP")
        
        try:
            # 1. Gerar configuração MCP otimizada
            success = self.manager.generate_mcp_integration()
            
            if success:
                # 2. Verificar servidores MCP existentes
                mcp_servers = [
                    "mcp_integration/custom_mcp_server.py",
                    "mcp_integration/central_mcp_server.py",
                    "external_mcp_servers/langgraph_mcp_example.py"
                ]
                
                active_servers = []
                for server_file in mcp_servers:
                    if Path(server_file).exists():
                        active_servers.append(server_file)
                
                # 3. Atualizar configuração com servidores
                config_file = Path("mcp_integration/mcp_config_optimized.json")
                if config_file.exists():
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    config["mcp_servers"] = {
                        "active_servers": active_servers,
                        "total_servers": len(active_servers),
                        "central_server": "mcp_integration/central_mcp_server.py"
                    }
                    
                    with open(config_file, 'w', encoding='utf-8') as f:
                        json.dump(config, f, indent=2, ensure_ascii=False)
                
                self.log_action("MCP SETUP", "sucesso", f"{len(active_servers)} servidores configurados")
                return True
            else:
                self.log_action("MCP SETUP", "erro", "Falha na geração da configuração")
                return False
                
        except Exception as e:
            self.log_action("MCP SETUP", "erro", str(e))
            return False
    
    async def deploy_to_autogen(self) -> bool:
        """Deploy completo para AutoGen Studio"""
        if not self.registry:
            self.log_action("DEPLOY AUTOGEN", "erro", "Sistema não inicializado")
            return False
        
        self.log_action("DEPLOY AUTOGEN", "processando", "Iniciando deploy para AutoGen Studio")
        
        try:
            success = self.manager.deploy_to_platform("autogen")
            
            if success:
                # Verificar se DB existe
                autogen_db = Path.home() / ".autogenstudio" / "autogen04202.db"
                db_exists = autogen_db.exists()
                
                self.log_action("DEPLOY AUTOGEN", "sucesso", 
                              f"Deploy realizado. DB existe: {db_exists}")
                
                # Instruções para reiniciar
                self.log_action("DEPLOY AUTOGEN", "info", 
                              "Execute: pkill -f autogenstudio && autogenstudio ui --port 8081")
                return True
            else:
                self.log_action("DEPLOY AUTOGEN", "erro", "Falha no deploy")
                return False
                
        except Exception as e:
            self.log_action("DEPLOY AUTOGEN", "erro", str(e))
            return False
    
    async def deploy_to_langsmith(self) -> bool:
        """Deploy completo para LangSmith/LangGraph"""
        if not self.registry:
            self.log_action("DEPLOY LANGSMITH", "erro", "Sistema não inicializado")
            return False
        
        self.log_action("DEPLOY LANGSMITH", "processando", "Iniciando deploy para LangSmith")
        
        try:
            success = self.manager.deploy_to_platform("langsmith")
            
            if success:
                # Verificar arquivos gerados
                controllers_dir = Path("langgraph_controllers")
                total_files = len(list(controllers_dir.glob("**/*.py"))) if controllers_dir.exists() else 0
                
                self.log_action("DEPLOY LANGSMITH", "sucesso", 
                              f"Deploy realizado. {total_files} controllers gerados")
                
                # Instruções para iniciar
                self.log_action("DEPLOY LANGSMITH", "info", 
                              "Execute: cd langgraph_controllers && langgraph dev")
                return True
            else:
                self.log_action("DEPLOY LANGSMITH", "erro", "Falha no deploy")
                return False
                
        except Exception as e:
            self.log_action("DEPLOY LANGSMITH", "erro", str(e))
            return False
    
    async def verify_system_integrity(self) -> dict:
        """Verifica integridade completa do sistema"""
        if not self.registry:
            return {"error": "Sistema não inicializado"}
        
        self.log_action("VERIFICAÇÃO DE INTEGRIDADE", "processando", "Analisando sistema completo")
        
        integrity_report = {
            "timestamp": datetime.now().isoformat(),
            "domains": {},
            "global_issues": [],
            "recommendations": [],
            "scores": {
                "structure_score": 0,
                "prompt_quality": 0,
                "tools_coverage": 0,
                "overall_health": 0
            }
        }
        
        total_agents = 0
        agents_with_issues = 0
        total_prompt_length = 0
        total_tools = 0
        
        # Analisar cada domínio
        for domain_name, agents in self.registry.domains.items():
            domain_report = {
                "agents_count": len(agents),
                "agents_issues": 0,
                "total_sub_agents": 0,
                "total_tools": 0,
                "agents_detail": []
            }
            
            for agent in agents:
                total_agents += 1
                is_valid, issues = self.manager.validate_agent_structure(agent)
                
                if not is_valid:
                    agents_with_issues += 1
                    domain_report["agents_issues"] += 1
                
                domain_report["total_sub_agents"] += len(agent.sub_agents)
                domain_report["total_tools"] += len(agent.tools)
                total_prompt_length += len(agent.system_message)
                total_tools += len(agent.tools)
                
                agent_detail = {
                    "name": agent.name,
                    "valid": is_valid,
                    "issues_count": len(issues),
                    "prompt_length": len(agent.system_message),
                    "tools_count": len(agent.tools),
                    "sub_agents_count": len(agent.sub_agents)
                }
                domain_report["agents_detail"].append(agent_detail)
            
            integrity_report["domains"][domain_name] = domain_report
        
        # Calcular scores
        integrity_report["scores"]["structure_score"] = max(0, 100 - (agents_with_issues / max(total_agents, 1) * 100))
        integrity_report["scores"]["prompt_quality"] = min(100, (total_prompt_length / max(total_agents, 1)) / 100)
        integrity_report["scores"]["tools_coverage"] = min(100, (total_tools / max(total_agents, 1)) * 20)
        integrity_report["scores"]["overall_health"] = (
            integrity_report["scores"]["structure_score"] * 0.5 +
            integrity_report["scores"]["prompt_quality"] * 0.3 +
            integrity_report["scores"]["tools_coverage"] * 0.2
        )
        
        # Recomendações
        if integrity_report["scores"]["overall_health"] < 70:
            integrity_report["recommendations"].append("Sistema precisa de otimização urgente")
        if agents_with_issues > 0:
            integrity_report["recommendations"].append(f"{agents_with_issues} agentes com problemas estruturais")
        if total_tools < total_agents:
            integrity_report["recommendations"].append("Baixa cobertura de ferramentas")
        
        self.log_action("VERIFICAÇÃO DE INTEGRIDADE", "sucesso", 
                       f"Score geral: {integrity_report['scores']['overall_health']:.1f}/100")
        
        return integrity_report
    
    async def generate_final_report(self) -> dict:
        """Gera relatório final da sessão"""
        report = {
            "session_summary": {
                "timestamp": datetime.now().isoformat(),
                "total_actions": len(self.session_log),
                "successful_actions": len([log for log in self.session_log if log["status"] == "sucesso"]),
                "failed_actions": len([log for log in self.session_log if log["status"] == "erro"]),
                "session_duration": "N/A"
            },
            "system_status": self.manager.generate_status_report() if self.registry else {"error": "Não inicializado"},
            "integrity_check": await self.verify_system_integrity(),
            "session_log": self.session_log,
            "next_steps": []
        }
        
        # Próximos passos baseados no status
        if self.registry:
            report["next_steps"].extend([
                "Sistema está operacional e pronto para uso",
                "Execute deploy para AutoGen: python -c 'from scripts.orchestrate_central_system import main; main(\"autogen\")'",
                "Execute deploy para LangSmith: python -c 'from scripts.orchestrate_central_system import main; main(\"langsmith\")'",
                "Inicie servidores MCP conforme necessário"
            ])
        else:
            report["next_steps"].append("Execute inicialização do sistema primeiro")
        
        return report
    
    async def run_complete_orchestration(self) -> dict:
        """Executa orquestração completa do sistema"""
        print("🚀 INICIANDO ORQUESTRAÇÃO CENTRAL DO SISTEMA MULTI-AGENT AI v3.0")
        print("=" * 70)
        
        # 1. Inicializar sistema
        init_success = await self.initialize_system()
        if not init_success:
            return await self.generate_final_report()
        
        # 2. Configurar MCP
        mcp_success = await self.setup_mcp_integration()
        
        # 3. Deploy para AutoGen (opcional, baseado em disponibilidade)
        autogen_success = await self.deploy_to_autogen()
        
        # 4. Deploy para LangSmith
        langsmith_success = await self.deploy_to_langsmith()
        
        # 5. Verificar integridade
        integrity_report = await self.verify_system_integrity()
        
        # 6. Gerar relatório final
        final_report = await self.generate_final_report()
        
        print("\n🎉 ORQUESTRAÇÃO COMPLETA FINALIZADA!")
        print(f"📊 Score de Saúde do Sistema: {integrity_report['scores']['overall_health']:.1f}/100")
        print(f"✅ Ações Bem-sucedidas: {final_report['session_summary']['successful_actions']}")
        print(f"❌ Ações com Erro: {final_report['session_summary']['failed_actions']}")
        
        # Salvar relatório
        report_file = f"docs/orchestration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        Path("docs").mkdir(exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Relatório salvo: {report_file}")
        return final_report

# Função principal para execução direta
async def main(action: str = "full"):
    """Função principal para execução"""
    orchestrator = CentralOrchestrator()
    
    if action == "full":
        return await orchestrator.run_complete_orchestration()
    elif action == "init":
        await orchestrator.initialize_system()
    elif action == "mcp":
        await orchestrator.setup_mcp_integration()
    elif action == "autogen":
        await orchestrator.deploy_to_autogen()
    elif action == "langsmith":
        await orchestrator.deploy_to_langsmith()
    elif action == "verify":
        return await orchestrator.verify_system_integrity()
    else:
        print(f"Ação não reconhecida: {action}")
        print("Ações disponíveis: full, init, mcp, autogen, langsmith, verify")

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "full"
    asyncio.run(main(action)) 