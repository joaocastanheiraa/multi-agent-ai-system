#!/usr/bin/env python3
"""
🚀 RECURSOS AVANÇADOS LANGCHAIN DESCOBERTOS VIA MCP
====================================================

Implementação de funcionalidades avançadas do LangChain que não estavam
sendo utilizadas, descobertas através da análise MCP-LangChain.

Funcionalidades incluídas:
- LangChain Expression Language (LCEL) Chains
- Output Parsers avançados
- Vector Stores e Retrievers
- Document Loaders e Text Splitters
- Prompt Templates avançados
- Streaming e callbacks especializados
- Ferramentas customizadas
- RAG (Retrieval Augmented Generation)
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Callable, Tuple
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

# LangChain Core imports
from langchain_core.runnables import (
    RunnablePassthrough, 
    RunnableLambda, 
    RunnableParallel,
    RunnableBranch
)
from langchain_core.output_parsers import (
    JsonOutputParser,
    PydanticOutputParser,
    StrOutputParser
)
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.embeddings import Embeddings
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import StreamingStdOutCallbackHandler

# LangChain imports
from langchain.chains import LLMChain, SequentialChain, TransformChain
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter
)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools import BaseTool, StructuredTool
from langchain.agents import AgentType, initialize_agent
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from pydantic import BaseModel, Field

# Import da base otimizada
from optimized_agent_base import OptimizedAgentBase, AgentConfig

logger = logging.getLogger(__name__)

@dataclass
class AdvancedFeatureConfig:
    """Configuração para recursos avançados"""
    enable_lcel_chains: bool = True
    enable_vector_store: bool = True
    enable_streaming: bool = True
    enable_advanced_prompts: bool = True
    enable_rag: bool = True
    enable_custom_tools: bool = True
    vector_store_type: str = "in_memory"  # in_memory, faiss, chroma
    embedding_model: str = "text-embedding-3-small"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retriever_k: int = 4

class AdvancedOutputParser:
    """Parser de saída avançado com múltiplas estratégias"""
    
    def __init__(self, parser_type: str = "json"):
        self.parser_type = parser_type
        self.parsers = {
            "json": JsonOutputParser(),
            "string": StrOutputParser(),
            "structured": self._create_structured_parser()
        }
    
    def _create_structured_parser(self):
        """Criar parser estruturado personalizado"""
        class ResponseModel(BaseModel):
            answer: str = Field(description="Resposta principal")
            confidence: float = Field(description="Nível de confiança (0-1)")
            sources: List[str] = Field(description="Fontes utilizadas", default=[])
            metadata: Dict[str, Any] = Field(description="Metadados adicionais", default={})
        
        return PydanticOutputParser(pydantic_object=ResponseModel)
    
    def get_parser(self, parser_type: str = None):
        """Obter parser específico"""
        return self.parsers.get(parser_type or self.parser_type, self.parsers["json"])

class AdvancedPromptTemplates:
    """Templates de prompt avançados"""
    
    @staticmethod
    def create_conversational_template():
        """Template para conversação com histórico"""
        return ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "Você é um assistente especializado. Use o contexto fornecido "
                "e o histórico da conversa para dar respostas precisas e úteis."
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ])
    
    @staticmethod
    def create_rag_template():
        """Template para RAG (Retrieval Augmented Generation)"""
        return ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "Use as seguintes informações do contexto para responder à pergunta. "
                "Se a informação não estiver no contexto, diga que não sabe.\n\n"
                "Contexto: {context}"
            ),
            HumanMessagePromptTemplate.from_template("Pergunta: {question}")
        ])
    
    @staticmethod
    def create_chain_of_thought_template():
        """Template para Chain of Thought reasoning"""
        return ChatPromptTemplate.from_template(
            "Analise a seguinte questão passo a passo:\n\n"
            "Questão: {question}\n\n"
            "Pense através do problema:\n"
            "1. Primeiro, identifique os elementos-chave\n"
            "2. Depois, considere as relações entre eles\n"
            "3. Finalmente, chegue a uma conclusão lógica\n\n"
            "Resposta estruturada:"
        )

class AdvancedVectorStore:
    """Sistema de vector store avançado"""
    
    def __init__(self, config: AdvancedFeatureConfig):
        self.config = config
        self.embeddings = OpenAIEmbeddings(model=config.embedding_model)
        self.vector_store = None
        self.retriever = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap
        )
    
    async def initialize(self):
        """Inicializar vector store"""
        if self.config.vector_store_type == "in_memory":
            self.vector_store = InMemoryVectorStore(embedding=self.embeddings)
        # Adicionar outros tipos conforme necessário
        
        if self.vector_store:
            self.retriever = self.vector_store.as_retriever(
                search_kwargs={"k": self.config.retriever_k}
            )
    
    async def add_documents(self, documents: List[Document]):
        """Adicionar documentos ao vector store"""
        if not self.vector_store:
            await self.initialize()
        
        # Dividir documentos em chunks
        split_docs = self.text_splitter.split_documents(documents)
        
        # Adicionar ao vector store
        await self.vector_store.aadd_documents(split_docs)
        
        logger.info(f"Adicionados {len(split_docs)} chunks ao vector store")
    
    async def similarity_search(self, query: str, k: int = None) -> List[Document]:
        """Busca por similaridade"""
        if not self.vector_store:
            await self.initialize()
        
        return await self.vector_store.asimilarity_search(
            query, k=k or self.config.retriever_k
        )

class LCELChainBuilder:
    """Construtor de chains usando LCEL (LangChain Expression Language)"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.output_parser = AdvancedOutputParser()
    
    def create_simple_chain(self, prompt_template: ChatPromptTemplate):
        """Chain simples: prompt | llm | parser"""
        return (
            prompt_template 
            | self.llm 
            | self.output_parser.get_parser("string")
        )
    
    def create_parallel_chain(self, prompts: Dict[str, ChatPromptTemplate]):
        """Chain paralelo para múltiplas tarefas"""
        parallel_chains = {}
        for name, prompt in prompts.items():
            parallel_chains[name] = prompt | self.llm | StrOutputParser()
        
        return RunnableParallel(parallel_chains)
    
    def create_conditional_chain(self, conditions: List[Tuple[Callable, Any]]):
        """Chain condicional usando RunnableBranch"""
        branches = []
        for condition, chain in conditions:
            branches.append((condition, chain))
        
        # Último elemento é o default
        default = branches[-1][1] if branches else self.llm
        return RunnableBranch(*branches[:-1], default)
    
    def create_rag_chain(self, retriever: BaseRetriever):
        """Chain RAG completo"""
        rag_template = AdvancedPromptTemplates.create_rag_template()
        
        return (
            {
                "context": retriever | self._format_docs,
                "question": RunnablePassthrough()
            }
            | rag_template
            | self.llm
            | StrOutputParser()
        )
    
    def _format_docs(self, docs: List[Document]) -> str:
        """Formatar documentos para contexto"""
        return "\n\n".join(doc.page_content for doc in docs)

