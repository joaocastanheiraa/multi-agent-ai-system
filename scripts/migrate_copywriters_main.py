#!/usr/bin/env python3
"""
Script para migrar os 6 agentes copywriters principais do sistema legado para v3.0
Tarefa 1.1: Migrar Domínio Copywriters - Agentes Principais
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class CopywritersMainMigrator:
    def __init__(self):
        self.source_dir = Path("/Users/joaovictormiranda/multi-agent-ai-sistem/multi-agent-ai-system/agents/agents_copywriters")
        self.target_dir = Path("domains/copywriters/agents")
        self.report = {
            "migration_type": "Copywriters Main Agents",
            "start_time": datetime.now().isoformat(),
            "agents_migrated": [],
            "files_migrated": 0,
            "errors": []
        }
        
        # Lista dos 6 agentes principais a migrar
        self.main_agents = [
            "conversion_catalyst",
            "neurohook_ultra", 
            "pain_detector",
            "paradigm_architect",
            "metaphor_architect",
            "retention_architect"
        ]
    
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
            
            # Migrar outras pastas se existirem (config, knowledge_base, etc.)
            for item in source_agent_dir.iterdir():
                if item.is_dir() and item.name not in ["sub-agents"]:
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
        
        manifest = {
            "agent_name": agent_name,
            "domain": "copywriters",
            "type": "main_agent",
            "architecture": "prompt_based",  # Será convertido para LangGraph na Fase B
            "migration_status": "migrated",
            "migration_date": datetime.now().isoformat(),
            "subagents_count": subagents_count,
            "subagents": subagents_list,
            "files": {
                "prompt": "prompt.txt",
                "tools": "tools.yaml",
                "subagents_dir": "sub-agents"
            },
            "next_phase": "langraph_conversion",
            "specialization": self.get_agent_specialization(agent_name)
        }
        
        manifest_path = agent_dir / "agent_manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Criado: agent_manifest.json ({subagents_count} sub-agentes)")
        self.report["files_migrated"] += 1
    
    def get_agent_specialization(self, agent_name):
        """Obter especialização específica de cada agente"""
        specializations = {
            "conversion_catalyst": "Otimização de conversão e análise de decisão neurológica",
            "neurohook_ultra": "Geração de hooks e otimização de atenção psicológica", 
            "pain_detector": "Detecção de dores e mapeamento de necessidades emocionais",
            "paradigm_architect": "Transformação paradigmática e engenharia de linguagem",
            "metaphor_architect": "Criação de metáforas e mapeamento isomórfico",
            "retention_architect": "Estruturas de tensão e engenharia de retenção"
        }
        return specializations.get(agent_name, "Agente especializado em copywriting")
    
    def generate_migration_report(self):
        """Gerar relatório da migração"""
        self.report["end_time"] = datetime.now().isoformat()
        self.report["success"] = len(self.report["errors"]) == 0
        self.report["agents_total"] = len(self.main_agents)
        self.report["agents_migrated_count"] = len(self.report["agents_migrated"])
        
        report_path = Path("migration_reports") / "copywriters_main_migration.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 RELATÓRIO DE MIGRAÇÃO")
        print(f"Agentes migrados: {self.report['agents_migrated_count']}/{self.report['agents_total']}")
        print(f"Arquivos migrados: {self.report['files_migrated']}")
        print(f"Erros: {len(self.report['errors'])}")
        print(f"Relatório salvo em: {report_path}")
        
        return self.report
    
    def run_migration(self):
        """Executar migração completa dos agentes principais"""
        print("🚀 INICIANDO MIGRAÇÃO DOS AGENTES COPYWRITERS PRINCIPAIS")
        print(f"Origem: {self.source_dir}")
        print(f"Destino: {self.target_dir}")
        
        # Garantir estrutura
        self.ensure_target_structure()
        
        # Migrar cada agente
        for agent_name in self.main_agents:
            self.migrate_agent(agent_name)
        
        # Gerar relatório
        report = self.generate_migration_report()
        
        if report["success"]:
            print("\n🎉 MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        else:
            print(f"\n⚠️  MIGRAÇÃO CONCLUÍDA COM {len(report['errors'])} ERROS")
        
        return report

if __name__ == "__main__":
    migrator = CopywritersMainMigrator()
    migrator.run_migration()
