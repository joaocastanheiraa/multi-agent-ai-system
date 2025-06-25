#!/usr/bin/env python3
"""
🎯 EXEMPLO PRÁTICO DE INTEGRAÇÃO MCP-LANGCHAIN
==============================================

Este exemplo demonstra como integrar servidores MCP aos seus agentes existentes
no repositório Multi-Agent AI System.

Funcionalidades incluídas:
- Manipulação de arquivos via MCP Filesystem
- Ferramentas customizadas via MCP
- Integração com agentes LangGraph existentes
"""

import asyncio
import os
from pathlib import Path
from typing import Dict, Any, List

# Imports MCP
from langchain_mcp_tools import convert_mcp_to_langchain_tools

# Imports LangChain/LangGraph
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

async def create_mcp_enhanced_agent():
    """
    Cria um agente LangGraph aprimorado com ferramentas MCP
    """
    print("🤖 Criando agente aprimorado com ferramentas MCP...")
    
    # Configurar servidores MCP
    mcp_servers = {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", str(Path.cwd())]
        }
    }
    
    try:
        # Converter servidores MCP em ferramentas LangChain
        tools, cleanup = await convert_mcp_to_langchain_tools(mcp_servers)
        
        print(f"✅ {len(tools)} ferramentas MCP carregadas")
        
        # Criar modelo de chat
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
        # Criar agente com ferramentas MCP
        agent = create_react_agent(llm, tools)
        
        return agent, cleanup, tools
        
    except Exception as e:
        print(f"❌ Erro ao criar agente MCP: {e}")
        return None, None, []

async def test_file_analysis_agent():
    """
    Testa agente para análise de arquivos do projeto
    """
    print("\n📁 TESTE: Agente de Análise de Arquivos")
    print("=" * 40)
    
    agent, cleanup, tools = await create_mcp_enhanced_agent()
    if not agent:
        return
    
    try:
        # Tarefas de análise de arquivos
        tasks = [
            "Liste todos os arquivos Python na pasta domains/",
            "Leia o conteúdo do arquivo README.md e me dê um resumo",
            "Procure por arquivos que contenham 'agent' no nome",
            "Me mostre a estrutura de diretórios da pasta mcp_integration/"
        ]
        
        for task in tasks:
            print(f"\n🔍 Tarefa: {task}")
            try:
                response = await agent.ainvoke({"messages": [("user", task)]})
                print(f"✅ Resultado: {response['messages'][-1].content[:200]}...")
            except Exception as e:
                print(f"❌ Erro: {e}")
        
        # Limpar recursos
        await cleanup()
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

async def test_code_analysis_agent():
    """
    Testa agente para análise de código
    """
    print("\n💻 TESTE: Agente de Análise de Código")
    print("=" * 40)
    
    agent, cleanup, tools = await create_mcp_enhanced_agent()
    if not agent:
        return
    
    try:
        # Tarefas de análise de código
        tasks = [
            "Analise o arquivo advanced_agent_dashboard.py e me diga quais são suas principais funcionalidades",
            "Procure por todos os arquivos controller.py e me diga quantos existem",
            "Leia o arquivo requirements.txt e liste as principais dependências"
        ]
        
        for task in tasks:
            print(f"\n🔍 Tarefa: {task}")
            try:
                response = await agent.ainvoke({"messages": [("user", task)]})
                print(f"✅ Resultado: {response['messages'][-1].content[:300]}...")
            except Exception as e:
                print(f"❌ Erro: {e}")
        
        # Limpar recursos
        await cleanup()
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

async def create_project_documentation_agent():
    """
    Cria um agente especializado em documentação do projeto
    """
    print("\n📚 CRIANDO: Agente de Documentação do Projeto")
    print("=" * 50)
    
    agent, cleanup, tools = await create_mcp_enhanced_agent()
    if not agent:
        return
    
    try:
        # Tarefa complexa de documentação
        task = """
        Analise o projeto Multi-Agent AI System e crie um relatório detalhado incluindo:
        
        1. Estrutura geral do projeto (principais diretórios)
        2. Tipos de agentes implementados (baseado nos diretórios em domains/)
        3. Principais scripts de configuração e inicialização
        4. Tecnologias utilizadas (baseado no requirements.txt)
        5. Recomendações para novos desenvolvedores
        
        Use as ferramentas de sistema de arquivos para explorar o projeto.
        """
        
        print(f"🔍 Gerando relatório completo do projeto...")
        
        response = await agent.ainvoke({"messages": [("user", task)]})
        
        # Salvar relatório
        report_content = response['messages'][-1].content
        report_path = Path("PROJECT_ANALYSIS_REPORT.md")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# Relatório de Análise do Projeto Multi-Agent AI System\n\n")
            f.write(f"*Gerado automaticamente por agente MCP-LangChain*\n\n")
            f.write(report_content)
        
        print(f"✅ Relatório salvo em: {report_path}")
        print(f"📄 Tamanho do relatório: {len(report_content)} caracteres")
        
        # Limpar recursos
        await cleanup()
        
    except Exception as e:
        print(f"❌ Erro na documentação: {e}")

