#!/usr/bin/env python3
"""
AutoGen Agent: dissonance_architect
Domain: copywriters
Parent Agent: neurohook_ultra
"""

import autogen
from typing import Dict, List, Any, Optional

class dissonance_architect_Agent(autogen.AssistantAgent):
    """
    dissonance_architect - Specialized AutoGen Agent
    Domain: copywriters
    Parent: neurohook_ultra
    """
    
    def __init__(self, name: str = "dissonance_architect", **kwargs):
        system_message = """
Você é dissonance_architect, um agente especializado do domínio copywriters.

Sua função é trabalhar como sub-agente especializado sob o agente principal neurohook_ultra.

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
        self.parent_agent = "neurohook_ultra"
    
    def process_request(self, request: str, context: Dict[str, Any] = None) -> str:
        """Processa requisição com contexto do domínio"""
        enhanced_request = f"""
        Como especialista em {self.domain}, processando: {request}
        
        Contexto adicional: {context or 'Nenhum'}
        """
        
        return enhanced_request

# Exemplo de uso:
# agent = dissonance_architect_Agent()
# response = agent.process_request("Sua requisição aqui")
