#!/usr/bin/env python3
"""
🔥 INTEGRAÇÃO MCP-LANGCHAIN OFICIAL
===================================

Este exemplo demonstra como usar servidores MCP oficiais com LangChain/LangGraph
usando os adaptadores oficiais da LangChain.

Baseado na documentação oficial:
- https://langchain-ai.github.io/langgraph/agents/mcp/
- https://pypi.org/project/langchain-mcp-adapters/
- https://pypi.org/project/langchain-mcp-tools/

Servidores MCP incluídos:
- Filesystem (manipulação de arquivos)
- Math (operações matemáticas)
- Weather (clima simulado)
"""

import asyncio
import os
from pathlib import Path
from typing import Dict, Any

# Imports MCP oficiais
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_tools import convert_mcp_to_langchain_tools

# Imports LangChain/LangGraph
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model

# Configuração dos servidores MCP
MCP_SERVERS_CONFIG = {
    "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", str(Path.cwd())],
        "transport": "stdio"
    },
    "math": {
        "command": "python",
        "args": [str(Path(__file__).parent / "math_server.py")],
        "transport": "stdio"
    },
    "weather": {
        "url": "http://localhost:8001/mcp",
        "transport": "streamable_http"
    }
}

async def test_mcp_adapters_integration():
    """
    Testa a integração usando langchain-mcp-adapters (método oficial)
    """
    print("🔧 Testando integração MCP-LangChain com adaptadores oficiais...")
    
    try:
        # Configurar cliente MCP multi-servidor
        client = MultiServerMCPClient(MCP_SERVERS_CONFIG)
        
        # Obter ferramentas dos servidores MCP
        tools = await client.get_tools()
        
        print(f"✅ {len(tools)} ferramentas MCP carregadas:")
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")
        
        # Criar agente LangGraph com as ferramentas MCP
        llm = init_chat_model("openai:gpt-4o-mini", model_provider="openai")
        agent = create_react_agent(llm, tools)
        
        # Testar o agente
        test_queries = [
            "Liste os arquivos no diretório atual",
            "Calcule 25 * 4 + 10",
            "Qual é o clima em São Paulo?"
        ]
        
        for query in test_queries:
            print(f"\n🤔 Pergunta: {query}")
            try:
                response = await agent.ainvoke({"messages": [("user", query)]})
                print(f"🤖 Resposta: {response['messages'][-1].content}")
            except Exception as e:
                print(f"❌ Erro: {e}")
        
        # Limpar recursos
        await client.close()
        
    except Exception as e:
        print(f"❌ Erro na integração MCP-Adapters: {e}")

async def test_mcp_tools_integration():
    """
    Testa a integração usando langchain-mcp-tools (método alternativo)
    """
    print("\n🔧 Testando integração MCP-LangChain com langchain-mcp-tools...")
    
    try:
        # Configurar servidores MCP
        mcp_servers = {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", str(Path.cwd())]
            }
        }
        
        # Converter servidores MCP em ferramentas LangChain
        tools, cleanup = await convert_mcp_to_langchain_tools(mcp_servers)
        
        print(f"✅ {len(tools)} ferramentas convertidas:")
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")
        
        # Criar agente com as ferramentas
        llm = init_chat_model("openai:gpt-4o-mini", model_provider="openai")
        agent = create_react_agent(llm, tools)
        
        # Testar o agente
        response = await agent.ainvoke({
            "messages": [("user", "Liste os arquivos Python no diretório atual")]
        })
        print(f"🤖 Resposta: {response['messages'][-1].content}")
        
        # Limpar recursos
        await cleanup()
        
    except Exception as e:
        print(f"❌ Erro na integração MCP-Tools: {e}")

async def create_custom_mcp_server():
    """
    Cria um servidor MCP customizado para demonstrar flexibilidade
    """
    print("\n🛠️ Criando servidor MCP customizado...")
    
    custom_server_code = '''
from mcp.server.fastmcp import FastMCP
import json
from datetime import datetime

mcp = FastMCP("CustomTools")

@mcp.tool()
def get_system_info() -> str:
    """Obter informações do sistema"""
    import platform
    return json.dumps({
        "system": platform.system(),
        "python_version": platform.python_version(),
        "timestamp": datetime.now().isoformat()
    })

@mcp.tool()
def calculate_fibonacci(n: int) -> str:
    """Calcular sequência de Fibonacci até n"""
    if n <= 0:
        return "[]"
    elif n == 1:
        return "[0]"
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    
    return json.dumps(fib)

if __name__ == "__main__":
    mcp.run(transport="stdio")
'''
    
    # Salvar servidor customizado
    custom_server_path = Path(__file__).parent / "custom_mcp_server.py"
    with open(custom_server_path, 'w') as f:
        f.write(custom_server_code)
    
    print(f"✅ Servidor MCP customizado criado em: {custom_server_path}")
    
    # Testar servidor customizado
    try:
        custom_config = {
            "custom": {
                "command": "python",
                "args": [str(custom_server_path)],
                "transport": "stdio"
            }
        }
        
        client = MultiServerMCPClient(custom_config)
        tools = await client.get_tools()
        
        print(f"✅ Servidor customizado carregado com {len(tools)} ferramentas:")
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")
        
        # Testar uma ferramenta
        llm = init_chat_model("openai:gpt-4o-mini", model_provider="openai")
        agent = create_react_agent(llm, tools)
        
        response = await agent.ainvoke({
            "messages": [("user", "Me mostre informações do sistema e calcule os primeiros 10 números de Fibonacci")]
        })
        print(f"🤖 Resposta: {response['messages'][-1].content}")
        
        await client.close()
        
    except Exception as e:
        print(f"❌ Erro no servidor customizado: {e}")

def check_environment():
    """
    Verificar se o ambiente está configurado corretamente
    """
    print("🔍 Verificando configuração do ambiente...")
    
    # Verificar variáveis de ambiente
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Variáveis de ambiente ausentes: {', '.join(missing_vars)}")
        print("   Configure-as no arquivo .env ou como variáveis de sistema")
        return False
    
    # Verificar Node.js para servidores MCP
    import subprocess
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js encontrado: {result.stdout.strip()}")
        else:
            print("⚠️  Node.js não encontrado - alguns servidores MCP podem não funcionar")
    except FileNotFoundError:
        print("⚠️  Node.js não encontrado - alguns servidores MCP podem não funcionar")
    
    print("✅ Verificação do ambiente concluída")
    return True

async def main():
    """
    Função principal que executa todos os testes de integração MCP
    """
    print("🚀 INTEGRAÇÃO MCP-LANGCHAIN OFICIAL")
    print("=" * 50)
    
    # Verificar ambiente
    if not check_environment():
        print("❌ Ambiente não configurado corretamente")
        return
    
    # Executar testes de integração
    await test_mcp_adapters_integration()
    await test_mcp_tools_integration()
    await create_custom_mcp_server()
    
    print("\n🎉 Integração MCP-LangChain concluída com sucesso!")
    print("\n📚 Próximos passos:")
    print("   1. Integre essas ferramentas MCP aos seus agentes existentes")
    print("   2. Crie servidores MCP customizados para suas necessidades específicas")
    print("   3. Use o MultiServerMCPClient para gerenciar múltiplos servidores")
    print("   4. Explore mais servidores MCP em: https://github.com/modelcontextprotocol")

if __name__ == "__main__":
    asyncio.run(main()) 