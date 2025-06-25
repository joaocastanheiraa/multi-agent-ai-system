#!/usr/bin/env python3
"""
🎯 EXEMPLOS PRÁTICOS DE OTIMIZAÇÕES LANGCHAIN
============================================

Demonstrações práticas de como usar as otimizações descobertas
para melhorar significativamente a performance e funcionalidade
dos agentes LangChain.
"""

import asyncio
import json
from pathlib import Path
from typing import List, Dict, Any

# Imports das otimizações
from optimized_agent_base import (
    OptimizedAgentBase, 
    AgentConfig, 
    OptimizedAgentFactory,
    ExampleOptimizedAgent
)

# Imports MCP para ferramentas avançadas
from langchain_mcp_tools import convert_mcp_to_langchain_tools

class AdvancedCopywriterAgent(OptimizedAgentBase):
    """
    Agente copywriter otimizado com funcionalidades avançadas
    """
    
    def __init__(self, config: AgentConfig, tools: List = None):
        super().__init__(config, tools)
        
        # Configurar contexto específico para copywriting
        if self.memory:
            self.memory.set_context("expertise", "copywriting")
            self.memory.set_context("style_guide", {
                "tone": "persuasivo",
                "target_audience": "empreendedores",
                "call_to_action": "sempre incluir"
            })
    
    async def _process_core_logic(self, input_text: str, context: Dict) -> str:
        """Lógica otimizada para copywriting"""
        
        # Enriquecer prompt com contexto de copywriting
        enhanced_prompt = f"""
        Como especialista em copywriting persuasivo, analise e responda:
        
        Contexto: {context.get('chat_history', 'Primeira interação')}
        Solicitação: {input_text}
        
        Diretrizes:
        - Use técnicas de neurociência da persuasão
        - Inclua gatilhos emocionais apropriados
        - Estruture com headlines impactantes
        - Termine sempre com call-to-action claro
        
        Resposta otimizada:
        """
        
        if self.agent:
            response = await self.agent.ainvoke({"messages": [("user", enhanced_prompt)]})
            return response['messages'][-1].content
        else:
            from langchain.schema import HumanMessage
            messages = [HumanMessage(content=enhanced_prompt)]
            response = await self.llm.ainvoke(messages)
            return response.content

class AnalyticsAgent(OptimizedAgentBase):
    """
    Agente de analytics otimizado com ferramentas MCP
    """
    
    async def _process_core_logic(self, input_text: str, context: Dict) -> str:
        """Lógica otimizada para análise de dados"""
        
        # Usar ferramentas MCP para análise de arquivos
        if self.agent and self.tools:
            enhanced_prompt = f"""
            Como especialista em analytics, analise a solicitação e use as ferramentas disponíveis:
            
            Solicitação: {input_text}
            
            Ferramentas disponíveis: {[tool.name for tool in self.tools]}
            
            Passos:
            1. Identifique se precisa acessar arquivos ou dados
            2. Use as ferramentas apropriadas para coleta
            3. Analise os dados coletados
            4. Forneça insights acionáveis
            5. Inclua visualizações ou métricas quando relevante
            """
            
            response = await self.agent.ainvoke({"messages": [("user", enhanced_prompt)]})
            return response['messages'][-1].content
        else:
            return await super()._process_core_logic(input_text, context)

class MultiAgentOrchestrator:
    """
    Orquestrador para múltiplos agentes otimizados
    """
    
    def __init__(self):
        self.agents = {}
        self.routing_rules = {}
    
    def add_agent(self, name: str, agent: OptimizedAgentBase, keywords: List[str] = None):
        """Adicionar agente ao orquestrador"""
        self.agents[name] = agent
        if keywords:
            for keyword in keywords:
                self.routing_rules[keyword.lower()] = name
    
    def _route_request(self, input_text: str) -> str:
        """Rotear solicitação para o agente apropriado"""
        input_lower = input_text.lower()
        
        for keyword, agent_name in self.routing_rules.items():
            if keyword in input_lower:
                return agent_name
        
        # Agente padrão
        return list(self.agents.keys())[0] if self.agents else None
    
    async def process_request(self, input_text: str, agent_name: str = None) -> Dict[str, Any]:
        """Processar solicitação com roteamento inteligente"""
        
        # Determinar agente
        if not agent_name:
            agent_name = self._route_request(input_text)
        
        if agent_name not in self.agents:
            return {
                "error": f"Agente '{agent_name}' não encontrado",
                "available_agents": list(self.agents.keys())
            }
        
        agent = self.agents[agent_name]
        
        # Processar com métricas
        start_time = asyncio.get_event_loop().time()
        result = await agent.process_input(input_text)
        end_time = asyncio.get_event_loop().time()
        
        return {
            "agent_used": agent_name,
            "result": result,
            "processing_time": end_time - start_time,
            "metrics": agent.get_metrics()
        }

