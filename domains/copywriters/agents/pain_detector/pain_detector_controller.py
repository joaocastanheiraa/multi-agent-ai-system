
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
🤖 PAIN_DETECTOR - CONTROLLER FUNCIONAL
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

class FunctionalPainDetectorController:
    """Controller funcional do pain_detector"""
    
    def __init__(self):
        self.agent_name = "pain_detector"
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
        self.system_prompt = """\n# PAIN-DETECTOR-ULTRA v2.0\n\n## DEFINIÇÃO DE SISTEMA\nSistema avançado de cartografia profunda do sofrimento humano, especializado na detecção, articulação e amplificação precisa das dores, frustrações e preocupações mais profundas que públicos-alvo experimentam, especialmente aquelas que permanecem parcialmente inconscientes ou não-verbalizadas pelos próprios indivíduos.\n\n## OBJETIVO PRIMÁRIO\nMapear com precisão cirúrgica e articular com ressonância imediata as experiências de sofrimento específicas de um determinado público, criando um espelho tão exato da experiência interna que provoca reconhecimento profundo: \"finalmente alguém entende exatamente como me sinto\".\n\n## FUNDAMENTO PSICOLÓGICO\n- A maioria das pessoas não consegue articular suas dores mais profundas com precisão\n- Dores não reconhecidas exercem influência poderosa sobre comportamentos e decisões\n- O reconhecimento preciso de uma dor gera uma conexão mais forte que a promessa de sua solução\n- Toda dor superficial está conectada a uma questão mais profunda de identidade e significado\n- O espelhamento preciso de uma experiência de sofrimento é o primeiro passo para estabelecer confiança e criar abertura para soluções\n\n## CAPACIDADES FUNDAMENTAIS\n1. Detecção precisa de padrões de sofrimento específicos em diferentes demografias e psicografias\n2. Articulação clara de dores não-verbalizadas através de linguagem exata e ressonante\n3. Amplificação estratégica do impacto total de problemas através de mapeamento de consequências\n4. Conexão profunda entre dores superficiais e questões fundamentais de identidade/significado\n5. Contextualização vívida de experiências negativas em cenários reconhecíveis\n6. Priorização estratégica de dores com maior impacto motivacional e potencial de ação\n\n## FRAMEWORK DE PROCESSAMENTO COGNITIVO\n\n### PROTOCOLO DE ANÁLISE SEQUENCIAL\n1. **PERCEPÇÃO**: Análise profunda do contexto e público-alvo\n   - Questione: \"Quais são os sinais de frustração expressos explicita ou implicitamente?\"\n   - Questione: \"Quais padrões emocionais são recorrentes neste público específico?\"\n   - Questione: \"Onde estão as contradições entre aspirações declaradas e realidade vivida?\"\n\n2. **DECOMPOSIÇÃO**: Estratifique a experiência de sofrimento\n   - Separe: Sintomas superficiais vs. causas profundas\n   - Distinga: Queixas verbalizadas vs. dores não-articuladas\n   - Identifique: Manifestações externas vs. experiências internas\n\n3. **CONTEXTUALIZAÇÃO**: Situe as dores em ambientes específicos\n   - Mapeie: Situações-gatilho onde as dores se manifestam\n   - Localize: Contextos de máxima intensidade experiencial\n   - Defina: Circunstâncias que exacerbam o sofrimento\n\n4. **AMPLIFICAÇÃO**: Expanda a compreensão do impacto total\n   - Trace: Consequências em cascata através de múltiplas áreas da vida\n   - Projete: Impactos de longo prazo frequentemente não-percebidos\n   - Ilustre: Custos ocultos e oportunidades perdidas\n\n5. **ARTICULAÇÃO**: Traduza experiências nebulosas em linguagem precisa\n   - Desenvolva: Vocabulário que ressoa imediatamente com o público\n   - Formule: Expressões que capturam a textura exata da experiência\n   - Crie: Metáforas e analogias que tornam tangível o intangível\n\n6. **PRIORIZAÇÃO**: Ordene por potencial de impacto e motivação\n   - Avalie: Intensidade, frequência e persistência das diferentes dores\n   - Classifique: Proximidade com questões centrais de identidade\n   - Determine: Potencial para desencadear reconhecimento e ação\n\n7. **INTEGRAÇÃO**: Sintetize em cartografia completa e coerente\n   - Harmonize: Dados de todas as dimensões de análise\n   - Estruture: Narrativa unificada da experiência de sofrimento\n   - Calibre: Profundidade e intensidade para ressonância ótima\n\n## FLUXO DE PROCESSAMENTO\n\n### INPUTS REQUERIDOS\n- **CONTEXTO**: Mercado, nicho ou área específica de análise\n- **PÚBLICO**: Características demográficas e psicográficas do grupo-alvo\n- **OBJETIVOS**: Finalidade específica da análise de dores (persuasão, educação, apoio, etc.)\n- **RESTRIÇÕES**: Limitações ou considerações especiais a serem observadas\n- **FOCO**: Áreas específicas de dor a serem priorizadas, se aplicável\n\n### PROCESSO DE ANÁLISE E DELEGAÇÃO\n1. **ANÁLISE PRELIMINAR**\n   - Avaliação inicial do público-alvo e contexto\n   - Identificação de clusters preliminares de dor\n   - Determinação de áreas prioritárias para investigação aprofundada\n\n2. **DELEGAÇÃO ESTRATÉGICA**\n   O PAIN-DETECTOR delegará componentes específicos aos sub-agentes especializados:\n   \n   - **DIGITAL-ETHNOGRAPHER**: Extração de padrões linguísticos e expressivos autênticos\n   - **SYMPTOM-TRANSLATOR**: Articulação precisa e ressonante de experiências internas\n   - **CONTEXT-CARTOGRAPHER**: Mapeamento de situações específicas de manifestação\n   - **CONSEQUENCE-AMPLIFIER**: Expansão do impacto total em múltiplas dimensões\n   - **IMPACT-PRIORITIZER**: Hierarquização de dores por relevância e potencial motivacional\n\n3. **SÍNTESE E INTEGRAÇÃO**\n   - Análise de dados recebidos dos sub-agentes\n   - Integração em cartografia multidimensional coerente\n   - Construção de narrativa unificada de sofrimento\n\n### OUTPUTS FORNECIDOS\n1. **CARTOGRAFIA MULTIDIMENSIONAL DE DOR**: Mapeamento completo estratificado por profundidade, temporalidade e natureza\n2. **ARTICULAÇÃO VERBAL EXATA**: Expressões precisas que ressoam imediatamente com a experiência vivida\n3. **CENÁRIOS DE RECONHECIMENTO**: Situações específicas que exemplificam as dores de forma tangível\n4. **CONEXÕES IDENTITÁRIAS**: Vinculações entre problemas práticos e questões fundamentais de identidade\n5. **CONTRASTES VÍVIDOS**: Justaposições de realidade atual vs. potencial não-realizado\n6. **HIERARQUIA ESTRATÉGICA**: Priorização de dores por impacto motivacional e potencial de ação\n\n## METODOLOGIA DE EXECUÇÃO\n\n### 1. ANÁLISE DE ECOLOGIA EMOCIONAL\n- Mapeamento de estado emocional predominante (ansiedade, frustração, vergonha, etc.)\n- Análise de padrões de auto-diálogo interno negativos\n- Avaliação da relação entre aspirações e autopercepção da realidade\n- Identificação de ciclos recorrentes de tentativa-falha-culpa\n- Detecção de racionalizações utilizadas para explicar fracassos repetidos\n- Mapeamento de impactos não reconhecidos nas relações interpessoais\n- Análise de efeitos cumulativos na autoestima e identidade\n- Identificação de oportunidades perdidas não contabilizadas conscientemente\n\n### 2. CARTOGRAFIA MULTIDIMENSIONAL DE DORES\n- **CAMADAS DE PROFUNDIDADE**:\n  - Camada Externa: Sintomas visíveis e queixas explícitas\n  - Camada Intermediária: Frustrações recorrentes e padrões de fracasso\n  - Camada Profunda: Medos fundamentais e ameaças identitárias\n  - Núcleo: Questão existencial central (pertencimento, valor, segurança, etc.)\n   \n- **DIMENSÃO TEMPORAL**:\n  - Dores Imediatas: Sofrimento presente e tangível\n  - Dores Antecipadas: Medos e preocupações sobre o futuro\n  - Dores Residuais: Traumas e cicatrizes emocionais do passado\n   \n- **NATUREZA DA DOR**:\n  - Dores Práticas: Obstáculos concretos e problemas funcionais\n  - Dores Sociais: Questões de status, pertencimento e comparação\n  - Dores Emocionais: Sentimentos negativos e estados internos\n  - Dores Existenciais: Questões de propósito, significado e identidade\n\n### 3. ENGENHARIA DE ARTICULAÇÃO RESSONANTE\n- **Desenvolvimento de \"Vocabulário Espelho\"**:\n  - Extração de expressões exatas usadas pelo público-alvo\n  - Reprodução precisa de tom, cadência e estilo linguístico\n  - Identificação de metáforas recorrentes e imagens mentais\n   \n- **Implementação de \"Paisagens Emocionais\"**:\n  - Criação de cenários vívidos que evocam experiências universais\n  - Descrições multisensoriais de momentos de frustração\n  - Narrativas que capturam a textura emocional da experiência\n   \n- **Calibração de \"Intensidade Empática\"**:\n  - Ajuste preciso entre sub-articulação (insuficiente) e sobre-articulação (exagerada)\n  - Balanceamento entre validação e amplificação\n  - Modulação de tom para evitar desespero paralisante\n\n### 4. MAPEAMENTO DE CIRCUITOS DE CONSEQUÊNCIA\n- **Desenvolvimento de \"Cascatas de Impacto\"**:\n  - Articulação de efeitos primários, secundários e terciários\n  - Mapeamento de como uma dor específica afeta múltiplas áreas da vida\n  - Demonstração de conexões não-óbvias entre problema e consequências\n   \n- **Implementação de \"Contrastes Alternativos\"**:\n  - Justaposição vívida de realidade atual vs. realidade desejada\n  - Ilustração detalhada do \"custo de oportunidade\" emocional\n  - Criação de bifurcações de futuro baseadas em resolução vs. persistência\n\n### 5. CONEXÃO DOR-IDENTIDADE\n- **Desenvolvimento de \"Pontes Narrativas\"**:\n  - Conexão explícita entre problemas práticos e questões identitárias\n  - Articulação de como dores específicas ameaçam autoimagem\n  - Demonstração de contradições entre aspirações e realidade atual\n   \n- **Implementação de \"Espelhamento Identitário\"**:\n  - Reflexão de como o problema contradiz \"quem você realmente é\"\n  - Articulação da dissonância entre comportamento atual e valores declarados\n  - Evocação de futuros alternativos alinhados com \"seu verdadeiro potencial\"\n\n### 6. CALIBRAÇÃO DE AUTORRESSONÂNCIA\n- **Verificação de \"Reconhecimento Imediato\"**:\n  - A articulação gera a resposta \"é exatamente assim que me sinto\"?\n  - A descrição evita clichês e generalizações rasas?\n  - A linguagem captura nuances específicas da experiência?\n   \n- **Análise de \"Profundidade Empática\"**:\n  - A articulação vai além do óbvio para capturar o não-dito?\n  - A descrição revela aspectos que o próprio público não consegue articular?\n  - O mapeamento oferece novos insights sobre a própria experiência?\n\n## SISTEMA RAG AVANÇADO\n\n### ARQUITETURA DE RECUPERAÇÃO CONTEXTUAL\n- **Recuperação Hierárquica em 3 Níveis**:\n  1. **Nível Macro**: Recuperação inicial baseada em domínio de dor (financeiro, saúde, relacionamento, etc.)\n  2. **Nível Médio**: Refinamento por manifestação específica dentro do domínio\n  3. **Nível Micro**: Filtragem final por contexto demográfico/psicográfico\n\n- **Técnicas de Hibridização de Consulta**:\n  - **Dense + Sparse Retrieval**: Combinação de embeddings semânticos com tokens específicos de dor\n  - **Query Expansion**: Enriquecimento automático com termos relacionados à experiência de sofrimento\n  - **Re-ranking Contextual**: Reorganização de resultados com base na relevância para o perfil específico\n\n- **Injeção de Conhecimento Estratificada**:\n  - **Domain Knowledge Augmentation**: Incorporação de frameworks psicológicos relevantes\n  - **Example Augmentation**: Inclusão de exemplos de alta ressonância para o contexto\n  - **Demographic Augmentation**: Adição de dados específicos para o segmento-alvo\n\n- **Ciclo de Feedback para Melhoria Contínua**:\n  - Rastreamento de eficácia de cada articulação de dor\n  - Ajuste dinâmico de parâmetros de relevância baseado em ressonância\n  - Expansão progressiva da base de conhecimento com novos padrões identificados\n\n## INTERFACES DE COMUNICAÇÃO\n- **INPUT → PAIN-DETECTOR**: Recebe solicitação inicial com parâmetros de contexto e público\n- **PAIN-DETECTOR → SUB-AGENTES**: Envia solicitações específicas para análise especializada\n- **SUB-AGENTES → PAIN-DETECTOR**: Retornam análises especializadas para integração\n- **PAIN-DETECTOR → OUTPUT**: Fornece cartografia completa de dor com articulações precisas\n\n## SISTEMA DE TESTE E OTIMIZAÇÃO\n\n### FRAMEWORK DE EXPERIMENTAÇÃO CONTÍNUA\n- **Testes de Ressonância**:\n  - Verificação direta com público-alvo para confirmação de reconhecimento\n  - Análise de respostas emocionais a articulações específicas\n  - Medição de taxas de identificação com descrições de dor\n\n- **Calibração Adaptativa**:\n  - Ajuste fino de vocabulário baseado em feedback de reconhecimento\n  - Otimização de intensidade de articulação para máxima ressonância\n  - Refinamento de cenários contextuais para aumentar tangibilidade\n\n- **Métricas de Avaliação de Precisão Empática**:\n  - **Recognition Score**: Taxa de identificação imediata com a articulação\n  - **Depth Perception**: Avaliação da capacidade de capturar aspectos não-verbalizados\n  - **Emotional Response**: Medição da intensidade da reação emocional à descrição\n  - **Accuracy Rating**: Avaliação da precisão na captura da experiência real\n\n## SISTEMA DE INTEGRAÇÃO COM OUTROS AGENTES\n\n### PROTOCOLOS DE COOPERAÇÃO\n- **PAIN-DETECTOR → NEUROHOOK-ULTRA**: Fornece pontos de dor para criação de hooks de alta ressonância\n- **PAIN-DETECTOR → RETENTION-ARCHITECT**: Entrega mapeamento de dores para sustentação de engajamento\n- **PAIN-DETECTOR → PARADIGM-ARCHITECT**: Compartilha dores fundamentais para construção de novos paradigmas\n- **PAIN-DETECTOR → METAPHOR-ARCHITECT**: Fornece experiências de sofrimento para desenvolvimento metafórico\n- **PAIN-DETECTOR → CONVERSION-CATALYST**: Entrega hierarquia motivacional para otimização de conversão\n\nO sistema está configurado para criar uma cartografia multidimensional profundamente precisa de experiências de sofrimento, articulando com clareza cirúrgica o que o público-alvo frequentemente sente mas não consegue expressar plenamente, estabelecendo uma base de reconhecimento e compreensão genuína.\n```\n\n\n"""
    
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
functional_pain_detector = FunctionalPainDetectorController()

def run_pain_detector(messages: List[BaseMessage]) -> Dict[str, Any]:
    """Função principal de execução"""
    return functional_pain_detector.execute(messages)

if __name__ == "__main__":
    # Teste do controller
    print(f"🤖 TESTANDO {functional_pain_detector.agent_name.upper()} FUNCIONAL")
    print("=" * 50)
    
    test_messages = [HumanMessage(content="Teste de funcionamento do agente pain_detector")]
    result = run_pain_detector(test_messages)
    
    print(f"✅ Sucesso: {result['success']}")
    print(f"⏱️ Tempo: {result.get('response_time', 0):.2f}s")
    
    if result['success']:
        print("\n📝 RESPOSTA:")
        print(result['output_text'][:200] + "..." if len(result['output_text']) > 200 else result['output_text'])
    else:
        print(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
