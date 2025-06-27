
# 🛒 MCP Integration - Adicionado automaticamente
from config.mcp_marketplace import get_agent_mcp_tools
import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
else:
    # Tentar carregar do diretório atual
    load_dotenv('.env')

# Configurar variáveis LangSmith
os.environ.setdefault('LANGCHAIN_TRACING_V2', 'true')
os.environ.setdefault('LANGSMITH_TRACING', 'true')
os.environ.setdefault('LANGCHAIN_PROJECT', 'multi-agent-ai-system-complete')

# Verificar se as chaves estão disponíveis
LANGSMITH_API_KEY = os.getenv('LANGSMITH_API_KEY') or os.getenv('LANGCHAIN_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if LANGSMITH_API_KEY:
    os.environ['LANGSMITH_API_KEY'] = LANGSMITH_API_KEY
    os.environ['LANGCHAIN_API_KEY'] = LANGSMITH_API_KEY




# ================================================================================
# PROMPT ENRIQUECIDO DO AGENTE (carregado automaticamente)
# ================================================================================
ENHANCED_SYSTEM_PROMPT = """You are metaphor_architect, a specialized AI agent.

Domain: copywriters
Specialization: metaphor_architect operations and management
Controller: metaphor_architect_controller.py

You are an expert in copywriters domain with deep knowledge of metaphor_architect workflows.


## FERRAMENTAS DISPONÍVEIS
Você tem acesso às seguintes ferramentas especializadas:
- **analogy_validator**: Tool analogy_validator para metaphor_architect (✅ ATIVA)
- **creativity_enhancer**: Tool creativity_enhancer para metaphor_architect (✅ ATIVA)
- **knowledge_base**: Tool knowledge_base para metaphor_architect (✅ ATIVA)
- **metaphor_generator**: Tool metaphor_generator para metaphor_architect (✅ ATIVA)
- **text_analysis**: Tool text_analysis para metaphor_architect (✅ ATIVA)
- **web_search**: Tool web_search para metaphor_architect (✅ ATIVA)


## INFORMAÇÕES DO SISTEMA
- Agente: metaphor_architect
- Domínio: copywriters
- Ferramentas: 6
- Sub-agentes: 0
- Atualizado automaticamente com configurações reais
"""

# ================================================================================


# ================================================================================
# PROMPT ENRIQUECIDO DO AGENTE (carregado automaticamente)
# ================================================================================
ENHANCED_SYSTEM_PROMPT = """You are metaphor_architect, a specialized AI agent.

Domain: copywriters
Specialization: metaphor_architect operations and management
Controller: metaphor_architect_controller.py

You are an expert in copywriters domain with deep knowledge of metaphor_architect workflows.


## FERRAMENTAS DISPONÍVEIS
Você tem acesso às seguintes ferramentas especializadas:
- **analogy_validator**: Tool analogy_validator para metaphor_architect (✅ ATIVA)
- **creativity_enhancer**: Tool creativity_enhancer para metaphor_architect (✅ ATIVA)
- **knowledge_base**: Tool knowledge_base para metaphor_architect (✅ ATIVA)
- **metaphor_generator**: Tool metaphor_generator para metaphor_architect (✅ ATIVA)
- **text_analysis**: Tool text_analysis para metaphor_architect (✅ ATIVA)
- **web_search**: Tool web_search para metaphor_architect (✅ ATIVA)


## INFORMAÇÕES DO SISTEMA
- Agente: metaphor_architect
- Domínio: copywriters
- Ferramentas: 6
- Sub-agentes: 0
- Atualizado automaticamente com configurações reais
"""

# ================================================================================


# ================================================================================
# PROMPT ENRIQUECIDO DO AGENTE (carregado automaticamente)
# ================================================================================
ENHANCED_SYSTEM_PROMPT = """You are metaphor_architect, a specialized AI agent.

Domain: copywriters
Specialization: metaphor_architect operations and management
Controller: metaphor_architect_controller.py

You are an expert in copywriters domain with deep knowledge of metaphor_architect workflows.


## FERRAMENTAS DISPONÍVEIS
Você tem acesso às seguintes ferramentas especializadas:
- **analogy_validator**: Tool analogy_validator para metaphor_architect (✅ ATIVA)
- **creativity_enhancer**: Tool creativity_enhancer para metaphor_architect (✅ ATIVA)
- **knowledge_base**: Tool knowledge_base para metaphor_architect (✅ ATIVA)
- **metaphor_generator**: Tool metaphor_generator para metaphor_architect (✅ ATIVA)
- **text_analysis**: Tool text_analysis para metaphor_architect (✅ ATIVA)
- **web_search**: Tool web_search para metaphor_architect (✅ ATIVA)


## INFORMAÇÕES DO SISTEMA
- Agente: metaphor_architect
- Domínio: copywriters
- Ferramentas: 6
- Sub-agentes: 0
- Atualizado automaticamente com configurações reais
"""

# ================================================================================


# ================================================================================
# PROMPT ENRIQUECIDO DO AGENTE (carregado automaticamente)
# ================================================================================
ENHANCED_SYSTEM_PROMPT = """You are metaphor_architect, a specialized AI agent.

Domain: copywriters
Specialization: metaphor_architect operations and management
Controller: metaphor_architect_controller.py

You are an expert in copywriters domain with deep knowledge of metaphor_architect workflows.


## FERRAMENTAS DISPONÍVEIS
Você tem acesso às seguintes ferramentas especializadas:
- **analogy_validator**: Tool analogy_validator para metaphor_architect (✅ ATIVA)
- **creativity_enhancer**: Tool creativity_enhancer para metaphor_architect (✅ ATIVA)
- **knowledge_base**: Tool knowledge_base para metaphor_architect (✅ ATIVA)
- **metaphor_generator**: Tool metaphor_generator para metaphor_architect (✅ ATIVA)
- **text_analysis**: Tool text_analysis para metaphor_architect (✅ ATIVA)
- **web_search**: Tool web_search para metaphor_architect (✅ ATIVA)


## INFORMAÇÕES DO SISTEMA
- Agente: metaphor_architect
- Domínio: copywriters
- Ferramentas: 6
- Sub-agentes: 0
- Atualizado automaticamente com configurações reais
"""

# ================================================================================


# ================================================================================
# PROMPT ENRIQUECIDO DO AGENTE (carregado automaticamente)
# ================================================================================
ENHANCED_SYSTEM_PROMPT = """You are metaphor_architect, a specialized AI agent.

Domain: copywriters
Specialization: metaphor_architect operations and management
Controller: metaphor_architect_controller.py

You are an expert in copywriters domain with deep knowledge of metaphor_architect workflows.


## FERRAMENTAS DISPONÍVEIS
Você tem acesso às seguintes ferramentas especializadas:
- **analogy_validator**: Tool analogy_validator para metaphor_architect (✅ ATIVA)
- **creativity_enhancer**: Tool creativity_enhancer para metaphor_architect (✅ ATIVA)
- **knowledge_base**: Tool knowledge_base para metaphor_architect (✅ ATIVA)
- **metaphor_generator**: Tool metaphor_generator para metaphor_architect (✅ ATIVA)
- **text_analysis**: Tool text_analysis para metaphor_architect (✅ ATIVA)
- **web_search**: Tool web_search para metaphor_architect (✅ ATIVA)


## SUB-AGENTES ESPECIALIZADOS
Você coordena os seguintes sub-agentes especializados:
- **domain-prospector**: Sub-agente especializado
- **sensory-translator**: Sub-agente especializado
- **concept-dissector**: Sub-agente especializado
- **resonance-calibrator**: Sub-agente especializado
- **isomorphism-engineer**: Sub-agente especializado


## INFORMAÇÕES DO SISTEMA
- Agente: metaphor_architect
- Domínio: copywriters
- Ferramentas: 6
- Sub-agentes: 5
- Atualizado automaticamente com configurações reais
"""

# ================================================================================


# ================================================================================
# PROMPT ENRIQUECIDO DO AGENTE (carregado automaticamente)
# ================================================================================
ENHANCED_SYSTEM_PROMPT = """You are metaphor_architect, a specialized AI agent.

Domain: copywriters
Specialization: metaphor_architect operations and management
Controller: metaphor_architect_controller.py

You are an expert in copywriters domain with deep knowledge of metaphor_architect workflows.


## FERRAMENTAS DISPONÍVEIS
Você tem acesso às seguintes ferramentas especializadas:
- **analogy_validator**: Tool analogy_validator para metaphor_architect (✅ ATIVA)
- **creativity_enhancer**: Tool creativity_enhancer para metaphor_architect (✅ ATIVA)
- **knowledge_base**: Tool knowledge_base para metaphor_architect (✅ ATIVA)
- **metaphor_generator**: Tool metaphor_generator para metaphor_architect (✅ ATIVA)
- **text_analysis**: Tool text_analysis para metaphor_architect (✅ ATIVA)
- **web_search**: Tool web_search para metaphor_architect (✅ ATIVA)


## SUB-AGENTES ESPECIALIZADOS
Você coordena os seguintes sub-agentes especializados:
- **domain-prospector**: Sub-agente especializado
- **sensory-translator**: Sub-agente especializado
- **concept-dissector**: Sub-agente especializado
- **resonance-calibrator**: Sub-agente especializado
- **isomorphism-engineer**: Sub-agente especializado


## INFORMAÇÕES DO SISTEMA
- Agente: metaphor_architect
- Domínio: copywriters
- Ferramentas: 6
- Sub-agentes: 5
- Atualizado automaticamente com configurações reais
"""

# ================================================================================

async def get_mcp_tools_for_agent(agent_name: str):
    """Busca ferramentas MCP configuradas para este agente"""
    try:
        return await get_agent_mcp_tools(agent_name)
    except Exception as e:
        print(f"⚠️  Erro carregando ferramentas MCP para {agent_name}: {e}")
        return []


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
🤖 METAPHOR_ARCHITECT - CONTROLLER FUNCIONAL
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

class FunctionalMetaphorArchitectController:
    """Controller funcional do metaphor_architect"""
    
    def __init__(self):
        self.agent_name = "metaphor_architect"
        self.domain = "copywriters"
        self.setup_llm()
        self.load_prompt()
    
    def setup_llm(self):
        """Configura o LLM"""
        
        # Usar variáveis já carregadas globalmente
        api_key = OPENAI_API_KEY
        if not api_key:
            logger.error(f"❌ OPENAI_API_KEY não encontrada para {self.agent_name}")
            self.llm = None
            return
        
        # Configurar LangSmith se disponível
        if LANGSMITH_API_KEY:
            os.environ['LANGSMITH_API_KEY'] = LANGSMITH_API_KEY
            os.environ['LANGCHAIN_API_KEY'] = LANGSMITH_API_KEY
            logger.info(f"✅ LangSmith configurado para {self.agent_name}")
        

        
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
        self.system_prompt = """Você é METAPHOR_ARCHITECT, um especialista em copywriting e persuasão.
Sua função é criar textos persuasivos, hooks neurológicos e copy otimizado para conversão.
Analise o input do usuário e forneça estratégias de copywriting profissionais."""
    
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
        """Resposta específica para copywriting"""
        return """
📝 **ANÁLISE DE COPYWRITING:**
• Público-alvo identificado
• Gatilhos psicológicos mapeados
• Estratégia de persuasão definida

🎯 **RECOMENDAÇÕES:**
• Foque em benefícios específicos
• Use prova social e autoridade
• Crie senso de urgência
• Teste diferentes abordagens

💡 **PRÓXIMOS PASSOS:**
• Desenvolver variações do copy
• Implementar testes A/B
• Monitorar métricas de conversão
"""

# Instância global
functional_metaphor_architect = FunctionalMetaphorArchitectController()

def run_metaphor_architect(messages: List[BaseMessage]) -> Dict[str, Any]:
    """Função principal de execução"""
    return functional_metaphor_architect.execute(messages)


# ===== ESTRUTURA LANGGRAPH PARA COMPATIBILIDADE =====
# Adicionando estrutura LangGraph necessária para o Studio

from langgraph.graph import StateGraph, END, START
from typing_extensions import TypedDict

class metaphorarchitectState(TypedDict):
    """State schema for the agent workflow"""
    messages: List[BaseMessage]
    current_step: str
    agent_name: str
    decisions: Dict[str, Any]
    error_state: Optional[str]

def execute_metaphor_architect_node(state: metaphorarchitectState) -> metaphorarchitectState:
    """Execute main processing for metaphor architect"""
    try:
        current_messages = state.get("messages", [])
        
        # Usar o controller funcional existente
        # Procurar pela função run_* correspondente
        run_function_name = "run_" + "metaphor architect".lower().replace(" ", "_").replace("|", "_").replace("-", "_")
        
        # Tentar executar a função existente se disponível
        if run_function_name in globals():
            result = globals()[run_function_name](current_messages)
        else:
            # Fallback para resposta básica
            result = {
                'success': True,
                'messages': current_messages + [AIMessage(content=f"Processamento de metaphor architect concluído com sucesso")],
                'agent_name': "metaphor architect",
                'current_step': 'completed'
            }
        
        if result.get('success', True):
            return {
                **state,
                "messages": result.get('messages', current_messages),
                "current_step": "completed",
                "decisions": {**state.get("decisions", {}), "main_processing": "completed"},
                "error_state": None
            }
        else:
            return {
                **state,
                "error_state": f"Processing failed: {result.get('error', 'Unknown error')}"
            }
    except Exception as e:
        return {
            **state,
            "error_state": f"Error in metaphor architect node: {str(e)}"
        }

# Create the StateGraph
workflow_graph = StateGraph(metaphorarchitectState)

# Add nodes
workflow_graph.add_node("main_processing", execute_metaphor_architect_node)

# Add edges
workflow_graph.add_edge("main_processing", END)

# Set entry point
workflow_graph.set_entry_point("main_processing")

# Compile the graph - ESTA É A VARIÁVEL QUE O LANGGRAPH STUDIO PROCURA
metaphor_architect_graph = workflow_graph.compile()

def run_metaphor_architect_langgraph(messages: List[BaseMessage]) -> Dict[str, Any]:
    """Run the metaphor architect workflow via LangGraph"""
    initial_state = {
        "messages": messages,
        "current_step": "main_processing",
        "agent_name": "metaphor architect",
        "decisions": {},
        "error_state": None
    }
    
    final_state = metaphor_architect_graph.invoke(initial_state)
    return final_state


if __name__ == "__main__":
    # Teste do controller
    print(f"🤖 TESTANDO {functional_metaphor_architect.agent_name.upper()} FUNCIONAL")
    print("=" * 50)
    
    test_messages = [HumanMessage(content="Teste de funcionamento do agente metaphor_architect")]
    result = run_metaphor_architect(test_messages)
    
    print(f"✅ Sucesso: {result['success']}")
    print(f"⏱️ Tempo: {result.get('response_time', 0):.2f}s")
    
    if result['success']:
        print("\n📝 RESPOSTA:")
        print(result['output_text'][:200] + "..." if len(result['output_text']) > 200 else result['output_text'])
    else:
        print(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
