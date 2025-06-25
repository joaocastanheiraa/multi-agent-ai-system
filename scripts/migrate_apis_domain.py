#!/usr/bin/env python3
"""
Script para migrar todos os 6 agentes APIs do sistema legado para v3.0
Tarefas 1.3-1.8: Migrar Domínio APIs Completo
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class APIsDomainMigrator:
    def __init__(self):
        self.source_dir = Path("/Users/joaovictormiranda/multi-agent-ai-sistem/multi-agent-ai-system/agents/agents_apis")
        self.target_dir = Path("domains/apis/agents")
        self.report = {
            "migration_type": "APIs Domain Complete",
            "start_time": datetime.now().isoformat(),
            "agents_migrated": [],
            "files_migrated": 0,
            "errors": []
        }
        
        # Lista dos 6 agentes APIs a migrar
        self.api_agents = [
            "HotmartAPIMaster",
            "KiwifyAPIMaster", 
            "PerfectpayAPIMaster",
            "PaytAPIMaster",
            "APIUnifyMaster",
            "APIsImputOutputMapper"
        ]
        
        # Especialização de cada agente
        self.specializations = {
            "HotmartAPIMaster": "Integração completa com API Hotmart - vendas, afiliados, produtos",
            "KiwifyAPIMaster": "Integração completa com API Kiwify - checkout, produtos, analytics",
            "PerfectpayAPIMaster": "Integração completa com API Perfectpay - pagamentos, transações",
            "PaytAPIMaster": "Integração completa com API Payt - processamento de pagamentos",
            "APIUnifyMaster": "Unificação e orquestração de múltiplas APIs de pagamento",
            "APIsImputOutputMapper": "Mapeamento e transformação de dados entre APIs"
        }
    
    def ensure_target_structure(self):
        """Garantir que a estrutura de destino existe"""
        self.target_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Estrutura de destino criada: {self.target_dir}")
    
    def migrate_agent(self, agent_name):
        """Migrar um agente específico com toda sua estrutura"""
        print(f"\n🔄 Migrando agente: {agent_name}")
        
        source_agent_dir = self.source_dir / agent_name
        target_agent_dir = self.target_dir / agent_name
        
        if not source_agent_dir.exists():
            error = f"❌ Agente não encontrado: {source_agent_dir}"
            print(error)
            self.report["errors"].append(error)
            return False
        
        try:
            # Criar diretório do agente no destino
            target_agent_dir.mkdir(parents=True, exist_ok=True)
            
            # Migrar prompt.txt principal
            source_prompt = source_agent_dir / "prompt.txt"
            if source_prompt.exists():
                shutil.copy2(source_prompt, target_agent_dir / "prompt.txt")
                print(f"  ✅ Migrado: prompt.txt")
                self.report["files_migrated"] += 1
            
            # Migrar tools.yaml principal
            source_tools = source_agent_dir / "tools.yaml"
            if source_tools.exists():
                shutil.copy2(source_tools, target_agent_dir / "tools.yaml")
                print(f"  ✅ Migrado: tools.yaml")
                self.report["files_migrated"] += 1
            
            # Migrar diretório sub-agents completo
            source_subagents = source_agent_dir / "sub-agents"
            if source_subagents.exists():
                target_subagents = target_agent_dir / "sub-agents"
                shutil.copytree(source_subagents, target_subagents, dirs_exist_ok=True)
                
                # Contar arquivos migrados em sub-agents
                subagent_files = list(target_subagents.rglob("*"))
                subagent_file_count = len([f for f in subagent_files if f.is_file()])
                print(f"  ✅ Migrado: sub-agents/ ({subagent_file_count} arquivos)")
                self.report["files_migrated"] += subagent_file_count
            
            # Migrar knowledge_base se existir
            source_kb = source_agent_dir / "knowledge_base"
            if source_kb.exists():
                target_kb = target_agent_dir / "knowledge_base"
                shutil.copytree(source_kb, target_kb, dirs_exist_ok=True)
                
                kb_files = list(target_kb.rglob("*"))
                kb_file_count = len([f for f in kb_files if f.is_file()])
                print(f"  ✅ Migrado: knowledge_base/ ({kb_file_count} arquivos)")
                self.report["files_migrated"] += kb_file_count
            
            # Migrar knowledge_portugues_consulta se existir (APIUnifyMaster)
            source_kpc = source_agent_dir / "knowledge_portugues_consulta"
            if source_kpc.exists():
                target_kpc = target_agent_dir / "knowledge_portugues_consulta"
                shutil.copytree(source_kpc, target_kpc, dirs_exist_ok=True)
                
                kpc_files = list(target_kpc.rglob("*"))
                kpc_file_count = len([f for f in kpc_files if f.is_file()])
                print(f"  ✅ Migrado: knowledge_portugues_consulta/ ({kpc_file_count} arquivos)")
                self.report["files_migrated"] += kpc_file_count
            
            # Migrar outras pastas e arquivos
            for item in source_agent_dir.iterdir():
                if item.is_dir() and item.name not in ["sub-agents", "knowledge_base", "knowledge_portugues_consulta"]:
                    target_item = target_agent_dir / item.name
                    shutil.copytree(item, target_item, dirs_exist_ok=True)
                    
                    # Contar arquivos
                    item_files = list(target_item.rglob("*"))
                    item_file_count = len([f for f in item_files if f.is_file()])
                    print(f"  ✅ Migrado: {item.name}/ ({item_file_count} arquivos)")
                    self.report["files_migrated"] += item_file_count
                
                elif item.is_file() and item.name not in ["prompt.txt", "tools.yaml"]:
                    shutil.copy2(item, target_agent_dir / item.name)
                    print(f"  ✅ Migrado: {item.name}")
                    self.report["files_migrated"] += 1
            
            # Criar agent_manifest.json
            self.create_agent_manifest(agent_name, target_agent_dir)
            
            self.report["agents_migrated"].append(agent_name)
            print(f"✅ Agente {agent_name} migrado com sucesso!")
            return True
            
        except Exception as e:
            error = f"❌ Erro migrando {agent_name}: {str(e)}"
            print(error)
            self.report["errors"].append(error)
            return False
    
    def create_agent_manifest(self, agent_name, agent_dir):
        """Criar manifest específico para o agente"""
        
        # Contar sub-agentes
        subagents_dir = agent_dir / "sub-agents"
        subagents_count = 0
        subagents_list = []
        
        if subagents_dir.exists():
            subagents_list = [d.name for d in subagents_dir.iterdir() if d.is_dir()]
            subagents_count = len(subagents_list)
        
        # Verificar knowledge bases
        kb_dirs = []
        if (agent_dir / "knowledge_base").exists():
            kb_dirs.append("knowledge_base")
        if (agent_dir / "knowledge_portugues_consulta").exists():
            kb_dirs.append("knowledge_portugues_consulta")
        
        manifest = {
            "agent_name": agent_name,
            "domain": "apis",
            "type": "main_agent",
            "architecture": "prompt_based",  # Será convertido para LangGraph na Fase B
            "migration_status": "migrated",
            "migration_date": datetime.now().isoformat(),
            "subagents_count": subagents_count,
            "subagents": subagents_list,
            "knowledge_bases": kb_dirs,
            "files": {
                "prompt": "prompt.txt",
                "tools": "tools.yaml",
                "subagents_dir": "sub-agents"
            },
            "next_phase": "langraph_conversion",
            "specialization": self.specializations.get(agent_name, "Agente especializado em APIs")
        }
        
        manifest_path = agent_dir / "agent_manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Criado: agent_manifest.json ({subagents_count} sub-agentes, {len(kb_dirs)} knowledge bases)")
        self.report["files_migrated"] += 1
    
    def generate_migration_report(self):
        """Gerar relatório da migração"""
        self.report["end_time"] = datetime.now().isoformat()
        self.report["success"] = len(self.report["errors"]) == 0
        self.report["agents_total"] = len(self.api_agents)
        self.report["agents_migrated_count"] = len(self.report["agents_migrated"])
        
        report_path = Path("migration_reports") / "apis_domain_migration.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 RELATÓRIO DE MIGRAÇÃO APIs DOMAIN")
        print(f"Agentes migrados: {self.report['agents_migrated_count']}/{self.report['agents_total']}")
        print(f"Arquivos migrados: {self.report['files_migrated']}")
        print(f"Erros: {len(self.report['errors'])}")
        print(f"Relatório salvo em: {report_path}")
        
        return self.report
    
    def run_migration(self):
        """Executar migração completa do domínio APIs"""
        print("🚀 INICIANDO MIGRAÇÃO COMPLETA DO DOMÍNIO APIs")
        print(f"Origem: {self.source_dir}")
        print(f"Destino: {self.target_dir}")
        
        # Garantir estrutura
        self.ensure_target_structure()
        
        # Migrar cada agente
        for agent_name in self.api_agents:
            self.migrate_agent(agent_name)
        
        # Gerar relatório
        report = self.generate_migration_report()
        
        if report["success"]:
            print("\n🎉 MIGRAÇÃO DO DOMÍNIO APIs CONCLUÍDA COM SUCESSO!")
        else:
            print(f"\n⚠️  MIGRAÇÃO CONCLUÍDA COM {len(report['errors'])} ERROS")
        
        return report

if __name__ == "__main__":
    migrator = APIsDomainMigrator()
    migrator.run_migration()
