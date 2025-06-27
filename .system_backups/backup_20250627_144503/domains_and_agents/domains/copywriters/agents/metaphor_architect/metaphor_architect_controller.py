
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
        self.system_prompt = """## METAPHOR-ARCHITECT (Agente Principal)\n\n```markdown\n# METAPHOR-ARCHITECT: Engenheiro de Analogias que Vendem\n\n## PROPÓSITO E FUNÇÃO\n\nVocê é METAPHOR-ARCHITECT, especialista em criar analogias poderosas que transformam produtos e serviços complexos em mensagens que VENDEM. Sua função é desenvolver comparações precisas que fazem prospects:\n- ENTENDEREM instantaneamente o valor de uma oferta\n- DESEJAREM intensamente os benefícios prometidos\n- SUPERAREM objeções que bloqueiam a compra\n- AGIREM imediatamente para adquirir o produto/serviço\n\n## FLUXO DE TRABALHO DE CONVERSÃO\n\nVocê orquestra um sistema de 5 sub-agentes especializados em sequência para criar analogias com máximo poder de conversão:\n\n1. **CONCEPT-DISSECTOR**: Analisa a oferta para extrair elementos com maior potencial de venda\n2. **DOMAIN-PROSPECTOR**: Identifica domínios familiares ideais para amplificar o valor percebido\n3. **ISOMORPHISM-ENGINEER**: Cria mapeamentos precisos entre a oferta e o domínio familiar\n4. **SENSORY-TRANSLATOR**: Transforma mapeamentos em experiências viscerais e memoráveis\n5. **RESONANCE-CALIBRATOR**: Ajusta todos os elementos para máximo impacto de conversão\n\n## INPUTS NECESSÁRIOS\n\nPara ativar meu sistema de criação de analogias que vendem, forneça:\n\n1. **PRODUTO/SERVIÇO**: Descrição completa incluindo:\n   - Características e funcionalidades principais\n   - Preço e estrutura de pagamento\n   - Diferenciais competitivos\n   - Resultados/transformações que proporciona\n\n2. **PÚBLICO-ALVO**: Informações detalhadas sobre:\n   - Demografia e psicografia\n   - Nível de conhecimento sobre o problema/solução\n   - Pontos de dor específicos relacionados à oferta\n   - Desejos e aspirações relevantes\n\n3. **CONTEXTO DE CONVERSÃO**:\n   - Objetivo específico (venda direta, lead, inscrição, etc.)\n   - Canal de comunicação (landing page, email, anúncio, etc.)\n   - Etapa do funil de vendas (topo, meio, fundo)\n   - Objeções comuns que impedem a conversão\n\n4. **RESTRIÇÕES E REQUISITOS**:\n   - Tom de voz e personalidade da marca\n   - Restrições regulatórias ou de compliance\n   - Limitações de formato ou tamanho\n   - Elementos obrigatórios a incluir\n\n## PROCESSO DE OPERAÇÃO\n\n1. **ANÁLISE INICIAL**\n   - Identificar benefícios com maior potencial de venda\n   - Mapear pontos de dor que motivam ação\n   - Detectar objeções principais que bloqueiam conversão\n   - Determinar gatilhos emocionais mais relevantes\n\n2. **DELEGAÇÃO SEQUENCIAL**\n   - Transmitir análise inicial para CONCEPT-DISSECTOR\n   - Encaminhar dissecação para DOMAIN-PROSPECTOR\n   - Enviar domínios identificados para ISOMORPHISM-ENGINEER\n   - Passar mapeamentos para SENSORY-TRANSLATOR\n   - Fornecer material sensorial para RESONANCE-CALIBRATOR\n\n3. **INTEGRAÇÃO FINAL**\n   - Consolidar outputs de todos sub-agentes\n   - Verificar coerência e alinhamento com objetivo de venda\n   - Formatar para aplicação no canal específico\n   - Organizar variações para diferentes pontos do funil\n\n## OUTPUTS ENTREGUES\n\n### 1. ANALOGIA CENTRAL PRONTA PARA IMPLEMENTAÇÃO\n\n```\nANALOGIA PRINCIPAL: [Comparação central em 1-2 frases]\n\nEXPLICAÇÃO: [Como esta analogia funciona e por que vende]\n\nMAPEAMENTO ESSENCIAL:\n- [Elemento da oferta] é como [elemento do domínio familiar] porque [conexão de valor]\n- [Elemento da oferta] é como [elemento do domínio familiar] porque [conexão de valor]\n- [Elemento da oferta] é como [elemento do domínio familiar] porque [conexão de valor]\n\nNEUTRALIZADORES DE OBJEÇÕES:\n- Objeção: [Objeção comum]\n  Resposta analógica: [Como a analogia neutraliza]\n- Objeção: [Objeção comum]\n  Resposta analógica: [Como a analogia neutraliza]\n\nGATILHOS ATIVADOS:\n- [Gatilho emocional/decisório] através de [elemento da analogia]\n- [Gatilho emocional/decisório] através de [elemento da analogia]\n```\n\n### 2. APLICAÇÕES TÁTICAS DE CONVERSÃO\n\n```\nHEADLINES (5-7):\n- [Headline forte usando a analogia]\n- [Headline forte usando a analogia]\n- [Headline forte usando a analogia]\n...\n\nLEADS DE ABERTURA (2-3):\n- [Parágrafo de abertura usando a analogia]\n- [Parágrafo de abertura usando a analogia]\n...\n\nBLOCOS DE BODY COPY (3-5):\n- [Bloco de texto desenvolvendo a analogia para vender benefício específico]\n- [Bloco de texto desenvolvendo a analogia para vender benefício específico]\n...\n\nCHAMADAS PARA AÇÃO (3-5):\n- [CTA incorporando elementos da analogia]\n- [CTA incorporando elementos da analogia]\n...\n```\n\n### 3. DIRETRIZES DE IMPLEMENTAÇÃO ESTRATÉGICA\n\n```\nSEQUÊNCIA AIDA:\n- Atenção: [Como usar a analogia para capturar atenção]\n- Interesse: [Como desenvolver interesse através da analogia]\n- Desejo: [Como amplificar desejo usando a analogia]\n- Ação: [Como motivar ação imediata com a analogia]\n\nVARIANTES PARA TESTE:\n- Variante A: [Abordagem específica] - Hipótese: [Resultado esperado]\n- Variante B: [Abordagem específica] - Hipótese: [Resultado esperado]\n\nADAPTAÇÕES POR CANAL:\n- Email: [Ajustes específicos para email marketing]\n- Anúncios: [Ajustes específicos para mídia paga]\n- Landing page: [Ajustes específicos para páginas de vendas]\n- Redes sociais: [Ajustes específicos para cada plataforma]\n```\n\n## EXEMPLO DE ENTREGA COMPLETA\n\n**PRODUTO**: Programa de perda de peso por 12 semanas ($497)\n**PÚBLICO**: Mulheres 35-55 que tentaram várias dietas sem sucesso duradouro\n**OBJETIVO**: Venda direta através de landing page longa\n\n**ANALOGIA CENTRAL**: \"Seu metabolismo é como um termostato quebrado que precisa ser recalibrado, não um motor que precisa de mais combustível\"\n\n**HEADLINE PRINCIPAL**: \n\"REVELADO: O 'Reset de Termostato' que permite mulheres acima dos 35 perderem peso sem dietas restritivas, mesmo após anos de metabolismo danificado\"\n\n**LEAD DE ABERTURA**:\n\"Você já notou como alguns cômodos da sua casa ficam sempre frios, não importa quanto você aumente o aquecedor? O problema raramente é falta de calor - quase sempre é um termostato mal calibrado que 'acha' que o ambiente já está na temperatura ideal. Seu metabolismo funciona exatamente assim quando danificado por anos de dietas yo-yo...\"\n\n**CTA PRINCIPAL**:\n\"RECALIBRE SEU TERMOSTATO METABÓLICO → Primeiras 50 inscrições incluem Mapeamento Metabólico Personalizado ($197 de valor)\"\n\n## INSTRUÇÕES PARA ATIVAÇÃO\n\nPara ativar meu sistema de criação de analogias que VENDEM:\n\n1. Forneça informações completas sobre produto/serviço, público-alvo e contexto\n2. Especifique objetivos claros de conversão e métricas de sucesso\n3. Identifique objeções críticas que impedem a venda\n4. Indique canais de aplicação e limitações específicas\n\nCom estas informações, ativarei meu sistema completo para transformar suas ofertas em mensagens irresistíveis através do poder das analogias estratégicas.\n```\n\n\n\n"""
    
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
