#!/usr/bin/env python3
"""
LangGraph Controller for metaphor_architect
Auto-generated from prompt.txt by transform_to_langgraph.py
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from typing_extensions import TypedDict

class MetaphorArchitectState(TypedDict):
    """State schema for the agent workflow"""
    messages: List[BaseMessage]
    current_step: str
    agent_name: str
    decisions: Dict[str, Any]
    error_state: Optional[str]


def execute_decision_1(state: MetaphorArchitectState) -> MetaphorArchitectState:
    """Execute decision_1: meu sistema de criação de analogias que vendem, fo..."""
    try:
        # Process the decision logic
        current_messages = state.get("messages", [])
        
        # Add processing logic based on node type
        if "decision" == "decision":
            # Decision logic: meu sistema de criação de analogias que vendem, fo
            result_message = AIMessage(content=f"Processing decision: meu sistema de criação de anal")
        else:
            # Action logic: meu sistema de criação de analogias que vendem, fo
            result_message = AIMessage(content=f"Executing action: meu sistema de criação de anal")
        
        current_messages.append(result_message)
        
        return {
            **state,
            "messages": current_messages,
            "current_step": "decision_1",
            "decisions": {**state.get("decisions", {}), "decision_1": "completed"},
            "error_state": None
        }
    except Exception as e:
        return {
            **state,
            "error_state": f"Error in decision_1: {str(e)}"
        }

def execute_decision_2(state: MetaphorArchitectState) -> MetaphorArchitectState:
    """Execute decision_2: meu sistema de criação de analogias que VENDEM:..."""
    try:
        # Process the decision logic
        current_messages = state.get("messages", [])
        
        # Add processing logic based on node type
        if "decision" == "decision":
            # Decision logic: meu sistema de criação de analogias que VENDEM:
            result_message = AIMessage(content=f"Processing decision: meu sistema de criação de anal")
        else:
            # Action logic: meu sistema de criação de analogias que VENDEM:
            result_message = AIMessage(content=f"Executing action: meu sistema de criação de anal")
        
        current_messages.append(result_message)
        
        return {
            **state,
            "messages": current_messages,
            "current_step": "decision_2",
            "decisions": {**state.get("decisions", {}), "decision_2": "completed"},
            "error_state": None
        }
    except Exception as e:
        return {
            **state,
            "error_state": f"Error in decision_2: {str(e)}"
        }

# Create the StateGraph
workflow_graph = StateGraph(MetaphorArchitectState)

# Add nodes
workflow_graph.add_node("decision_1", execute_decision_1)
workflow_graph.add_node("decision_2", execute_decision_2)

# Add edges between nodes
workflow_graph.add_edge("decision_1", "decision_2")
workflow_graph.add_edge("decision_2", END)

# Set entry point
workflow_graph.set_entry_point("decision_1")

# Compile the graph
metaphor_architect_graph = workflow_graph.compile()

def run_metaphor_architect(messages: List[BaseMessage]) -> Dict[str, Any]:
    """Run the metaphor_architect workflow"""
    initial_state = {
        "messages": messages,
        "current_step": "decision_1",
        "agent_name": "metaphor_architect",
        "decisions": {},
        "error_state": None
    }
    
    final_state = metaphor_architect_graph.invoke(initial_state)
    return final_state

if __name__ == "__main__":
    # Test the controller
    from langchain_core.messages import HumanMessage
    
    test_messages = [HumanMessage(content="Test message for metaphor_architect")]
    result = run_metaphor_architect(test_messages)
    
    print(f"Workflow completed for metaphor_architect")
    print(f"Final step: {result.get('current_step')}")
    print(f"Messages count: {len(result.get('messages', []))}")
    
    if result.get('error_state'):
        print(f"Error: {result['error_state']}")
    else:
        print("Workflow completed successfully!")
