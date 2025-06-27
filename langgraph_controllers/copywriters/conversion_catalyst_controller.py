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
SYSTEM_MESSAGE = """You are conversion_catalyst, a specialized AI agent.

Domain: copywriters
Specialization: conversion_catalyst operations and management
Controller: conversion_catalyst_controller.py

You are an expert in copywriters domain with deep knowledge of conversion_catalyst workflows."""

def conversion_catalyst_agent(state: MessagesState) -> Dict[str, Any]:
    """
    Agente: conversion_catalyst
    Domínio: copywriters
    Especialização: conversion_catalyst
    """
    messages = state["messages"]
    
    # Adicionar system message
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_MESSAGE)] + messages
    
    # Chamar o modelo
    response = llm.invoke(messages)
    
    return {"messages": [response]}

# Criação do grafo LangGraph
def create_conversion_catalyst_graph():
    workflow = StateGraph(MessagesState)
    
    # Adicionar nó principal
    workflow.add_node("conversion_catalyst", conversion_catalyst_agent)
    
    # Definir entrada e saída
    workflow.set_entry_point("conversion_catalyst")
    workflow.set_finish_point("conversion_catalyst")
    
    return workflow.compile()

# Instanciar o grafo
conversion_catalyst_graph = create_conversion_catalyst_graph()

if __name__ == "__main__":
    # Teste do agente
    result = conversion_catalyst_graph.invoke({
        "messages": [HumanMessage(content="Olá, preciso de ajuda com conversion_catalyst")]
    })
    print(result)
