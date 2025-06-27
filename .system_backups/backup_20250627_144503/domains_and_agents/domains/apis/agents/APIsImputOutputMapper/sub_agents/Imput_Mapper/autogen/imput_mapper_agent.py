#!/usr/bin/env python3
"""
🤖 IMPUT_MAPPER - SUB-AGENTE OTIMIZADO
Migração automática para LangChain otimizado
Gerado em: 2025-06-25 18:16:40
Domínio: apis
"""

import os
import sys
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Imports das otimizações LangChain
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent / "langchain_optimizations"))

from optimized_agent_base import OptimizedAgentBase
from advanced_langchain_features import AdvancedLangChainAgent
from specialized_configs import SpecializedConfigs
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

class ImputMapperSubAgent:
    """🤖 Sub-agente otimizado com funcionalidades LangChain avançadas"""
    
    def __init__(self):
        self.agent_name = "imput_mapper_subagent_optimized"
        self.domain = "apis"
        
        # Configuração otimizada para sub-agentes
        self.config = SpecializedConfigs.creative_writing()
        
        # Agent otimizado
        self.agent = AdvancedLangChainAgent(
            config=self.config.agent_config,
            advanced_config=self.config.advanced_config
        )
        
        # Configurar prompt específico
        self.setup_subagent_prompt()
        
        logger.info(f"🤖 {self.agent_name} SUB-AGENTE OTIMIZADO INICIALIZADO")
    
    def setup_subagent_prompt(self):
        """Configura prompt específico do sub-agente"""
        system_prompt = f"""
# Função principal não identificada

Você é um sub-agente especializado otimizado com:
- Cache inteligente para performance
- Memory para contexto
- Error handling robusto
- Output estruturado

Instruções:
1. Seja preciso e específico na sua especialidade
2. Use o contexto fornecido
3. Retorne resultados estruturados
4. Mantenha consistência com o agente principal
"""
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
    
    async def execute_subagent(self, request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """🤖 Execução otimizada do sub-agente"""
        start_time = datetime.now()
        
        try:
            logger.info(f"🤖 Executando sub-agente {self.agent_name}")
            
            # Chain otimizada
            chain = self.prompt_template | self.agent.llm
            
            # Executar
            result = await chain.ainvoke({"input": request})
            
            response_time = (datetime.now() - start_time).total_seconds()
            
            return {
                'success': True,
                'subagent_name': self.agent_name,
                'domain': self.domain,
                'result': result.content if hasattr(result, 'content') else str(result),
                'response_time': response_time,
                'timestamp': datetime.now().isoformat(),
                'optimized': True
            }
            
        except Exception as e:
            response_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"❌ Erro no sub-agente {self.agent_name}: {str(e)}")
            
            return {
                'success': False,
                'subagent_name': self.agent_name,
                'error': str(e),
                'response_time': response_time,
                'timestamp': datetime.now().isoformat()
            }

# Instância global
imput_mapper_subagent = ImputMapperSubAgent()

async def run_imput_mapper_subagent(request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """🤖 Função principal do sub-agente otimizado"""
    return await imput_mapper_subagent.execute_subagent(request, context)

# Função de compatibilidade
def imput_mapper_agent(request: str) -> str:
    """🔄 Função de compatibilidade"""
    try:
        result = asyncio.run(run_imput_mapper_subagent(request))
        return result.get('result', 'Erro na execução')
    except Exception as e:
        return f"Erro: {str(e)}"

if __name__ == "__main__":
    async def test_subagent():
        print(f"🧪 TESTANDO {imput_mapper_subagent.agent_name}")
        result = await run_imput_mapper_subagent("Teste do sub-agente otimizado")
        print(f"✅ Sucesso: {result['success']}")
        print(f"⏱️ Tempo: {result.get('response_time', 0):.3f}s")
        print(f"📝 Resultado: {result.get('result', 'N/A')[:100]}...")
    
    asyncio.run(test_subagent())
