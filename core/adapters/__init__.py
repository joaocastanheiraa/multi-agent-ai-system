"""
🎯 ADAPTADORES - CONVERSORES PARA DIFERENTES PLATAFORMAS
Adaptadores específicos para cada plataforma (AutoGen, LangSmith, etc.)
"""

from .autogen_adapter import AutoGenAdapter
from .langsmith_adapter import LangSmithAdapter

__all__ = [
    'AutoGenAdapter',
    'LangSmithAdapter'
] 