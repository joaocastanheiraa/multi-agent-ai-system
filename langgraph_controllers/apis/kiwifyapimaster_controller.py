#!/usr/bin/env python3
"""
🎯 KIWIFYAPIMASTER - CONTROLLER LANGGRAPH
Gerado automaticamente pelo sistema Multi-Agent AI
"""

from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated

class KiwifyAPIMasterState(TypedDict):
    """Estado do agente KiwifyAPIMaster"""
    messages: Annotated[list, add_messages]
    context: Dict[str, Any]

class KiwifyAPIMasterController:
    """Controller LangGraph para KiwifyAPIMaster"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            max_tokens=4000
        )
        self.system_prompt = """You are KiwifyAPIMaster, a specialized AI agent.

Domain: apis
Specialization: KiwifyAPIMaster operations and management
Controller: KiwifyAPIMaster_controller.py

You are an expert in apis domain with deep knowledge of KiwifyAPIMaster workflows.


## FERRAMENTAS DISPONÍVEIS
Você tem acesso às seguintes ferramentas especializadas:
- **api_client**: Tool api_client para KiwifyAPIMaster (✅ ATIVA)
- **json_parser**: Tool json_parser para KiwifyAPIMaster (✅ ATIVA)
- **webhook_handler**: Tool webhook_handler para KiwifyAPIMaster (✅ ATIVA)


## SUB-AGENTES ESPECIALIZADOS
Você coordena os seguintes sub-agentes especializados:
- **1 copy 3**: Sub-agente especializado
- **1 copy 4**: Sub-agente especializado
- **1 copy 2**: Sub-agente especializado
- **1**: Sub-agente especializado
- **1 copy**: Sub-agente especializado


## INFORMAÇÕES DO SISTEMA
- Agente: KiwifyAPIMaster
- Domínio: apis
- Ferramentas: 3
- Sub-agentes: 5
- Atualizado automaticamente com configurações reais"""
        
        # Configurar grafo
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Constrói o grafo LangGraph"""
        graph = StateGraph(KiwifyAPIMasterState)
        
        # Adicionar nós
        graph.add_node("agent", self._agent_node)
        
        # Definir fluxo
        graph.set_entry_point("agent")
        graph.add_edge("agent", END)
        
        return graph.compile()
    
    def _agent_node(self, state: KiwifyAPIMasterState) -> Dict[str, Any]:
        """Nó principal do agente"""
        messages = [SystemMessage(content=self.system_prompt)] + state["messages"]
        response = self.llm.invoke(messages)
        
        return {
            "messages": [response],
            "context": state.get("context", {})
        }
    
    def process(self, input_data: str, context: Dict[str, Any] = None) -> str:
        """Processa entrada usando o agente"""
        if context is None:
            context = {}
        
        initial_state = {
            "messages": [HumanMessage(content=input_data)],
            "context": context
        }
        
        result = self.graph.invoke(initial_state)
        return result["messages"][-1].content

# Instância global do controller
kiwifyapimaster_controller = KiwifyAPIMasterController()

def process_kiwifyapimaster(input_data: str, context: Dict[str, Any] = None) -> str:
    """Função de entrada para o agente KiwifyAPIMaster"""
    return kiwifyapimaster_controller.process(input_data, context)

if __name__ == "__main__":
    # Teste do controller
    test_input = "Olá, preciso de ajuda com apis"
    result = process_kiwifyapimaster(test_input)
    print(f"Resultado: {result}")
