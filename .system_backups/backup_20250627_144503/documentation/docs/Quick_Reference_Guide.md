# LangGraph Controller Converter - Quick Reference

## 🚀 Quick Start

### Generate Controllers
```bash
# Single agent
python scripts/transform_to_langgraph_clean.py --agent-dir domains/copywriters/agents/paradigm_architect

# Entire domain
python scripts/transform_to_langgraph_clean.py --domain copywriters

# All agents
python scripts/transform_to_langgraph_clean.py --all
```

### Use Generated Controller
```python
from domains.copywriters.agents.paradigm_architect.paradigm_architect_controller import (
    create_paradigm_architect_controller
)

# Initialize
controller = create_paradigm_architect_controller()

# Execute
initial_state = {
    "messages": [HumanMessage(content="Your input")],
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

result = controller.graph.invoke(initial_state)
```

## 📋 Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--agent-dir` | Process single agent | `--agent-dir domains/copywriters/agents/paradigm_architect` |
| `--domain` | Process all agents in domain | `--domain copywriters` |
| `--all` | Process all agents everywhere | `--all` |
| `--output-dir` | Custom output directory | `--output-dir ./controllers` |

## 🏗️ Generated Controller Structure

### State Schema
```python
class AgentState(TypedDict):
    messages: List[BaseMessage]           # Message history
    current_step: str                     # Current workflow step
    agent_name: str                       # Agent identifier
    analysis_results: Dict[str, Any]      # Analysis data
    decisions: Dict[str, Any]             # Decision history
    sub_agent_results: Dict[str, Any]     # Sub-agent outputs
    verification_status: Dict[str, bool]  # Verification flags
    output_data: Dict[str, Any]           # Final outputs
    metadata: Dict[str, Any]              # Additional data
    error_state: Optional[str]            # Error information
```

### Controller Class
```python
class AgentController:
    def __init__(self):
        self.agent_name = 'agent_name'
        self.graph = self._build_graph()
        
    def _build_graph(self) -> StateGraph:
        # Builds LangGraph StateGraph
        
    def _decision_1(self, state) -> state:
        # Individual node functions
```

## 🔧 Key Functions

### Core Classes
- `LogicFlowExtractor`: Extracts workflow from prompt.txt
- `LangGraphController`: Generates controller code
- `LogicNode`: Represents workflow nodes
- `AgentWorkflow`: Complete workflow structure

### Main Functions
- `process_agent(agent_dir, output_dir)`: Process single agent
- `main()`: CLI entry point with argument parsing

## 🎯 File Locations

### Input
- `domains/{domain}/agents/{agent}/prompt.txt` - Agent prompts

### Output
- `domains/{domain}/agents/{agent}/controllers/{agent}_controller.py` - Generated controller
- `domains/{domain}/agents/{agent}/{agent}_controller.py` - Backup copy

## ⚡ Quick Debugging

### Check Generated Controller
```python
# Test basic functionality
from generated_controller import create_agent_controller
controller = create_agent_controller()
print(f"Agent: {controller.agent_name}")
```

### Common Issues
1. **Import Error**: Ensure controller was generated successfully
2. **State Error**: Validate state dictionary structure
3. **Missing Fields**: Check all required state fields are present

### Error Recovery
```python
try:
    result = controller.graph.invoke(state)
    if result.get('error_state'):
        print(f"Workflow error: {result['error_state']}")
except Exception as e:
    print(f"Execution error: {e}")
```

## 📊 Monitoring Execution

### Basic Monitoring
```python
result = controller.graph.invoke(initial_state)

print(f"Final step: {result.get('current_step')}")
print(f"Decisions made: {len(result.get('decisions', {}))}")
print(f"Messages: {len(result.get('messages', []))}")
```

### Decision Trace
```python
for step, decision in result.get('decisions', {}).items():
    print(f"{step}: {decision.get('description', 'No description')}")
```

## 🔄 Multi-Agent Orchestration

### Sequential Execution
```python
# Agent 1
result1 = controller1.graph.invoke(initial_state)

# Agent 2 (using Agent 1 results)
state2 = {
    **initial_state,
    "messages": result1.get("messages", []),
    "sub_agent_results": {"agent1": result1.get("output_data", {})}
}
result2 = controller2.graph.invoke(state2)
```

## 📁 File Structure

```
scripts/
├── transform_to_langgraph_clean.py     # Main converter
├── LangGraph_Controller_Converter_README.md  # Full documentation
├── controller_usage_examples.py        # Usage examples
└── Quick_Reference_Guide.md            # This file

domains/{domain}/agents/{agent}/
├── prompt.txt                          # Input prompt
├── {agent}_controller.py              # Generated controller
└── controllers/
    └── {agent}_controller.py          # Organized storage
```

## 🛟 Help & Documentation

- **Full Documentation**: `LangGraph_Controller_Converter_README.md`
- **Usage Examples**: `controller_usage_examples.py`
- **CLI Help**: `python scripts/transform_to_langgraph_clean.py --help`

## 🔗 Dependencies

```bash
pip install langgraph langchain-core typing-extensions pandas
```

---
*For complete documentation and examples, see the full README and usage examples files.* 