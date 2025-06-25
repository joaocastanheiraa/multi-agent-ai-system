#!/usr/bin/env python3
"""
Configuração customizada do AutoGen Studio com nossos agentes
"""

import os
import json
from pathlib import Path

def load_our_agents():
    """Carrega nossos agentes do sistema"""
    agents = []
    
    # Domínios principais
    domains = ['copywriters', 'apis', 'analytics', 'knowledge']
    
    for domain in domains:
        domain_path = f"domains/{domain}/agents"
        if os.path.exists(domain_path):
            for agent_dir in os.listdir(domain_path):
                agent_path = os.path.join(domain_path, agent_dir)
                if os.path.isdir(agent_path):
                    # Carregar manifest
                    manifest_path = os.path.join(agent_path, "agent_manifest.json")
                    prompt_path = os.path.join(agent_path, "prompt.txt")
                    
                    if os.path.exists(manifest_path) and os.path.exists(prompt_path):
                        with open(manifest_path, 'r') as f:
                            manifest = json.load(f)
                        
                        with open(prompt_path, 'r', encoding='utf-8') as f:
                            prompt = f.read()
                        
                        agent_config = {
                            "name": manifest.get("agent_name", agent_dir),
                            "description": manifest.get("specialization", "Agente especializado"),
                            "system_message": prompt,
                            "domain": domain,
                            "type": manifest.get("type", "main_agent"),
                            "subagents": manifest.get("subagents", [])
                        }
                        
                        agents.append(agent_config)
    
    return agents

def create_autogen_studio_config():
    """Cria arquivo de configuração para AutoGen Studio"""
    
    print("🔧 CRIANDO CONFIGURAÇÃO PARA AUTOGEN STUDIO")
    print("===========================================")
    
    # Carregar nossos agentes
    agents = load_our_agents()
    
    print(f"📂 Encontrados {len(agents)} agentes:")
    
    # Criar configuração
    config = {
        "agents": [],
        "workflows": [],
        "version": "1.0"
    }
    
    for agent in agents:
        autogen_agent = {
            "name": agent['name'],
            "description": agent['description'],
            "system_message": agent['system_message'],
            "llm_config": {
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 2000
            },
            "domain": agent['domain'],
            "type": agent['type']
        }
        
        config["agents"].append(autogen_agent)
        print(f"  ✅ {agent['name']} ({agent['domain']})")
    
    # Criar workflows por domínio
    domains_workflows = {
        "copywriters": ["conversion_catalyst", "neurohook_ultra", "pain_detector", "metaphor_architect", "paradigm_architect", "retention_architect"],
        "apis": ["APIUnifyMaster", "HotmartAPIMaster", "KiwifyAPIMaster", "PerfectpayAPIMaster", "PaytAPIMaster", "APIsImputOutputMapper"],
        "analytics": ["ANALYTICSGPT | Super Track"],
        "knowledge": ["DocRAGOptimizer"]
    }
    
    for domain, agent_names in domains_workflows.items():
        workflow = {
            "name": f"{domain.title()} Workflow",
            "description": f"Workflow completo para {domain}",
            "agents": agent_names,
            "domain": domain
        }
        config["workflows"].append(workflow)
    
    # Salvar configuração
    config_path = ".autogenstudio_config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"")
    print(f"✅ Configuração salva em: {config_path}")
    print(f"📊 {len(config['agents'])} agentes configurados")
    print(f"📋 {len(config['workflows'])} workflows criados")
    
    return config_path

def start_autogen_studio_with_agents():
    """Inicia AutoGen Studio com configuração dos agentes"""
    
    # Criar configuração
    config_path = create_autogen_studio_config()
    
    print("")
    print("🚀 INICIANDO AUTOGEN STUDIO COM NOSSOS AGENTES")
    print("==============================================")
    
    # Comando para iniciar com configuração
    print("💡 Execute este comando para iniciar com os agentes:")
    print(f"   autogenstudio ui --port 8081 --host 0.0.0.0")
    print("")
    print("📁 Arquivo de configuração criado:")
    print(f"   {os.path.abspath(config_path)}")
    print("")
    print("🌐 Após iniciar, acesse:")
    print("   http://localhost:8081")
    print("")
    print("📋 Os agentes estarão disponíveis na interface!")

if __name__ == "__main__":
    start_autogen_studio_with_agents() 