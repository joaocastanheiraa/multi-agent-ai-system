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
SYSTEM_MESSAGE = """You are metaphor_architect, a specialized AI agent.

Domain: copywriters
Specialization: metaphor_architect operations and management
Controller: metaphor_architect_controller.py

You are an expert in copywriters domain with deep knowledge of metaphor_architect workflows."""

def metaphor_architect_agent(state: MessagesState) -> Dict[str, Any]:
    """
    Agente: metaphor_architect
    Domínio: copywriters
    Especialização: metaphor_architect
    """
    messages = state["messages"]
    
    # Adicionar system message
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_MESSAGE)] + messages
    
    # Chamar o modelo
    response = llm.invoke(messages)
    
    return {"messages": [response]}

# Criação do grafo LangGraph
def create_metaphor_architect_graph():
    workflow = StateGraph(MessagesState)
    
    # Adicionar nó principal
    workflow.add_node("metaphor_architect", metaphor_architect_agent)
    
    # Definir entrada e saída
    workflow.set_entry_point("metaphor_architect")
    workflow.set_finish_point("metaphor_architect")
    
    return workflow.compile()

# Instanciar o grafo
metaphor_architect_graph = create_metaphor_architect_graph()

if __name__ == "__main__":
    # Teste do agente
    result = metaphor_architect_graph.invoke({
        "messages": [HumanMessage(content="Olá, preciso de ajuda com metaphor_architect")]
    })
    print(result)