async def demonstrate_optimizations():
    """Demonstrar as otimizações implementadas"""
    print("🚀 DEMONSTRAÇÃO DE OTIMIZAÇÕES LANGCHAIN")
    print("=" * 60)
    
    # 1. Criar agentes otimizados com diferentes configurações
    print("\n1️⃣ CRIANDO AGENTES OTIMIZADOS")
    print("-" * 40)
    
    # Agente de alta performance
    hp_config = AgentConfig(
        name="high_performance",
        temperature=0.3,
        max_tokens=1500,
        enable_cache=True,
        cache_ttl=7200,
        memory_type="summary"
    )
    
    # Agente criativo
    creative_config = AgentConfig(
        name="creative",
        temperature=0.9,
        max_tokens=3000,
        enable_cache=False,
        memory_type="buffer"
    )
    
    # Criar agentes
    hp_agent = ExampleOptimizedAgent(hp_config)
    creative_agent = ExampleOptimizedAgent(creative_config)
    
    print(f"✅ Agente de alta performance criado: {hp_agent.config.name}")
    print(f"✅ Agente criativo criado: {creative_agent.config.name}")
    
    # 2. Demonstrar cache inteligente
    print("\n2️⃣ DEMONSTRANDO CACHE INTELIGENTE")
    print("-" * 40)
    
    test_query = "Explique o conceito de inteligência artificial"
    
    # Primeira chamada (sem cache)
    print("Primeira chamada (sem cache)...")
    result1 = await hp_agent.process_input(test_query)
    print(f"Resultado: {result1[:100]}...")
    
    # Segunda chamada (com cache)
    print("Segunda chamada (com cache)...")
    result2 = await hp_agent.process_input(test_query)
    print(f"Resultado: {result2[:100]}...")
    print(f"Cache hit: {result1 == result2}")
    
    # 3. Demonstrar memória avançada
    print("\n3️⃣ DEMONSTRANDO MEMÓRIA AVANÇADA")
    print("-" * 40)
    
    # Conversação com memória
    await creative_agent.process_input("Meu nome é João e gosto de tecnologia")
    response = await creative_agent.process_input("Qual é o meu nome e o que eu gosto?")
    print(f"Resposta com memória: {response}")
    
    # 4. Demonstrar agente especializado
    print("\n4️⃣ DEMONSTRANDO AGENTE COPYWRITER ESPECIALIZADO")
    print("-" * 50)
    
    copywriter_config = AgentConfig(
        name="copywriter_pro",
        temperature=0.7,
        max_tokens=2000,
        enable_memory=True,
        memory_type="buffer"
    )
    
    copywriter = AdvancedCopywriterAgent(copywriter_config)
    copy_result = await copywriter.process_input(
        "Crie um headline para um curso de marketing digital"
    )
    print(f"Copy gerada: {copy_result}")
    
    # 5. Demonstrar orquestrador multi-agente
    print("\n5️⃣ DEMONSTRANDO ORQUESTRADOR MULTI-AGENTE")
    print("-" * 50)
    
    orchestrator = MultiAgentOrchestrator()
    orchestrator.add_agent("copywriter", copywriter, ["copy", "headline", "texto"])
    orchestrator.add_agent("analytics", hp_agent, ["dados", "análise", "métricas"])
    
    # Teste de roteamento
    copy_request = await orchestrator.process_request(
        "Preciso de um copy para minha landing page"
    )
    print(f"Agente usado: {copy_request['agent_used']}")
    print(f"Resultado: {copy_request['result'][:100]}...")
    
    # 6. Demonstrar métricas e observabilidade
    print("\n6️⃣ DEMONSTRANDO MÉTRICAS E OBSERVABILIDADE")
    print("-" * 50)
    
    metrics = hp_agent.get_metrics()
    print("Métricas do agente de alta performance:")
    print(json.dumps(metrics, indent=2, default=str))
    
    print("\n✅ DEMONSTRAÇÃO CONCLUÍDA!")
    print("=" * 60)
    
    # Cleanup
    hp_agent.cleanup()
    creative_agent.cleanup()
    copywriter.cleanup()

