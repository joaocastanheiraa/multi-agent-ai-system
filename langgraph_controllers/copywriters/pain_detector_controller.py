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
SYSTEM_MESSAGE = """You are pain_detector, a specialized AI agent.

Domain: copywriters
Specialization: pain_detector operations and management
Controller: pain_detector_controller.py

You are an expert in copywriters domain with deep knowledge of pain_detector workflows."""

def pain_detector_agent(state: MessagesState) -> Dict[str, Any]:
    """
    Agente: pain_detector
    Domínio: copywriters
    Especialização: pain_detector
    """
    messages = state["messages"]
    
    # Adicionar system message
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_MESSAGE)] + messages
    
    # Chamar o modelo
    response = llm.invoke(messages)
    
    return {"messages": [response]}

# Criação do grafo LangGraph
def create_pain_detector_graph():
    workflow = StateGraph(MessagesState)
    
    # Adicionar nó principal
    workflow.add_node("pain_detector", pain_detector_agent)
    
    # Definir entrada e saída
    workflow.set_entry_point("pain_detector")
    workflow.set_finish_point("pain_detector")
    
    return workflow.compile()

# Instanciar o grafo
pain_detector_graph = create_pain_detector_graph()

if __name__ == "__main__":
    # Teste do agente
    result = pain_detector_graph.invoke({
        "messages": [HumanMessage(content="Olá, preciso de ajuda com pain_detector")]
    })
    print(result)
