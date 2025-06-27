#!/usr/bin/env python3
"""
🧠 NEUROHOOK ULTRA - Controller com MCP Integration
Exemplo prático de como integrar ferramentas MCP ao controller de um agente
Baseado no artigo do Victor Dibia e documentação oficial AutoGen MCP
"""

import asyncio
import os
import sys
from pathlib import Path

# Adicionar path do projeto
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console
try:
    from config.mcp_marketplace import get_agent_mcp_tools
except ImportError:
    # Adicionar caminho para encontrar o módulo config
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from config.mcp_marketplace import get_agent_mcp_tools

class NeuroHookUltraMCPController:
    """
    🧠 NeuroHook Ultra com MCP Tools Integration
    
    Este exemplo demonstra:
    1. Como carregar ferramentas MCP automaticamente
    2. Como criar um agente com as ferramentas
    3. Como usar o agente com ferramentas MCP em ação
    """
    
    def __init__(self):
        self.agent_name = "neurohook_ultra"
        self.model_client = OpenAIChatCompletionClient(
            model="gpt-4o",
            temperature=0.8,
            max_tokens=4000
        )
        self.agent = None
        
    async def setup_agent_with_mcp(self):
        """Configura o agente com ferramentas MCP do marketplace"""
        print("🧠 Iniciando NeuroHook Ultra com MCP Tools...")
        
        # 1. Carregar ferramentas MCP automaticamente do marketplace
        print("🛒 Carregando ferramentas MCP do marketplace...")
        tools = await get_agent_mcp_tools(self.agent_name)
        
        if not tools:
            print("⚠️  Nenhuma ferramenta MCP configurada para neurohook_ultra")
            print("💡 Execute: python scripts/setup_mcp_marketplace.py")
            print("🌐 Ou abra: streamlit run config/mcp_marketplace_ui.py")
            return False
        
        print(f"✅ {len(tools)} ferramentas MCP carregadas:")
        for i, tool in enumerate(tools, 1):
            print(f"  {i}. {tool.name if hasattr(tool, 'name') else 'Ferramenta MCP'}")
        
        # 2. Criar agente com sistema de prompt otimizado para MCP
        system_message = """
        Você é NeuroHook Ultra, um especialista em neurociência da atenção e persuasão.
        
        🧠 ESPECIALIZAÇÃO:
        - Geração de hooks hipnóticos e persuasivos
        - Análise neuropsicológica de atenção
        - Otimização de engagement cognitivo
        - Engenharia de linguagem persuasiva
        
        🛠️ FERRAMENTAS MCP DISPONÍVEIS:
        Você tem acesso a ferramentas MCP avançadas para:
        - Pesquisar informações atualizadas sobre neurociência
        - Analisar conteúdo web para insights de persuasão
        - Acessar e processar arquivos de conhecimento
        - Executar buscas especializadas
        
        🎯 INSTRUÇÕES DE USO:
        1. SEMPRE use suas ferramentas MCP para pesquisar informações atualizadas
        2. Combine research com seu conhecimento especializado
        3. Cite fontes quando usar informações pesquisadas
        4. Crie hooks baseados em evidências neurológicas
        
        🧪 FORMATO DE RESPOSTA:
        Para cada hook gerado, inclua:
        - O hook em si (máximo 2 linhas)
        - Base neurológica (qual princípio cognitivo utiliza)
        - Contexto de uso recomendado
        - Variações para teste A/B
        """
        
        # 3. Criar agente com as ferramentas MCP
        self.agent = AssistantAgent(
            name=self.agent_name,
            model_client=self.model_client,
            tools=tools,  # ← Ferramentas MCP do marketplace!
            system_message=system_message,
            reflect_on_tool_use=True,
            model_client_stream=True
        )
        
        print("✅ NeuroHook Ultra configurado com ferramentas MCP!")
        return True
    
    async def demo_basic_hook_generation(self):
        """Demonstra geração básica de hooks com MCP"""
        print("\n🎯 DEMO: Geração Básica de Hooks")
        print("=" * 40)
        
        prompt = """
        Quero que você demonstre suas capacidades MCP + NeuroHook.
        
        TAREFA: Gere hooks persuasivos para um curso sobre "Produtividade com IA"
        
        PROCESSO:
        1. Use suas ferramentas MCP para pesquisar tendências atuais sobre IA e produtividade
        2. Analise o que está chamando atenção no mercado agora
        3. Gere 3 hooks diferentes baseados em princípios neurológicos
        4. Explique a base científica de cada hook
        
        TARGET: Profissionais que querem usar IA para ser mais produtivos
        """
        
        print("🧠 Executando NeuroHook Ultra com MCP...")
        result = await self.agent.run(prompt)
        
        print("\n🎯 RESULTADO:")
        print("-" * 40)
        # O resultado será exibido automaticamente pelo Console
        
        return result
    
    async def demo_research_based_hooks(self):
        """Demonstra hooks baseados em research real com MCP"""
        print("\n🔬 DEMO: Hooks Baseados em Research")
        print("=" * 40)
        
        prompt = """
        MISSÃO AVANÇADA: Research + NeuroHook
        
        1. Use suas ferramentas MCP para pesquisar:
           - Últimas descobertas em neurociência da atenção (2024-2025)
           - Estudos sobre procrastinação e motivação
           - Dados sobre uso de IA no trabalho
        
        2. Com base no research, crie:
           - 2 hooks para LinkedIn (profissional)
           - 2 hooks para YouTube (casual)
           - 2 hooks para email marketing (direto)
        
        3. Para cada hook, explique:
           - Qual estudo/dado você encontrou
           - Como aplicou neurociência
           - Por que vai funcionar
        
        CONTEXTO: Lançamento de um programa "IA para Executivos"
        """
        
        print("🔬 Executando research avançado com MCP...")
        result = await self.agent.run(prompt)
        
        return result
    
    async def demo_interactive_session(self):
        """Demonstra sessão interativa com o agente MCP"""
        print("\n💬 DEMO: Sessão Interativa")
        print("=" * 40)
        print("💡 Digite prompts para o NeuroHook Ultra (digite 'sair' para terminar)")
        
        while True:
            user_input = input("\n🧠 Você: ")
            
            if user_input.lower() in ['sair', 'quit', 'exit']:
                print("👋 Sessão encerrada!")
                break
            
            if user_input.strip():
                try:
                    result = await self.agent.run(user_input)
                    print(f"\n🎯 NeuroHook Ultra: {result}")
                except Exception as e:
                    print(f"❌ Erro: {e}")
    
    async def run_all_demos(self):
        """Executa todas as demonstrações"""
        print("🚀 NEUROHOOK ULTRA - MCP INTEGRATION DEMO")
        print("=" * 50)
        
        # Setup
        success = await self.setup_agent_with_mcp()
        if not success:
            return
        
        # Demos
        await self.demo_basic_hook_generation()
        
        print("\n" + "="*50)
        input("⏸️  Pressione Enter para continuar para o demo avançado...")
        
        await self.demo_research_based_hooks()
        
        print("\n" + "="*50)
        choice = input("🤔 Deseja testar a sessão interativa? (s/n): ").lower()
        if choice.startswith('s'):
            await self.demo_interactive_session()
        
        print("\n✅ Todas as demos concluídas!")
        print("🌐 Para configurar outros agentes: streamlit run config/mcp_marketplace_ui.py")

# Funções de conveniência para uso direto
async def create_neurohook_with_mcp():
    """Função de conveniência para criar NeuroHook com MCP"""
    controller = NeuroHookUltraMCPController()
    await controller.setup_agent_with_mcp()
    return controller.agent

async def quick_hook_generation(prompt: str):
    """Função para geração rápida de hooks"""
    controller = NeuroHookUltraMCPController()
    await controller.setup_agent_with_mcp()
    
    if controller.agent:
        return await controller.agent.run(prompt)
    else:
        return "❌ Erro ao configurar agente MCP"

# Exemplo de uso em outros scripts
async def example_usage():
    """Exemplo de como usar em outros scripts"""
    
    # Modo 1: Usar o controller completo
    controller = NeuroHookUltraMCPController()
    await controller.setup_agent_with_mcp()
    
    # Modo 2: Usar função de conveniência
    agent = await create_neurohook_with_mcp()
    
    # Modo 3: Geração rápida
    hook = await quick_hook_generation(
        "Crie um hook sobre economia de tempo com IA"
    )
    print(hook)

if __name__ == "__main__":
    # Demo completa
    controller = NeuroHookUltraMCPController()
    asyncio.run(controller.run_all_demos()) 