async def integrate_with_existing_agents():
    """
    Demonstra como integrar MCP com agentes existentes do repositório
    """
    print("\n🔗 INTEGRAÇÃO: MCP com Agentes Existentes")
    print("=" * 50)
    
    # Configurar múltiplos servidores MCP
    mcp_servers = {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", str(Path.cwd())]
        }
    }
    
    try:
        # Converter servidores MCP em ferramentas
        tools, cleanup = await convert_mcp_to_langchain_tools(mcp_servers)
        
        print(f"✅ {len(tools)} ferramentas MCP disponíveis para integração")
        
        # Exemplo de como adicionar às configurações existentes
        integration_example = {
            "agent_name": "Enhanced Analytics Agent",
            "base_agent": "domains/analytics/agents/ANALYTICSGPT",
            "mcp_tools": [tool.name for tool in tools],
            "integration_method": "MultiServerMCPClient",
            "benefits": [
                "Manipulação direta de arquivos",
                "Análise de código em tempo real",
                "Geração automática de documentação",
                "Busca inteligente em arquivos"
            ]
        }
        
        print("\n📋 Exemplo de Integração:")
        for key, value in integration_example.items():
            print(f"   {key}: {value}")
        
        # Demonstrar uso prático
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        agent = create_react_agent(llm, tools)
        
        # Tarefa específica para agentes de analytics
        analytics_task = """
        Como um agente de analytics aprimorado com ferramentas MCP, analise:
        1. Quantos agentes de analytics existem no projeto
        2. Quais são suas principais funcionalidades (lendo os arquivos)
        3. Como posso usar ferramentas MCP para aprimorar esses agentes
        """
        
        response = await agent.ainvoke({"messages": [("user", analytics_task)]})
        print(f"\n🤖 Análise de Integração: {response['messages'][-1].content[:400]}...")
        
        # Limpar recursos
        await cleanup()
        
    except Exception as e:
        print(f"❌ Erro na integração: {e}")

def show_integration_guide():
    """
    Mostra guia de integração para desenvolvedores
    """
    print("\n📖 GUIA DE INTEGRAÇÃO MCP-LANGCHAIN")
    print("=" * 50)
    
    guide = """
    🚀 COMO INTEGRAR MCP AOS SEUS AGENTES:
    
    1. 📦 INSTALAÇÃO:
       pip install langchain-mcp-adapters langchain-mcp-tools
    
    2. 🔧 CONFIGURAÇÃO BÁSICA:
       from langchain_mcp_tools import convert_mcp_to_langchain_tools
       
       mcp_servers = {
           "filesystem": {
               "command": "npx",
               "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
           }
       }
       
       tools, cleanup = await convert_mcp_to_langchain_tools(mcp_servers)
    
    3. 🤖 INTEGRAÇÃO COM AGENTES:
       from langgraph.prebuilt import create_react_agent
       
       agent = create_react_agent(llm, tools)
    
    4. 🛠️ SERVIDORES MCP DISPONÍVEIS:
       - @modelcontextprotocol/server-filesystem (manipulação de arquivos)
       - @modelcontextprotocol/server-brave-search (busca web)
       - @modelcontextprotocol/server-github (integração GitHub)
       - Custom servers (seus próprios servidores)
    
    5. 💡 CASOS DE USO NO PROJETO:
       - Análise automática de código
       - Geração de documentação
       - Busca inteligente em arquivos
       - Manipulação de configurações
       - Integração com APIs externas
    
    6. 🔗 INTEGRAÇÃO COM AGENTES EXISTENTES:
       - Adicione ferramentas MCP aos controllers existentes
       - Use MultiServerMCPClient para múltiplos servidores
       - Combine com knowledge bases existentes
    """
    
    print(guide)

async def main():
    """
    Função principal que executa todos os exemplos práticos
    """
    print("🎯 EXEMPLOS PRÁTICOS DE INTEGRAÇÃO MCP-LANGCHAIN")
    print("=" * 60)
    
    # Verificar ambiente
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY não configurada")
        print("   Configure antes de executar os testes")
        return
    
    # Executar testes práticos
    await test_file_analysis_agent()
    await test_code_analysis_agent()
    await create_project_documentation_agent()
    await integrate_with_existing_agents()
    
    # Mostrar guia de integração
    show_integration_guide()
    
    print("\n🎉 INTEGRAÇÃO MCP-LANGCHAIN CONCLUÍDA!")
    print("\n📚 Próximos passos:")
    print("   1. Integre MCP aos seus agentes em domains/")
    print("   2. Crie servidores MCP customizados para suas necessidades")
    print("   3. Use ferramentas MCP nos dashboards existentes")
    print("   4. Explore mais servidores MCP oficiais")

if __name__ == "__main__":
    asyncio.run(main()) 