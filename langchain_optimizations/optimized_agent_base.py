#!/usr/bin/env python3
"""
🚀 CLASSE BASE OTIMIZADA PARA AGENTES LANGCHAIN
===============================================

Implementação das principais otimizações descobertas via análise MCP:
- Configuração centralizada
- Memória avançada
- Observabilidade
- Cache inteligente
- Error handling robusto
- Performance otimizada
"""

import asyncio
import logging
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

@dataclass
class AgentConfig:
    """Configuração centralizada para agentes"""
    name: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 60
    enable_memory: bool = True
    memory_type: str = "buffer"  # buffer, summary, custom
    enable_cache: bool = True
    cache_ttl: int = 3600  # 1 hora
    log_level: str = "INFO"
    enable_streaming: bool = False
    max_retries: int = 3
    retry_delay: float = 1.0

class OptimizedCallbackHandler(BaseCallbackHandler):
    """Callback handler otimizado para observabilidade"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.logger = logging.getLogger(f"agent.{agent_name}")
        self.metrics = {
            "total_calls": 0,
            "total_tokens": 0,
            "avg_response_time": 0,
            "errors": 0
        }
        self.start_time = None
    
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs) -> None:
        self.start_time = time.time()
        self.metrics["total_calls"] += 1
        self.logger.info(f"LLM call started for {self.agent_name}")
    
    def on_llm_end(self, response, **kwargs) -> None:
        if self.start_time:
            duration = time.time() - self.start_time
            self.metrics["avg_response_time"] = (
                (self.metrics["avg_response_time"] * (self.metrics["total_calls"] - 1) + duration) 
                / self.metrics["total_calls"]
            )
            self.logger.info(f"LLM call completed in {duration:.2f}s")
    
    def on_llm_error(self, error: Exception, **kwargs) -> None:
        self.metrics["errors"] += 1
        self.logger.error(f"LLM error in {self.agent_name}: {error}")

class IntelligentCache:
    """Cache inteligente com TTL e estratégias avançadas"""
    
    def __init__(self, ttl: int = 3600):
        self.cache = {}
        self.ttl = ttl
        self.access_count = {}
        self.last_access = {}
    
    def _is_expired(self, key: str) -> bool:
        if key not in self.last_access:
            return True
        return time.time() - self.last_access[key] > self.ttl
    
    def get(self, key: str) -> Optional[Any]:
        if key in self.cache and not self._is_expired(key):
            self.access_count[key] = self.access_count.get(key, 0) + 1
            self.last_access[key] = time.time()
            return self.cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        self.cache[key] = value
        self.access_count[key] = 1
        self.last_access[key] = time.time()
    
    def clear_expired(self) -> None:
        expired_keys = [k for k in self.cache.keys() if self._is_expired(k)]
        for key in expired_keys:
            del self.cache[key]
            del self.access_count[key]
            del self.last_access[key]

class AdvancedMemory:
    """Sistema de memória avançado com múltiplas estratégias"""
    
    def __init__(self, memory_type: str = "buffer", max_token_limit: int = 2000, llm=None):
        self.memory_type = memory_type
        self.max_token_limit = max_token_limit
        
        if memory_type == "buffer":
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        elif memory_type == "summary" and llm:
            self.memory = ConversationSummaryMemory(
                llm=llm,
                memory_key="chat_history",
                return_messages=True,
                max_token_limit=max_token_limit
            )
        else:
            # Fallback para buffer se não tiver LLM para summary
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        
        self.context_memory = {}  # Memória de contexto personalizada
        self.session_data = {}    # Dados da sessão
    
    def add_message(self, human_message: str, ai_message: str) -> None:
        """Adicionar mensagem à memória"""
        self.memory.chat_memory.add_user_message(human_message)
        self.memory.chat_memory.add_ai_message(ai_message)
    
    def get_memory_variables(self) -> Dict[str, Any]:
        """Obter variáveis de memória"""
        return self.memory.load_memory_variables({})
    
    def set_context(self, key: str, value: Any) -> None:
        """Definir contexto personalizado"""
        self.context_memory[key] = value
    
    def get_context(self, key: str) -> Any:
        """Obter contexto personalizado"""
        return self.context_memory.get(key)
    
    def clear_memory(self) -> None:
        """Limpar memória"""
        self.memory.clear()
        self.context_memory.clear()

class OptimizedAgentBase(ABC):
    """
    Classe base otimizada para agentes LangChain
    
    Funcionalidades incluídas:
    - Configuração centralizada
    - Memória avançada
    - Cache inteligente
    - Observabilidade completa
    - Error handling robusto
    - Performance otimizada
    """
    
    def __init__(self, config: AgentConfig, tools: List = None):
        self.config = config
        self.tools = tools or []
        
        # Configurar logging
        self._setup_logging()
        
        # Inicializar callback handler primeiro
        self.callback_handler = OptimizedCallbackHandler(config.name)
        
        # Configurar LLM
        self.llm = self._create_llm()
        
        # Inicializar componentes (memória precisa do LLM para summary)
        self.cache = IntelligentCache(ttl=config.cache_ttl) if config.enable_cache else None
        self.memory = AdvancedMemory(config.memory_type, llm=self.llm) if config.enable_memory else None
        
        # Criar agente
        self.agent = self._create_agent()
        
        self.logger.info(f"Agente otimizado '{config.name}' inicializado com sucesso")
    
    def _setup_logging(self) -> None:
        """Configurar logging"""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(f"agent.{self.config.name}")
    
    def _create_llm(self) -> ChatOpenAI:
        """Criar LLM otimizado"""
        return ChatOpenAI(
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            timeout=self.config.timeout,
            streaming=self.config.enable_streaming,
            callbacks=[self.callback_handler]
        )
    
    def _create_agent(self):
        """Criar agente LangGraph otimizado"""
        if self.tools:
            return create_react_agent(self.llm, self.tools)
        return None
    
    def _generate_cache_key(self, input_text: str, context: Dict = None) -> str:
        """Gerar chave de cache"""
        context_str = json.dumps(context or {}, sort_keys=True)
        return f"{self.config.name}:{hash(input_text + context_str)}"
    
    async def _execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Executar função com retry automático"""
        last_exception = None
        
        for attempt in range(self.config.max_retries):
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                self.logger.warning(f"Tentativa {attempt + 1} falhou: {e}")
                if attempt < self.config.max_retries - 1:
                    await asyncio.sleep(self.config.retry_delay * (2 ** attempt))
        
        raise last_exception
    
    async def process_input(self, input_text: str, context: Dict = None) -> str:
        """
        Processar entrada com todas as otimizações
        """
        start_time = time.time()
        context = context or {}
        
        try:
            # Verificar cache
            cache_key = self._generate_cache_key(input_text, context)
            if self.cache:
                cached_result = self.cache.get(cache_key)
                if cached_result:
                    self.logger.info("Resultado obtido do cache")
                    return cached_result
            
            # Preparar contexto com memória
            if self.memory:
                memory_vars = self.memory.get_memory_variables()
                context.update(memory_vars)
            
            # Executar processamento personalizado
            result = await self._execute_with_retry(self._process_core_logic, input_text, context)
            
            # Salvar na memória
            if self.memory:
                self.memory.add_message(input_text, result)
            
            # Salvar no cache
            if self.cache:
                self.cache.set(cache_key, result)
            
            # Log de performance
            duration = time.time() - start_time
            self.logger.info(f"Processamento concluído em {duration:.2f}s")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Erro no processamento: {e}")
            return await self._handle_error(e, input_text, context)
    
    @abstractmethod
    async def _process_core_logic(self, input_text: str, context: Dict) -> str:
        """
        Lógica principal do agente (deve ser implementada pelas subclasses)
        """
        pass
    
    async def _handle_error(self, error: Exception, input_text: str, context: Dict) -> str:
        """
        Tratamento de erro personalizado
        """
        return f"Desculpe, ocorreu um erro ao processar sua solicitação: {type(error).__name__}"
    
    def get_metrics(self) -> Dict[str, Any]:
        """Obter métricas do agente"""
        metrics = {
            "agent_name": self.config.name,
            "callback_metrics": self.callback_handler.metrics,
            "timestamp": datetime.now().isoformat()
        }
        
        if self.cache:
            metrics["cache_stats"] = {
                "total_items": len(self.cache.cache),
                "access_counts": self.cache.access_count
            }
        
        if self.memory:
            metrics["memory_stats"] = {
                "memory_type": self.config.memory_type,
                "context_items": len(self.memory.context_memory)
            }
        
        return metrics
    
    def save_config(self, filepath: str) -> None:
        """Salvar configuração em arquivo"""
        config_dict = asdict(self.config)
        with open(filepath, 'w') as f:
            json.dump(config_dict, f, indent=2)
    
    @classmethod
    def load_config(cls, filepath: str) -> AgentConfig:
        """Carregar configuração de arquivo"""
        with open(filepath, 'r') as f:
            config_dict = json.load(f)
        return AgentConfig(**config_dict)
    
    def cleanup(self) -> None:
        """Limpeza de recursos"""
        if self.cache:
            self.cache.clear_expired()
        if self.memory:
            self.memory.clear_memory()
        self.logger.info(f"Agente '{self.config.name}' limpo")

