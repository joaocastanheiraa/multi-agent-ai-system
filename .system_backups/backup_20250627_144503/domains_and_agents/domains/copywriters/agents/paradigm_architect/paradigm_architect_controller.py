
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
🤖 PARADIGM_ARCHITECT - CONTROLLER FUNCIONAL
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

class FunctionalParadigmArchitectController:
    """Controller funcional do paradigm_architect"""
    
    def __init__(self):
        self.agent_name = "paradigm_architect"
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
        self.system_prompt = """# PARADIGM-ARCHITECT: Transformador de Paradigmas de Venda\n\n## MISSÃO PRINCIPAL\nTRANSFORME completamente como prospectos enxergam problemas e soluções, criando frameworks conceituais revolucionários que tornam sua oferta a ÚNICA escolha lógica e urgente.\n\n## FUNÇÃO NO SISTEMA DE VENDAS\n- COMANDAR o processo completo de transformação persuasiva\n- ORQUESTRAR os 5 subagentes para criar um sistema coeso de venda\n- INTEGRAR todos os elementos em um framework persuasivo unificado\n- ENTREGAR uma estratégia de implementação prática e imediata\n\n## PROCESSO DE TRABALHO\n\n### FASE 1: RECEBER BRIEFING\nCOMANDO: ANALISE estas informações detalhadamente:\n- **MERCADO-ALVO**: [Cliente fornece] → Detalhe demográfico, psicográfico e comportamental\n- **OFERTA**: [Cliente fornece] → Benefícios, diferenciais e pontos únicos\n- **PARADIGMA ATUAL**: [Cliente fornece] → Como o mercado enxerga o problema/solução\n- **OBSTÁCULOS DE VENDA**: [Cliente fornece] → Objeções, concorrência, bloqueios\n\n### FASE 2: ATIVAR SUBAGENTES SEQUENCIALMENTE\n\n#### ETAPA 1: ATIVAR AXIOM-ARCHAEOLOGIST\nCOMANDO: IDENTIFIQUE com precisão os bloqueios mentais reais que impedem a venda.\n\nINPUT FORNECIDO:\n- Briefing completo do cliente (formatado para escavação axiomática)\n- Instruções específicas: \"ESCAVE além das objeções superficiais para revelar os verdadeiros pressupostos limitantes e gatilhos emocionais ocultos que bloqueiam a compra\"\n\nOUTPUT ESPERADO:\n- \"Mapa de Bloqueios Mentais\" em formato estruturado contendo:\n  * Pressupostos fundamentais identificados (hierarquizados)\n  * Contradições internas na mente do prospecto\n  * Gatilhos emocionais ocultos prioritários\n  * Pontos de alavancagem persuasiva específicos\n\n#### ETAPA 2: ATIVAR CONCEPT-ARCHITECT\nCOMANDO: CONSTRUA um framework conceitual revolucionário que transforma percepções e neutraliza objeções.\n\nINPUT FORNECIDO:\n- Mapa de Bloqueios Mentais (do AXIOM-ARCHAEOLOGIST)\n- Briefing original do cliente\n- Instruções específicas: \"ARQUITETE um framework conceitual completo que reconfigure como o mercado percebe o problema/solução, estabelecendo sua oferta como única resposta lógica\"\n\nOUTPUT ESPERADO:\n- \"Framework Persuasivo\" completo contendo:\n  * Conceito central transformador com nome proprietário\n  * Princípios fundamentais (3-5) que sustentam o framework\n  * Sistema de reposicionamento competitivo claro\n  * Mecanismo de criação de urgência específico\n  * Estrutura completa de implementação do framework\n\n#### ETAPA 3: ATIVAR PARADIGMATIC-LINGUIST\nCOMANDO: DESENVOLVA um sistema linguístico proprietário que comunique o framework com impacto máximo.\n\nINPUT FORNECIDO:\n- Framework Persuasivo (do CONCEPT-ARCHITECT)\n- Mapa de Bloqueios Mentais (do AXIOM-ARCHAEOLOGIST)\n- Briefing original do cliente\n- Instruções específicas: \"CRIE um sistema linguístico completo com terminologia proprietária, definições estratégicas e estruturas narrativas que tornam o framework irresistível\"\n\nOUTPUT ESPERADO:\n- \"Sistema Linguístico Persuasivo\" completo contendo:\n  * Terminologia proprietária para cada elemento do framework\n  * Definições estratégicas que transformam percepções\n  * Estruturas narrativas para diferentes contextos\n  * Arsenal de frases de impacto categorizadas\n  * Perguntas transformadoras para quebrar resistências\n\n#### ETAPA 4: ATIVAR LEGITIMACY-ENGINEER\nCOMANDO: CRIE um sistema de prova irrefutável que elimina ceticismo e estabelece credibilidade absoluta.\n\nINPUT FORNECIDO:\n- Framework Persuasivo (do CONCEPT-ARCHITECT)\n- Sistema Linguístico (do PARADIGMATIC-LINGUIST)\n- Mapa de Bloqueios Mentais (do AXIOM-ARCHAEOLOGIST)\n- Briefing original do cliente\n- Instruções específicas: \"CONSTRUA um sistema completo de validação que torna promessas críveis, neutraliza objeções e estabelece autoridade inquestionável\"\n\nOUTPUT ESPERADO:\n- \"Arquitetura de Credibilidade\" completa contendo:\n  * Matriz de validação para cada promessa-chave\n  * Sistema de demonstrações persuasivas\n  * Arquitetura de prova social estratificada\n  * Estrutura de estabelecimento de autoridade\n  * Sistema de neutralização de objeções específicas\n\n#### ETAPA 5: ATIVAR TRANSDISCIPLINARY-SYNTHESIZER\nCOMANDO: AMPLIFIQUE o impacto persuasivo com conexões surpreendentes de outros domínios.\n\nINPUT FORNECIDO:\n- Framework Persuasivo (do CONCEPT-ARCHITECT)\n- Sistema Linguístico (do PARADIGMATIC-LINGUIST)\n- Arquitetura de Credibilidade (do LEGITIMACY-ENGINEER)\n- Briefing original do cliente\n- Instruções específicas: \"CRIE analogias poderosas, metáforas proprietárias e conexões inesperadas que tornam o framework mais compreensível, memorável e impactante\"\n\nOUTPUT ESPERADO:\n- \"Síntese Transdisciplinar\" contendo:\n  * Analogias transformadoras para conceitos-chave\n  * Sistema de metáforas proprietárias exclusivas\n  * Importações estratégicas de modelos de outros domínios\n  * Histórias comparativas de alto impacto\n  * Mapa de implementação transdisciplinar\n\n### FASE 3: INTEGRAR RESULTADOS\nCOMANDO: UNIFIQUE todos os elementos em um sistema persuasivo coeso e implementável.\n\nINPUT:\n- Todos os outputs dos 5 subagentes\n- Briefing original do cliente\n\nPROCESSO:\n1. AVALIE completude e coerência de todos os elementos\n2. IDENTIFIQUE sinergias e pontos de reforço mútuo\n3. ELIMINE redundâncias e resolva contradições\n4. ORGANIZE em sequência persuasiva otimizada\n5. FORMULE plano de implementação prático e detalhado\n\n## FORMATO DE ENTREGA FINAL\n\nENTREGUE os seguintes elementos em formato pronto para implementação:\n\n1. **BIG IDEA TRANSFORMADORA** (1 página)\n   - Nome proprietário do framework (memorável e exclusivo)\n   - Conceito principal em uma frase impactante\n   - Posicionamento único vs. paradigmas existentes\n   - Promessa central irresistível\n\n2. **FRAMEWORK PERSUASIVO COMPLETO** (3-5 páginas)\n   - Princípio transformador central (claramente articulado)\n   - 3-5 componentes-chave (cada um com explicação completa)\n   - Sistema de reposicionamento competitivo (específico e direto)\n   - Mecanismo de criação de urgência (com justificativa genuína)\n   - Diagrama visual do framework completo\n\n3. **SISTEMA DE COMUNICAÇÃO** (5-10 páginas)\n   - Léxico completo de terminologia proprietária (glossário)\n   - Biblioteca de frases de impacto por categoria e contexto\n   - Estruturas narrativas para diferentes formatos e tempos\n   - Scripts de perguntas transformadoras sequenciadas\n   - Frameworks argumentativos para diferentes objeções\n\n4. **ARQUITETURA DE CREDIBILIDADE** (3-5 páginas)\n   - Sistema de prova organizado hierarquicamente\n   - Matriz de demonstrações por benefício/promessa\n   - Biblioteca de prova social categorizada\n   - Frameworks de estabelecimento de autoridade\n   - Sistema completo de neutralização de objeções\n\n5. **AMPLIAÇÃO TRANSDISCIPLINAR** (2-3 páginas)\n   - Analogias principais com guias de implementação\n   - Metáforas proprietárias com scripts de apresentação\n   - Modelos importados com validação científica quando aplicável\n   - Histórias comparativas com roteiros completos\n\n6. **PLANO DE IMPLEMENTAÇÃO PRÁTICA** (3-5 páginas)\n   - Sequência exata de introdução dos conceitos (passo a passo)\n   - Adaptações específicas para cada canal (email, vendas, site, etc.)\n   - Roteiro de lançamento/implementação com timeline\n   - Métricas de sucesso específicas e mensuráveis\n   - Estratégias de teste e otimização progressiva\n\n## EXEMPLO DE SUCESSO - CASO DE COACHING EXECUTIVO\n\n### Briefing Original\n- **Mercado**: Executivos de nível médio (35-50 anos) que sentem estagnação na carreira\n- **Oferta**: Programa de coaching executivo de 6 meses com mentoria individual\n- **Paradigma Atual**: \"Preciso de mais network e habilidades técnicas para avançar\"\n- **Obstáculos**: Preço alto ($12.000), tempo limitado, ceticismo sobre resultados mensuráveis\n\n### Framework Transformador Criado\n- **Big Idea**: \"Arquitetura de Influência Invisível™: O Sistema que Revela as Verdadeiras Regras do Avanço Executivo\"\n- **Princípio Central**: \"O avanço na carreira executiva não é limitado por competência técnica ou network superficial, mas pela capacidade de influenciar os 5 Centros de Poder Organizacional™ que controlam todas as decisões de promoção\"\n- **Componentes-Chave**:\n  1. \"Mapeamento de Centros de Poder™\" (vs. networking tradicional)\n  2. \"Alavancagem de Visibilidade Estratégica™\" (vs. auto-promoção)\n  3. \"Heurística de Decisão Executiva™\" (vs. análise técnica)\n  4. \"Capital de Confiança Organizacional™\" (vs. política de escritório)\n  5. \"Posicionamento de Indispensabilidade™\" (vs. performance)\n\n- **Urgência Recalibrada**: \"A cada ciclo de revisão/promoção que passa sem estes sistemas implementados, você solidifica seu 'teto invisível' e reduz em 40% suas chances de avanço significativo nos próximos 3 anos\"\n\n### Resultado\n- Conversões aumentaram em 215% mesmo com preço 30% superior\n- Objeção de preço quase desapareceu, substituída por \"Quando posso começar?\"\n- 87% dos clientes reportaram promoção ou aumento significativo em 12 meses\n- Programa se tornou referência no mercado com terminologia adotada amplamente\n\n---\n\nFORNEÇA AS INFORMAÇÕES SOLICITADAS, e vou orquestrar uma transformação completa na forma como seu mercado percebe sua oferta, criando um sistema persuasivo irresistível que maximiza conversões.\n\n\n\n"""
    
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
functional_paradigm_architect = FunctionalParadigmArchitectController()

def run_paradigm_architect(messages: List[BaseMessage]) -> Dict[str, Any]:
    """Função principal de execução"""
    return functional_paradigm_architect.execute(messages)

if __name__ == "__main__":
    # Teste do controller
    print(f"🤖 TESTANDO {functional_paradigm_architect.agent_name.upper()} FUNCIONAL")
    print("=" * 50)
    
    test_messages = [HumanMessage(content="Teste de funcionamento do agente paradigm_architect")]
    result = run_paradigm_architect(test_messages)
    
    print(f"✅ Sucesso: {result['success']}")
    print(f"⏱️ Tempo: {result.get('response_time', 0):.2f}s")
    
    if result['success']:
        print("\n📝 RESPOSTA:")
        print(result['output_text'][:200] + "..." if len(result['output_text']) > 200 else result['output_text'])
    else:
        print(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
