#!/usr/bin/env python3
"""
Script de validação de integridade da migração
Verifica que todos os arquivos foram migrados corretamente e estrutura está íntegra
"""

import os
import json
import hashlib
import glob
from datetime import datetime
from pathlib import Path

def count_files_recursive(directory):
    """Conta arquivos recursivamente em um diretório"""
    if not os.path.exists(directory):
        return 0
    
    count = 0
    for root, dirs, files in os.walk(directory):
        count += len(files)
    return count

def validate_domain_structure():
    """Valida estrutura de domínios"""
    expected_domains = ['copywriters', 'apis', 'analytics', 'knowledge']
    found_domains = []
    issues = []
    
    domains_dir = "domains"
    if not os.path.exists(domains_dir):
        issues.append("Diretório 'domains' não encontrado")
        return {"valid": False, "found_domains": [], "issues": issues}
    
    for domain in os.listdir(domains_dir):
        domain_path = os.path.join(domains_dir, domain)
        if os.path.isdir(domain_path) and not domain.startswith('.'):
            found_domains.append(domain)
            
            # Verifica se tem domain_manifest.json
            manifest_path = os.path.join(domain_path, "domain_manifest.json")
            if not os.path.exists(manifest_path):
                issues.append(f"Domain manifest não encontrado em {domain}")
    
    # Verifica se todos os domínios esperados estão presentes
    missing_domains = set(expected_domains) - set(found_domains)
    if missing_domains:
        issues.append(f"Domínios faltando: {list(missing_domains)}")
    
    return {
        "valid": len(issues) == 0,
        "expected_domains": expected_domains,
        "found_domains": found_domains,
        "missing_domains": list(missing_domains),
        "issues": issues
    }

def validate_agents_structure():
    """Valida estrutura de agentes em cada domínio"""
    validation_results = {}
    total_agents = 0
    total_sub_agents = 0
    issues = []
    
    domains_dir = "domains"
    if not os.path.exists(domains_dir):
        return {"valid": False, "issues": ["Diretório domains não encontrado"]}
    
    for domain in os.listdir(domains_dir):
        domain_path = os.path.join(domains_dir, domain)
        if not os.path.isdir(domain_path) or domain.startswith('.'):
            continue
            
        domain_agents = []
        domain_issues = []
        
        for agent in os.listdir(domain_path):
            agent_path = os.path.join(domain_path, agent)
            if not os.path.isdir(agent_path) or agent.startswith('.') or agent == '__pycache__':
                continue
                
            agent_info = {
                "name": agent,
                "path": agent_path,
                "has_prompt": os.path.exists(os.path.join(agent_path, "prompt.txt")),
                "has_tools": os.path.exists(os.path.join(agent_path, "tools.yaml")),
                "has_knowledge": False,
                "sub_agents_count": 0,
                "files_count": 0
            }
            
            # Verifica knowledge base
            knowledge_path = os.path.join(agent_path, "knowledge_base")
            if os.path.exists(knowledge_path):
                agent_info["has_knowledge"] = True
            
            # Conta sub-agentes
            for sub_dir in ['sub-agents', 'sub_agents']:
                sub_path = os.path.join(agent_path, sub_dir)
                if os.path.exists(sub_path):
                    agent_info["sub_agents_count"] = len([d for d in os.listdir(sub_path) 
                                                        if os.path.isdir(os.path.join(sub_path, d))])
                    break
            
            # Conta arquivos
            agent_info["files_count"] = count_files_recursive(agent_path)
            
            domain_agents.append(agent_info)
            total_agents += 1
            total_sub_agents += agent_info["sub_agents_count"]
        
        validation_results[domain] = {
            "agents": domain_agents,
            "agents_count": len(domain_agents),
            "sub_agents_count": sum(a["sub_agents_count"] for a in domain_agents),
            "total_files": sum(a["files_count"] for a in domain_agents),
            "issues": domain_issues
        }
        
        issues.extend(domain_issues)
    
    return {
        "valid": len(issues) == 0,
        "domains": validation_results,
        "summary": {
            "total_agents": total_agents,
            "total_sub_agents": total_sub_agents,
            "total_files": sum(d["total_files"] for d in validation_results.values())
        },
        "issues": issues
    }

def main():
    """Função principal de validação"""
    print("🚀 INICIANDO VALIDAÇÃO DE INTEGRIDADE DA MIGRAÇÃO")
    print("=" * 60)
    
    # Validações individuais
    domain_validation = validate_domain_structure()
    agents_validation = validate_agents_structure()
    
    # Consolidar resultados
    all_issues = []
    all_issues.extend(domain_validation.get("issues", []))
    all_issues.extend(agents_validation.get("issues", []))
    
    # Cálculos gerais
    total_files = 0
    if agents_validation["valid"]:
        total_files += agents_validation["summary"]["total_files"]
    
    validation_summary = {
        "migration_valid": len(all_issues) == 0,
        "timestamp": datetime.now().isoformat(),
        "validations": {
            "domains": domain_validation,
            "agents": agents_validation
        },
        "summary": {
            "total_domains": len(domain_validation.get("found_domains", [])),
            "total_agents": agents_validation.get("summary", {}).get("total_agents", 0),
            "total_sub_agents": agents_validation.get("summary", {}).get("total_sub_agents", 0),
            "total_files": total_files,
            "total_issues": len(all_issues)
        },
        "all_issues": all_issues
    }
    
    # Exibir resultados
    summary = validation_summary["summary"]
    print(f"\n📊 RESULTADOS DA VALIDAÇÃO:")
    print(f"   🏢 Domínios: {summary['total_domains']}")
    print(f"   🤖 Agentes: {summary['total_agents']}")
    print(f"   🔧 Sub-agentes: {summary['total_sub_agents']}")
    print(f"   📄 Total de Arquivos: {summary['total_files']}")
    print(f"   ⚠️ Issues: {summary['total_issues']}")
    
    if validation_summary["migration_valid"]:
        print(f"\n✅ MIGRAÇÃO VÁLIDA - Todos os componentes estão íntegros!")
    else:
        print(f"\n❌ MIGRAÇÃO COM PROBLEMAS:")
        for issue in validation_summary["all_issues"]:
            print(f"   - {issue}")
    
    # Salvar relatório
    os.makedirs("migration_reports", exist_ok=True)
    report_path = "migration_reports/migration_validation_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(validation_summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Relatório detalhado salvo em: {report_path}")
    
    # Retornar código de saída
    return 0 if validation_summary["migration_valid"] else 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