class AdvancedStreamingHandler(StreamingStdOutCallbackHandler):
    """Handler de streaming avançado"""
    
    def __init__(self, callback_func: Optional[Callable] = None):
        super().__init__()
        self.callback_func = callback_func
        self.tokens = []
    
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Processar novo token"""
        self.tokens.append(token)
        if self.callback_func:
            self.callback_func(token)
        super().on_llm_new_token(token, **kwargs)
    
    def get_full_response(self) -> str:
        """Obter resposta completa"""
        return "".join(self.tokens)

class CustomTool(BaseTool):
    """Ferramenta customizada base"""
    
    name: str = "custom_tool"
    description: str = "Ferramenta customizada"
    
    def _run(self, query: str) -> str:
        """Executar ferramenta"""
        return f"Resultado para: {query}"
    
    async def _arun(self, query: str) -> str:
        """Executar ferramenta assincronamente"""
        return self._run(query)

class DocumentProcessingTools:
    """Ferramentas para processamento de documentos"""
    
    @staticmethod
    def create_text_analysis_tool():
        """Ferramenta para análise de texto"""
        def analyze_text(text: str) -> Dict[str, Any]:
            """Analisar texto e retornar métricas"""
            words = text.split()
            sentences = text.split('.')
            
            return {
                "word_count": len(words),
                "sentence_count": len(sentences),
                "avg_words_per_sentence": len(words) / len(sentences) if sentences else 0,
                "character_count": len(text)
            }
        
        return StructuredTool.from_function(
            func=analyze_text,
            name="text_analyzer",
            description="Analyze text and return metrics"
        )
    
    @staticmethod
    def create_document_summarizer_tool(llm: ChatOpenAI):
        """Ferramenta para sumarização de documentos"""
        def summarize_document(text: str) -> str:
            """Sumarizar documento"""
            prompt = ChatPromptTemplate.from_template(
                "Resuma o seguinte texto em 3-5 frases principais:\n\n{text}"
            )
            chain = prompt | llm | StrOutputParser()
            return chain.invoke({"text": text})
        
        return StructuredTool.from_function(
            func=summarize_document,
            name="document_summarizer",
            description="Summarize long documents into key points"
        )

class AdvancedLangChainAgent(OptimizedAgentBase):
    """
    Agente LangChain com recursos avançados descobertos via MCP
    """
    
    def __init__(self, config: AgentConfig, advanced_config: AdvancedFeatureConfig = None):
        super().__init__(config)
        self.advanced_config = advanced_config or AdvancedFeatureConfig()
        
        # Componentes avançados
        self.vector_store = None
        self.chain_builder = None
        self.streaming_handler = None
        self.custom_tools = []
        
        # Inicializar componentes
        asyncio.create_task(self._initialize_advanced_features())
    
    async def _initialize_advanced_features(self):
        """Inicializar recursos avançados"""
        try:
            # Vector Store
            if self.advanced_config.enable_vector_store:
                self.vector_store = AdvancedVectorStore(self.advanced_config)
                await self.vector_store.initialize()
            
            # LCEL Chain Builder
            if self.advanced_config.enable_lcel_chains:
                self.chain_builder = LCELChainBuilder(self.llm)
            
            # Streaming Handler
            if self.advanced_config.enable_streaming:
                self.streaming_handler = AdvancedStreamingHandler()
            
            # Custom Tools
            if self.advanced_config.enable_custom_tools:
                self.custom_tools = [
                    DocumentProcessingTools.create_text_analysis_tool(),
                    DocumentProcessingTools.create_document_summarizer_tool(self.llm)
                ]
            
            logger.info("Recursos avançados inicializados com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar recursos avançados: {e}")
    
    async def _process_core_logic(self, input_text: str, context: Dict) -> str:
        """Lógica de processamento com recursos avançados"""
        
        # Determinar tipo de processamento
        if self._is_rag_query(input_text) and self.vector_store:
            return await self._process_rag_query(input_text, context)
        elif self._is_analysis_query(input_text):
            return await self._process_analysis_query(input_text, context)
        else:
            return await self._process_standard_query(input_text, context)
    
    def _is_rag_query(self, input_text: str) -> bool:
        """Verificar se é uma query RAG"""
        rag_keywords = ["buscar", "encontrar", "documento", "arquivo", "informação"]
        return any(keyword in input_text.lower() for keyword in rag_keywords)
    
    def _is_analysis_query(self, input_text: str) -> bool:
        """Verificar se é uma query de análise"""
        analysis_keywords = ["analisar", "análise", "métricas", "estatísticas"]
        return any(keyword in input_text.lower() for keyword in analysis_keywords)
    
    async def _process_rag_query(self, input_text: str, context: Dict) -> str:
        """Processar query RAG"""
        if not self.vector_store or not self.chain_builder:
            return "RAG não está configurado"
        
        # Buscar documentos relevantes
        docs = await self.vector_store.similarity_search(input_text)
        
        if not docs:
            return "Não foram encontrados documentos relevantes"
        
        # Criar chain RAG
        rag_chain = self.chain_builder.create_rag_chain(self.vector_store.retriever)
        
        # Executar chain
        result = await rag_chain.ainvoke(input_text)
        
        return result
    
    async def _process_analysis_query(self, input_text: str, context: Dict) -> str:
        """Processar query de análise"""
        if not self.custom_tools:
            return "Ferramentas de análise não estão disponíveis"
        
        # Usar ferramenta de análise de texto
        analysis_tool = self.custom_tools[0]  # text_analyzer
        
        # Extrair texto a ser analisado do input
        text_to_analyze = self._extract_text_from_input(input_text)
        
        if text_to_analyze:
            result = await analysis_tool.arun(text_to_analyze)
            return f"Análise do texto:\n{json.dumps(result, indent=2, ensure_ascii=False)}"
        else:
            return "Não foi possível extrair texto para análise"
    
    async def _process_standard_query(self, input_text: str, context: Dict) -> str:
        """Processar query padrão com LCEL"""
        if not self.chain_builder:
            return await super()._process_core_logic(input_text, context)
        
        # Usar template conversacional
        template = AdvancedPromptTemplates.create_conversational_template()
        
        # Criar chain simples
        chain = self.chain_builder.create_simple_chain(template)
        
        # Preparar input
        chain_input = {
            "input": input_text,
            "chat_history": context.get("chat_history", [])
        }
        
        # Executar com streaming se habilitado
        if self.streaming_handler:
            # Para streaming, usar invoke normal e capturar tokens
            result = await chain.ainvoke(chain_input)
        else:
            result = await chain.ainvoke(chain_input)
        
        return result
    
    def _extract_text_from_input(self, input_text: str) -> Optional[str]:
        """Extrair texto para análise do input"""
        # Lógica simples - pode ser melhorada
        if "analisar:" in input_text.lower():
            return input_text.split("analisar:", 1)[1].strip()
        return None
    
    async def add_knowledge_documents(self, documents: List[Document]):
        """Adicionar documentos à base de conhecimento"""
        if self.vector_store:
            await self.vector_store.add_documents(documents)
            logger.info(f"Adicionados {len(documents)} documentos à base de conhecimento")
        else:
            logger.warning("Vector store não está inicializado")
    
    def get_advanced_metrics(self) -> Dict[str, Any]:
        """Obter métricas avançadas"""
        base_metrics = self.get_metrics()
        
        advanced_metrics = {
            "vector_store_enabled": self.vector_store is not None,
            "lcel_chains_enabled": self.chain_builder is not None,
            "streaming_enabled": self.streaming_handler is not None,
            "custom_tools_count": len(self.custom_tools),
            "advanced_features": {
                "rag": self.advanced_config.enable_rag,
                "vector_store": self.advanced_config.enable_vector_store,
                "streaming": self.advanced_config.enable_streaming,
                "custom_tools": self.advanced_config.enable_custom_tools
            }
        }
        
        return {**base_metrics, **advanced_metrics}

class AdvancedAgentFactory:
    """Factory para criar agentes com recursos avançados"""
    
    @staticmethod
    def create_rag_agent(name: str = "rag_agent") -> AdvancedLangChainAgent:
        """Criar agente especializado em RAG"""
        config = AgentConfig(
            name=name,
            temperature=0.3,
            enable_memory=True,
            memory_type="summary",
            enable_cache=True
        )
        
        advanced_config = AdvancedFeatureConfig(
            enable_rag=True,
            enable_vector_store=True,
            enable_lcel_chains=True,
            chunk_size=500,
            retriever_k=5
        )
        
        return AdvancedLangChainAgent(config, advanced_config)
    
    @staticmethod
    def create_analysis_agent(name: str = "analysis_agent") -> AdvancedLangChainAgent:
        """Criar agente especializado em análise"""
        config = AgentConfig(
            name=name,
            temperature=0.1,
            enable_memory=True,
            enable_cache=True
        )
        
        advanced_config = AdvancedFeatureConfig(
            enable_custom_tools=True,
            enable_lcel_chains=True,
            enable_streaming=True
        )
        
        return AdvancedLangChainAgent(config, advanced_config)
    
    @staticmethod
    def create_streaming_agent(name: str = "streaming_agent") -> AdvancedLangChainAgent:
        """Criar agente com streaming avançado"""
        config = AgentConfig(
            name=name,
            enable_streaming=True,
            temperature=0.7
        )
        
        advanced_config = AdvancedFeatureConfig(
            enable_streaming=True,
            enable_lcel_chains=True,
            enable_advanced_prompts=True
        )
        
        return AdvancedLangChainAgent(config, advanced_config)

# Exemplo de uso e testes
async def demonstrate_advanced_features():
    """Demonstrar recursos avançados"""
    print("🚀 DEMONSTRAÇÃO DE RECURSOS AVANÇADOS LANGCHAIN")
    print("=" * 60)
    
    # 1. Criar agente RAG
    print("\n1️⃣ CRIANDO AGENTE RAG")
    print("-" * 30)
    rag_agent = AdvancedAgentFactory.create_rag_agent()
    
    # Adicionar documentos de exemplo
    docs = [
        Document(page_content="Python é uma linguagem de programação de alto nível.", 
                metadata={"source": "doc1"}),
        Document(page_content="LangChain é um framework para desenvolvimento de aplicações com LLMs.",
                metadata={"source": "doc2"})
    ]
    
    await rag_agent.add_knowledge_documents(docs)
    
    # Testar query RAG
    rag_result = await rag_agent.process_input("Buscar informações sobre Python")
    print(f"Resultado RAG: {rag_result}")
    
    # 2. Criar agente de análise
    print("\n2️⃣ CRIANDO AGENTE DE ANÁLISE")
    print("-" * 30)
    analysis_agent = AdvancedAgentFactory.create_analysis_agent()
    
    # Testar análise
    analysis_result = await analysis_agent.process_input(
        "Analisar: Este é um texto de exemplo para análise de métricas."
    )
    print(f"Resultado Análise: {analysis_result}")
    
    # 3. Métricas avançadas
    print("\n3️⃣ MÉTRICAS AVANÇADAS")
    print("-" * 30)
    metrics = rag_agent.get_advanced_metrics()
    print(json.dumps(metrics, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(demonstrate_advanced_features()) 