async def create_optimized_agent_from_existing():
    """
    Exemplo de como migrar um agente existente para a versão otimizada
    """
    print("\n🔄 MIGRANDO AGENTE EXISTENTE PARA VERSÃO OTIMIZADA")
    print("=" * 60)
    
    # Configuração baseada em um agente existente do projeto
    existing_agent_config = AgentConfig(
        name="neurohook_ultra_optimized",
        model="gpt-4o-mini",
        temperature=0.8,  # Criatividade para hooks
        max_tokens=2500,
        enable_memory=True,
        memory_type="buffer",
        enable_cache=True,
        cache_ttl=3600,
        log_level="INFO",
        max_retries=3
    )
    
    class NeurohookUltraOptimized(OptimizedAgentBase):
        """Versão otimizada do Neurohook Ultra"""
        
        def __init__(self, config: AgentConfig, tools: List = None):
            super().__init__(config, tools)
            
            # Configurar contexto específico
            if self.memory:
                self.memory.set_context("expertise", "neurohooks")
                self.memory.set_context("techniques", [
                    "curiosity_gap",
                    "social_proof",
                    "scarcity",
                    "authority",
                    "reciprocity"
                ])
        
        async def _process_core_logic(self, input_text: str, context: Dict) -> str:
            """Lógica otimizada para criação de neurohooks"""
            
            enhanced_prompt = f"""
            Como especialista em neurohooks e psicologia da atenção, crie hooks magnéticos:
            
            Contexto da conversa: {context.get('chat_history', 'Nova sessão')}
            Solicitação: {input_text}
            
            Técnicas disponíveis: {self.memory.get_context('techniques') if self.memory else 'Todas'}
            
            Diretrizes:
            1. Use gatilhos neurológicos comprovados
            2. Crie curiosity gaps irresistíveis
            3. Aplique princípios de neurociência da atenção
            4. Teste múltiplas variações
            5. Otimize para diferentes plataformas
            
            Resposta com neurohooks otimizados:
            """
            
            if self.agent:
                response = await self.agent.ainvoke({"messages": [("user", enhanced_prompt)]})
                return response['messages'][-1].content
            else:
                from langchain.schema import HumanMessage
                messages = [HumanMessage(content=enhanced_prompt)]
                response = await self.llm.ainvoke(messages)
                return response.content
    
    # Criar agente otimizado
    neurohook_agent = NeurohookUltraOptimized(existing_agent_config)
    
    # Testar
    result = await neurohook_agent.process_input(
        "Crie 5 hooks para um post sobre produtividade no LinkedIn"
    )
    
    print("🎯 Neurohooks gerados:")
    print(result)
    
    # Mostrar métricas
    print("\n📊 Métricas do agente:")
    metrics = neurohook_agent.get_metrics()
    print(json.dumps(metrics, indent=2, default=str))
    
    # Salvar configuração para reutilização
    neurohook_agent.save_config("config_examples/neurohook_optimized.json")
    print("\n💾 Configuração salva para reutilização")
    
    neurohook_agent.cleanup()

async def demonstrate_mcp_integration():
    """Demonstrar integração com ferramentas MCP"""
    print("\n🔧 DEMONSTRANDO INTEGRAÇÃO MCP AVANÇADA")
    print("=" * 50)
    
    try:
        # Configurar servidores MCP
        mcp_servers = {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", str(Path.cwd())]
            }
        }
        
        # Converter para ferramentas LangChain
        tools, cleanup = await convert_mcp_to_langchain_tools(mcp_servers)
        
        print(f"✅ {len(tools)} ferramentas MCP carregadas")
        
        # Criar agente analytics com ferramentas MCP
        analytics_config = AgentConfig(
            name="analytics_mcp",
            temperature=0.2,
            max_tokens=2000,
            enable_memory=True,
            memory_type="summary"
        )
        
        analytics_agent = AnalyticsAgent(analytics_config, tools)
        
        # Testar análise de arquivos
        result = await analytics_agent.process_input(
            "Analise a estrutura do projeto e identifique os principais arquivos Python"
        )
        
        print("📊 Análise com ferramentas MCP:")
        print(result)
        
        # Cleanup
        analytics_agent.cleanup()
        await cleanup()
        
    except Exception as e:
        print(f"⚠️ Erro na integração MCP: {e}")

async def main():
    """Função principal com todas as demonstrações"""
    try:
        await demonstrate_optimizations()
        await create_optimized_agent_from_existing()
        await demonstrate_mcp_integration()
        
    except Exception as e:
        print(f"❌ Erro na demonstração: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 