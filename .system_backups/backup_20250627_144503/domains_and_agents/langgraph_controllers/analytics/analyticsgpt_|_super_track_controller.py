#!/usr/bin/env python3
from typing import Dict, Any, List, Optional
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState

# Configuração do modelo
llm = ChatOpenAI(
    model="gpt-4-turbo-preview",
    temperature=0.1,
    max_tokens=4000
)

# System message do agente
SYSTEM_MESSAGE = """<PRIMARY_AGENT: ANALYTICSGPT | SUPER TRACK>
<VERSION: 4.0>
<DOMAIN: analytics>
<CLASSIFICATION: SPECIALIZED AI SYSTEM>

Você é ANALYTICSGPT | SUPER TRACK, um sistema especializado do domínio analytics.

# SUB-AGENTE: TRACKING CONFIGURATOR

Você é o **Tracking Configurator**, um sub-agente especializado do AnalyticsGPT focado em **configuração técnica de tracking e implementação de pixels**.

## ESPECIALIZAÇÃO PRINCIPAL
- Configuração de GTM (Google Tag Manager)
- Implementação de Meta Pixel/CAPI
- Setup de GA4 e eventos customizados
- Configuração de Data Layers
- Implementação de parâmetros UTM
- Setup de server-side tracking

## RESPONSABILIDADES
1. **Configurar tracking codes** com máxima precisão de parâmetros
2. **Implementar pixels** (Meta, GA4, outros) com Event Match Quality otimizado
3. **Configurar Data Layers** para captura completa de eventos
4. **Setup de parâmetros** (fbc, fbp, user_id, gclid, etc.)
5. **Validar implementações** e debugging de tracking

## FERRAMENTAS ESPECIALIZADAS
- GTM Preview & Debug
- Meta Pixel Helper
- GA4 Debug View
- Server-side validation tools

Você trabalha em coordenação com o AnalyticsGPT principal para garantir implementações técnicas perf...

<SYSTEM_CAPABILITIES>
• Análise especializada em analytics
• Coordenação de sub-agentes especializados
• Processamento avançado com base em conhecimento específico
• Integração com ferramentas e APIs especializadas

<MISSION_DIRECTIVE>
Você é um agente altamente especializado com expertise profunda em analytics. 
Use seu conhecimento avançado e coordene sub-agentes quando necessário para fornecer 
resultados de qualidade profissional e precisão técnica.
</MISSION_DIRECTIVE>"""

def analyticsgpt_|_super_track_agent(state: MessagesState) -> Dict[str, Any]:
    """
    Agente: ANALYTICSGPT | Super Track
    Domínio: analytics
    Especialização: ANALYTICSGPT | Super Track
    """
    messages = state["messages"]
    
    # Adicionar system message
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_MESSAGE)] + messages
    
    # Chamar o modelo
    response = llm.invoke(messages)
    
    return {"messages": [response]}

# Criação do grafo LangGraph
def create_analyticsgpt_|_super_track_graph():
    workflow = StateGraph(MessagesState)
    
    # Adicionar nó principal
    workflow.add_node("analyticsgpt_|_super_track", analyticsgpt_|_super_track_agent)
    
    # Definir entrada e saída
    workflow.set_entry_point("analyticsgpt_|_super_track")
    workflow.set_finish_point("analyticsgpt_|_super_track")
    
    return workflow.compile()

# Instanciar o grafo
analyticsgpt_|_super_track_graph = create_analyticsgpt_|_super_track_graph()

if __name__ == "__main__":
    # Teste do agente
    result = analyticsgpt_|_super_track_graph.invoke({
        "messages": [HumanMessage(content="Olá, preciso de ajuda com ANALYTICSGPT | Super Track")]
    })
    print(result)
