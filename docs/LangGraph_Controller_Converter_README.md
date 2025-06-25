# LangGraph Controller Converter

## Overview

The **LangGraph Controller Converter** is an advanced tool that automatically transforms agent prompt.txt files into fully functional LangGraph controllers with proper state management. This system enables seamless integration of conversational AI agents into LangGraph workflows, providing structured state handling, decision logic, and orchestrated sub-agent execution.

## 🚀 Features

- **Automatic Workflow Extraction**: Analyzes prompt.txt files to identify decision points, actions, and logic flows
- **LangGraph Integration**: Generates complete StateGraph implementations with proper node connections
- **State Management**: Creates TypedDict schemas for robust state handling throughout the workflow
- **Batch Processing**: Supports processing single agents, entire domains, or the complete repository
- **Error Handling**: Comprehensive error management and logging throughout the conversion process
- **Quality Controllers**: Generates professional-grade controller code with proper imports and documentation

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- LangGraph library
- LangChain Core

### Install Dependencies
```bash
pip install langgraph langchain-core typing-extensions pandas
```

## 📖 Usage

### Command Line Interface

The script provides multiple options for processing agents:

#### Process a Single Agent
```bash
python scripts/transform_to_langgraph_clean.py --agent-dir domains/copywriters/agents/paradigm_architect
```

#### Process All Agents in a Domain
```bash
python scripts/transform_to_langgraph_clean.py --domain copywriters
```

#### Process All Agents in All Domains
```bash
python scripts/transform_to_langgraph_clean.py --all
```

#### Custom Output Directory
```bash
python scripts/transform_to_langgraph_clean.py --domain apis --output-dir ./custom_controllers
```

### Python Integration

```python
from scripts.transform_to_langgraph_clean import LogicFlowExtractor, LangGraphController, process_agent

# Process a single agent programmatically
success = process_agent(
    agent_dir="domains/copywriters/agents/paradigm_architect",
    output_dir="./controllers"
)

# Initialize the components directly
extractor = LogicFlowExtractor()
controller_generator = LangGraphController()

# Extract workflow from prompt text
workflow = extractor.extract_logic_flow(prompt_text, agent_name)

# Generate controller code
controller_code = controller_generator.create_langgraph_controller(workflow)
```

## 🏗️ Generated Controller Structure

### State Schema
Each generated controller includes a comprehensive state schema:

```python
class AgentNameState(TypedDict):
    """State schema for the agent workflow"""
    messages: List[BaseMessage]
    current_step: str
    agent_name: str
    analysis_results: Dict[str, Any]
    decisions: Dict[str, Any]
    sub_agent_results: Dict[str, Any]
    verification_status: Dict[str, bool]
    output_data: Dict[str, Any]
    metadata: Dict[str, Any]
    error_state: Optional[str]
```

### Node Functions
Decision and action nodes are automatically generated:

```python
def _decision_1(self, state: AgentState) -> AgentState:
    """Execute decision logic with error handling"""
    try:
        # Decision evaluation logic
        decision_result = {
            "step": "decision_1",
            "description": "...",
            "decision": "proceed",
            "reasoning": "...",
            "timestamp": str(pd.Timestamp.now())
        }
        
        state["current_step"] = "decision_1"
        state["decisions"]["decision_1"] = decision_result
        return state
        
    except Exception as e:
        state["error_state"] = f"Error in decision_1: {str(e)}"
        return state
```

### Graph Construction
Complete StateGraph setup with nodes and edges:

```python
def _build_graph(self) -> StateGraph:
    """Build the LangGraph workflow"""
    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node('decision_1', self._decision_1)
    graph.add_node('action_1', self._action_1)
    
    # Add edges
    graph.add_edge("decision_1", "action_1")
    graph.add_edge("action_1", END)
    
    # Set entry point
    graph.set_entry_point('decision_1')
    
    return graph.compile()
```

## 🎯 Usage Examples

### Example 1: Using a Generated Controller

```python
from domains.copywriters.agents.paradigm_architect.paradigm_architect_controller import ParadigmArchitectController
from langchain_core.messages import HumanMessage

# Initialize the controller
controller = ParadigmArchitectController()

# Create initial state
initial_state = {
    "messages": [HumanMessage(content="Analyze this marketing campaign")],
    "current_step": "start",
    "agent_name": "paradigm_architect",
    "analysis_results": {},
    "decisions": {},
    "sub_agent_results": {},
    "verification_status": {},
    "output_data": {},
    "metadata": {},
    "error_state": None
}

# Execute the workflow
result = controller.graph.invoke(initial_state)

# Check results
print(f"Final step: {result.get('current_step')}")
print(f"Messages: {len(result.get('messages', []))}")
if result.get('error_state'):
    print(f"Error: {result['error_state']}")
```

