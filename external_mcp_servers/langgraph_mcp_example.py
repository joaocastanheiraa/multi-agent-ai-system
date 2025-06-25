#!/usr/bin/env python3
"""
Exemplo de integração LangGraph com servidores MCP externos
Baseado na documentação oficial: https://langchain-ai.github.io/langgraph/agents/mcp/
"""

import asyncio
import os
from pathlib import Path
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

# Configurar caminhos absolutos para os servidores MCP
current_dir = Path(__file__).parent.absolute()
math_server_path = current_dir / "math_server.py"
weather_server_url = "http://localhost:8000/mcp"

async def main():
    """Função principal que demonstra a integração MCP + LangGraph"""
    
    # Verificar se as variáveis de ambiente estão configuradas
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY não configurada. Configure no .env")
        return
    
    print("🚀 Iniciando integração LangGraph + MCP")
    print("=" * 50)
    
    # Configurar cliente MCP com múltiplos servidores
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": [str(math_server_path)],
                "transport": "stdio",
            },
            "weather": {
                "url": weather_server_url,
                "transport": "streamable_http",
            }
        }
    )
    
    try:
        # Obter ferramentas dos servidores MCP
        print("📡 Conectando aos servidores MCP...")
        tools = await client.get_tools()
        print(f"✅ {len(tools)} ferramentas carregadas dos servidores MCP:")
        for tool in tools:
            print(f"   • {tool.name}: {tool.description}")
        
        # Criar agente LangGraph com as ferramentas MCP
        print("\n🤖 Criando agente LangGraph...")
        agent = create_react_agent(
            ChatOpenAI(model="gpt-4o-mini", temperature=0),
            tools
        )
        print("✅ Agente criado com sucesso!")
        
        # Teste 1: Operação matemática
        print("\n" + "=" * 50)
        print("🧮 TESTE 1: Operação Matemática")
        print("=" * 50)
        
        math_response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
        )
        
        print("👤 Pergunta: what's (3 + 5) x 12?")
        print(f"🤖 Resposta: {math_response['messages'][-1].content}")
        
        # Teste 2: Consulta de clima
        print("\n" + "=" * 50)
        print("🌤️  TESTE 2: Consulta de Clima")
        print("=" * 50)
        
        weather_response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "what is the weather in New York?"}]}
        )
        
        print("👤 Pergunta: what is the weather in New York?")
        print(f"🤖 Resposta: {weather_response['messages'][-1].content}")
        
        # Teste 3: Operação complexa combinando ferramentas
        print("\n" + "=" * 50)
        print("🔄 TESTE 3: Operação Complexa")
        print("=" * 50)
        
        complex_response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "Calculate 15 * 4, then tell me if it's good weather for that temperature in São Paulo"}]}
        )
        
        print("👤 Pergunta: Calculate 15 * 4, then tell me if it's good weather for that temperature in São Paulo")
        print(f"🤖 Resposta: {complex_response['messages'][-1].content}")
        
        print("\n🎉 Todos os testes concluídos com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Limpar recursos
        print("\n🧹 Limpando recursos...")

if __name__ == "__main__":
    asyncio.run(main()) 