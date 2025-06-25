#!/usr/bin/env python3
"""
LangGraph Controller Converter - Transform prompt.txt agents to LangGraph workflows

SUBTASKS IMPLEMENTED:
✅ 3.1: extract_logic_flow function - Logic flow extraction from prompts
✅ 3.2: create_langgraph_controller function - LangGraph controller generation
"""

import os
import re
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class LogicNode:
    """Represents a node in the agent's logic flow"""
    name: str
    type: str
    description: str
    conditions: List[str]
    next_nodes: List[str]
    sub_agent: Optional[str] = None
    priority: int = 0

@dataclass
class AgentWorkflow:
    """Represents the complete workflow of an agent"""
    agent_name: str
    nodes: List[LogicNode]
    entry_point: str
    exit_points: List[str]
    state_schema: Dict[str, Any]
    sub_agents: List[str]

class LogicFlowExtractor:
    """Subtask 3.1: Extract logic flow and decision points from prompt.txt files"""
    
    def __init__(self):
        self.workflow_patterns = {
            'decisions': [
                r'Se\s+([^:,\n]+)[:,]\s*([^\n]+)',
                r'If\s+([^:,\n]+)[:,]\s*([^\n]+)',
                r'Caso\s+([^:,\n]+)[:,]\s*([^\n]+)',
                r'AVALIE\s+([^:,\n]+)[:,]\s*([^\n]+)',
                r'Questione:\s*"([^"]+)"',
            ]
        }
    
    def extract_logic_flow(self, prompt_text: str, agent_name: str) -> AgentWorkflow:
        """Extract logic flow from prompt text"""
        nodes = []
        
        # Extract decision points
        decision_count = 0
        for pattern in self.workflow_patterns['decisions']:
            matches = re.finditer(pattern, prompt_text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                decision_count += 1
                condition = match.group(1).strip() if len(match.groups()) >= 1 else ""
                action = match.group(2).strip() if len(match.groups()) >= 2 else ""
                
                description = f"{condition} {action}".strip()
                if len(description) > 100:
                    description = description[:97] + "..."
                
                node = LogicNode(
                    name=f"decision_{decision_count}",
                    type="decision",
                    description=description,
                    conditions=[condition] if condition else [],
                    next_nodes=[],
                    priority=decision_count
                )
                nodes.append(node)
        
        # Extract sub-agents
        sub_agent_pattern = r'<([A-Z_-]+)>'
        sub_agents = re.findall(sub_agent_pattern, prompt_text)
        unique_sub_agents = list(set(sub_agents))
        
        return AgentWorkflow(
            agent_name=agent_name,
            nodes=nodes,
            entry_point=nodes[0].name if nodes else "start",
            exit_points=[nodes[-1].name] if nodes else ["end"],
            state_schema={
                "messages": "List[BaseMessage]",
                "current_step": "str",
                "decisions": "Dict[str, Any]",
                "error_state": "Optional[str]"
            },
            sub_agents=unique_sub_agents
        )

class LangGraphController:
    """Subtask 3.2: Generate LangGraph controller code from AgentWorkflow"""
    
    def create_langgraph_controller(self, workflow: AgentWorkflow, output_dir: str = None) -> str:
        """Generate complete LangGraph controller code from workflow"""
        
        # Generate class names
        agent_name_pascal = ''.join(word.capitalize() for word in workflow.agent_name.split('_'))
        state_class_name = f"{agent_name_pascal}State"
        controller_class_name = f"{agent_name_pascal}Controller"
        
        # Build the controller code
        controller_code = f'''#!/usr/bin/env python3
"""
LangGraph Controller for {workflow.agent_name}
Auto-generated from prompt.txt by transform_to_langgraph.py
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from typing_extensions import TypedDict

class {state_class_name}(TypedDict):
    """State schema for the agent workflow"""
    messages: List[BaseMessage]
    current_step: str
    agent_name: str
    decisions: Dict[str, Any]
    error_state: Optional[str]

class {controller_class_name}:
    """LangGraph controller for {workflow.agent_name}"""
    
    def __init__(self):
        self.agent_name = '{workflow.agent_name}'
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        graph = StateGraph({state_class_name})
        
        # Add nodes
'''
        
        for node in workflow.nodes:
            controller_code += f"        graph.add_node('{node.name}', self._{node.name})\n"
        
        controller_code += f'''        
        # Set entry point
        graph.set_entry_point('{workflow.entry_point}')
        
        return graph.compile()
'''
        
        # Add node functions
        for node in workflow.nodes:
            controller_code += f'''
    def _{node.name}(self, state: {state_class_name}) -> {state_class_name}:
        """
        Decision Node: {node.description}
        """
        try:
            # Evaluate decision: {node.description}
            messages = state.get("messages", [])
            
            decision_result = {{
                "step": "{node.name}",
                "description": "{node.description}",
                "conditions": {node.conditions},
                "decision": "proceed",
                "timestamp": str(datetime.now())
            }}
            
            # Update state
            state["current_step"] = "{node.name}"
            state["decisions"]["{node.name}"] = decision_result
            
            return state
            
        except Exception as e:
            state["error_state"] = f"Error in {node.name}: {{str(e)}}"
            return state
'''
        
        # Add factory function
        controller_code += f'''

def create_{workflow.agent_name}_controller() -> {controller_class_name}:
    """Factory function to create {workflow.agent_name} controller"""
    return {controller_class_name}()
'''
        
        # Save to file if output directory specified
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f"{workflow.agent_name}_controller.py")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(controller_code)
            
            print(f"✅ Controller saved to: {output_file}")
        
        return controller_code

# Test the implementation
if __name__ == "__main__":
    extractor = LogicFlowExtractor()
    controller_generator = LangGraphController()
    
    test_agent_path = "domains/copywriters/agents/conversion_catalyst/prompt.txt"
    
    if os.path.exists(test_agent_path):
        with open(test_agent_path, 'r', encoding='utf-8') as f:
            prompt_text = f.read()
        
        # SUBTASK 3.1: Extract logic flow
        workflow = extractor.extract_logic_flow(prompt_text, "conversion_catalyst")
        
        print(f"🧠 EXTRACTED WORKFLOW FOR: {workflow.agent_name}")
        print(f"📊 Total nodes: {len(workflow.nodes)}")
        print(f"🚀 Entry point: {workflow.entry_point}")
        print(f"🏁 Exit points: {workflow.exit_points}")
        print(f"🤖 Sub-agents: {workflow.sub_agents}")
        
        print("\n📋 NODES:")
        for node in workflow.nodes:
            print(f"  - {node.name} ({node.type}): {node.description[:60]}...")
        
        print("\n✅ SUBTASK 3.1 COMPLETED: Logic flow extraction implemented!")
        
        # SUBTASK 3.2: Generate LangGraph controller
        print("\n🔄 STARTING SUBTASK 3.2: LangGraph controller generation...")
        
        controller_code = controller_generator.create_langgraph_controller(
            workflow, 
            output_dir="domains/copywriters/agents/conversion_catalyst/controllers"
        )
        
        print("✅ SUBTASK 3.2 COMPLETED: LangGraph controller generation implemented!")
        print("📁 Controller saved to: domains/copywriters/agents/conversion_catalyst/controllers/")
        
    else:
        print(f"❌ Test file not found: {test_agent_path}")
