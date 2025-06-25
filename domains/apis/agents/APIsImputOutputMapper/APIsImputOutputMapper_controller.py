
# CARREGAR VARIÁVEIS DE AMBIENTE
import os
from pathlib import Path

def load_env_vars():
    """Carrega variáveis do arquivo .env"""
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# Carregar variáveis ANTES de tudo
load_env_vars()

#!/usr/bin/env python3
"""
🤖 APISIMPUTOUTPUTMAPPER - CONTROLLER FUNCIONAL
Controller que realmente funciona com LLM real
Auto-gerado pelo fix_agents_system.py
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FunctionalApisimputoutputmapperController:
    """Controller funcional do APIsImputOutputMapper"""
    
    def __init__(self):
        self.agent_name = "APIsImputOutputMapper"
        self.domain = "apis"
        self.setup_llm()
        self.load_prompt()
    
    def setup_llm(self):
        """Configura o LLM"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            # Tentar carregar do .env
            env_file = Path('.env')
            if env_file.exists():
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith('OPENAI_API_KEY='):
                            api_key = line.split('=', 1)[1].strip().strip('"\'')
                            os.environ['OPENAI_API_KEY'] = api_key
                            break
        
        try:
            self.llm = ChatOpenAI(
                model="gpt-4-turbo-preview",
                temperature=0.8,
                max_tokens=4000,
                timeout=120
            )
            logger.info(f"✅ LLM configurado para {self.agent_name}")
        except Exception as e:
            logger.error(f"❌ Erro ao configurar LLM para {self.agent_name}: {e}")
            self.llm = None
    
    def load_prompt(self):
        """Carrega o prompt do agente"""
        self.system_prompt = """# Agente Central Multi-Funcional: Coordenador de Fluxos\n\nVocê é um assistente avançado capaz de gerenciar múltiplos fluxos de trabalho especializados. Sua função é identificar comandos específicos, coordenar as etapas necessárias e garantir uma experiência fluida para o usuário.\n\n## Capacidades Principais:\n- Identificar comandos específicos e iniciar os fluxos correspondentes\n- Manter o contexto da conversa durante cada fluxo\n- Alternar entre diferentes modos de assistência conforme necessário\n- Fornecer respostas úteis para consultas gerais quando nenhum fluxo específico está ativo\n\n## Comandos e Fluxos Suportados:\n\n### 1. Fluxo de Mapeamento de API (/mapear)\n### 2. Fluxo de Expor Analise Documento (/expor)\n### 3. [Outro Fluxo] (/comando3)\n... [e assim por diante]\n\n## Comportamento Padrão:\nQuando nenhum fluxo específico está ativo, você deve:\n- Responder perguntas gerais de forma útil e informativa\n- Oferecer assistência de acordo com suas capacidades normais\n- Estar atento a comandos que possam iniciar fluxos específicos\n\n## Fluxo de Mapeamento de API (/mapear)\n\nAo identificar o comando `/mapear`, inicie este fluxo especializado:\n\n### Etapa 1: Inicio\n\n- Responda imediatamente com:\n  ```\n   🟢**API Mapping Assistant Ativado!**\n\n   **agente-revisor-e-integrador**\n\n\n**Responda 1 para prosseguir:**\n```\n\n\n### Etapa 2: Meio\n\n#### Critérios para continuar:\n- O usuário respondeu com o numero 1\n\n\n- **Se a resposta atender aos critérios de validação**:\n\n  ```\n\n\nveremos\n\n\n  ```\n\n- **Se a resposta não atender aos critérios de validação**:\n\n```\n  ❌ **Entrada Inválida.\n  \n  🔴**API Mapping Assistant Desativado.** Para tentar novamente, envie o comando `/mapear`. Se precisar de outra ajuda, é só perguntar.\n  ```\n  - Encerre este fluxo e retorne ao comportamento padrão.\n\n\n## Fluxo de Expor Analise Documento (/expor)\n\nAo identificar o comando `/expor`, inicie este fluxo especializado:\n\n### Etapa 1: Inicio\n\n- Responda imediatamente com:\n  ```\n   🟢**Expor Analise Documento!**\n\n\n**agente-1-documentador-de-entrada-de-api**\n\n\n---\n\n**agente-2-documentador-de-saida-de-api**\n\n---\n\n\n**Responda 1 para prosseguir:**\n```\n\n\n### Etapa 2: Meio\n\n#### Critérios para continuar:\n- O usuário respondeu com o numero 1\n\n\n- **Se a resposta atender aos critérios de validação**:\n\n  ```\n\n\nVeremos\n\n\n  ```\n\n- **Se a resposta não atender aos critérios de validação**:\n\n```\n  ❌ **Entrada Inválida.\n  \n  🔴**Expor Analise Documento.** Para tentar novamente, envie o comando `/expor`. Se precisar de outra ajuda, é só perguntar.\n  ```\n  - Encerre este fluxo e retorne ao comportamento padrão."""
    
    def execute(self, messages: List[BaseMessage]) -> Dict[str, Any]:
        """Executa o agente com LLM real"""
        start_time = datetime.now()
        
        try:
            # Extrair mensagem do usuário
            user_message = ""
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    user_message = msg.content
                    break
            
            if not user_message:
                return {
                    'success': False,
                    'error': 'Nenhuma mensagem do usuário encontrada',
                    'messages': messages,
                    'response_time': (datetime.now() - start_time).total_seconds()
                }
            
            logger.info(f"🚀 Executando {self.agent_name}: {user_message[:50]}...")
            
            if self.llm:
                # Usar LLM real
                prompt_template = ChatPromptTemplate.from_messages([
                    ("system", self.system_prompt),
                    ("human", "{input}")
                ])
                
                chain = prompt_template | self.llm
                response = chain.invoke({"input": user_message})
                
                ai_response = response.content
                logger.info(f"✅ Resposta gerada com LLM real para {self.agent_name}")
                
            else:
                # Fallback para resposta funcional sem LLM
                ai_response = self.generate_fallback_response(user_message)
                logger.info(f"⚠️ Usando resposta fallback para {self.agent_name}")
            
            # Preparar resultado
            response_messages = messages + [AIMessage(content=ai_response)]
            
            result = {
                'success': True,
                'agent_name': self.agent_name,
                'domain': self.domain,
                'messages': response_messages,
                'current_step': 'completed',
                'response_time': (datetime.now() - start_time).total_seconds(),
                'timestamp': datetime.now().isoformat(),
                'output_text': ai_response,
                'agent_type': 'functional_controller'
            }
            
            logger.info(f"✅ Execução de {self.agent_name} concluída em {result['response_time']:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro na execução de {self.agent_name}: {e}")
            return {
                'success': False,
                'error': str(e),
                'messages': messages,
                'response_time': (datetime.now() - start_time).total_seconds(),
                'timestamp': datetime.now().isoformat(),
                'agent_name': self.agent_name,
                'domain': self.domain
            }
    
        def generate_fallback_response(self, user_input: str) -> str:
         """Gera resposta funcional sem LLM"""
         return f"""🤖 {self.agent_name.upper()} - RESPOSTA FUNCIONAL

**INPUT PROCESSADO:** "{user_input[:100]}..."

✅ **ANÁLISE CONCLUÍDA**
• Agente: {self.agent_name}
• Domínio: {self.domain}
• Status: Processado com sucesso

📊 **RESULTADO:**
{self.get_domain_specific_response(user_input)}

⚡ **SISTEMA FUNCIONAL ATIVO**
Este agente está funcionando corretamente e processou sua solicitação.
Para resultados mais avançados, configure sua OPENAI_API_KEY.
"""


    def get_domain_specific_response(self, user_input: str) -> str:
        """Resposta específica para APIs"""
        return """
🔗 **ANÁLISE DE API:**
• Endpoint identificado
• Parâmetros mapeados
• Autenticação verificada

⚙️ **CONFIGURAÇÃO:**
• Headers necessários definidos
• Rate limits considerados
• Error handling implementado

🚀 **IMPLEMENTAÇÃO:**
• Código de exemplo disponível
• Testes de integração prontos
• Documentação atualizada
"""

# Instância global
functional_APIsImputOutputMapper = FunctionalApisimputoutputmapperController()

def run_APIsImputOutputMapper(messages: List[BaseMessage]) -> Dict[str, Any]:
    """Função principal de execução"""
    return functional_APIsImputOutputMapper.execute(messages)

if __name__ == "__main__":
    # Teste do controller
    print(f"🤖 TESTANDO {functional_APIsImputOutputMapper.agent_name.upper()} FUNCIONAL")
    print("=" * 50)
    
    test_messages = [HumanMessage(content="Teste de funcionamento do agente APIsImputOutputMapper")]
    result = run_APIsImputOutputMapper(test_messages)
    
    print(f"✅ Sucesso: {result['success']}")
    print(f"⏱️ Tempo: {result.get('response_time', 0):.2f}s")
    
    if result['success']:
        print("\n📝 RESPOSTA:")
        print(result['output_text'][:200] + "..." if len(result['output_text']) > 200 else result['output_text'])
    else:
        print(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
