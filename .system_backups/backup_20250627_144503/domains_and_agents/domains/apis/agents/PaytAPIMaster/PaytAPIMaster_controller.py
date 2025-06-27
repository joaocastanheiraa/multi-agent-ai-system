#!/usr/bin/env python3
"""
🚀 PAYTAPIMASTER - CONTROLLER OTIMIZADO
Migração automática para LangChain otimizado
Gerado em: 2025-06-25 18:16:40
Domínio: apis | Configuração: enterprise_rag
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Imports das otimizações LangChain
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "langchain_optimizations"))

from optimized_agent_base import OptimizedAgentBase, AgentConfig
from advanced_langchain_features import AdvancedLangChainAgent, AdvancedFeatureConfig
from specialized_configs import SpecializedConfigs
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PaytapimasterOutput(BaseModel):
    """Estrutura de saída otimizada"""
    result: str = Field(description="Resultado principal")
    analysis: List[str] = Field(description="Análise detalhada", default_factory=list)
    recommendations: List[str] = Field(description="Recomendações", default_factory=list)
    confidence_score: float = Field(description="Score de confiança (0-10)", default=8.0)
    metadata: Dict[str, Any] = Field(description="Metadados", default_factory=dict)

class OptimizedPaytapimasterController:
    """🚀 Controller otimizado com todas as funcionalidades LangChain avançadas"""
    
    def __init__(self):
        self.agent_name = "PaytAPIMaster_optimized"
        self.domain = "apis"
        
        # Configuração especializada
        self.config = getattr(SpecializedConfigs, "enterprise_rag")()
        
        # Agent otimizado
        self.agent = AdvancedLangChainAgent(
            config=self.config.agent_config,
            advanced_config=self.config.advanced_config
        )
        
        # Parser estruturado
        self.output_parser = PydanticOutputParser(pydantic_object=PaytapimasterOutput)
        
        # Configurar prompt
        self.setup_optimized_prompt()
        
        # Métricas
        self.performance_metrics = {
            'total_executions': 0,
            'average_response_time': 0,
            'cache_hit_rate': 0,
            'success_rate': 0
        }
        
        logger.info(f"🚀 {self.agent_name} CONTROLLER OTIMIZADO INICIALIZADO")
    
    def setup_optimized_prompt(self):
        """Configura prompt otimizado"""
        system_prompt = """Você é PAYTAPIMASTER, um especialista em integração de APIs.
Sua função é ajudar com consultas, integrações e otimização de APIs.
Forneça informações técnicas precisas e soluções práticas.

INSTRUÇÕES DE OUTPUT:
{format_instructions}

OTIMIZAÇÕES ATIVAS:
- Cache inteligente para respostas similares
- Memory system para contexto entre conversas
- Streaming para feedback em tempo real
- Observabilidade para métricas de performance
- Error handling para robustez máxima

INSTRUÇÕES DE OUTPUT:
{format_instructions}

OTIMIZAÇÕES ATIVAS:
- Cache inteligente para performance
- Memory system para contexto
- Streaming para UX
- Observabilidade para métricas
- Error handling robusto
"""
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ]).partial(format_instructions=self.output_parser.get_format_instructions())
    
    async def execute_optimized(self, request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """🚀 Execução otimizada principal"""
        start_time = datetime.now()
        execution_id = f"{self.agent_name}_{int(start_time.timestamp())}"
        
        try:
            logger.info(f"🧠 Executando {self.agent_name}: {request[:50]}...")
            
            # Preparar contexto
            chat_history = []
            if context and 'chat_history' in context:
                chat_history.extend(context['chat_history'])
            
            # Chain otimizada
            chain = self.prompt_template | self.agent.llm | self.output_parser
            
            # Executar
            result = await chain.ainvoke({
                "input": request,
                "chat_history": chat_history
            })
            
            # Métricas
            response_time = (datetime.now() - start_time).total_seconds()
            self._update_metrics(response_time, True)
            
            return {
                'success': True,
                'execution_id': execution_id,
                'agent_name': self.agent_name,
                'domain': self.domain,
                'result': result.dict() if hasattr(result, 'dict') else result,
                'response_time': response_time,
                'optimizations_active': self._get_active_optimizations(),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds()
            self._update_metrics(response_time, False)
            
            logger.error(f"❌ Erro em {self.agent_name}: {str(e)}")
            
            return {
                'success': False,
                'execution_id': execution_id,
                'agent_name': self.agent_name,
                'error': str(e),
                'response_time': response_time,
                'timestamp': datetime.now().isoformat()
            }
    
    def _update_metrics(self, response_time: float, success: bool):
        """Atualiza métricas de performance"""
        self.performance_metrics['total_executions'] += 1
        
        # Média de tempo
        total = self.performance_metrics['total_executions']
        current_avg = self.performance_metrics['average_response_time']
        self.performance_metrics['average_response_time'] = (
            (current_avg * (total - 1) + response_time) / total
        )
        
        # Taxa de sucesso
        if success:
            current_success_rate = self.performance_metrics['success_rate']
            self.performance_metrics['success_rate'] = (
                (current_success_rate * (total - 1) + 1) / total
            )
    
    def _get_active_optimizations(self) -> List[str]:
        """Lista de otimizações ativas"""
        active = []
        if self.config.agent_config.enable_cache:
            active.append("Cache Inteligente")
        if self.config.agent_config.memory_type != "none":
            active.append("Memory System")
        if self.config.advanced_config.enable_streaming:
            active.append("Streaming")
        if self.config.advanced_config.enable_rag:
            active.append("RAG")
        active.extend(["Observabilidade", "Error Handling", "Output Estruturado"])
        return active

# Instância global otimizada
optimized_PaytAPIMaster = OptimizedPaytapimasterController()

async def run_PaytAPIMaster_optimized(request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """🚀 Função principal otimizada"""
    return await optimized_PaytAPIMaster.execute_optimized(request, context)

# Compatibilidade com código existente
def run_PaytAPIMaster(messages: List[BaseMessage]) -> Dict[str, Any]:
    """🔄 Função de compatibilidade"""
    user_message = ""
    for msg in messages:
        if isinstance(msg, HumanMessage):
            user_message = msg.content
            break
    
    if not user_message:
        return {'success': False, 'error': 'Nenhuma mensagem encontrada'}
    
    try:
        result = asyncio.run(run_PaytAPIMaster_optimized(user_message))
        
        if result['success']:
            ai_response = AIMessage(content=str(result['result']))
            return {
                'success': True,
                'agent_name': result['agent_name'],
                'messages': messages + [ai_response],
                'response_time': result['response_time'],
                'optimizations_used': result['optimizations_active'],
                'timestamp': result['timestamp']
            }
        else:
            return result
    except Exception as e:
        return {
            'success': False,
            'error': f'Erro na execução: {str(e)}',
            'agent_name': 'PaytAPIMaster_optimized'
        }

if __name__ == "__main__":
    async def test_controller():
        print(f"🧪 TESTANDO {optimized_PaytAPIMaster.agent_name}")
        result = await run_PaytAPIMaster_optimized("Teste do controller otimizado")
        print(f"✅ Sucesso: {result['success']}")
        print(f"⏱️ Tempo: {result.get('response_time', 0):.3f}s")
        print(f"🚀 Otimizações: {', '.join(result.get('optimizations_active', []))}")
    
    asyncio.run(test_controller())
