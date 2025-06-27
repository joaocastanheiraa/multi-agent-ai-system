#!/usr/bin/env python3
"""
🎯 PERFECTPAYAPIMASTER - CONTROLLER LANGGRAPH
Gerado automaticamente pelo sistema Multi-Agent AI
"""

from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated

class PerfectpayAPIMasterState(TypedDict):
    """Estado do agente PerfectpayAPIMaster"""
    messages: Annotated[list, add_messages]
    context: Dict[str, Any]

class PerfectpayAPIMasterController:
    """Controller LangGraph para PerfectpayAPIMaster"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            max_tokens=4000
        )
        self.system_prompt = """You are PerfectpayAPIMaster, a specialized AI agent.

Domain: apis
Specialization: PerfectpayAPIMaster operations and management
Controller: PerfectpayAPIMaster_controller.py

You are an expert in apis domain with deep knowledge of PerfectpayAPIMaster workflows.


## FERRAMENTAS DISPONÍVEIS
Você tem acesso às seguintes ferramentas especializadas:
- **api_client**: Tool api_client para PerfectpayAPIMaster (✅ ATIVA)
- **json_parser**: Tool json_parser para PerfectpayAPIMaster (✅ ATIVA)
- **webhook_handler**: Tool webhook_handler para PerfectpayAPIMaster (✅ ATIVA)


## SUB-AGENTES ESPECIALIZADOS
Você coordena os seguintes sub-agentes especializados:
- **1 copy 3**: Sub-agente especializado
- **1 copy 4**: Sub-agente especializado
- **1 copy 2**: Sub-agente especializado
- **1**: Sub-agente especializado
- **1 copy**: Sub-agente especializado


## INFORMAÇÕES DO SISTEMA
- Agente: PerfectpayAPIMaster
- Domínio: apis
- Ferramentas: 3
- Sub-agentes: 5
- Atualizado automaticamente com configurações reais"""
        
        # Configurar grafo
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Constrói o grafo LangGraph"""
        graph = StateGraph(PerfectpayAPIMasterState)
        
        # Adicionar nós
        graph.add_node("agent", self._agent_node)
        
        # Definir fluxo
        graph.set_entry_point("agent")
        graph.add_edge("agent", END)
        
        return graph.compile()
    
    def _agent_node(self, state: PerfectpayAPIMasterState) -> Dict[str, Any]:
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
perfectpayapimaster_controller = PerfectpayAPIMasterController()

def process_perfectpayapimaster(input_data: str, context: Dict[str, Any] = None) -> str:
    """Função de entrada para o agente PerfectpayAPIMaster"""
    return perfectpayapimaster_controller.process(input_data, context)

if __name__ == "__main__":
    # Teste do controller
    test_input = "Olá, preciso de ajuda com apis"
    result = process_perfectpayapimaster(test_input)
    print(f"Resultado: {result}")
