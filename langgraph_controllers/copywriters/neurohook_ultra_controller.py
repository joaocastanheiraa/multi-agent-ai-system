#!/usr/bin/env python3
from typing import Dict, Any, List, Optional
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState

# Configuração do modelo
llm = ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0.1,
    max_tokens=4000
)

# System message do agente
SYSTEM_MESSAGE = """You are neurohook_ultra, a specialized AI agent.

Domain: copywriters
Specialization: neurohook_ultra operations and management
Controller: neurohook_ultra_controller.py

You are an expert in copywriters domain with deep knowledge of neurohook_ultra workflows."""

def neurohook_ultra_agent(state: MessagesState) -> Dict[str, Any]:
    """
    Agente: neurohook_ultra
    Domínio: copywriters
    Especialização: neurohook_ultra
    """
    messages = state["messages"]
    
    # Adicionar system message
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_MESSAGE)] + messages
    
    # Chamar o modelo
    response = llm.invoke(messages)
    
    return {"messages": [response]}

# Criação do grafo LangGraph
def create_neurohook_ultra_graph():
    workflow = StateGraph(MessagesState)
    
    # Adicionar nó principal
    workflow.add_node("neurohook_ultra", neurohook_ultra_agent)
    
    # Definir entrada e saída
    workflow.set_entry_point("neurohook_ultra")
    workflow.set_finish_point("neurohook_ultra")
    
    return workflow.compile()

# Instanciar o grafo
neurohook_ultra_graph = create_neurohook_ultra_graph()

if __name__ == "__main__":
    # Teste do agente
    result = neurohook_ultra_graph.invoke({
        "messages": [HumanMessage(content="Olá, preciso de ajuda com neurohook_ultra")]
    })
    print(result)
