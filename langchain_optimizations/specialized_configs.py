#!/usr/bin/env python3
"""
🎯 CONFIGURAÇÕES ESPECIALIZADAS DE AGENTES LANGCHAIN
====================================================

Configurações pré-definidas para diferentes tipos de agentes especializados,
utilizando todos os recursos avançados descobertos via análise MCP-LangChain.
"""

import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

from optimized_agent_base import AgentConfig
from advanced_langchain_features import AdvancedFeatureConfig

@dataclass
class SpecializedAgentTemplate:
    """Template para agente especializado"""
    name: str
    description: str
    use_cases: List[str]
    agent_config: AgentConfig
    advanced_config: AdvancedFeatureConfig
    custom_prompts: Dict[str, str]
    recommended_tools: List[str]
    performance_profile: Dict[str, Any]

class SpecializedConfigs:
    """Configurações especializadas para diferentes tipos de agentes"""
    
    @staticmethod
    def enterprise_rag() -> SpecializedAgentTemplate:
        """Agente RAG empresarial com alta precisão"""
        return SpecializedAgentTemplate(
            name="enterprise_rag",
            description="Agente RAG empresarial com alta precisão e segurança",
            use_cases=[
                "Consulta a bases de conhecimento corporativas",
                "Análise de documentos internos",
                "Suporte a decisões baseadas em dados"
            ],
            agent_config=AgentConfig(
                name="enterprise_rag",
                model="gpt-4o",
                temperature=0.1,
                max_tokens=4000,
                enable_memory=True,
                memory_type="summary",
                enable_cache=True,
                cache_ttl=7200,
                max_retries=5
            ),
            advanced_config=AdvancedFeatureConfig(
                enable_lcel_chains=True,
                enable_vector_store=True,
                enable_rag=True,
                embedding_model="text-embedding-3-large",
                chunk_size=800,
                retriever_k=10
            ),
            custom_prompts={
                "system": "Você é um assistente corporativo especializado em análise de documentos empresariais.",
                "rag": "Com base nos documentos fornecidos, analise cuidadosamente a questão."
            },
            recommended_tools=["document_analyzer", "compliance_checker"],
            performance_profile={
                "accuracy_priority": "high",
                "security_level": "high"
            }
        )
    
    @staticmethod
    def creative_writing() -> SpecializedAgentTemplate:
        """Agente de escrita criativa"""
        return SpecializedAgentTemplate(
            name="creative_writing",
            description="Agente especializado em escrita criativa e narrativa",
            use_cases=[
                "Criação de conteúdo narrativo",
                "Desenvolvimento de personagens",
                "Copywriting criativo"
            ],
            agent_config=AgentConfig(
                name="creative_writing",
                model="gpt-4o",
                temperature=0.8,
                max_tokens=8000,
                enable_memory=True,
                memory_type="buffer",
                enable_cache=False,
                enable_streaming=True
            ),
            advanced_config=AdvancedFeatureConfig(
                enable_lcel_chains=True,
                enable_streaming=True,
                enable_rag=False,
                chunk_size=1500
            ),
            custom_prompts={
                "system": "Você é um escritor criativo especializado em narrativas envolventes.",
                "story": "Desenvolva uma história baseada em: {prompt}"
            },
            recommended_tools=["story_analyzer", "character_generator"],
            performance_profile={
                "creativity_priority": "very_high",
                "originality": "very_high"
            }
        )
    
    @staticmethod
    def code_analysis() -> SpecializedAgentTemplate:
        """Agente de análise de código"""
        return SpecializedAgentTemplate(
            name="code_analysis",
            description="Agente especializado em análise e revisão de código",
            use_cases=[
                "Code review automatizado",
                "Detecção de bugs e vulnerabilidades",
                "Sugestões de otimização"
            ],
            agent_config=AgentConfig(
                name="code_analysis",
                model="gpt-4o",
                temperature=0.1,
                max_tokens=4000,
                enable_memory=True,
                memory_type="summary",
                enable_cache=True,
                enable_streaming=False
            ),
            advanced_config=AdvancedFeatureConfig(
                enable_lcel_chains=True,
                enable_vector_store=True,
                enable_rag=True,
                chunk_size=800,
                retriever_k=12
            ),
            custom_prompts={
                "system": "Você é um especialista em análise de código e arquitetura de software.",
                "review": "Realize uma revisão completa do código: {code}"
            },
            recommended_tools=["static_analyzer", "vulnerability_scanner"],
            performance_profile={
                "technical_accuracy": "very_high",
                "security_focus": "very_high"
            }
        )

    @staticmethod
    def get_all_configs() -> Dict[str, SpecializedAgentTemplate]:
        """Obter todas as configurações"""
        return {
            "enterprise_rag": SpecializedConfigs.enterprise_rag(),
            "creative_writing": SpecializedConfigs.creative_writing(),
            "code_analysis": SpecializedConfigs.code_analysis()
        } 