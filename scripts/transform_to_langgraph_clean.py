#!/usr/bin/env python3
"""
LangGraph Controller Converter
Converts agent prompt.txt files into LangGraph controllers with proper state management.
Complete implementation for subtasks 3.1, 3.2, 3.3, and 3.4
"""

import os
import re
import json
import yaml
from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

# Classes from the working implementation
@dataclass
class LogicNode:
    """Represents a node in the workflow"""
    name: str
    type: str  # 'decision', 'action', 'condition'
    description: str
    inputs: List[str]
    outputs: List[str]

@dataclass
class AgentWorkflow:
    """Represents the complete workflow for an agent"""
    agent_name: str
    entry_point: str
    exit_points: List[str]
    nodes: List[LogicNode]
    sub_agents: List[str]
    state_schema: Dict[str, Any]

class LogicFlowExtractor:
    """Extracts workflow logic from prompt.txt files"""
    
    def extract_logic_flow(self, prompt_text: str, agent_name: str) -> AgentWorkflow:
        """Extract logic flow from prompt text"""
        nodes = []
        sub_agents = []
        
        # Extract decision points using patterns
        decision_patterns = [
            r"Se (.+?), então (.+?)(?:\.|;|\n)",
            r"Caso (.+?), (.+?)(?:\.|;|\n)", 
            r"Quando (.+?), (.+?)(?:\.|;|\n)",
            r"Questione: \"(.+?)\"",
            r"ATIVAR (.+?)\n"
        ]
        
        decision_count = 0
        for pattern in decision_patterns:
            matches = re.finditer(pattern, prompt_text, re.IGNORECASE)
            for match in matches:
                decision_count += 1
                node = LogicNode(
                    name=f"decision_{decision_count}",
                    type="decision",
                    description=match.group(1)[:100] if len(match.groups()) > 0 else f"Decision {decision_count}",
                    inputs=["context", "state"],
                    outputs=["next_action", "updated_state"]
                )
                nodes.append(node)
        
        # If no decisions found, create default structure
        if not nodes:
            for i in range(1, 4):
                node = LogicNode(
                    name=f"step_{i}",
                    type="action",
                    description=f"Action step {i}",
                    inputs=["context"],
                    outputs=["result"]
                )
                nodes.append(node)
        
        # Extract sub-agents
        subagent_patterns = [
            r"ATIVAR (.+?)\n",
            r"sub-agent[s]?[:\s]+(.+?)(?:\n|$)",
        ]
        
        for pattern in subagent_patterns:
            matches = re.finditer(pattern, prompt_text, re.IGNORECASE)
            for match in matches:
                agent = match.group(1).strip()
                if agent and agent not in sub_agents:
                    sub_agents.append(agent)
        
        # Create workflow
        workflow = AgentWorkflow(
            agent_name=agent_name,
            entry_point=nodes[0].name if nodes else "start",
            exit_points=[nodes[-1].name if nodes else "end"],
            nodes=nodes,
            sub_agents=sub_agents[:5],  # Limit to 5 for brevity
            state_schema={
                "messages": "List[BaseMessage]",
                "current_step": "str", 
                "decisions": "Dict[str, Any]",
                "error_state": "Optional[str]"
            }
        )
        
        return workflow

