#!/usr/bin/env python3
"""
FASE E: MCP Integration Setup
Integra todos os agentes (LangGraph + AutoGen) com protocolo MCP
"""

import os
import json
from datetime import datetime

def main():
    """Função principal para setup MCP"""
    print("�� FASE E: MCP INTEGRATION SETUP")
    print("=" * 60)
    
    # Descobrir controllers LangGraph
    print("🔍 Descobrindo controllers LangGraph...")
    controllers = []
    controllers_dir = "langgraph_controllers"
    
    if os.path.exists(controllers_dir):
        for file in os.listdir(controllers_dir):
            if file.endswith('_controller.py'):
                controller_name = file.replace('_controller.py', '')
                controllers.append({
                    'name': controller_name,
                    'type': 'langgraph',
                    'file': os.path.join(controllers_dir, file),
                    'endpoint': f"/langgraph/{controller_name}"
                })
    
    print(f"✅ Encontrados {len(controllers)} controllers LangGraph")
    
    # Descobrir agentes AutoGen
    print("🔍 Descobrindo agentes AutoGen...")
    agents = []
    
    report_file = "migration_reports/phase_d_autogen_setup.json"
    if os.path.exists(report_file):
        with open(report_file, 'r') as f:
            report = json.load(f)
            
        for result in report.get('results', []):
            agents.append({
                'name': result['name'],
                'type': 'autogen',
                'domain': result['domain'],
                'parent': result['parent'],
                'file': result['autogen_file'],
                'endpoint': f"/autogen/{result['domain']}/{result['name']}"
            })
    
    print(f"✅ Encontrados {len(agents)} agentes AutoGen")
    
    if not controllers and not agents:
        print("❌ Nenhum agente encontrado!")
        return False
    
    # Criar estrutura MCP
    print("\n🔧 Criando integração MCP...")
    os.makedirs('mcp_integration', exist_ok=True)
    
    # Configuração MCP
    mcp_config = {
        "version": "1.0",
        "name": "multi-agent-ai-system-mcp",
        "description": "MCP Integration for Multi-Agent AI System v3.0",
        "agents": {
            "langgraph_controllers": controllers,
            "autogen_agents": agents
        },
        "tools": {
            "shared_tools": [
                {"name": "research", "endpoint": "/tools/research"},
                {"name": "knowledge_search", "endpoint": "/tools/knowledge_search"},
                {"name": "file_operations", "endpoint": "/tools/files"},
                {"name": "agent_coordination", "endpoint": "/tools/coordination"}
            ]
        },
        "communication": {
            "protocol": "MCP",
            "timeout": 120,
            "retry_attempts": 3
        }
    }
    
    # Salvar configuração
    with open('mcp_integration/mcp_config.json', 'w') as f:
        json.dump(mcp_config, f, indent=2, ensure_ascii=False)
    
    # Criar servidor MCP básico
    server_code = f'''#!/usr/bin/env python3
"""
MCP Server para Multi-Agent AI System v3.0
Gerado em: {datetime.now().isoformat()}
"""

import json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

app = FastAPI(title="Multi-Agent AI System MCP Server", version="3.0.0")

# Carregar configuração
with open('mcp_config.json', 'r') as f:
    CONFIG = json.load(f)

class AgentRequest(BaseModel):
    agent_name: str
    method: str
    payload: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None

@app.get("/")
async def root():
    return {{
        "status": "healthy",
        "server": "Multi-Agent AI System MCP Server",
        "version": "3.0.0",
        "agents": {{
            "langgraph": len(CONFIG['agents']['langgraph_controllers']),
            "autogen": len(CONFIG['agents']['autogen_agents'])
        }}
    }}

@app.get("/agents")
async def list_agents():
    return CONFIG['agents']

@app.post("/agent/process")
async def process_agent_request(request: AgentRequest):
    return {{
        "agent_name": request.agent_name,
        "status": "processed",
        "result": "Mock response from MCP server",
        "timestamp": datetime.now().isoformat()
    }}

@app.get("/tools")
async def list_tools():
    return CONFIG['tools']

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting MCP Server...")
    print(f"�� LangGraph Controllers: {{len(CONFIG['agents']['langgraph_controllers'])}}")
    print(f"🤖 AutoGen Agents: {{len(CONFIG['agents']['autogen_agents'])}}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    with open('mcp_integration/mcp_server.py', 'w') as f:
        f.write(server_code)
    
    # Cliente exemplo
    client_code = '''#!/usr/bin/env python3
"""
Cliente MCP exemplo
"""

import asyncio
import aiohttp
import json

class MCPClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    async def list_agents(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/agents") as response:
                return await response.json()
    
    async def call_agent(self, agent_name, method, payload):
        data = {"agent_name": agent_name, "method": method, "payload": payload}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/agent/process", json=data) as response:
                return await response.json()

async def example():
    client = MCPClient()
    agents = await client.list_agents()
    print("Agentes:", json.dumps(agents, indent=2))

if __name__ == "__main__":
    asyncio.run(example())
'''
    
    with open('mcp_integration/mcp_client_example.py', 'w') as f:
        f.write(client_code)
    
    # Requirements
    requirements = """fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
aiohttp>=3.9.0
"""
    
    with open('mcp_integration/requirements_mcp.txt', 'w') as f:
        f.write(requirements)
    
    # Salvar relatório
    os.makedirs('migration_reports', exist_ok=True)
    report = {
        'phase': 'E - MCP Integration',
        'timestamp': datetime.now().isoformat(),
        'langgraph_controllers': len(controllers),
        'autogen_agents': len(agents),
        'total_agents': len(controllers) + len(agents),
        'mcp_server_created': True,
        'files_created': [
            'mcp_integration/mcp_config.json',
            'mcp_integration/mcp_server.py', 
            'mcp_integration/mcp_client_example.py',
            'mcp_integration/requirements_mcp.txt'
        ]
    }
    
    with open('migration_reports/phase_e_mcp_integration.json', 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 FASE E CONCLUÍDA!")
    print(f"🔧 Servidor MCP: mcp_integration/mcp_server.py")
    print(f"📋 Configuração: mcp_integration/mcp_config.json")
    print(f"💻 Cliente exemplo: mcp_integration/mcp_client_example.py")
    print(f"📊 {len(controllers)} controllers + {len(agents)} agentes integrados")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 PRONTO PARA FASE F: DEPLOY & TESTING")
    else:
        print("\n⚠️ Verificar erros antes de continuar")
