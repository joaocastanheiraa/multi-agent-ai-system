#!/usr/bin/env python3
"""
Script para migrar agentes Analytics e Knowledge do sistema legado para v3.0
Tarefas 1.9-1.10: Migrar Domínios Analytics e Knowledge
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class AnalyticsKnowledgeMigrator:
    def __init__(self):
        self.source_analytics = Path("/Users/joaovictormiranda/multi-agent-ai-sistem/multi-agent-ai-system/agents/agents_analytics")
        self.source_knowledge = Path("/Users/joaovictormiranda/multi-agent-ai-sistem/multi-agent-ai-system/agents/agents_knowledgebases_masters")
        self.target_analytics = Path("domains/analytics/agents")
        self.target_knowledge = Path("domains/knowledge/agents")
        
        self.report = {
            "migration_type": "Analytics & Knowledge Domains",
            "start_time": datetime.now().isoformat(),
            "agents_migrated": [],
            "files_migrated": 0,
            "errors": []
        }
    
    def ensure_target_structures(self):
        """Garantir que as estruturas de destino existem"""
        self.target_analytics.mkdir(parents=True, exist_ok=True)
        self.target_knowledge.mkdir(parents=True, exist_ok=True)
        print(f"✅ Estruturas criadas: {self.target_analytics} e {self.target_knowledge}")
    
    def migrate_analytics_domain(self):
        """Migrar domínio Analytics"""
        print("\n🔄 MIGRANDO DOMÍNIO ANALYTICS")
        
        # Verificar se existe ANALYTICSGPT
        analytics_agent = None
        if self.source_analytics.exists():
            for item in self.source_analytics.iterdir():
                if "ANALYTICSGPT" in item.name or "analytics" in item.name.lower():
                    analytics_agent = item
                    break
        
        if not analytics_agent:
            # Buscar em outros locais
            possible_locations = [
                Path("/Users/joaovictormiranda/multi-agent-ai-sistem/multi-agent-ai-system/agents") / "ANALYTICSGPT Super Track",
                Path("/Users/joaovictormiranda/multi-agent-ai-sistem/multi-agent-ai-system/agents") / "analytics",
            ]
            
            for loc in possible_locations:
                if loc.exists():
                    analytics_agent = loc
                    break
        
        if analytics_agent:
            return self.migrate_agent(analytics_agent, self.target_analytics, "analytics", "Análise de dados e geração de insights avançados")
        else:
            print("❌ Agente ANALYTICSGPT não encontrado")
            return False
    
    def migrate_knowledge_domain(self):
        """Migrar domínio Knowledge"""
        print("\n🔄 MIGRANDO DOMÍNIO KNOWLEDGE")
        
        # Verificar se existe DocRAGOptimizer
        knowledge_agent = None
        if self.source_knowledge.exists():
            for item in self.source_knowledge.iterdir():
                if "DocRAGOptimizer" in item.name or "rag" in item.name.lower():
                    knowledge_agent = item
                    break
        
        if not knowledge_agent:
            # Buscar em outros locais
            possible_locations = [
                Path("/Users/joaovictormiranda/multi-agent-ai-sistem/multi-agent-ai-system/agents") / "DocRAGOptimizer",
                Path("/Users/joaovictormiranda/multi-agent-ai-sistem/multi-agent-ai-system/agents") / "knowledge",
            ]
            
            for loc in possible_locations:
                if loc.exists():
                    knowledge_agent = loc
                    break
        
        if knowledge_agent:
            return self.migrate_agent(knowledge_agent, self.target_knowledge, "knowledge", "Otimização RAG e processamento de documentos")
        else:
            print("❌ Agente DocRAGOptimizer não encontrado")
            return False
    
    def migrate_agent(self, source_agent_dir, target_domain_dir, domain_name, specialization):
        """Migrar um agente específico"""
        agent_name = source_agent_dir.name
        print(f"\n🔄 Migrando agente: {agent_name}")
        
        target_agent_dir = target_domain_dir / agent_name
        
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
            
            # Migrar todas as pastas e arquivos
            for item in source_agent_dir.iterdir():
                if item.is_dir():
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
            self.create_agent_manifest(agent_name, target_agent_dir, domain_name, specialization)
            
            self.report["agents_migrated"].append(agent_name)
            print(f"✅ Agente {agent_name} migrado com sucesso!")
            return True
            
        except Exception as e:
            error = f"❌ Erro migrando {agent_name}: {str(e)}"
            print(error)
            self.report["errors"].append(error)
            return False
    
    def create_agent_manifest(self, agent_name, agent_dir, domain_name, specialization):
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
        for item in agent_dir.iterdir():
            if item.is_dir() and "knowledge" in item.name.lower():
                kb_dirs.append(item.name)
        
        manifest = {
            "agent_name": agent_name,
            "domain": domain_name,
            "type": "main_agent",
            "architecture": "prompt_based",
            "migration_status": "migrated",
            "migration_date": datetime.now().isoformat(),
            "subagents_count": subagents_count,
            "subagents": subagents_list,
            "knowledge_bases": kb_dirs,
            "files": {
                "prompt": "prompt.txt",
                "tools": "tools.yaml"
            },
            "next_phase": "langraph_conversion",
            "specialization": specialization
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
        self.report["agents_migrated_count"] = len(self.report["agents_migrated"])
        
        report_path = Path("migration_reports") / "analytics_knowledge_migration.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 RELATÓRIO DE MIGRAÇÃO Analytics & Knowledge")
        print(f"Agentes migrados: {self.report['agents_migrated_count']}")
        print(f"Arquivos migrados: {self.report['files_migrated']}")
        print(f"Erros: {len(self.report['errors'])}")
        print(f"Relatório salvo em: {report_path}")
        
        return self.report
    
    def run_migration(self):
        """Executar migração completa dos domínios Analytics e Knowledge"""
        print("🚀 INICIANDO MIGRAÇÃO DOS DOMÍNIOS ANALYTICS E KNOWLEDGE")
        
        # Garantir estruturas
        self.ensure_target_structures()
        
        # Migrar Analytics
        self.migrate_analytics_domain()
        
        # Migrar Knowledge
        self.migrate_knowledge_domain()
        
        # Gerar relatório
        report = self.generate_migration_report()
        
        if report["success"]:
            print("\n🎉 MIGRAÇÃO DOS DOMÍNIOS ANALYTICS E KNOWLEDGE CONCLUÍDA!")
        else:
            print(f"\n⚠️  MIGRAÇÃO CONCLUÍDA COM {len(report['errors'])} ERROS")
        
        return report

if __name__ == "__main__":
    migrator = AnalyticsKnowledgeMigrator()
    migrator.run_migration()
