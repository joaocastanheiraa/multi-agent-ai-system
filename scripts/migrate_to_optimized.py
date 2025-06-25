#!/usr/bin/env python3
"""
FASE A: Estrutura Base e Migração de Conteúdo
Script para migrar sistema multi-agente para repository-optimized/ com arquitetura v3.0
"""

import os
import sys
import shutil
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('migration.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class RepositoryMigrator:
    """Migrador principal para repository-optimized"""
    
    def __init__(self, source_dir: str = "../", target_dir: str = "./"):
        self.source_dir = Path(source_dir).resolve()
        self.target_dir = Path(target_dir).resolve()
        self.migration_report = {
            "started_at": datetime.now().isoformat(),
            "source_dir": str(self.source_dir),
            "target_dir": str(self.target_dir),
            "migrated_files": [],
            "created_directories": [],
            "errors": [],
            "summary": {}
        }
        
    def create_directory_structure(self):
        """Criar estrutura de diretórios v3.0"""
        logger.info("🏗️ Criando estrutura de diretórios v3.0...")
        
        directories = [
            # Domínios principais
            "domains/copywriters",
            "domains/analytics", 
            "domains/apis",
            
            # Componentes compartilhados
            "shared",
            
            # Pipeline de ingestão
            "ingestion/processors",
            
            # Gerador de agentes
            "magenerator/core",
            "magenerator/templates/agent",
            "magenerator/templates/subagent", 
            "magenerator/templates/controller",
            
            # Interfaces externas
            "interfaces/api",
            "interfaces/websocket",
            
            # Testes
            "tests/unit",
            "tests/integration", 
            "tests/e2e",
            "tests/fixtures",
            
            # Configurações
            "config",
            
            # Scripts
            "scripts",
            
            # Documentação
            "docs",
            
            # CI/CD
            ".github/workflows",
            
            # Docker
            "docker",
            
            # Kubernetes
            "k8s"
        ]
        
        for dir_path in directories:
            full_path = self.target_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            self.migration_report["created_directories"].append(str(full_path))
            logger.info(f"✅ Criado: {dir_path}")
            
    def migrate_agents_to_domains(self):
        """Migrar agentes para estrutura de domínios"""
        logger.info("🤖 Migrando agentes para domínios...")
        
        # Mapeamento de migração
        agent_mappings = {
            # Copywriters
            "agents_copywriters/conversion_catalyst": "domains/copywriters/conversion_catalyst",
            "agents_copywriters/neurohook_ultra": "domains/copywriters/neurohook_ultra", 
            "agents_copywriters/pain_detector": "domains/copywriters/pain_detector",
            "agents_copywriters/paradigm_architect": "domains/copywriters/paradigm_architect",
            "agents_copywriters/metaphor_architect": "domains/copywriters/metaphor_architect",
            "agents_copywriters/retention_architect": "domains/copywriters/retention_architect",
            
            # Analytics
            "agents_analytics/ANALYTICSGPT | Super Track": "domains/analytics/super_track",
            
            # APIs
            "agents_apis/HotmartAPIMaster": "domains/apis/hotmart_master",
            "agents_apis/KiwifyAPIMaster": "domains/apis/kiwify_master",
            "agents_apis/PerfectpayAPIMaster": "domains/apis/perfectpay_master",
            "agents_apis/PaytAPIMaster": "domains/apis/payt_master",
            "agents_apis/APIUnifyMaster": "domains/apis/api_unify_master",
            "agents_apis/APIsImputOutputMapper": "domains/apis/input_output_mapper"
        }
        
        for source_path, target_path in agent_mappings.items():
            source_full = self.source_dir / source_path
            target_full = self.target_dir / target_path
            
            if source_full.exists():
                logger.info(f"📦 Migrando {source_path} → {target_path}")
                
                # Criar diretório de destino
                target_full.mkdir(parents=True, exist_ok=True)
                
                # Copiar arquivos
                self._copy_directory_contents(source_full, target_full)
                
                # Criar estrutura específica do agente
                self._create_agent_structure(target_full)
                
                self.migration_report["migrated_files"].append({
                    "source": str(source_full),
                    "target": str(target_full),
                    "type": "agent_directory"
                })
            else:
                logger.warning(f"⚠️ Diretório fonte não encontrado: {source_path}")
                
    def migrate_knowledge_bases(self):
        """Migrar knowledge bases para domínios"""
        logger.info("📚 Migrando knowledge bases...")
        
        knowledge_mappings = {
            # Copywriters knowledge
            "knowledge_base_source/conversion_catalyst_knowledge": "domains/copywriters/conversion_catalyst/knowledge",
            "knowledge_base_source/neurohook_knowledge": "domains/copywriters/neurohook_ultra/knowledge",
            "knowledge_base_source/pain_detector_knowledge": "domains/copywriters/pain_detector/knowledge", 
            "knowledge_base_source/paradigm_architect_knowledge": "domains/copywriters/paradigm_architect/knowledge",
            "knowledge_base_source/metaphor_architect_knowledge": "domains/copywriters/metaphor_architect/knowledge",
            "knowledge_base_source/retention_architect_knowledge": "domains/copywriters/retention_architect/knowledge"
        }
        
        for source_path, target_path in knowledge_mappings.items():
            source_full = self.source_dir / source_path
            target_full = self.target_dir / target_path
            
            if source_full.exists():
                logger.info(f"📖 Migrando knowledge: {source_path} → {target_path}")
                target_full.mkdir(parents=True, exist_ok=True)
                self._copy_directory_contents(source_full, target_full)
                
                self.migration_report["migrated_files"].append({
                    "source": str(source_full),
                    "target": str(target_full),
                    "type": "knowledge_base"
                })
            else:
                logger.warning(f"⚠️ Knowledge base não encontrada: {source_path}")
                
    def migrate_shared_components(self):
        """Migrar componentes compartilhados"""
        logger.info("🔧 Migrando componentes compartilhados...")
        
        shared_mappings = {
            "shared": "shared",
            "ingestion": "ingestion", 
            "magenerator": "magenerator"
        }
        
        for source_path, target_path in shared_mappings.items():
            source_full = self.source_dir / source_path
            target_full = self.target_dir / target_path
            
            if source_full.exists():
                logger.info(f"🔄 Migrando {source_path} → {target_path}")
                target_full.mkdir(parents=True, exist_ok=True)
                self._copy_directory_contents(source_full, target_full)
                
                self.migration_report["migrated_files"].append({
                    "source": str(source_full),
                    "target": str(target_full),
                    "type": "shared_component"
                })
                
    def migrate_configuration(self):
        """Migrar configurações"""
        logger.info("⚙️ Migrando configurações...")
        
        config_files = [
            ".env",
            "pyproject.toml",
            "requirements.txt",
            "makefile"
        ]
        
        for config_file in config_files:
            source_full = self.source_dir / config_file
            target_full = self.target_dir / config_file
            
            if source_full.exists():
                logger.info(f"📄 Migrando config: {config_file}")
                shutil.copy2(source_full, target_full)
                
                self.migration_report["migrated_files"].append({
                    "source": str(source_full),
                    "target": str(target_full),
                    "type": "configuration"
                })
                
    def migrate_documentation(self):
        """Migrar documentação"""
        logger.info("📚 Migrando documentação...")
        
        docs_source = self.source_dir / "docs"
        docs_target = self.target_dir / "docs"
        
        if docs_source.exists():
            docs_target.mkdir(parents=True, exist_ok=True)
            self._copy_directory_contents(docs_source, docs_target)
            
            self.migration_report["migrated_files"].append({
                "source": str(docs_source),
                "target": str(docs_target),
                "type": "documentation"
            })
            
    def create_domain_manifests(self):
        """Criar manifests para cada domínio"""
        logger.info("📋 Criando domain manifests...")
        
        domains = {
            "copywriters": {
                "name": "Copywriters Domain",
                "description": "Agentes especializados em copywriting e persuasão",
                "agents": [
                    "conversion_catalyst",
                    "neurohook_ultra", 
                    "pain_detector",
                    "paradigm_architect",
                    "metaphor_architect",
                    "retention_architect"
                ],
                "version": "3.0.0"
            },
            "analytics": {
                "name": "Analytics Domain", 
                "description": "Agentes de análise e tracking",
                "agents": ["super_track"],
                "version": "3.0.0"
            },
            "apis": {
                "name": "APIs Domain",
                "description": "Agentes de integração com APIs externas", 
                "agents": [
                    "hotmart_master",
                    "kiwify_master",
                    "perfectpay_master", 
                    "payt_master",
                    "api_unify_master",
                    "input_output_mapper"
                ],
                "version": "3.0.0"
            }
        }
        
        for domain_name, manifest in domains.items():
            manifest_path = self.target_dir / f"domains/{domain_name}/domain_manifest.json"
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
                
            logger.info(f"📋 Criado manifest: {domain_name}")
            
    def create_init_files(self):
        """Criar arquivos __init__.py necessários"""
        logger.info("🐍 Criando arquivos __init__.py...")
        
        init_dirs = [
            "shared",
            "ingestion", 
            "magenerator",
            "interfaces",
            "tests",
            "domains/copywriters",
            "domains/analytics",
            "domains/apis"
        ]
        
        for init_dir in init_dirs:
            init_path = self.target_dir / init_dir / "__init__.py"
            init_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(init_path, 'w') as f:
                f.write(f'"""{"".join(init_dir.split("/")).title()} module"""\n')
                
            logger.info(f"🐍 Criado: {init_dir}/__init__.py")
            
    def _copy_directory_contents(self, source: Path, target: Path):
        """Copiar conteúdo de diretório recursivamente"""
        try:
            for item in source.rglob("*"):
                if item.is_file():
                    relative_path = item.relative_to(source)
                    target_file = target / relative_path
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, target_file)
        except Exception as e:
            logger.error(f"❌ Erro copiando {source} → {target}: {e}")
            self.migration_report["errors"].append(str(e))
            
    def _create_agent_structure(self, agent_dir: Path):
        """Criar estrutura específica para cada agente"""
        subdirs = ["controller", "subagents", "knowledge", "tests"]
        
        for subdir in subdirs:
            subdir_path = agent_dir / subdir
            subdir_path.mkdir(parents=True, exist_ok=True)
            
            # Criar __init__.py
            init_file = subdir_path / "__init__.py"
            with open(init_file, 'w') as f:
                f.write(f'"""{subdir.title()} module for {agent_dir.name}"""\n')
                
    def generate_migration_report(self):
        """Gerar relatório de migração"""
        self.migration_report["completed_at"] = datetime.now().isoformat()
        self.migration_report["summary"] = {
            "total_files_migrated": len(self.migration_report["migrated_files"]),
            "total_directories_created": len(self.migration_report["created_directories"]),
            "total_errors": len(self.migration_report["errors"]),
            "success": len(self.migration_report["errors"]) == 0
        }
        
        report_path = self.target_dir / "migration_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.migration_report, f, indent=2, ensure_ascii=False)
            
        logger.info(f"📊 Relatório de migração salvo em: {report_path}")
        
    def run_migration(self):
        """Executar migração completa"""
        logger.info("🚀 Iniciando migração para repository-optimized...")
        
        try:
            # Fase 1: Estrutura
            self.create_directory_structure()
            
            # Fase 2: Agentes
            self.migrate_agents_to_domains()
            
            # Fase 3: Knowledge bases
            self.migrate_knowledge_bases()
            
            # Fase 4: Componentes compartilhados
            self.migrate_shared_components()
            
            # Fase 5: Configurações
            self.migrate_configuration()
            
            # Fase 6: Documentação
            self.migrate_documentation()
            
            # Fase 7: Manifests
            self.create_domain_manifests()
            
            # Fase 8: Init files
            self.create_init_files()
            
            # Fase 9: Relatório
            self.generate_migration_report()
            
            logger.info("✅ Migração FASE A concluída com sucesso!")
            
        except Exception as e:
            logger.error(f"❌ Erro durante migração: {e}")
            self.migration_report["errors"].append(str(e))
            self.generate_migration_report()
            sys.exit(1)

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Migração FASE A para repository-optimized")
    parser.add_argument("--source", default="../", help="Diretório fonte")
    parser.add_argument("--target", default="./", help="Diretório destino")
    parser.add_argument("--validate", action="store_true", help="Validar migração")
    parser.add_argument("--backup", action="store_true", help="Criar backup")
    
    args = parser.parse_args()
    
    migrator = RepositoryMigrator(args.source, args.target)
    migrator.run_migration()
    
    if args.validate:
        logger.info("🔍 Executando validação...")
        # TODO: Implementar validação
        
    logger.info("🎉 FASE A: Migração concluída!")

if __name__ == "__main__":
    main() 