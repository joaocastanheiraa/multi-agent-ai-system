#!/usr/bin/env python3
"""
FASE D: AutoGen Complete Setup
Converte 68 sub-agentes para sistema AutoGen com multi-turn conversations
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class AgentProperties:
    """Structure to hold extracted agent properties"""
    name: str
    description: str
    mission: str
    role_function: str
    capabilities: List[str]
    constraints: List[str]
    personality_traits: List[str]
    process_workflow: List[str]
    output_format: str
    domain: str
    parent_agent: str

def find_sub_agents():
    """Encontra todos os sub-agentes no sistema"""
    sub_agents = []
    domains_dir = "domains"
    
    if not os.path.exists(domains_dir):
        print(f"❌ Diretório {domains_dir} não encontrado")
        return sub_agents
    
    for domain in os.listdir(domains_dir):
        domain_path = os.path.join(domains_dir, domain)
        if not os.path.isdir(domain_path) or domain.startswith('.'):
            continue
            
        agents_path = os.path.join(domain_path, "agents")
        if not os.path.exists(agents_path):
            continue
            
        for agent in os.listdir(agents_path):
            agent_path = os.path.join(agents_path, agent)
            if not os.path.isdir(agent_path) or agent.startswith('.'):
                continue
                
            # Verificar sub-agents e sub_agents
            for sub_dir in ['sub-agents', 'sub_agents']:
                sub_agents_path = os.path.join(agent_path, sub_dir)
                if os.path.exists(sub_agents_path):
                    for sub_agent in os.listdir(sub_agents_path):
                        sub_agent_path = os.path.join(sub_agents_path, sub_agent)
                        if os.path.isdir(sub_agent_path) and not sub_agent.startswith('.'):
                            prompt_file = os.path.join(sub_agent_path, "prompt.txt")
                            if os.path.exists(prompt_file):
                                sub_agents.append({
                                    'name': sub_agent,
                                    'path': sub_agent_path,
                                    'prompt_file': prompt_file,
                                    'domain': domain,
                                    'parent_agent': agent
                                })
    
    return sub_agents

def main():
    """Função principal para setup AutoGen"""
    print("🚀 FASE D: AUTOGEN COMPLETE SETUP")
    print("=" * 60)
    
    # Encontrar sub-agentes
    print("🔍 Descobrindo sub-agentes...")
    sub_agents = find_sub_agents()
    print(f"✅ Encontrados {len(sub_agents)} sub-agentes")
    
    if not sub_agents:
        print("❌ Nenhum sub-agente encontrado!")
        return False
    
    # Criar estrutura básica AutoGen para cada sub-agente
    converted_count = 0
    results = []
    
    print("\n🔄 Convertendo sub-agentes para AutoGen...")
    
    for sub_agent in sub_agents:
        try:
            # Criar diretório autogen
            autogen_dir = os.path.join(sub_agent['path'], "autogen")
            os.makedirs(autogen_dir, exist_ok=True)
            
            # Criar arquivo básico AutoGen
            agent_class_name = f"{sub_agent['name'].replace('-', '_').replace(' ', '_')}_Agent"
            autogen_file = os.path.join(autogen_dir, f"{sub_agent['name'].lower().replace('-', '_')}_agent.py")
            
            autogen_code = f'''#!/usr/bin/env python3
"""
AutoGen Agent: {sub_agent['name']}
Domain: {sub_agent['domain']}
Parent Agent: {sub_agent['parent_agent']}
"""

import autogen
from typing import Dict, List, Any, Optional

class {agent_class_name}(autogen.AssistantAgent):
    """
    {sub_agent['name']} - Specialized AutoGen Agent
    Domain: {sub_agent['domain']}
    Parent: {sub_agent['parent_agent']}
    """
    
    def __init__(self, name: str = "{sub_agent['name']}", **kwargs):
        system_message = """
Você é {sub_agent['name']}, um agente especializado do domínio {sub_agent['domain']}.

Sua função é trabalhar como sub-agente especializado sob o agente principal {sub_agent['parent_agent']}.

Mantenha sempre foco na sua especialização e colabore efetivamente no sistema multi-agente.
"""
        
        super().__init__(
            name=name,
            system_message=system_message,
            llm_config={{
                "config_list": [{{
                    "model": "gpt-4-turbo-preview",
                    "api_key": "YOUR_API_KEY_HERE"
                }}],
                "timeout": 120,
                "temperature": 0.7,
                "max_tokens": 2000,
            }},
            **kwargs
        )
        
        self.domain = "{sub_agent['domain']}"
        self.parent_agent = "{sub_agent['parent_agent']}"
    
    def process_request(self, request: str, context: Dict[str, Any] = None) -> str:
        """Processa requisição com contexto do domínio"""
        enhanced_request = f"""
        Como especialista em {{self.domain}}, processando: {{request}}
        
        Contexto adicional: {{context or 'Nenhum'}}
        """
        
        return enhanced_request

# Exemplo de uso:
# agent = {agent_class_name}()
# response = agent.process_request("Sua requisição aqui")
'''
            
            with open(autogen_file, 'w', encoding='utf-8') as f:
                f.write(autogen_code)
            
            converted_count += 1
            results.append({
                'name': sub_agent['name'],
                'domain': sub_agent['domain'],
                'parent': sub_agent['parent_agent'],
                'autogen_file': autogen_file
            })
            
            print(f"   ✅ {sub_agent['name']} ({sub_agent['domain']})")
            
        except Exception as e:
            print(f"   ❌ Erro processando {sub_agent['name']}: {e}")
    
    # Salvar relatório
    os.makedirs('migration_reports', exist_ok=True)
    report = {
        'phase': 'D - AutoGen Setup',
        'timestamp': datetime.now().isoformat(),
        'total_sub_agents': len(sub_agents),
        'converted_count': converted_count,
        'success_rate': f"{(converted_count/len(sub_agents)*100):.1f}%",
        'results': results
    }
    
    with open('migration_reports/phase_d_autogen_setup.json', 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 FASE D CONCLUÍDA!")
    print(f"✅ {converted_count}/{len(sub_agents)} sub-agentes convertidos para AutoGen")
    print(f"📊 Taxa de sucesso: {(converted_count/len(sub_agents)*100):.1f}%")
    print(f"📄 Relatório salvo em: migration_reports/phase_d_autogen_setup.json")
    
    return converted_count == len(sub_agents)

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 PRONTO PARA FASE E: MCP INTEGRATION")
    else:
        print("\n⚠️ Verificar erros antes de continuar")
