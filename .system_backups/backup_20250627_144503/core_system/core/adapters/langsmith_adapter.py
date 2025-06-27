#!/usr/bin/env python3
"""
🎯 ADAPTADOR LANGSMITH
Converte estrutura central de agentes para formato específico do LangSmith/LangGraph
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

from ..agent_structure import AgentCore, Tool, PlatformAdapter, PlatformType

class LangSmithAdapter(PlatformAdapter):
    """Adaptador específico para LangSmith/LangGraph"""
    
    def __init__(self, output_dir: str = "langgraph_controllers"):
        super().__init__(PlatformType.LANGSMITH)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def convert_tool(self, tool: Tool) -> Dict[str, Any]:
        """Converte ferramenta para formato LangGraph"""
        return {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.config,
            "enabled": tool.enabled
        }
    
    def convert_agent(self, agent: AgentCore) -> Dict[str, Any]:
        """Converte agente para formato LangGraph"""
        # Converter ferramentas
        tools = [self.convert_tool(tool) for tool in agent.tools]
        
        # Estrutura do agente LangGraph
        langgraph_agent = {
            "name": agent.name,
            "system_message": agent.system_message,
            "tools": tools,
            "llm_config": {
                "model": agent.llm_config.model,
                "temperature": agent.llm_config.temperature,
                "max_tokens": agent.llm_config.max_tokens
            },
            "metadata": {
                "domain": agent.metadata.domain,
                "type": agent.metadata.agent_type.value,
                "specialization": agent.metadata.specialization,
                "parent": agent.metadata.parent,
                "sub_agents_count": len(agent.sub_agents),
                "tools_count": len(agent.tools)
            }
        }
        
        return langgraph_agent
    
    def convert_agent_to_langgraph(self, agent: AgentCore) -> str:
        """Converte agente para formato LangGraph Python"""
        
        # Template básico
        template = '''#!/usr/bin/env python3
from typing import Dict, Any, List, Optional
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState

# Configuração do modelo
llm = ChatOpenAI(
    model="{model}",
    temperature={temperature},
    max_tokens={max_tokens}
)

# System message do agente
SYSTEM_MESSAGE = """{system_message}"""

def {agent_name}_agent(state: MessagesState) -> Dict[str, Any]:
    """
    Agente: {agent_display_name}
    Domínio: {domain}
    Especialização: {specialization}
    """
    messages = state["messages"]
    
    # Adicionar system message
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_MESSAGE)] + messages
    
    # Chamar o modelo
    response = llm.invoke(messages)
    
    return {{"messages": [response]}}

# Criação do grafo LangGraph
def create_{agent_name}_graph():
    workflow = StateGraph(MessagesState)
    
    # Adicionar nó principal
    workflow.add_node("{agent_name}", {agent_name}_agent)
    
    # Definir entrada e saída
    workflow.set_entry_point("{agent_name}")
    workflow.set_finish_point("{agent_name}")
    
    return workflow.compile()

# Instanciar o grafo
{agent_name}_graph = create_{agent_name}_graph()

if __name__ == "__main__":
    # Teste do agente
    result = {agent_name}_graph.invoke({{
        "messages": [HumanMessage(content="Olá, preciso de ajuda com {specialization}")]
    }})
    print(result)
'''
        
        # Preparar dados
        agent_name_safe = agent.name.lower().replace(' ', '_').replace('-', '_')
        
        # Substituir valores no template
        code = template.format(
            model=agent.llm_config.model,
            temperature=agent.llm_config.temperature,
            max_tokens=agent.llm_config.max_tokens,
            system_message=agent.system_message.replace('"""', '\\"""'),
            agent_name=agent_name_safe,
            agent_display_name=agent.name,
            domain=agent.metadata.domain,
            specialization=agent.metadata.specialization
        )
        
        return code
    
    def deploy_agents(self, agents_by_domain: Dict[str, List[AgentCore]]) -> bool:
        """Deploy completo de agentes para LangGraph"""
        print("🚀 DEPLOY LANGSMITH/LANGGRAPH - ESTRUTURA ORGANIZADA")
        print("=" * 60)
        
        total_agents = 0
        total_sub_agents = 0
        total_files = 0
        
        # Processar todos os domínios
        for domain_name, agents in agents_by_domain.items():
            print(f"📁 Processando domínio: {domain_name}")
            
            domain_dir = self.output_dir / domain_name
            domain_dir.mkdir(exist_ok=True)
            
            for agent in agents:
                try:
                    # Gerar código LangGraph
                    langgraph_code = self.convert_agent_to_langgraph(agent)
                    
                    # Salvar arquivo
                    filename = f"{agent.name.lower().replace(' ', '_')}_controller.py"
                    file_path = domain_dir / filename
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(langgraph_code)
                    
                    total_agents += 1
                    total_sub_agents += len(agent.sub_agents)
                    total_files += 1
                    
                    print(f"✅ {agent.name}: {len(agent.sub_agents)} sub-agentes → {filename}")
                    
                except Exception as e:
                    print(f"❌ Erro ao processar {agent.name}: {e}")
        
        # Criar arquivo de configuração principal
        config = {
            "project": "multi-agent-ai-system",
            "created_at": datetime.now().isoformat(),
            "domains": list(agents_by_domain.keys()),
            "total_agents": total_agents,
            "total_sub_agents": total_sub_agents,
            "langsmith_config": {
                "tracing": True,
                "project": "multi-agent-ai-system",
                "endpoint": "https://api.smith.langchain.com"
            }
        }
        
        config_file = self.output_dir / "langgraph_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        print("\n🎉 DEPLOY LANGSMITH FINALIZADO!")
        print(f"📊 ESTATÍSTICAS:")
        print(f"   • Agentes principais: {total_agents}")
        print(f"   • Sub-agentes: {total_sub_agents}")
        print(f"   • Arquivos gerados: {total_files}")
        print(f"   • Diretório: {self.output_dir}")
        print(f"🚀 Para iniciar: cd {self.output_dir} && langgraph dev")
        
        return True
    
    def generate_controller(self, agent: 'AgentCore') -> str:
        """Gera código do controller LangGraph para um agente"""
        
        controller_template = f'''#!/usr/bin/env python3
"""
🎯 {agent.name.upper()} - CONTROLLER LANGGRAPH
Gerado automaticamente pelo sistema Multi-Agent AI
"""

from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated

class {agent.name.replace(' ', '').replace('|', '')}State(TypedDict):
    """Estado do agente {agent.name}"""
    messages: Annotated[list, add_messages]
    context: Dict[str, Any]

class {agent.name.replace(' ', '').replace('|', '')}Controller:
    """Controller LangGraph para {agent.name}"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            max_tokens=4000
        )
        self.system_prompt = """{agent.system_message}"""
        
        # Configurar grafo
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Constrói o grafo LangGraph"""
        graph = StateGraph({agent.name.replace(' ', '').replace('|', '')}State)
        
        # Adicionar nós
        graph.add_node("agent", self._agent_node)
        
        # Definir fluxo
        graph.set_entry_point("agent")
        graph.add_edge("agent", END)
        
        return graph.compile()
    
    def _agent_node(self, state: {agent.name.replace(' ', '').replace('|', '')}State) -> Dict[str, Any]:
        """Nó principal do agente"""
        messages = [SystemMessage(content=self.system_prompt)] + state["messages"]
        response = self.llm.invoke(messages)
        
        return {{
            "messages": [response],
            "context": state.get("context", {{}})
        }}
    
    def process(self, input_data: str, context: Dict[str, Any] = None) -> str:
        """Processa entrada usando o agente"""
        if context is None:
            context = {{}}
        
        initial_state = {{
            "messages": [HumanMessage(content=input_data)],
            "context": context
        }}
        
        result = self.graph.invoke(initial_state)
        return result["messages"][-1].content

# Instância global do controller
{agent.name.lower().replace(' ', '_').replace('|', '')}_controller = {agent.name.replace(' ', '').replace('|', '')}Controller()

def process_{agent.name.lower().replace(' ', '_').replace('|', '')}(input_data: str, context: Dict[str, Any] = None) -> str:
    """Função de entrada para o agente {agent.name}"""
    return {agent.name.lower().replace(' ', '_').replace('|', '')}_controller.process(input_data, context)

if __name__ == "__main__":
    # Teste do controller
    test_input = "Olá, preciso de ajuda com {agent.metadata.domain}"
    result = process_{agent.name.lower().replace(' ', '_').replace('|', '')}(test_input)
    print(f"Resultado: {{result}}")
'''
        
        return controller_template 