#!/usr/bin/env python3
"""
AutoGen Agent: transition_specialist
Domain: copywriters
Parent Agent: retention_architect
"""

import autogen
from typing import Dict, List, Any, Optional

class transition_specialist_Agent(autogen.AssistantAgent):
    """
    transition_specialist - Specialized AutoGen Agent
    Domain: copywriters
    Parent: retention_architect
    """
    
    def __init__(self, name: str = "transition_specialist", **kwargs):
        system_message = """
Você é transition_specialist, um agente especializado do domínio copywriters.

Sua função é trabalhar como sub-agente especializado sob o agente principal retention_architect.

Mantenha sempre foco na sua especialização e colabore efetivamente no sistema multi-agente.
"""
        
        super().__init__(
            name=name,
            system_message=system_message,
            llm_config={
                "config_list": [{
                    "model": "gpt-4-turbo-preview",
                    "api_key": "YOUR_API_KEY_HERE"
                }],
                "timeout": 120,
                "temperature": 0.7,
                "max_tokens": 2000,
            },
            **kwargs
        )
        
        self.domain = "copywriters"
        self.parent_agent = "retention_architect"
    
    def process_request(self, request: str, context: Dict[str, Any] = None) -> str:
        """Processa requisição com contexto do domínio"""
        enhanced_request = f"""
        Como especialista em {self.domain}, processando: {request}
        
        Contexto adicional: {context or 'Nenhum'}
        """
        
        return enhanced_request

# Exemplo de uso:
# agent = transition_specialist_Agent()
# response = agent.process_request("Sua requisição aqui")