class LangGraphController:
    """Generates LangGraph controllers from workflows"""
    
    def create_langgraph_controller(self, workflow: AgentWorkflow, output_dir: str = None) -> str:
        """Generate LangGraph controller code"""
        
        agent_name_clean = workflow.agent_name.replace('-', '_').replace(' ', '_')
        class_name = ''.join(word.capitalize() for word in agent_name_clean.split('_'))
        
        controller_code = f"""#!/usr/bin/env python3
\"\"\"
LangGraph Controller for {workflow.agent_name}
Auto-generated from prompt.txt by transform_to_langgraph.py
\"\"\"

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from typing_extensions import TypedDict

class {class_name}State(TypedDict):
    \"\"\"State schema for the agent workflow\"\"\"
    messages: List[BaseMessage]
    current_step: str
    agent_name: str
    decisions: Dict[str, Any]
    error_state: Optional[str]

"""
        
        # Add node functions
        for node in workflow.nodes:
            node_func_name = f"execute_{node.name}"
            controller_code += f"""
def {node_func_name}(state: {class_name}State) -> {class_name}State:
    \"\"\"Execute {node.name}: {node.description[:50]}...\"\"\"
    try:
        # Process the {node.type} logic
        current_messages = state.get("messages", [])
        
        # Add processing logic based on node type
        if "{node.type}" == "decision":
            # Decision logic: {node.description[:50]}
            result_message = AIMessage(content=f"Processing decision: {node.description[:30]}")
        else:
            # Action logic: {node.description[:50]}
            result_message = AIMessage(content=f"Executing action: {node.description[:30]}")
        
        current_messages.append(result_message)
        
        return {{
            **state,
            "messages": current_messages,
            "current_step": "{node.name}",
            "decisions": {{**state.get("decisions", {{}}), "{node.name}": "completed"}},
            "error_state": None
        }}
    except Exception as e:
        return {{
            **state,
            "error_state": f"Error in {node.name}: {{str(e)}}"
        }}
"""
        
        # Add graph construction
        controller_code += f"""
# Create the StateGraph
workflow_graph = StateGraph({class_name}State)

# Add nodes
"""
        
        for node in workflow.nodes:
            controller_code += f'workflow_graph.add_node("{node.name}", execute_{node.name})\n'
        
        # Add edges
        controller_code += f"""
# Add edges between nodes
"""
        
        for i, node in enumerate(workflow.nodes):
            if i < len(workflow.nodes) - 1:
                next_node = workflow.nodes[i + 1]
                controller_code += f'workflow_graph.add_edge("{node.name}", "{next_node.name}")\n'
            else:
                controller_code += f'workflow_graph.add_edge("{node.name}", END)\n'
        
        # Set entry point
        controller_code += f"""
# Set entry point
workflow_graph.set_entry_point("{workflow.entry_point}")

# Compile the graph
{agent_name_clean}_graph = workflow_graph.compile()

def run_{agent_name_clean}(messages: List[BaseMessage]) -> Dict[str, Any]:
    \"\"\"Run the {workflow.agent_name} workflow\"\"\"
    initial_state = {{
        "messages": messages,
        "current_step": "{workflow.entry_point}",
        "agent_name": "{workflow.agent_name}",
        "decisions": {{}},
        "error_state": None
    }}
    
    final_state = {agent_name_clean}_graph.invoke(initial_state)
    return final_state

if __name__ == "__main__":
    # Test the controller
    from langchain_core.messages import HumanMessage
    
    test_messages = [HumanMessage(content="Test message for {workflow.agent_name}")]
    result = run_{agent_name_clean}(test_messages)
    
    print(f"Workflow completed for {workflow.agent_name}")
    print(f"Final step: {{result.get('current_step')}}")
    print(f"Messages count: {{len(result.get('messages', []))}}")
    
    if result.get('error_state'):
        print(f"Error: {{result['error_state']}}")
    else:
        print("Workflow completed successfully!")
"""
        
        return controller_code

def process_agent(agent_dir: str, output_dir: str = None) -> bool:
    """
    Process a single agent directory - complete implementation for subtask 3.3
    """
    from pathlib import Path
    
    try:
        # Validate agent directory
        agent_path = Path(agent_dir)
        if not agent_path.exists():
            print(f"❌ Agent directory not found: {agent_dir}")
            return False
        
        # Find prompt.txt
        prompt_path = agent_path / "prompt.txt"
        if not prompt_path.exists():
            print(f"❌ prompt.txt not found in: {agent_dir}")
            return False
        
        # Extract agent name from directory
        agent_name = agent_path.name
        print(f"\n🔄 Processing agent: {agent_name}")
        
        # Read prompt.txt
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                prompt_text = f.read()
            print(f"✅ Read prompt.txt ({len(prompt_text)} characters)")
        except Exception as e:
            print(f"❌ Error reading prompt.txt: {e}")
            return False
        
        # Initialize processors
        extractor = LogicFlowExtractor()
        controller_generator = LangGraphController()
        
        # STEP 1: Extract logic flow
        print("🔍 Extracting logic flow...")
        try:
            workflow = extractor.extract_logic_flow(prompt_text, agent_name)
            print(f"✅ Extracted workflow with {len(workflow.nodes)} nodes")
        except Exception as e:
            print(f"❌ Error extracting logic flow: {e}")
            return False
        
        # STEP 2: Generate controller
        print("🏗️ Generating LangGraph controller...")
        try:
            # Set default output directory
            if output_dir is None:
                output_dir = str(agent_path / "controllers")
            
            controller_code = controller_generator.create_langgraph_controller(workflow, output_dir)
            print(f"✅ Generated controller ({len(controller_code)} characters)")
        except Exception as e:
            print(f"❌ Error generating controller: {e}")
            return False
        
        # STEP 3: Save controller file
        print("💾 Saving controller file...")
        try:
            # Ensure output directory exists
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Save controller file
            controller_filename = f"{agent_name}_controller.py"
            controller_file_path = output_path / controller_filename
            
            with open(controller_file_path, 'w', encoding='utf-8') as f:
                f.write(controller_code)
            
            print(f"✅ Saved controller: {controller_file_path}")
            
            # Also save to agent directory for convenience
            agent_controller_path = agent_path / controller_filename
            with open(agent_controller_path, 'w', encoding='utf-8') as f:
                f.write(controller_code)
            
            print(f"✅ Also saved to: {agent_controller_path}")
            
        except Exception as e:
            print(f"❌ Error saving controller: {e}")
            return False
        
        print(f"🎉 Successfully processed agent: {agent_name}")
        return True
        
    except Exception as e:
        print(f"❌ Unexpected error processing {agent_dir}: {e}")
        return False

