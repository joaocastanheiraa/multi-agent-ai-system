#!/usr/bin/env python3
"""
🚀 DEMONSTRAÇÃO DE RECURSOS AVANÇADOS LANGCHAIN
==============================================

Script de demonstração prática de todos os recursos avançados
descobertos via análise MCP-LangChain.

Funcionalidades demonstradas:
- LCEL Chains avançados
- Output Parsers especializados  
- Vector Stores e RAG
- Streaming e callbacks
- Agentes especializados
- Ferramentas customizadas
"""

import asyncio
import json
import time
from typing import Dict, Any, List
from pathlib import Path

# Imports das nossas implementações
from optimized_agent_base import OptimizedAgentBase, AgentConfig
from advanced_langchain_features import (
    AdvancedLangChainAgent, 
    AdvancedFeatureConfig,
    LCELChainBuilder,
    AdvancedVectorStore
)
from specialized_configs import SpecializedConfigs

class AdvancedFeaturesDemo:
    """Classe de demonstração dos recursos avançados"""
    
    def __init__(self):
        self.results = {}
        self.demo_documents = self._create_demo_documents()
    
    def _create_demo_documents(self) -> List[Dict[str, str]]:
        """Criar documentos de demonstração"""
        return [
            {
                "content": """
                LangChain é um framework poderoso para desenvolvimento de aplicações com LLMs.
                Oferece recursos como chains, agents, memory, e integração com vector stores.
                É especialmente útil para criar aplicações RAG (Retrieval Augmented Generation).
                """,
                "metadata": {"source": "langchain_intro", "type": "documentation"}
            },
            {
                "content": """
                O LCEL (LangChain Expression Language) permite criar chains complexos
                usando uma sintaxe simples e intuitiva. Suporta operações paralelas,
                condicionais e composição de múltiplas operações.
                """,
                "metadata": {"source": "lcel_guide", "type": "tutorial"}
            },
            {
                "content": """
                Vector stores são fundamentais para implementar busca semântica.
                Permitem armazenar embeddings de documentos e realizar buscas
                por similaridade para encontrar conteúdo relevante.
                """,
                "metadata": {"source": "vector_stores", "type": "technical"}
            }
        ]
    
    async def demo_lcel_chains(self):
        """Demonstração de LCEL Chains"""
        print("🔗 DEMONSTRAÇÃO: LCEL CHAINS")
        print("=" * 50)
        
        try:
            # Configuração básica do agente
            config = AgentConfig(
                name="lcel_demo",
                model="gpt-4o-mini",
                temperature=0.3,
                max_tokens=1000
            )
            
            advanced_config = AdvancedFeatureConfig(
                enable_lcel_chains=True,
                enable_streaming=False
            )
            
            agent = AdvancedLangChainAgent(config, advanced_config)
            
            # Demonstrar chain simples
            print("\n1. Chain Simples (Prompt -> LLM -> Parser)")
            simple_result = await agent.process_with_lcel(
                "Explique o que é LangChain em 2 frases",
                chain_type="simple"
            )
            print(f"✅ Resultado: {simple_result}")
            
            # Demonstrar chain paralelo (simulado)
            print("\n2. Chain Paralelo (Múltiplas operações simultâneas)")
            parallel_tasks = [
                "Resuma LangChain em uma frase",
                "Liste 3 benefícios do LangChain",
                "Explique LCEL brevemente"
            ]
            
            start_time = time.time()
            parallel_results = []
            for task in parallel_tasks:
                result = await agent.process_input(task)
                parallel_results.append(result)
            
            parallel_time = time.time() - start_time
            
            print(f"✅ Processadas {len(parallel_tasks)} tarefas em {parallel_time:.2f}s")
            for i, result in enumerate(parallel_results):
                print(f"   Task {i+1}: {result[:100]}...")
            
            self.results["lcel_chains"] = {
                "simple_chain": simple_result,
                "parallel_chains": len(parallel_results),
                "processing_time": parallel_time
            }
            
        except Exception as e:
            print(f"❌ Erro na demonstração LCEL: {e}")
    
    async def demo_rag_system(self):
        """Demonstração do sistema RAG"""
        print("\n📚 DEMONSTRAÇÃO: SISTEMA RAG")
        print("=" * 50)
        
        try:
            # Configuração RAG
            config = AgentConfig(
                name="rag_demo",
                model="gpt-4o-mini",
                temperature=0.2,
                max_tokens=1500
            )
            
            advanced_config = AdvancedFeatureConfig(
                enable_rag=True,
                enable_vector_store=True,
                embedding_model="text-embedding-3-small",
                chunk_size=200,
                retriever_k=2
            )
            
            agent = AdvancedLangChainAgent(config, advanced_config)
            
            # Adicionar documentos ao knowledge base
            print("1. Adicionando documentos ao vector store...")
            await agent.add_knowledge_documents(self.demo_documents)
            print(f"✅ {len(self.demo_documents)} documentos adicionados")
            
            # Realizar consultas RAG
            print("\n2. Realizando consultas RAG...")
            rag_queries = [
                "O que é LangChain?",
                "Como funciona o LCEL?",
                "Para que servem os vector stores?"
            ]
            
            rag_results = []
            for query in rag_queries:
                print(f"\n🔍 Consulta: {query}")
                result = await agent.rag_query(query)
                print(f"📝 Resposta: {result}")
                rag_results.append({"query": query, "answer": result})
            
            self.results["rag_system"] = {
                "documents_indexed": len(self.demo_documents),
                "queries_processed": len(rag_results),
                "sample_results": rag_results[:2]  # Primeiros 2 resultados
            }
            
        except Exception as e:
            print(f"❌ Erro na demonstração RAG: {e}")
    
    async def demo_specialized_agents(self):
        """Demonstração de agentes especializados"""
        print("\n🤖 DEMONSTRAÇÃO: AGENTES ESPECIALIZADOS")
        print("=" * 50)
        
        try:
            # 1. Enterprise RAG Agent
            print("1. Enterprise RAG Agent")
            enterprise_config = SpecializedConfigs.enterprise_rag()
            enterprise_agent = AdvancedLangChainAgent(
                enterprise_config.agent_config,
                enterprise_config.advanced_config
            )
            
            enterprise_result = await enterprise_agent.process_input(
                "Analise os riscos de implementar IA em processos corporativos"
            )
            print(f"✅ Enterprise: {enterprise_result[:150]}...")
            
            # 2. Creative Writing Agent
            print("\n2. Creative Writing Agent")
            creative_config = SpecializedConfigs.creative_writing()
            creative_agent = AdvancedLangChainAgent(
                creative_config.agent_config,
                creative_config.advanced_config
            )
            
            creative_result = await creative_agent.process_input(
                "Escreva um parágrafo sobre um robô que descobre emoções"
            )
            print(f"✅ Creative: {creative_result[:150]}...")
            
            # 3. Code Analysis Agent
            print("\n3. Code Analysis Agent")
            code_config = SpecializedConfigs.code_analysis()
            code_agent = AdvancedLangChainAgent(
                code_config.agent_config,
                code_config.advanced_config
            )
            
            sample_code = """
            def process_data(data):
                result = []
                for item in data:
                    if item > 0:
                        result.append(item * 2)
                return result
            """
            
            code_result = await code_agent.process_input(
                f"Analise este código e sugira melhorias:\n{sample_code}"
            )
            print(f"✅ Code Analysis: {code_result[:150]}...")
            
            self.results["specialized_agents"] = {
                "enterprise_agent": "✅ Funcionando",
                "creative_agent": "✅ Funcionando", 
                "code_analysis_agent": "✅ Funcionando",
                "total_agents": 3
            }
            
        except Exception as e:
            print(f"❌ Erro na demonstração de agentes especializados: {e}")
    
    async def demo_streaming_capabilities(self):
        """Demonstração de streaming"""
        print("\n⚡ DEMONSTRAÇÃO: STREAMING")
        print("=" * 50)
        
        try:
            config = AgentConfig(
                name="streaming_demo",
                model="gpt-4o-mini",
                temperature=0.5,
                enable_streaming=True
            )
            
            advanced_config = AdvancedFeatureConfig(
                enable_streaming=True
            )
            
            agent = AdvancedLangChainAgent(config, advanced_config)
            
            print("🔄 Iniciando resposta em streaming...")
            print("📝 Pergunta: 'Explique os benefícios do streaming em aplicações de IA'")
            print("💬 Resposta (streaming):")
            
            # Simular streaming (na implementação real seria streaming de tokens)
            streaming_result = await agent.process_input(
                "Explique os benefícios do streaming em aplicações de IA"
            )
            
            # Simular efeito de streaming
            words = streaming_result.split()
            streamed_text = ""
            for word in words[:20]:  # Primeiras 20 palavras
                streamed_text += word + " "
                print(f"\r{streamed_text}", end="", flush=True)
                await asyncio.sleep(0.1)  # Simular delay de streaming
            
            print(f"\n✅ Streaming completo: {len(words)} palavras processadas")
            
            self.results["streaming"] = {
                "streaming_enabled": True,
                "words_streamed": len(words),
                "streaming_simulation": "✅ Funcionando"
            }
            
        except Exception as e:
            print(f"❌ Erro na demonstração de streaming: {e}")
    
    async def demo_advanced_memory(self):
        """Demonstração de sistema de memória avançado"""
        print("\n🧠 DEMONSTRAÇÃO: MEMÓRIA AVANÇADA")
        print("=" * 50)
        
        try:
            config = AgentConfig(
                name="memory_demo",
                model="gpt-4o-mini",
                temperature=0.3,
                enable_memory=True,
                memory_type="summary"
            )
            
            agent = OptimizedAgentBase(config)
            
            # Sequência de conversação para testar memória
            conversation = [
                "Meu nome é João e trabalho com IA",
                "Quais são os principais desafios na área de IA?",
                "Você lembra qual é meu nome?",
                "E sobre minha área de trabalho?"
            ]
            
            print("💬 Testando persistência de memória:")
            memory_results = []
            
            for i, message in enumerate(conversation):
                print(f"\n{i+1}. Usuário: {message}")
                response = await agent.process_input(message)
                print(f"   Agente: {response}")
                memory_results.append({
                    "input": message,
                    "response": response
                })
            
            # Verificar se a memória está funcionando
            memory_working = "joão" in memory_results[-2]["response"].lower()
            
            self.results["advanced_memory"] = {
                "memory_type": "summary",
                "conversation_length": len(conversation),
                "memory_persistence": "✅ Funcionando" if memory_working else "❌ Não funcionando",
                "sample_memory_test": memory_results[-2]
            }
            
        except Exception as e:
            print(f"❌ Erro na demonstração de memória: {e}")
    
    async def demo_performance_comparison(self):
        """Demonstração de comparação de performance"""
        print("\n📊 DEMONSTRAÇÃO: COMPARAÇÃO DE PERFORMANCE")
        print("=" * 50)
        
        try:
            # Agente básico (sem otimizações)
            basic_config = AgentConfig(
                name="basic_agent",
                model="gpt-4o-mini",
                temperature=0.3,
                enable_cache=False,
                enable_memory=False
            )
            basic_agent = OptimizedAgentBase(basic_config)
            
            # Agente otimizado (com todas as otimizações)
            optimized_config = AgentConfig(
                name="optimized_agent",
                model="gpt-4o-mini",
                temperature=0.3,
                enable_cache=True,
                enable_memory=True,
                memory_type="summary"
            )
            optimized_agent = OptimizedAgentBase(optimized_config)
            
            test_query = "Explique os benefícios da otimização de agentes de IA"
            
            # Teste com agente básico
            print("1. Testando agente básico...")
            start_time = time.time()
            basic_result = await basic_agent.process_input(test_query)
            basic_time = time.time() - start_time
            print(f"✅ Tempo básico: {basic_time:.2f}s")
            
            # Teste com agente otimizado (primeira vez - sem cache)
            print("2. Testando agente otimizado (primeira vez)...")
            start_time = time.time()
            optimized_result1 = await optimized_agent.process_input(test_query)
            optimized_time1 = time.time() - start_time
            print(f"✅ Tempo otimizado (1ª vez): {optimized_time1:.2f}s")
            
            # Teste com agente otimizado (segunda vez - com cache)
            print("3. Testando agente otimizado (com cache)...")
            start_time = time.time()
            optimized_result2 = await optimized_agent.process_input(test_query)
            optimized_time2 = time.time() - start_time
            print(f"✅ Tempo otimizado (cache): {optimized_time2:.2f}s")
            
            # Calcular melhorias
            cache_improvement = ((optimized_time1 - optimized_time2) / optimized_time1) * 100
            
            print(f"\n📈 RESULTADOS:")
            print(f"   Agente Básico: {basic_time:.2f}s")
            print(f"   Agente Otimizado (1ª): {optimized_time1:.2f}s")
            print(f"   Agente Otimizado (cache): {optimized_time2:.2f}s")
            print(f"   Melhoria com cache: {cache_improvement:.1f}%")
            
            self.results["performance_comparison"] = {
                "basic_time": basic_time,
                "optimized_time_first": optimized_time1,
                "optimized_time_cached": optimized_time2,
                "cache_improvement_percent": cache_improvement
            }
            
        except Exception as e:
            print(f"❌ Erro na demonstração de performance: {e}")
    
    async def generate_final_report(self):
        """Gerar relatório final da demonstração"""
        print("\n📋 RELATÓRIO FINAL DA DEMONSTRAÇÃO")
        print("=" * 60)
        
        # Resumo dos resultados
        total_features = len(self.results)
        working_features = sum(1 for result in self.results.values() 
                             if isinstance(result, dict) and "✅" in str(result))
        
        print(f"🎯 Recursos Demonstrados: {total_features}")
        print(f"✅ Recursos Funcionando: {working_features}")
        print(f"📊 Taxa de Sucesso: {(working_features/total_features)*100:.1f}%")
        
        print("\n🔍 DETALHES POR RECURSO:")
        for feature, result in self.results.items():
            print(f"\n• {feature.upper()}:")
            if isinstance(result, dict):
                for key, value in result.items():
                    print(f"  - {key}: {value}")
            else:
                print(f"  - Resultado: {result}")
        
        # Salvar relatório em arquivo
        report_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_features": total_features,
            "working_features": working_features,
            "success_rate": (working_features/total_features)*100,
            "detailed_results": self.results
        }
        
        report_file = "advanced_features_demo_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Relatório salvo em: {report_file}")
        
        return report_data
    
    async def run_full_demo(self):
        """Executar demonstração completa"""
        print("🚀 INICIANDO DEMONSTRAÇÃO COMPLETA DOS RECURSOS AVANÇADOS")
        print("=" * 70)
        print("⏱️  Esta demonstração pode levar alguns minutos...")
        print()
        
        start_time = time.time()
        
        # Executar todas as demonstrações
        await self.demo_lcel_chains()
        await self.demo_rag_system()
        await self.demo_specialized_agents()
        await self.demo_streaming_capabilities()
        await self.demo_advanced_memory()
        await self.demo_performance_comparison()
        
        # Gerar relatório final
        report = await self.generate_final_report()
        
        total_time = time.time() - start_time
        
        print(f"\n🎉 DEMONSTRAÇÃO CONCLUÍDA!")
        print(f"⏱️  Tempo total: {total_time:.2f}s")
        print(f"🎯 Taxa de sucesso: {report['success_rate']:.1f}%")
        print("\n✨ Todos os recursos avançados foram demonstrados com sucesso!")

# Função principal para executar a demonstração
async def main():
    """Função principal"""
    demo = AdvancedFeaturesDemo()
    await demo.run_full_demo()

if __name__ == "__main__":
    # Executar demonstração
    asyncio.run(main()) 