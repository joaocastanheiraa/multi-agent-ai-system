#!/usr/bin/env python3
"""
AutoGen Agent: impact-prioritizer
Domain: copywriters
Parent Agent: pain_detector
"""

import autogen
from typing import Dict, List, Any, Optional

class impact_prioritizer_Agent(autogen.AssistantAgent):
    """
    impact-prioritizer - Specialized AutoGen Agent
    Domain: copywriters
    Parent: pain_detector
    """
    
    def __init__(self, name: str = "impact-prioritizer", **kwargs):
        system_message = """
Você é impact-prioritizer, um agente especializado do domínio copywriters.

Sua função é trabalhar como sub-agente especializado sob o agente principal pain_detector.

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
        self.parent_agent = "pain_detector"
    
    def process_request(self, request: str, context: Dict[str, Any] = None) -> str:
        """Processa requisição com contexto do domínio"""
        enhanced_request = f"""
        Como especialista em {self.domain}, processando: {request}
        
        Contexto adicional: {context or 'Nenhum'}
        """
        
        return enhanced_request

# Exemplo de uso:
# agent = impact_prioritizer_Agent()
# response = agent.process_request("Sua requisição aqui")
