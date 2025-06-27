#!/usr/bin/env python3
"""
🎯 ADAPTADOR AUTOGEN STUDIO
Converte estrutura central de agentes para formato específico do AutoGen Studio
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

from ..agent_structure import AgentCore, Tool, PlatformAdapter, PlatformType

class AutoGenAdapter(PlatformAdapter):
    """Adaptador específico para AutoGen Studio"""
    
    def __init__(self, db_path: str = None):
        super().__init__(PlatformType.AUTOGEN)
        if db_path is None:
            db_path = Path.home() / ".autogenstudio" / "autogen04202.db"
        self.db_path = db_path
    
    def convert_tool(self, tool: Tool) -> Dict[str, Any]:
        """Converte ferramenta para formato AutoGen"""
        return {
            "type": tool.type,
            "name": tool.name,
            "description": tool.description,
            "enabled": tool.enabled,
            "config": tool.config
        }
    
    def convert_agent(self, agent: AgentCore) -> Dict[str, Any]:
        """Converte agente para formato AutoGen Studio v2"""
        # Converter ferramentas
        tools = [self.convert_tool(tool) for tool in agent.tools]
        
        # Configuração LLM
        llm_config = {
            "model": agent.llm_config.model,
            "temperature": agent.llm_config.temperature,
            "max_tokens": agent.llm_config.max_tokens,
            "top_p": agent.llm_config.top_p,
            "frequency_penalty": agent.llm_config.frequency_penalty,
            "presence_penalty": agent.llm_config.presence_penalty
        }
        
        # Estrutura do agente AutoGen
        autogen_agent = {
            "type": "assistant",
            "label": agent.name,
            "config": {
                "llm_config": llm_config,
                "human_input_mode": "NEVER",
                "system_message": agent.system_message,
                "tools": tools
            },
            "metadata": {
                "domain": agent.metadata.domain,
                "type": agent.metadata.agent_type.value,
                "specialization": agent.metadata.specialization,
                "parent": agent.metadata.parent,
                "version": agent.metadata.version,
                "created_by": agent.metadata.created_by,
                "capabilities": agent.metadata.capabilities,
                "sub_agents_count": len(agent.sub_agents),
                "tools_count": len(agent.tools),
                "prompt_length": len(agent.system_message)
            }
        }
        
        return autogen_agent
    
    def load_current_gallery(self) -> Dict[str, Any]:
        """Carrega galeria atual do AutoGen Studio"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT config FROM gallery WHERE id = 1")
            result = cursor.fetchone()
            
            if result:
                return json.loads(result[0])
            return self.create_default_gallery()
        except Exception as e:
            print(f"Erro ao carregar galeria: {e}")
            return self.create_default_gallery()
        finally:
            conn.close()
    
    def create_default_gallery(self) -> Dict[str, Any]:
        """Cria galeria padrão do AutoGen"""
        return {
            "components": {
                "agents": [
                    {
                        "type": "assistant",
                        "label": "AssistantAgent",
                        "config": {
                            "llm_config": {"model": "gpt-4", "temperature": 0.1},
                            "human_input_mode": "NEVER",
                            "system_message": "You are a helpful AI assistant."
                        }
                    },
                    {
                        "type": "assistant", 
                        "label": "Web Surfer Agent",
                        "config": {
                            "llm_config": {"model": "gpt-4", "temperature": 0.1},
                            "human_input_mode": "NEVER",
                            "system_message": "You are a web research assistant."
                        }
                    },
                    {
                        "type": "assistant",
                        "label": "Verification Assistant", 
                        "config": {
                            "llm_config": {"model": "gpt-4", "temperature": 0.1},
                            "human_input_mode": "NEVER",
                            "system_message": "You verify and validate information."
                        }
                    },
                    {
                        "type": "userproxy",
                        "label": "UserProxyAgent",
                        "config": {
                            "human_input_mode": "ALWAYS",
                            "system_message": "You are a user proxy agent."
                        }
                    }
                ]
            }
        }
    
    def deploy_agents(self, agents_by_domain: Dict[str, List[AgentCore]]) -> bool:
        """Deploy completo de agentes no AutoGen Studio"""
        print("🚀 DEPLOY AUTOGEN STUDIO - ESTRUTURA ORGANIZADA")
        print("=" * 55)
        
        # Carregar galeria atual
        gallery = self.load_current_gallery()
        
        # Manter apenas os 4 agentes originais
        original_agents = gallery["components"]["agents"][:4]
        
        total_agents = 0
        total_sub_agents = 0
        total_tools = 0
        
        # Processar todos os domínios
        for domain_name, agents in agents_by_domain.items():
            print(f"📁 Processando domínio: {domain_name}")
            
            for agent in agents:
                try:
                    # Converter agente principal
                    autogen_agent = self.convert_agent(agent)
                    original_agents.append(autogen_agent)
                    total_agents += 1
                    total_tools += len(agent.tools)
                    
                    # Converter sub-agentes
                    for sub_agent in agent.sub_agents:
                        autogen_sub_agent = self.convert_agent(sub_agent)
                        original_agents.append(autogen_sub_agent)
                        total_sub_agents += 1
                        total_tools += len(sub_agent.tools)
                    
                    print(f"✅ {agent.name}: {len(agent.sub_agents)} sub-agentes, {len(agent.tools)} ferramentas")
                    
                except Exception as e:
                    print(f"❌ Erro ao processar {agent.name}: {e}")
        
        # Atualizar galeria
        gallery["components"]["agents"] = original_agents
        
        # Salvar no banco
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE gallery 
                SET config = ?, updated_at = ?
                WHERE id = 1
            """, (json.dumps(gallery), datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            print("\n🎉 DEPLOY AUTOGEN FINALIZADO!")
            print(f"📊 ESTATÍSTICAS:")
            print(f"   • Agentes principais: {total_agents}")
            print(f"   • Sub-agentes: {total_sub_agents}")
            print(f"   • Total de ferramentas: {total_tools}")
            print(f"   • Total na galeria: {len(original_agents)} agentes")
            print(f"🔄 Reinicie o AutoGen Studio: pkill -f autogenstudio && autogenstudio ui --port 8081")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar galeria: {e}")
            return False 