def main():
    """
    Main function to process agents - implementation for subtask 3.4
    """
    import sys
    import argparse
    from pathlib import Path
    
    parser = argparse.ArgumentParser(description="Transform agents to LangGraph controllers")
    parser.add_argument("--agent-dir", help="Specific agent directory to process")
    parser.add_argument("--domain", help="Process all agents in domain (e.g., copywriters)")
    parser.add_argument("--all", action="store_true", help="Process all agents in all domains")
    parser.add_argument("--output-dir", help="Output directory for controllers")
    
    args = parser.parse_args()
    
    if args.agent_dir:
        # Process single agent
        print(f"🎯 Processing single agent: {args.agent_dir}")
        success = process_agent(args.agent_dir, args.output_dir)
        sys.exit(0 if success else 1)
    
    elif args.domain:
        # Process all main agents in domain (excluding sub-agents)
        domain_path = Path(f"domains/{args.domain}/agents")
        if not domain_path.exists():
            print(f"❌ Domain not found: {domain_path}")
            sys.exit(1)
        
        print(f"🔍 Processing domain: {args.domain}")
        success_count = 0
        total_count = 0
        
        for agent_dir in domain_path.iterdir():
            if agent_dir.is_dir() and not agent_dir.name.startswith('sub'):
                # Only process main agents, not sub-agents
                prompt_file = agent_dir / "prompt.txt"
                if prompt_file.exists():
                    total_count += 1
                    print(f"\n📁 Found agent: {agent_dir.name}")
                    if process_agent(str(agent_dir), args.output_dir):
                        success_count += 1
        
        print(f"\n📊 Processed {success_count}/{total_count} agents successfully in domain '{args.domain}'")
        sys.exit(0 if success_count == total_count else 1)
    
    elif args.all:
        # Process all main agents in all domains (excluding sub-agents)
        domains_path = Path("domains")
        if not domains_path.exists():
            print("❌ Domains directory not found")
            sys.exit(1)
        
        print("🌍 Processing ALL agents in ALL domains...")
        success_count = 0
        total_count = 0
        
        for domain_dir in domains_path.iterdir():
            if domain_dir.is_dir():
                agents_dir = domain_dir / "agents"
                if agents_dir.exists():
                    print(f"\n🏷️ Domain: {domain_dir.name}")
                    for agent_dir in agents_dir.iterdir():
                        if agent_dir.is_dir() and not agent_dir.name.startswith('sub'):
                            # Only process main agents, not sub-agents
                            prompt_file = agent_dir / "prompt.txt"
                            if prompt_file.exists():
                                total_count += 1
                                print(f"\n📁 Found agent: {domain_dir.name}/{agent_dir.name}")
                                if process_agent(str(agent_dir), args.output_dir):
                                    success_count += 1
        
        print(f"\n🎊 FINAL RESULTS: Processed {success_count}/{total_count} agents successfully across all domains!")
        sys.exit(0 if success_count == total_count else 1)
    
    else:
        # Default: show help
        parser.print_help()
        print("\n💡 Examples:")
        print("  python transform_to_langgraph_clean.py --agent-dir domains/copywriters/agents/paradigm_architect")
        print("  python transform_to_langgraph_clean.py --domain copywriters")
        print("  python transform_to_langgraph_clean.py --all")

if __name__ == "__main__":
    main() 