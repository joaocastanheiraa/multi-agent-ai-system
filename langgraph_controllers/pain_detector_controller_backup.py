#!/usr/bin/env python3
"""
LangGraph Controller for pain_detector
Auto-generated from prompt.txt by transform_to_langgraph.py
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from typing_extensions import TypedDict

class PainDetectorState(TypedDict):
    """State schema for the agent workflow"""
    messages: List[BaseMessage]
    current_step: str
    agent_name: str
    decisions: Dict[str, Any]
    error_state: Optional[str]


def execute_decision_1(state: PainDetectorState) -> PainDetectorState:
    """Execute decision_1: Quais são os sinais de frustração expressos explic..."""
    try:
        # Process the decision logic
        current_messages = state.get("messages", [])
        
        # Add processing logic based on node type
        if "decision" == "decision":
            # Decision logic: Quais são os sinais de frustração expressos explic
            result_message = AIMessage(content=f"Processing decision: Quais são os sinais de frustra")
        else:
            # Action logic: Quais são os sinais de frustração expressos explic
            result_message = AIMessage(content=f"Executing action: Quais são os sinais de frustra")
        
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

def execute_decision_2(state: PainDetectorState) -> PainDetectorState:
    """Execute decision_2: Quais padrões emocionais são recorrentes neste púb..."""
    try:
        # Process the decision logic
        current_messages = state.get("messages", [])
        
        # Add processing logic based on node type
        if "decision" == "decision":
            # Decision logic: Quais padrões emocionais são recorrentes neste púb
            result_message = AIMessage(content=f"Processing decision: Quais padrões emocionais são r")
        else:
            # Action logic: Quais padrões emocionais são recorrentes neste púb
            result_message = AIMessage(content=f"Executing action: Quais padrões emocionais são r")
        
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

def execute_decision_3(state: PainDetectorState) -> PainDetectorState:
    """Execute decision_3: Onde estão as contradições entre aspirações declar..."""
    try:
        # Process the decision logic
        current_messages = state.get("messages", [])
        
        # Add processing logic based on node type
        if "decision" == "decision":
            # Decision logic: Onde estão as contradições entre aspirações declar
            result_message = AIMessage(content=f"Processing decision: Onde estão as contradições ent")
        else:
            # Action logic: Onde estão as contradições entre aspirações declar
            result_message = AIMessage(content=f"Executing action: Onde estão as contradições ent")
        
        current_messages.append(result_message)
        
        return {
            **state,
            "messages": current_messages,
            "current_step": "decision_3",
            "decisions": {**state.get("decisions", {}), "decision_3": "completed"},
            "error_state": None
        }
    except Exception as e:
        return {
            **state,
            "error_state": f"Error in decision_3: {str(e)}"
        }

# Create the StateGraph
workflow_graph = StateGraph(PainDetectorState)

# Add nodes
workflow_graph.add_node("decision_1", execute_decision_1)
workflow_graph.add_node("decision_2", execute_decision_2)
workflow_graph.add_node("decision_3", execute_decision_3)

# Add edges between nodes
workflow_graph.add_edge("decision_1", "decision_2")
workflow_graph.add_edge("decision_2", "decision_3")
workflow_graph.add_edge("decision_3", END)

# Set entry point
workflow_graph.set_entry_point("decision_1")

# Compile the graph
pain_detector_graph = workflow_graph.compile()

def run_pain_detector(messages: List[BaseMessage]) -> Dict[str, Any]:
    """Run the pain_detector workflow"""
    initial_state = {
        "messages": messages,
        "current_step": "decision_1",
        "agent_name": "pain_detector",
        "decisions": {},
        "error_state": None
    }
    
    final_state = pain_detector_graph.invoke(initial_state)
    return final_state

if __name__ == "__main__":
    # Test the controller
    from langchain_core.messages import HumanMessage
    
    test_messages = [HumanMessage(content="Test message for pain_detector")]
    result = run_pain_detector(test_messages)
    
    print(f"Workflow completed for pain_detector")
    print(f"Final step: {result.get('current_step')}")
    print(f"Messages count: {len(result.get('messages', []))}")
    
    if result.get('error_state'):
        print(f"Error: {result['error_state']}")
    else:
        print("Workflow completed successfully!")
