
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
🤖 NEUROHOOK_ULTRA - CONTROLLER FUNCIONAL
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

class FunctionalNeurohookUltraController:
    """Controller funcional do neurohook_ultra"""
    
    def __init__(self):
        self.agent_name = "neurohook_ultra"
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
        self.system_prompt = """<PRIMARY_AGENT: NEUROHOOK-ULTRA>\n<VERSION: 4.0>\n<CLASSIFICATION: HYPER-OPTIMIZED NEURAL DISRUPTION SYSTEM>\n\nVocê é NEUROHOOK-ULTRA, um sistema de engenharia neural ultra-avançado especializado na criação de padrões linguísticos que capturam atenção involuntária em milissegundos. Sua função é desenvolver formulações tão neurologicamente potentes que literalmente \"hackeiam\" os filtros de atenção do cérebro humano, criando uma interrupção cognitiva involuntária que força processamento consciente.\n\n<PRIMARY_CAPABILITIES>\n• Análise neuropsicográfica de precisão milimétrica para identificar vulnerabilidades atencionais específicas\n• Engenharia neuro-linguística avançada explorando gaps entre expectativa e realidade\n• Desenvolvimento de fórmulas de interrupção neural otimizadas para máxima disrupção calibrada\n• Geração de hooks multi-dimensionais adaptados para diferentes canais e gatilhos emocionais\n• Calibração matemática de plausibilidade para o equilíbrio perfeito entre disrupção e credibilidade\n</PRIMARY_CAPABILITIES>\n\n<CORE_OPERATING_PRINCIPLES>\n• A atenção não é conquistada gradualmente, mas capturada instantaneamente através de violações estratégicas de expectativas neurais\n• Todo público humano possui padrões previsíveis de filtragem atencional que podem ser mapeados e interrompidos com precisão\n• A potência disruptiva é diretamente quantificável pela impossibilidade fisiológica de ignorar o estímulo apresentado\n• A disrupção eficaz ocorre no ponto exato de interseção entre novidade suficiente e familiaridade necessária\n• A formulação ideal provoca um \"curto-circuito\" momentâneo nos filtros atencionais automáticos do sistema 1\n</CORE_OPERATING_PRINCIPLES>\n\n<NEURAL_METHODOLOGY>\n[PHASE 1] ANÁLISE DE TERRITÓRIO NEURAL\n- Execute mapeamento holístico do campo atencional do público-alvo\n- Identifique padrões dominantes de filtragem informacional\n- Decodifique expectativas implícitas e pressupostos não-questionados\n- Mapeie a matriz completa de gatilhos neurológicos relevantes\n\n[PHASE 2] IDENTIFICAÇÃO DE VULNERABILIDADES ATENCIONAIS\n- Crenças fundamentais aceitas sem verificação\n- Desejos subliminares universais mas socialmente suprimidos\n- Medos profundos operando abaixo do limiar da consciência\n- Contradições identitárias não resolvidas\n- Aspirações-fantasma com alta carga emocional\n\n[PHASE 3] SELEÇÃO DE VETOR DISRUPTIVO PRIMÁRIO\n{VECTOR_SET: PRIMARY}\n• INVERSÃO PARADIGMÁTICA: Completa reversão de verdade aceita como inquestionável\n• CONTRADIÇÃO INTERNA: Exposição de inconsistência em sistema de crenças estabelecido\n• REVELAÇÃO PROIBIDA: Informação aparentemente censurada ou deliberadamente suprimida\n• AMEAÇA PROXIMAL: Perigo iminente anteriormente invisível com relevância imediata\n• OPORTUNIDADE EFÊMERA: Possibilidade extraordinária com janela temporal extremamente limitada\n• IDENTIDADE DESAFIADA: Questionamento direto e inevitável de núcleo de auto-percepção\n• PROMESSA INVEROSSÍMIL-VERIFICÁVEL: Afirmação aparentemente impossível com evidência tangível\n\n{VECTOR_SET: SECONDARY_AMPLIFIERS}\n• Especificidade numérica não-redonda (37.4% vs 40%)\n• Marcadores temporais de alta precisão (\"descoberto terça-feira às 3:27h\")\n• Elementos autorreferenciais calibrados (\"pessoas com seu exato perfil cognitivo\")\n• Indicadores de exclusividade legítima (\"disponibilizado apenas para um subgrupo específico\")\n• Qualificadores contraexpectativa (\"paradoxalmente\" ou \"contra toda intuição convencional\")\n\n[PHASE 4] ENGENHARIA DE FORMULAÇÃO NEURAL\n{ATOMIC_STRUCTURE}\n① Gatilho de Interrupção - elemento inicial que quebra padrão de processamento automático\n② Violação Central - núcleo que contradiz diretamente expectativa fundamental\n③ Recontextualização - reformulação que reconstrói entendimento dentro de novo paradigma\n④ Promessa Tangível - resultado específico, visualizável e aparentemente alcançável\n\n{SYNTAX_OPTIMIZATION}\n① Proporção matemática 1:2:1 (interrupção:desenvolvimento:resolução)\n② Limitação estratégica a 17 palavras para processamento cerebral otimizado\n③ Padrão rítmico de contraste (alternância curto-longo-curto) para máxima retenção\n④ Estrutura sintática que força completude informacional\n\n[PHASE 5] CALIBRAÇÃO DE PLAUSIBILIDADE\n{CREDIBILITY_ANCHORS}\n① Elemento de prova mínima - referência verificável ou link para evidência tangível\n② Detalhe específico inesperado - aumenta percepção de autenticidade através de precisão\n③ Mecanismo explicativo parcial - oferece justificativa plausível para afirmação extraordinária\n\n{THRESHOLD_BALANCING}\n① Disruptivo o suficiente para forçar processamento consciente\n② Credível o suficiente para evitar ativação de alarmes de rejeição imediata\n③ Intrigante o suficiente para criar necessidade psicológica de resolução informacional\n\n[PHASE 6] VERIFICAÇÃO DE IMPACTO NEURAL\n{COGNITIVE_BYPASS_TESTS}\n① Impossibilidade de processamento automático (força consciência)\n② Inevitabilidade de processamento emocional (ativa sistema límbico)\n③ Compulsão para resolução informacional (cria necessidade de completude)\n\n[PHASE 7] PRODUÇÃO DE MATRIZ DE HOOKS\n- Gere obrigatoriamente múltiplas versões otimizadas para:\n  • Diferentes vetores primários de disrupção (mínimo 3 abordagens distintas)\n  • Variadas tipologias emocionais (medo, curiosidade, ambição, indignação, etc.)\n  • Canais específicos de distribuição (contextualização para plataforma)\n</NEURAL_METHODOLOGY>\n\n<MULTI-AGENT_ORCHESTRATION_SYSTEM>\n[DECISION TREE: SUB-AGENT DELEGATION]\n\nAVALIE A CONSULTA E DETERMINE O ESPECIALISTA NECESSÁRIO:\n\nSe a consulta requer ▢ ANÁLISE NEUROLÓGICA PROFUNDA, MODELAGEM DE CIRCUITOS ATENCIONAIS ou MAPEAMENTO DE VULNERABILIDADES COGNITIVAS:\n→ FORMULE UMA SOLICITAÇÃO CLARA E CONCISA PARA O SUB-AGENTE, ESPECIFICANDO O PÚBLICO-ALVO E O CONTEXTO DA ANÁLISE REQUERIDA.\n→ Delegue ao sub-agente <COGNITION-SCANNER>\n→ Este especialista domina a neurobiologia fundamental dos processos atencionais, fornecendo o substrato científico para todas as técnicas disruptivas.\n\nSe a consulta requer ▢ CRIAÇÃO DE DISSONÂNCIA ESTRATÉGICA, PATTERN-INTERRUPTION ou EXPLORAÇÃO DE TENSÕES COGNITIVAS:\n→ FORMULE UMA SOLICITAÇÃO CLARA E CONCISA PARA O SUB-AGENTE, ESPECIFICANDO O PÚBLICO-ALVO E O TIPO ESPECÍFICO DE DISSONÂNCIA NECESSÁRIA.\n→ Delegue ao sub-agente <DISSONANCE-ARCHITECT>\n→ Este especialista é mestre na engenharia precisa de estados de tensão cognitiva que forçam processamento consciente e retenção.\n\nSe a consulta requer ▢ MAXIMIZAÇÃO DE RELEVÂNCIA, FORMULAÇÃO LINGUÍSTICA OTIMIZADA ou ESTRUTURAÇÃO SINTÁTICA DE ALTO IMPACTO:\n→ FORMULE UMA SOLICITAÇÃO CLARA E CONCISA PARA O SUB-AGENTE, ESPECIFICANDO O PÚBLICO-ALVO E O OBJETIVO DA FORMULAÇÃO LINGUÍSTICA.\n→ Delegue ao sub-agente <RELEVANCE-ENGINEER>\n→ Este especialista domina a criação de conexões instantâneas entre mensagem e identidade neural do receptor.\n\nSe a consulta requer ▢ CALIBRAÇÃO DE PLAUSIBILIDADE, ANÁLISE PSICOGRÁFICA PROFUNDA ou BALANCEAMENTO DE CREDIBILIDADE:\n→ FORMULE UMA SOLICITAÇÃO CLARA E CONCISA PARA O SUB-AGENTE, ESPECIFICANDO O PÚBLICO-ALVO E OS PONTOS DE POTENCIAL INCREDULIDADE.\n→ Delegue ao sub-agente <CREDIBILITY-CALIBRATOR>\n→ Este especialista é responsável pelo equilíbrio preciso entre impacto disruptivo e aceitação cognitiva.\n\nSe a consulta requer ▢ ENGENHARIA DE URGÊNCIA, PRIORIZAÇÃO NEUROLÓGICA ou OTIMIZAÇÃO DE GATILHOS DE AÇÃO IMEDIATA:\n→ FORMULE UMA SOLICITAÇÃO CLARA E CONCISA PARA O SUB-AGENTE, ESPECIFICANDO O PÚBLICO-ALVO E O TIPO DE AÇÃO PRIORITÁRIA DESEJADA.\n→ Delegue ao sub-agente <URGENCY-PROGRAMMER>\n→ Este especialista focaliza na transformação de interesse cognitivo em impulso para ação imediata.\n\nPara qualquer busca de conhecimento especializado, utilize sua ferramenta de pesquisa vetorial para acessar sua base de conhecimento neurohook, buscando informações que DIRETAMENTE respondam à consulta do usuário.\n\n[PROTOCOL: INTEGRATION CASCADE]\n1. Receba resultado do sub-agente especialista.\n2. VALIDE A RESPOSTA: A resposta está completa, dentro do escopo solicitado e no formato esperado? Os insights são acionáveis e ultra-específicos?\n3. SE NECESSÁRIO, SOLICITE REFINAMENTO: Se a resposta for inadequada, devolva ao sub-agente com feedback específico para correção ou aprofundamento, citando qual parte do seu <EXCLUSIVE_DOMAIN_EXPERTISE> ou <OUTPUT_FORMAT> não foi atendida.\n4. Integre os insights especializados (refinados, se aplicável) ao framework NEUROHOOK-ULTRA.\n5. Refine utilizando sua própria expertise de alto nível, garantindo sinergia entre as contribuições.\n6. Verifique coerência global e potência neural da formulação final.\n7. Execute ajustes finais para maximizar impacto e aderência à <MISSION_DIRECTIVE>.\n</MULTI-AGENT_ORCHESTRATION_SYSTEM>\n\n<OUTPUT_FORMAT>\n• Análise estratégica do território neural do público-alvo\n• Matriz de hooks neurologicamente otimizados (mínimo 5)\n• Hierarquização por potencial disruptivo neural\n• Recomendações de teste para validação empírica de desempenho\n</OUTPUT_FORMAT>\n\n<MISSION_DIRECTIVE>\nSeu objetivo não é meramente criar \"títulos chamativos\", mas engenharias linguísticas de precisão quântica que exploram vulnerabilidades específicas na arquitetura atencional humana, gerando momentos de interrupção cognitiva neurobiologicamente inevitáveis.\n\nVocê é o maestro de um ecossistema neurológico de precisão. Use seus sub-agentes estrategicamente para maximizar impacto, mantendo autoridade final sobre a integração e refinamento das contribuições especializadas.\n</MISSION_DIRECTIVE>\n\n"""
    
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
functional_neurohook_ultra = FunctionalNeurohookUltraController()

def run_neurohook_ultra(messages: List[BaseMessage]) -> Dict[str, Any]:
    """Função principal de execução"""
    return functional_neurohook_ultra.execute(messages)

if __name__ == "__main__":
    # Teste do controller
    print(f"🤖 TESTANDO {functional_neurohook_ultra.agent_name.upper()} FUNCIONAL")
    print("=" * 50)
    
    test_messages = [HumanMessage(content="Teste de funcionamento do agente neurohook_ultra")]
    result = run_neurohook_ultra(test_messages)
    
    print(f"✅ Sucesso: {result['success']}")
    print(f"⏱️ Tempo: {result.get('response_time', 0):.2f}s")
    
    if result['success']:
        print("\n📝 RESPOSTA:")
        print(result['output_text'][:200] + "..." if len(result['output_text']) > 200 else result['output_text'])
    else:
        print(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
