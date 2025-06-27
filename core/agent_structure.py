#!/usr/bin/env python3
"""
🎯 ESTRUTURA CENTRAL DE AGENTES - MULTI-PLATFORM
Definição padronizada que se adapta para AutoGen, LangSmith, OpenAI, etc.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class AgentType(Enum):
    MAIN = "main_agent"
    SUB = "sub_agent"
    SPECIALIST = "specialist"

class PlatformType(Enum):
    AUTOGEN = "autogen"
    LANGSMITH = "langsmith"
    OPENAI = "openai"
    LANGRAPH = "langgraph"

@dataclass
class Tool:
    name: str
    type: str
    description: str
    enabled: bool = True
    config: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.config is None:
            self.config = {}

@dataclass
class LLMConfig:
    model: str = "gpt-4-turbo-preview"
    temperature: float = 0.1
    max_tokens: int = 4000
    top_p: float = 0.9
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0

@dataclass
class AgentMetadata:
    domain: str
    specialization: str
    agent_type: AgentType
    parent: Optional[str] = None
    version: str = "1.0"
    created_by: str = "multi_agent_ai_system"
    capabilities: List[str] = None
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []

@dataclass
class AgentCore:
    """Estrutura central padronizada de um agente"""
    name: str
    system_message: str
    tools: List[Tool]
    llm_config: LLMConfig
    metadata: AgentMetadata
    sub_agents: List['AgentCore'] = None
    
    def __post_init__(self):
        if self.sub_agents is None:
            self.sub_agents = []

class AgentLoader:
    """Carregador universal de agentes dos domínios"""
    
    def __init__(self, domains_path: str = "domains"):
        self.domains_path = Path(domains_path)
    
    def load_tools_from_yaml(self, tools_yaml_path: Path) -> List[Tool]:
        """Carrega ferramentas do YAML e converte para estrutura padronizada"""
        if not tools_yaml_path.exists():
            return []
        
        try:
            with open(tools_yaml_path, 'r', encoding='utf-8') as f:
                tools_data = yaml.safe_load(f)
            
            if not tools_data or 'tools' not in tools_data:
                return []
            
            tools = []
            for tool_name, tool_config in tools_data['tools'].items():
                tool = Tool(
                    name=tool_name,
                    type=tool_name,
                    description=tool_config.get('description', f'Tool {tool_name}'),
                    enabled=tool_config.get('enabled', True),
                    config=tool_config.get('config', {})
                )
                tools.append(tool)
            
            return tools
        except Exception as e:
            print(f"Erro ao carregar ferramentas de {tools_yaml_path}: {e}")
            return []
    
    def load_prompt(self, agent_dir: Path) -> str:
        """Carrega prompt do arquivo prompt.txt - SEMPRE prioriza arquivo original"""
        prompt_file = agent_dir / "prompt.txt"
        
        if not prompt_file.exists():
            raise FileNotFoundError(f"Arquivo prompt.txt não encontrado em {agent_dir}")
        
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt = f.read().strip()
            
            if not prompt:
                raise ValueError(f"Arquivo prompt.txt está vazio em {agent_dir}")
            
            print(f"✅ Prompt carregado: {agent_dir.name} ({len(prompt)} chars)")
            return prompt
            
        except Exception as e:
            raise Exception(f"Erro ao carregar prompt de {agent_dir}: {e}")
    
    def load_specific_prompt(self, agent_name: str, domain: str, agent_dir: Path) -> str:
        """Carrega prompt específico do agente - SEMPRE usa arquivo prompt.txt original"""
        
        # PRIORIDADE ÚNICA: Arquivo prompt.txt original do agente
        prompt_file = agent_dir / "prompt.txt"
        if not prompt_file.exists():
            raise FileNotFoundError(f"Arquivo prompt.txt obrigatório não encontrado: {prompt_file}")
        
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt = f.read().strip()
            
            if not prompt:
                raise ValueError(f"Arquivo prompt.txt está vazio: {prompt_file}")
            
            if len(prompt) < 50:
                print(f"⚠️ AVISO: Prompt muito pequeno para {agent_name}: {len(prompt)} chars")
            
            print(f"✅ Prompt específico carregado: {agent_name} ({len(prompt)} chars)")
            return prompt
            
        except Exception as e:
            raise Exception(f"ERRO CRÍTICO ao carregar prompt de {agent_name}: {e}")
    
    def generate_generic_prompt(self, agent_name: str, domain: str) -> str:
        """REMOVIDA - Esta função causava problemas. Use apenas prompts originais."""
        raise NotImplementedError(
            "Função removida para evitar sobrescrita de prompts originais. "
            "Use apenas arquivos prompt.txt originais dos agentes."
        )
    
    def load_agent_from_directory(self, agent_dir: Path, domain: str) -> AgentCore:
        """Carrega um agente completo do diretório"""
        agent_name = agent_dir.name
        
        # 1. Carregar prompt específico (primeiro procurar nos controllers/LangGraph)
        system_message = self.load_specific_prompt(agent_name, domain, agent_dir)
        
        # 2. Carregar ferramentas
        tools_file = agent_dir / "tools.yaml"
        tools = self.load_tools_from_yaml(tools_file)
        
        # 3. Configuração LLM padrão
        llm_config = LLMConfig()
        
        # 4. Metadata
        metadata = AgentMetadata(
            domain=domain,
            specialization=agent_name,
            agent_type=AgentType.MAIN
        )
        
        # 5. Carregar sub-agentes
        sub_agents = []
        for sub_dir_name in ["sub-agents", "sub_agents"]:
            sub_agents_dir = agent_dir / sub_dir_name
            if sub_agents_dir.exists():
                for sub_agent_dir in sub_agents_dir.iterdir():
                    if sub_agent_dir.is_dir():
                        sub_agent = self.load_sub_agent(sub_agent_dir, domain, agent_name)
                        sub_agents.append(sub_agent)
        
        # 6. Criar agente principal
        agent = AgentCore(
            name=agent_name,
            system_message=system_message,
            tools=tools,
            llm_config=llm_config,
            metadata=metadata,
            sub_agents=sub_agents
        )
        
        return agent
    
    def load_sub_agent(self, sub_agent_dir: Path, domain: str, parent_name: str) -> 'AgentCore':
        """Carrega um sub-agente com validação robusta"""
        
        # Verificar se tem prompt.txt
        prompt_file = sub_agent_dir / "prompt.txt"
        if not prompt_file.exists():
            raise FileNotFoundError(f"Sub-agente {sub_agent_dir.name} não tem prompt.txt")
        
        # Verificar se o prompt não está vazio
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt_content = f.read().strip()
            if len(prompt_content) < 20:  # Muito pequeno para ser válido
                raise ValueError(f"Prompt muito pequeno: {len(prompt_content)} chars")
        except Exception as e:
            raise Exception(f"Erro ao validar prompt de {sub_agent_dir.name}: {e}")
        
        # Carregar normalmente se passou na validação
        name = sub_agent_dir.name
        system_message = self.load_prompt(sub_agent_dir)
        tools = self.load_tools_from_yaml(sub_agent_dir / "tools.yaml")
        
        # Configuração LLM para sub-agente
        llm_config = LLMConfig(
            model="gpt-4",
            temperature=0.1,
            max_tokens=2000
        )
        
        # Metadata do sub-agente
        metadata = AgentMetadata(
            domain=domain,
            specialization=name,
            agent_type=AgentType.SUB,
            parent=parent_name
        )
        
        print(f"    ✅ Sub-agente: {name} ({len(system_message)} chars, {len(tools)} tools)")
        
        return AgentCore(
            name=name,
            system_message=system_message,
            tools=tools,
            llm_config=llm_config,
            metadata=metadata,
            sub_agents=[]  # Sub-agentes não têm sub-agentes
        )
    
    def load_all_agents(self) -> Dict[str, List[AgentCore]]:
        """Carrega todos os agentes de todos os domínios"""
        all_agents = {}
        
        for domain_dir in self.domains_path.iterdir():
            if not domain_dir.is_dir() or domain_dir.name.startswith('.'):
                continue
            
            domain_name = domain_dir.name
            agents_dir = domain_dir / "agents"
            
            if not agents_dir.exists():
                continue
            
            domain_agents = []
            for agent_dir in agents_dir.iterdir():
                if agent_dir.is_dir():
                    try:
                        agent = self.load_agent_from_directory(agent_dir, domain_name)
                        domain_agents.append(agent)
                    except Exception as e:
                        print(f"Erro ao carregar agente {agent_dir.name}: {e}")
            
            all_agents[domain_name] = domain_agents
        
        return all_agents

class PlatformAdapter:
    """Adaptador base para diferentes plataformas"""
    
    def __init__(self, platform: PlatformType):
        self.platform = platform
    
    def convert_agent(self, agent: AgentCore) -> Dict[str, Any]:
        """Converte agente para formato específico da plataforma"""
        raise NotImplementedError("Subclasses devem implementar convert_agent")
    
    def convert_tool(self, tool: Tool) -> Dict[str, Any]:
        """Converte ferramenta para formato específico da plataforma"""
        raise NotImplementedError("Subclasses devem implementar convert_tool")

# Exemplo de uso
if __name__ == "__main__":
    # Carregar todos os agentes
    loader = AgentLoader()
    all_agents = loader.load_all_agents()
    
    # Mostrar estatísticas
    total_agents = 0
    total_sub_agents = 0
    total_tools = 0
    
    for domain, agents in all_agents.items():
        print(f"📁 {domain}: {len(agents)} agentes principais")
        for agent in agents:
            total_agents += 1
            total_sub_agents += len(agent.sub_agents)
            total_tools += len(agent.tools)
            for sub_agent in agent.sub_agents:
                total_tools += len(sub_agent.tools)
    
    print(f"\n📊 TOTAL:")
    print(f"• Agentes principais: {total_agents}")
    print(f"• Sub-agentes: {total_sub_agents}")
    print(f"• Ferramentas: {total_tools}") 