# Exemplo de implementação concreta
class ExampleOptimizedAgent(OptimizedAgentBase):
    """Exemplo de agente otimizado"""
    
    async def _process_core_logic(self, input_text: str, context: Dict) -> str:
        """Implementação da lógica principal"""
        if self.agent:
            # Usar agente LangGraph
            response = await self.agent.ainvoke({"messages": [("user", input_text)]})
            return response['messages'][-1].content
        else:
            # Usar LLM diretamente
            messages = [HumanMessage(content=input_text)]
            response = await self.llm.ainvoke(messages)
            return response.content

# Factory para criação de agentes otimizados
class OptimizedAgentFactory:
    """Factory para criação de agentes otimizados"""
    
    @staticmethod
    def create_agent(agent_type: str, config: AgentConfig, tools: List = None) -> OptimizedAgentBase:
        """Criar agente otimizado baseado no tipo"""
        if agent_type == "example":
            return ExampleOptimizedAgent(config, tools)
        else:
            raise ValueError(f"Tipo de agente não suportado: {agent_type}")
    
    @staticmethod
    def create_from_config_file(config_file: str, agent_type: str, tools: List = None) -> OptimizedAgentBase:
        """Criar agente a partir de arquivo de configuração"""
        config = OptimizedAgentBase.load_config(config_file)
        return OptimizedAgentFactory.create_agent(agent_type, config, tools) 