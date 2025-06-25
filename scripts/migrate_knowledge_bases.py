#!/usr/bin/env python3
"""
Script para migrar todas as knowledge bases principais do sistema
Tarefa 1.11: Migrar Knowledge Bases Completas
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class KnowledgeBasesMigrator:
    def __init__(self):
        self.source_dir = Path("/Users/joaovictormiranda/multi-agent-ai-sistem/multi-agent-ai-system/knowledge_base_source")
        self.target_dir = Path("knowledge_bases")
        self.report = {
            "migration_type": "Knowledge Bases Complete",
            "start_time": datetime.now().isoformat(),
            "knowledge_bases_migrated": [],
            "files_migrated": 0,
            "errors": []
        }
        
        # Lista das knowledge bases principais
        self.knowledge_bases = [
            "conversion_catalyst_knowledge",
            "metaphor_architect_knowledge",
            "neurohook_knowledge",
            "pain_detector_knowledge", 
            "paradigm_architect_knowledge",
            "retention_architect_knowledge"
        ]
    
    def ensure_target_structure(self):
        """Garantir que a estrutura de destino existe"""
        self.target_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Estrutura de destino criada: {self.target_dir}")
    
    def migrate_knowledge_base(self, kb_name):
        """Migrar uma knowledge base específica"""
        print(f"\n🔄 Migrando knowledge base: {kb_name}")
        
        source_kb_dir = self.source_dir / kb_name
        target_kb_dir = self.target_dir / kb_name
        
        if not source_kb_dir.exists():
            error = f"❌ Knowledge base não encontrada: {source_kb_dir}"
            print(error)
            self.report["errors"].append(error)
            return False
        
        try:
            # Copiar toda a estrutura da knowledge base
            shutil.copytree(source_kb_dir, target_kb_dir, dirs_exist_ok=True)
            
            # Contar arquivos migrados
            kb_files = list(target_kb_dir.rglob("*"))
            kb_file_count = len([f for f in kb_files if f.is_file()])
            
            print(f"  ✅ Migrado: {kb_name}/ ({kb_file_count} arquivos)")
            self.report["files_migrated"] += kb_file_count
            
            # Criar knowledge_base_manifest.json
            self.create_kb_manifest(kb_name, target_kb_dir)
            
            self.report["knowledge_bases_migrated"].append(kb_name)
            print(f"✅ Knowledge base {kb_name} migrada com sucesso!")
            return True
            
        except Exception as e:
            error = f"❌ Erro migrando {kb_name}: {str(e)}"
            print(error)
            self.report["errors"].append(error)
            return False
    
    def create_kb_manifest(self, kb_name, kb_dir):
        """Criar manifest específico para a knowledge base"""
        
        # Analisar estrutura da knowledge base
        subdirs = [d.name for d in kb_dir.iterdir() if d.is_dir()]
        files = [f.name for f in kb_dir.iterdir() if f.is_file()]
        
        # Contar total de arquivos
        all_files = list(kb_dir.rglob("*"))
        total_files = len([f for f in all_files if f.is_file()])
        
        # Determinar especialização baseada no nome
        specializations = {
            "conversion_catalyst_knowledge": "Neurociência da decisão e psicologia comportamental",
            "metaphor_architect_knowledge": "Princípios de mapeamento isomórfico e psicologia da compreensão analógica",
            "neurohook_knowledge": "Audience psychology, hook techniques, linguistic engineering",
            "pain_detector_knowledge": "Agent architecture, foundational psychology, pain taxonomy",
            "paradigm_architect_knowledge": "Frameworks de transformação, metodologias de legitimação, técnicas de engenharia",
            "retention_architect_knowledge": "Cognitive foundations, master examples, retention techniques"
        }
        
        manifest = {
            "knowledge_base_name": kb_name,
            "type": "domain_knowledge_base",
            "migration_status": "migrated",
            "migration_date": datetime.now().isoformat(),
            "total_files": total_files,
            "subdirectories": subdirs,
            "root_files": files,
            "specialization": specializations.get(kb_name, "Knowledge base especializada"),
            "next_phase": "rag_optimization",
            "target_vector_db": "supabase",
            "chunking_strategy": "semantic",
            "embedding_model": "text-embedding-3-large"
        }
        
        manifest_path = kb_dir / "knowledge_base_manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Criado: knowledge_base_manifest.json ({total_files} arquivos total)")
        self.report["files_migrated"] += 1
    
    def create_global_kb_index(self):
        """Criar índice global das knowledge bases"""
        index = {
            "knowledge_bases_index": {
                "total_knowledge_bases": len(self.report["knowledge_bases_migrated"]),
                "knowledge_bases": [],
                "migration_date": datetime.now().isoformat(),
                "next_phase": "rag_optimization_phase_d"
            }
        }
        
        # Adicionar informações de cada KB
        for kb_name in self.report["knowledge_bases_migrated"]:
            kb_dir = self.target_dir / kb_name
            manifest_path = kb_dir / "knowledge_base_manifest.json"
            
            if manifest_path.exists():
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    kb_manifest = json.load(f)
                
                index["knowledge_bases_index"]["knowledge_bases"].append({
                    "name": kb_name,
                    "path": str(kb_dir),
                    "total_files": kb_manifest.get("total_files", 0),
                    "specialization": kb_manifest.get("specialization", ""),
                    "status": "ready_for_rag"
                })
        
        index_path = self.target_dir / "knowledge_bases_index.json"
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Criado: knowledge_bases_index.json")
        self.report["files_migrated"] += 1
    
    def generate_migration_report(self):
        """Gerar relatório da migração"""
        self.report["end_time"] = datetime.now().isoformat()
        self.report["success"] = len(self.report["errors"]) == 0
        self.report["kb_total"] = len(self.knowledge_bases)
        self.report["kb_migrated_count"] = len(self.report["knowledge_bases_migrated"])
        
        report_path = Path("migration_reports") / "knowledge_bases_migration.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 RELATÓRIO DE MIGRAÇÃO KNOWLEDGE BASES")
        print(f"Knowledge bases migradas: {self.report['kb_migrated_count']}/{self.report['kb_total']}")
        print(f"Arquivos migrados: {self.report['files_migrated']}")
        print(f"Erros: {len(self.report['errors'])}")
        print(f"Relatório salvo em: {report_path}")
        
        return self.report
    
    def run_migration(self):
        """Executar migração completa das knowledge bases"""
        print("🚀 INICIANDO MIGRAÇÃO DAS KNOWLEDGE BASES PRINCIPAIS")
        print(f"Origem: {self.source_dir}")
        print(f"Destino: {self.target_dir}")
        
        # Garantir estrutura
        self.ensure_target_structure()
        
        # Migrar cada knowledge base
        for kb_name in self.knowledge_bases:
            self.migrate_knowledge_base(kb_name)
        
        # Criar índice global
        self.create_global_kb_index()
        
        # Gerar relatório
        report = self.generate_migration_report()
        
        if report["success"]:
            print("\n🎉 MIGRAÇÃO DAS KNOWLEDGE BASES CONCLUÍDA COM SUCESSO!")
        else:
            print(f"\n⚠️  MIGRAÇÃO CONCLUÍDA COM {len(report['errors'])} ERROS")
        
        return report

if __name__ == "__main__":
    migrator = KnowledgeBasesMigrator()
    migrator.run_migration()
