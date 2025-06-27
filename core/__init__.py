"""
🎯 CORE - ESTRUTURA CENTRAL DO SISTEMA MULTI-AGENT AI
Módulo principal com estrutura padronizada e adaptadores para diferentes plataformas
"""

from .agent_structure import (
    AgentCore, 
    AgentLoader, 
    Tool, 
    LLMConfig, 
    AgentMetadata, 
    AgentType, 
    PlatformType,
    PlatformAdapter
)

__all__ = [
    'AgentCore',
    'AgentLoader', 
    'Tool',
    'LLMConfig',
    'AgentMetadata',
    'AgentType',
    'PlatformType',
    'PlatformAdapter'
] 