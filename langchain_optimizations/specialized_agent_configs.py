#!/usr/bin/env python3
"""
🎯 CONFIGURAÇÕES ESPECIALIZADAS DE AGENTES LANGCHAIN
====================================================

Configurações pré-definidas para diferentes tipos de agentes especializados,
utilizando todos os recursos avançados descobertos via análise MCP-LangChain.

Tipos de agentes especializados:
- Enterprise RAG Agent
- Research Analysis Agent  
- Creative Writing Agent
- Technical Documentation Agent
- Code Analysis Agent
- Multi-Modal Agent
- Streaming Analytics Agent
"""

import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

from optimized_agent_base import AgentConfig
from advanced_langchain_features import AdvancedFeatureConfig, AdvancedLangChainAgent

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

class SpecializedAgentConfigs:
    """Configurações para agentes especializados"""
    
    @staticmethod
    def get_enterprise_rag_config() -> SpecializedAgentTemplate:
        """Configuração para Enterprise RAG Agent"""
        return SpecializedAgentTemplate(
            name="enterprise_rag_agent",
            description="Agente especializado em RAG empresarial com alta precisão e segurança",
            use_cases=[
                "Consulta a bases de conhecimento corporativas",
                "Análise de documentos internos",
                "Suporte a decisões baseadas em dados",
                "Compliance e auditoria de informações"
            ],
            agent_config=AgentConfig(
                name="enterprise_rag",
                model="gpt-4o",  # Modelo mais robusto para empresa
                temperature=0.1,  # Baixa criatividade, alta precisão
                max_tokens=4000,
                timeout=120,  # Timeout maior para consultas complexas
                enable_memory=True,
                memory_type="summary",
                enable_cache=True,
                cache_ttl=7200,  # Cache de 2 horas
                log_level="INFO",
                enable_streaming=False,  # Desabilitado para maior controle
                max_retries=5,
                retry_delay=2.0
            ),
            advanced_config=AdvancedFeatureConfig(
                enable_lcel_chains=True,
                enable_vector_store=True,
                enable_streaming=False,
                enable_advanced_prompts=True,
                enable_rag=True,
                enable_custom_tools=True,
                vector_store_type="in_memory",  # Pode ser alterado para FAISS/Chroma
                embedding_model="text-embedding-3-large",  # Embeddings de alta qualidade
                chunk_size=800,  # Chunks menores para maior precisão
                chunk_overlap=100,
                retriever_k=10  # Mais documentos para análise
            ),
            custom_prompts={
                "system": """Você é um assistente corporativo especializado em análise de documentos empresariais. 
                Suas respostas devem ser:
                - Precisas e baseadas em evidências
                - Profissionais e objetivas
                - Incluir referências às fontes
                - Considerar aspectos de compliance e segurança
                - Estruturadas e bem organizadas""",
                
                "rag": """Com base nos documentos fornecidos, analise cuidadosamente a questão e forneça uma resposta abrangente.
                
                DOCUMENTOS DE REFERÊNCIA:
                {context}
                
                QUESTÃO: {question}
                
                INSTRUÇÕES:
                1. Cite especificamente os documentos utilizados
                2. Indique o nível de confiança na resposta
                3. Destaque qualquer informação conflitante
                4. Sugira próximos passos se aplicável
                
                RESPOSTA:""",
                
                "analysis": """Realize uma análise detalhada considerando:
                - Aspectos técnicos e operacionais
                - Implicações estratégicas
                - Riscos e oportunidades
                - Recomendações práticas
                
                Questão: {input}
                Análise:"""
            },
            recommended_tools=[
                "document_analyzer",
                "compliance_checker", 
                "risk_assessor",
                "citation_generator"
            ],
            performance_profile={
                "accuracy_priority": "high",
                "speed_priority": "medium", 
                "cost_efficiency": "medium",
                "security_level": "high",
                "scalability": "high"
            }
        )
    
    @staticmethod
    def get_research_analysis_config() -> SpecializedAgentTemplate:
        """Configuração para Research Analysis Agent"""
        return SpecializedAgentTemplate(
            name="research_analysis_agent",
            description="Agente especializado em pesquisa acadêmica e análise científica",
            use_cases=[
                "Análise de papers acadêmicos",
                "Síntese de literatura científica",
                "Identificação de tendências de pesquisa",
                "Suporte à escrita acadêmica"
            ],
            agent_config=AgentConfig(
                name="research_analysis",
                model="gpt-4o",
                temperature=0.3,  # Equilibrio entre precisão e criatividade
                max_tokens=6000,  # Respostas mais longas para análises
                enable_memory=True,
                memory_type="summary",
                enable_cache=True,
                cache_ttl=14400,  # Cache de 4 horas para pesquisas
                enable_streaming=True,
                max_retries=3
            ),
            advanced_config=AdvancedFeatureConfig(
                enable_lcel_chains=True,
                enable_vector_store=True,
                enable_streaming=True,
                enable_advanced_prompts=True,
                enable_rag=True,
                enable_custom_tools=True,
                embedding_model="text-embedding-3-large",
                chunk_size=1200,  # Chunks maiores para contexto acadêmico
                chunk_overlap=200,
                retriever_k=15  # Muitos documentos para análise abrangente
            ),
            custom_prompts={
                "system": """Você é um assistente de pesquisa acadêmica especializado em análise científica.
                Suas análises devem ser:
                - Metodologicamente rigorosas
                - Baseadas em evidências científicas
                - Críticas e imparciais
                - Bem estruturadas com argumentação lógica
                - Incluir limitações e incertezas""",
                
                "literature_review": """Realize uma revisão sistemática da literatura sobre: {topic}
                
                DOCUMENTOS ANALISADOS:
                {context}
                
                ESTRUTURA DA ANÁLISE:
                1. Contexto e relevância do tema
                2. Principais achados e tendências
                3. Metodologias utilizadas
                4. Gaps de conhecimento identificados
                5. Direções futuras de pesquisa
                
                REVISÃO:""",
                
                "methodology_analysis": """Analise criticamente a metodologia apresentada:
                
                {input}
                
                Considere:
                - Validade interna e externa
                - Limitações metodológicas
                - Adequação dos métodos aos objetivos
                - Possíveis vieses
                - Sugestões de melhoria
                
                ANÁLISE METODOLÓGICA:"""
            },
            recommended_tools=[
                "citation_analyzer",
                "methodology_checker",
                "statistical_analyzer", 
                "literature_mapper"
            ],
            performance_profile={
                "accuracy_priority": "very_high",
                "depth_analysis": "very_high",
                "speed_priority": "medium",
                "cost_efficiency": "low",
                "academic_rigor": "very_high"
            }
        )
    
    @staticmethod
    def get_creative_writing_config() -> SpecializedAgentTemplate:
        """Configuração para Creative Writing Agent"""
        return SpecializedAgentTemplate(
            name="creative_writing_agent",
            description="Agente especializado em escrita criativa e conteúdo narrativo",
            use_cases=[
                "Criação de conteúdo narrativo",
                "Desenvolvimento de personagens",
                "Escrita de roteiros e histórias",
                "Copywriting criativo"
            ],
            agent_config=AgentConfig(
                name="creative_writing",
                model="gpt-4o",
                temperature=0.8,  # Alta criatividade
                max_tokens=8000,  # Textos longos e criativos
                enable_memory=True,
                memory_type="buffer",  # Memória detalhada para continuidade narrativa
                enable_cache=False,  # Evitar repetição criativa
                enable_streaming=True,
                max_retries=2
            ),
            advanced_config=AdvancedFeatureConfig(
                enable_lcel_chains=True,
                enable_vector_store=True,
                enable_streaming=True,
                enable_advanced_prompts=True,
                enable_rag=False,  # Foco na criatividade original
                enable_custom_tools=True,
                embedding_model="text-embedding-3-small",
                chunk_size=1500,
                chunk_overlap=300,
                retriever_k=5
            ),
            custom_prompts={
                "system": """Você é um escritor criativo especializado em narrativas envolventes.
                Sua escrita deve ser:
                - Imaginativa e original
                - Emocionalmente envolvente
                - Bem estruturada narrativamente
                - Rica em detalhes sensoriais
                - Adequada ao público-alvo""",
                
                "story_development": """Desenvolva uma história baseada em: {prompt}
                
                ELEMENTOS A INCLUIR:
                - Personagens bem desenvolvidos
                - Conflito central interessante
                - Ambientação rica
                - Diálogos naturais
                - Arco narrativo satisfatório
                
                ESTILO: {style}
                PÚBLICO: {audience}
                
                HISTÓRIA:""",
                
                "character_development": """Crie um personagem detalhado baseado em: {description}
                
                DESENVOLVA:
                - Aparência física
                - Personalidade e motivações
                - História pessoal
                - Conflitos internos
                - Relacionamentos
                - Arco de desenvolvimento
                
                PERSONAGEM:"""
            },
            recommended_tools=[
                "story_structure_analyzer",
                "character_consistency_checker",
                "style_advisor",
                "plot_generator"
            ],
            performance_profile={
                "creativity_priority": "very_high",
                "originality": "very_high",
                "emotional_impact": "high",
                "accuracy_priority": "medium",
                "speed_priority": "medium"
            }
        )
    
    @staticmethod
    def get_technical_documentation_config() -> SpecializedAgentTemplate:
        """Configuração para Technical Documentation Agent"""
        return SpecializedAgentTemplate(
            name="technical_documentation_agent",
            description="Agente especializado em documentação técnica e manuais",
            use_cases=[
                "Criação de documentação de APIs",
                "Manuais de usuário técnicos",
                "Guias de instalação e configuração",
                "Documentação de código"
            ],
            agent_config=AgentConfig(
                name="technical_docs",
                model="gpt-4o",
                temperature=0.2,  # Baixa criatividade, alta precisão técnica
                max_tokens=5000,
                enable_memory=True,
                memory_type="summary",
                enable_cache=True,
                cache_ttl=10800,  # Cache de 3 horas
                enable_streaming=True,
                max_retries=3
            ),
            advanced_config=AdvancedFeatureConfig(
                enable_lcel_chains=True,
                enable_vector_store=True,
                enable_streaming=True,
                enable_advanced_prompts=True,
                enable_rag=True,
                enable_custom_tools=True,
                embedding_model="text-embedding-3-large",
                chunk_size=1000,
                chunk_overlap=150,
                retriever_k=8
            ),
            custom_prompts={
                "system": """Você é um especialista em documentação técnica.
                Sua documentação deve ser:
                - Clara e concisa
                - Estruturada logicamente
                - Incluir exemplos práticos
                - Considerar diferentes níveis de expertise
                - Seguir padrões de documentação""",
                
                "api_documentation": """Documente a seguinte API: {api_spec}
                
                ESTRUTURA:
                1. Visão geral e propósito
                2. Autenticação e autorização
                3. Endpoints disponíveis
                4. Parâmetros e formato de dados
                5. Exemplos de requisições/respostas
                6. Códigos de erro
                7. Limitações e considerações
                
                DOCUMENTAÇÃO:""",
                
                "user_manual": """Crie um manual de usuário para: {product}
                
                PÚBLICO-ALVO: {audience_level}
                
                INCLUIR:
                - Pré-requisitos e instalação
                - Primeiros passos
                - Funcionalidades principais
                - Solução de problemas comuns
                - Referência rápida
                
                MANUAL:"""
            },
            recommended_tools=[
                "code_analyzer",
                "documentation_formatter",
                "example_generator",
                "accessibility_checker"
            ],
            performance_profile={
                "clarity_priority": "very_high",
                "accuracy_priority": "very_high",
                "completeness": "high",
                "usability": "very_high",
                "maintainability": "high"
            }
        )
    
    @staticmethod
    def get_code_analysis_config() -> SpecializedAgentTemplate:
        """Configuração para Code Analysis Agent"""
        return SpecializedAgentTemplate(
            name="code_analysis_agent",
            description="Agente especializado em análise e revisão de código",
            use_cases=[
                "Code review automatizado",
                "Detecção de bugs e vulnerabilidades",
                "Sugestões de otimização",
                "Análise de arquitetura de software"
            ],
            agent_config=AgentConfig(
                name="code_analysis",
                model="gpt-4o",
                temperature=0.1,  # Muito baixa para análise técnica precisa
                max_tokens=4000,
                enable_memory=True,
                memory_type="summary",
                enable_cache=True,
                cache_ttl=3600,
                enable_streaming=False,  # Análise completa antes de resposta
                max_retries=3
            ),
            advanced_config=AdvancedFeatureConfig(
                enable_lcel_chains=True,
                enable_vector_store=True,
                enable_streaming=False,
                enable_advanced_prompts=True,
                enable_rag=True,
                enable_custom_tools=True,
                embedding_model="text-embedding-3-large",
                chunk_size=800,  # Chunks menores para análise precisa
                chunk_overlap=100,
                retriever_k=12
            ),
            custom_prompts={
                "system": """Você é um especialista em análise de código e arquitetura de software.
                Suas análises devem ser:
                - Tecnicamente precisas
                - Focadas em boas práticas
                - Incluir sugestões de melhoria
                - Considerar performance e segurança
                - Seguir padrões da indústria""",
                
                "code_review": """Realize uma revisão completa do código: {code}
                
                LINGUAGEM: {language}
                CONTEXTO: {context}
                
                ANALISE:
                1. Qualidade do código
                2. Possíveis bugs ou vulnerabilidades
                3. Performance e otimizações
                4. Aderência a padrões
                5. Manutenibilidade
                6. Testes necessários
                
                REVISÃO:""",
                
                "architecture_analysis": """Analise a arquitetura do sistema: {architecture}
                
                CONSIDERE:
                - Padrões arquiteturais utilizados
                - Acoplamento e coesão
                - Escalabilidade
                - Pontos de falha
                - Sugestões de melhoria
                
                ANÁLISE ARQUITETURAL:"""
            },
            recommended_tools=[
                "static_code_analyzer",
                "vulnerability_scanner",
                "performance_profiler",
                "pattern_detector"
            ],
            performance_profile={
                "technical_accuracy": "very_high",
                "security_focus": "very_high", 
                "performance_analysis": "high",
                "best_practices": "very_high",
                "speed_priority": "medium"
            }
        )
    
    @staticmethod
    def get_all_specialized_configs() -> Dict[str, SpecializedAgentTemplate]:
        """Obter todas as configurações especializadas"""
        return {
            "enterprise_rag": SpecializedAgentConfigs.get_enterprise_rag_config(),
            "research_analysis": SpecializedAgentConfigs.get_research_analysis_config(),
            "creative_writing": SpecializedAgentConfigs.get_creative_writing_config(),
            "technical_docs": SpecializedAgentConfigs.get_technical_documentation_config(),
            "code_analysis": SpecializedAgentConfigs.get_code_analysis_config()
        }
    
    @staticmethod
    def save_configs_to_file(filepath: str = "specialized_agent_configs.json"):
        """Salvar configurações em arquivo JSON"""
        configs = SpecializedAgentConfigs.get_all_specialized_configs()
        
        # Converter para formato serializável
        serializable_configs = {}
        for name, template in configs.items():
            serializable_configs[name] = {
                "name": template.name,
                "description": template.description,
                "use_cases": template.use_cases,
                "agent_config": asdict(template.agent_config),
                "advanced_config": asdict(template.advanced_config),
                "custom_prompts": template.custom_prompts,
                "recommended_tools": template.recommended_tools,
                "performance_profile": template.performance_profile
            }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_configs, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Configurações salvas em {filepath}")
    
    @staticmethod
    def load_config_from_file(config_name: str, filepath: str = "specialized_agent_configs.json") -> Optional[SpecializedAgentTemplate]:
        """Carregar configuração específica do arquivo"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                configs = json.load(f)
            
            if config_name not in configs:
                return None
            
            config_data = configs[config_name]
            
            return SpecializedAgentTemplate(
                name=config_data["name"],
                description=config_data["description"],
                use_cases=config_data["use_cases"],
                agent_config=AgentConfig(**config_data["agent_config"]),
                advanced_config=AdvancedFeatureConfig(**config_data["advanced_config"]),
                custom_prompts=config_data["custom_prompts"],
                recommended_tools=config_data["recommended_tools"],
                performance_profile=config_data["performance_profile"]
            )
            
        except FileNotFoundError:
            print(f"❌ Arquivo {filepath} não encontrado")
            return None
        except Exception as e:
            print(f"❌ Erro ao carregar configuração: {e}")
            return None

class SpecializedAgentFactory:
    """Factory para criar agentes especializados"""
    
    @staticmethod
    def create_specialized_agent(config_name: str) -> Optional[AdvancedLangChainAgent]:
        """Criar agente especializado por nome"""
        configs = SpecializedAgentConfigs.get_all_specialized_configs()
        
        if config_name not in configs:
            print(f"❌ Configuração '{config_name}' não encontrada")
            print(f"Configurações disponíveis: {list(configs.keys())}")
            return None
        
        template = configs[config_name]
        
        # Criar agente com configurações especializadas
        agent = AdvancedLangChainAgent(
            config=template.agent_config,
            advanced_config=template.advanced_config
        )
        
        # Adicionar prompts customizados (implementação futura)
        agent.custom_prompts = template.custom_prompts
        
        print(f"✅ Agente especializado '{config_name}' criado com sucesso")
        print(f"📝 Descrição: {template.description}")
        print(f"🎯 Casos de uso: {', '.join(template.use_cases[:2])}...")
        
        return agent
    
    @staticmethod
    def list_available_configs():
        """Listar configurações disponíveis"""
        configs = SpecializedAgentConfigs.get_all_specialized_configs()
        
        print("🤖 AGENTES ESPECIALIZADOS DISPONÍVEIS")
        print("=" * 50)
        
        for name, template in configs.items():
            print(f"\n🔹 {name.upper()}")
            print(f"   📝 {template.description}")
            print(f"   🎯 Casos de uso:")
            for use_case in template.use_cases[:3]:
                print(f"      • {use_case}")
            if len(template.use_cases) > 3:
                print(f"      • ... e mais {len(template.use_cases) - 3}")
            print(f"   ⚡ Performance: {template.performance_profile}")
    
    @staticmethod
    def compare_agents(agent_names: List[str]):
        """Comparar diferentes agentes especializados"""
        configs = SpecializedAgentConfigs.get_all_specialized_configs()
        
        print("📊 COMPARAÇÃO DE AGENTES ESPECIALIZADOS")
        print("=" * 60)
        
        comparison_data = []
        for name in agent_names:
            if name in configs:
                template = configs[name]
                comparison_data.append({
                    "name": name,
                    "model": template.agent_config.model,
                    "temperature": template.agent_config.temperature,
                    "max_tokens": template.agent_config.max_tokens,
                    "cache_enabled": template.agent_config.enable_cache,
                    "streaming": template.advanced_config.enable_streaming,
                    "rag_enabled": template.advanced_config.enable_rag,
                    "embedding_model": template.advanced_config.embedding_model
                })
        
        # Exibir comparação em formato tabular
        if comparison_data:
            print(f"{'Agent':<20} {'Model':<12} {'Temp':<6} {'Tokens':<8} {'Cache':<7} {'Stream':<8} {'RAG':<5} {'Embedding'}")
            print("-" * 90)
            for data in comparison_data:
                print(f"{data['name']:<20} {data['model']:<12} {data['temperature']:<6.1f} {data['max_tokens']:<8} "
                      f"{'✓' if data['cache_enabled'] else '✗':<7} {'✓' if data['streaming'] else '✗':<8} "
                      f"{'✓' if data['rag_enabled'] else '✗':<5} {data['embedding_model']}")

# Exemplo de uso
if __name__ == "__main__":
    # Salvar todas as configurações
    SpecializedAgentConfigs.save_configs_to_file()
    
    # Listar agentes disponíveis
    SpecializedAgentFactory.list_available_configs()
    
    # Comparar alguns agentes
    print("\n")
    SpecializedAgentFactory.compare_agents([
        "enterprise_rag", 
        "research_analysis", 
        "creative_writing"
    ])
    
    # Criar um agente especializado
    print("\n")
    rag_agent = SpecializedAgentFactory.create_specialized_agent("enterprise_rag") 