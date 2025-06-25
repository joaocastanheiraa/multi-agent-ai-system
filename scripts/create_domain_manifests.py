#!/usr/bin/env python3
"""
Script para criar domain manifests para cada domínio
Tarefa 1.12: Configurar Domain Manifests
"""

import json
from pathlib import Path
from datetime import datetime

class DomainManifestsCreator:
    def __init__(self):
        self.domains_dir = Path("domains")
        self.report = {
            "task": "Create Domain Manifests",
            "start_time": datetime.now().isoformat(),
            "manifests_created": [],
            "errors": []
        }
    
    def create_copywriters_manifest(self):
        """Criar manifest para domínio copywriters"""
        domain_dir = self.domains_dir / "copywriters"
        
        manifest = {
            "domain_name": "copywriters",
            "domain_type": "content_creation",
            "description": "Domínio especializado em copywriting avançado com neurociência aplicada",
            "migration_status": "migrated",
            "migration_date": datetime.now().isoformat(),
            "agents": {
                "main_agents_count": 6,
                "sub_agents_count": 30,
                "total_agents": 36,
                "main_agents": [
                    "conversion_catalyst",
                    "neurohook_ultra",
                    "pain_detector", 
                    "paradigm_architect",
                    "metaphor_architect",
                    "retention_architect"
                ]
            },
            "specializations": [
                "Otimização de conversão neurológica",
                "Geração de hooks psicológicos",
                "Detecção e mapeamento de dores",
                "Transformação paradigmática",
                "Criação de metáforas isomórficas",
                "Engenharia de retenção"
            ],
            "knowledge_bases": [
                "conversion_catalyst_knowledge",
                "metaphor_architect_knowledge", 
                "neurohook_knowledge",
                "pain_detector_knowledge",
                "paradigm_architect_knowledge",
                "retention_architect_knowledge"
            ],
            "architecture": {
                "current": "prompt_based",
                "target": "langgraph_controllers",
                "sub_agents_target": "autogen_agents"
            },
            "next_phases": [
                "langraph_conversion",
                "autogen_implementation",
                "rag_optimization"
            ],
            "dependencies": [],
            "interfaces": ["mcp_server", "fastapi", "websocket"]
        }
        
        manifest_path = domain_dir / "domain_manifest.json"
        domain_dir.mkdir(parents=True, exist_ok=True)
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Criado: {manifest_path}")
        self.report["manifests_created"].append("copywriters")
        return True
    
    def create_apis_manifest(self):
        """Criar manifest para domínio APIs"""
        domain_dir = self.domains_dir / "apis"
        
        manifest = {
            "domain_name": "apis",
            "domain_type": "integration_services",
            "description": "Domínio especializado em integrações com APIs de pagamento e e-commerce",
            "migration_status": "migrated",
            "migration_date": datetime.now().isoformat(),
            "agents": {
                "main_agents_count": 6,
                "sub_agents_count": 28,
                "total_agents": 34,
                "main_agents": [
                    "HotmartAPIMaster",
                    "KiwifyAPIMaster",
                    "PerfectpayAPIMaster",
                    "PaytAPIMaster",
                    "APIUnifyMaster",
                    "APIsImputOutputMapper"
                ]
            },
            "api_integrations": [
                "Hotmart API",
                "Kiwify API", 
                "Perfectpay API",
                "Payt API"
            ],
            "specializations": [
                "Integração Hotmart completa",
                "Integração Kiwify completa",
                "Integração Perfectpay completa",
                "Integração Payt completa",
                "Unificação de múltiplas APIs",
                "Mapeamento input/output"
            ],
            "architecture": {
                "current": "prompt_based",
                "target": "langgraph_controllers",
                "sub_agents_target": "autogen_agents"
            },
            "next_phases": [
                "langraph_conversion",
                "autogen_implementation",
                "api_optimization"
            ],
            "dependencies": ["external_apis"],
            "interfaces": ["mcp_server", "fastapi", "webhooks"]
        }
        
        manifest_path = domain_dir / "domain_manifest.json"
        domain_dir.mkdir(parents=True, exist_ok=True)
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Criado: {manifest_path}")
        self.report["manifests_created"].append("apis")
        return True
    
    def create_analytics_manifest(self):
        """Criar manifest para domínio analytics"""
        domain_dir = self.domains_dir / "analytics"
        
        manifest = {
            "domain_name": "analytics",
            "domain_type": "data_analysis",
            "description": "Domínio especializado em análise de dados e geração de insights avançados",
            "migration_status": "migrated",
            "migration_date": datetime.now().isoformat(),
            "agents": {
                "main_agents_count": 1,
                "sub_agents_count": 5,
                "total_agents": 6,
                "main_agents": [
                    "ANALYTICSGPT | Super Track"
                ]
            },
            "specializations": [
                "Análise de dados avançada",
                "Geração de insights",
                "Tracking e monitoramento",
                "Métricas de performance",
                "Relatórios automatizados"
            ],
            "architecture": {
                "current": "prompt_based",
                "target": "langgraph_controllers",
                "sub_agents_target": "autogen_agents"
            },
            "next_phases": [
                "langraph_conversion",
                "autogen_implementation",
                "analytics_optimization"
            ],
            "dependencies": ["data_sources"],
            "interfaces": ["mcp_server", "fastapi", "dashboards"]
        }
        
        manifest_path = domain_dir / "domain_manifest.json"
        domain_dir.mkdir(parents=True, exist_ok=True)
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Criado: {manifest_path}")
        self.report["manifests_created"].append("analytics")
        return True
    
    def create_knowledge_manifest(self):
        """Criar manifest para domínio knowledge"""
        domain_dir = self.domains_dir / "knowledge"
        
        manifest = {
            "domain_name": "knowledge",
            "domain_type": "knowledge_management",
            "description": "Domínio especializado em otimização RAG e processamento de documentos",
            "migration_status": "migrated",
            "migration_date": datetime.now().isoformat(),
            "agents": {
                "main_agents_count": 1,
                "sub_agents_count": 5,
                "total_agents": 6,
                "main_agents": [
                    "DocRAGOptimizer"
                ]
            },
            "specializations": [
                "Otimização RAG",
                "Processamento de documentos",
                "Busca semântica",
                "Extração de conhecimento",
                "Indexação vetorial"
            ],
            "knowledge_bases_managed": [
                "conversion_catalyst_knowledge",
                "metaphor_architect_knowledge",
                "neurohook_knowledge", 
                "pain_detector_knowledge",
                "paradigm_architect_knowledge",
                "retention_architect_knowledge"
            ],
            "architecture": {
                "current": "prompt_based",
                "target": "langgraph_controllers",
                "sub_agents_target": "autogen_agents"
            },
            "next_phases": [
                "langraph_conversion",
                "autogen_implementation", 
                "rag_optimization"
            ],
            "dependencies": ["supabase_vector_db"],
            "interfaces": ["mcp_server", "fastapi", "vector_search"]
        }
        
        manifest_path = domain_dir / "domain_manifest.json"
        domain_dir.mkdir(parents=True, exist_ok=True)
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Criado: {manifest_path}")
        self.report["manifests_created"].append("knowledge")
        return True
    
    def create_global_domains_index(self):
        """Criar índice global dos domínios"""
        index = {
            "domains_index": {
                "total_domains": 4,
                "domains": [
                    {
                        "name": "copywriters",
                        "type": "content_creation",
                        "agents_count": 36,
                        "status": "migrated"
                    },
                    {
                        "name": "apis", 
                        "type": "integration_services",
                        "agents_count": 34,
                        "status": "migrated"
                    },
                    {
                        "name": "analytics",
                        "type": "data_analysis", 
                        "agents_count": 6,
                        "status": "migrated"
                    },
                    {
                        "name": "knowledge",
                        "type": "knowledge_management",
                        "agents_count": 6,
                        "status": "migrated"
                    }
                ],
                "total_agents": 82,
                "migration_date": datetime.now().isoformat(),
                "next_phase": "langraph_conversion_phase_b"
            }
        }
        
        index_path = self.domains_dir / "domains_index.json"
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Criado: {index_path}")
        return True
    
    def generate_report(self):
        """Gerar relatório da criação de manifests"""
        self.report["end_time"] = datetime.now().isoformat()
        self.report["success"] = len(self.report["errors"]) == 0
        self.report["manifests_count"] = len(self.report["manifests_created"])
        
        report_path = Path("migration_reports") / "domain_manifests_creation.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 RELATÓRIO DE CRIAÇÃO DE MANIFESTS")
        print(f"Manifests criados: {self.report['manifests_count']}")
        print(f"Erros: {len(self.report['errors'])}")
        print(f"Relatório salvo em: {report_path}")
        
        return self.report
    
    def run_creation(self):
        """Executar criação de todos os manifests"""
        print("🚀 INICIANDO CRIAÇÃO DOS DOMAIN MANIFESTS")
        
        # Criar manifest para cada domínio
        self.create_copywriters_manifest()
        self.create_apis_manifest()
        self.create_analytics_manifest()
        self.create_knowledge_manifest()
        
        # Criar índice global
        self.create_global_domains_index()
        
        # Gerar relatório
        report = self.generate_report()
        
        if report["success"]:
            print("\n🎉 CRIAÇÃO DOS DOMAIN MANIFESTS CONCLUÍDA!")
        else:
            print(f"\n⚠️  CRIAÇÃO CONCLUÍDA COM {len(report['errors'])} ERROS")
        
        return report

if __name__ == "__main__":
    creator = DomainManifestsCreator()
    creator.run_creation()