### Example 2: Batch Processing Results

```python
import os
from pathlib import Path

def process_domain_agents(domain_name: str):
    """Process all agents in a domain and return results"""
    domain_path = Path(f"domains/{domain_name}/agents")
    results = {}
    
    for agent_dir in domain_path.iterdir():
        if agent_dir.is_dir() and (agent_dir / "prompt.txt").exists():
            success = process_agent(str(agent_dir))
            results[agent_dir.name] = success
    
    return results

# Process copywriters domain
results = process_domain_agents("copywriters")
print(f"Processed {sum(results.values())}/{len(results)} agents successfully")
```

### Example 3: Custom Workflow Integration

```python
from langgraph.graph import StateGraph, END
from generated_controller import AgentController

# Integrate with existing workflow
def create_multi_agent_workflow():
    """Create a multi-agent workflow using generated controllers"""
    
    # Initialize multiple controllers
    paradigm_controller = ParadigmArchitectController()
    pain_controller = PainDetectorController()
    
    # Create master workflow
    master_graph = StateGraph(MasterState)
    
    # Add agent nodes
    master_graph.add_node("paradigm_analysis", paradigm_controller.graph)
    master_graph.add_node("pain_detection", pain_controller.graph)
    
    # Connect agents
    master_graph.add_edge("paradigm_analysis", "pain_detection")
    master_graph.add_edge("pain_detection", END)
    
    master_graph.set_entry_point("paradigm_analysis")
    
    return master_graph.compile()
```

## 🔧 Architecture Details

### Logic Flow Extraction

The system uses sophisticated pattern matching to extract workflow elements:

1. **Decision Points**: Identifies conditional logic using patterns like "Se..., então...", "Caso...", "Quando..."
2. **Action Sequences**: Extracts procedural steps and operations
3. **Sub-Agent References**: Locates mentions of sub-agents and orchestration points
4. **State Dependencies**: Maps data flow between workflow steps

### Controller Generation

1. **Class Structure**: Creates controller classes with proper inheritance
2. **State Management**: Implements TypedDict schemas for type safety
3. **Node Functions**: Generates executable functions for each workflow step
4. **Graph Assembly**: Constructs LangGraph StateGraph with proper connections
5. **Error Handling**: Adds comprehensive try-catch blocks throughout

### File Organization

Generated controllers are saved in two locations:
- `{agent_directory}/controllers/` - Organized controller storage
- `{agent_directory}/` - Direct access within agent folder

## ⚡ Performance Considerations

- **Parallel Processing**: Domain and full repository processing runs agents in sequence with detailed progress reporting
- **Memory Management**: State schemas are designed for efficient memory usage
- **Error Recovery**: Individual agent failures don't stop batch processing
- **Logging**: Comprehensive logging for debugging and monitoring

## 🛡️ Error Handling

The system includes multiple layers of error handling:

1. **File System Errors**: Missing directories, unreadable files
2. **Parsing Errors**: Invalid prompt formats, extraction failures  
3. **Generation Errors**: Code generation issues, template problems
4. **Runtime Errors**: State management errors, execution failures

## 📊 Output Examples

### Successful Processing Output
```
🎯 Processing single agent: domains/copywriters/agents/paradigm_architect

🔄 Processing agent: paradigm_architect
✅ Read prompt.txt (9200 characters)
🔍 Extracting logic flow...
✅ Extracted workflow with 6 nodes
🏗️ Generating LangGraph controller...
✅ Generated controller (9014 characters)
💾 Saving controller file...
✅ Saved controller: domains/copywriters/agents/paradigm_architect/controllers/paradigm_architect_controller.py
✅ Also saved to: domains/copywriters/agents/paradigm_architect/paradigm_architect_controller.py
🎉 Successfully processed agent: paradigm_architect
```

### Batch Processing Summary
```
📊 Processed 6/6 agents successfully in domain 'copywriters'
🎊 FINAL RESULTS: Processed 15/18 agents successfully across all domains!
```

## 🤝 Contributing

To contribute to the LangGraph Controller Converter:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## 📝 License

This project is part of the Multi-Agent AI System and follows the same licensing terms.

## 🔗 Related Documentation

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [LangChain Core Reference](https://python.langchain.com/docs/langchain_core)
- [Multi-Agent System Architecture](../docs/architecture.md)

---

**Note**: This tool is designed specifically for the Multi-Agent AI System architecture and may require adaptation for other use cases. 