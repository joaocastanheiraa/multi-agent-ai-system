# 🚀 GUIA DE MIGRAÇÃO PARA AGENTES OTIMIZADOS

*Como aplicar as otimizações LangChain descobertas aos seus agentes existentes*

## 📋 ÍNDICE

1. [Visão Geral das Otimizações](#visão-geral)
2. [Pré-requisitos](#pré-requisitos)
3. [Migração Passo a Passo](#migração-passo-a-passo)
4. [Exemplos de Migração](#exemplos-de-migração)
5. [Configurações Recomendadas](#configurações-recomendadas)
6. [Testes e Validação](#testes-e-validação)
7. [Troubleshooting](#troubleshooting)

## 🎯 VISÃO GERAL DAS OTIMIZAÇÕES

### Principais Melhorias Implementadas:

✅ **Configuração Centralizada**
- Configurações via arquivos JSON
- Factory pattern para criação de agentes
- Environment-specific configs

✅ **Memória Avançada**
- ConversationBufferMemory
- ConversationSummaryMemory
- Contexto personalizado persistente

✅ **Cache Inteligente**
- TTL configurável
- Estratégias de invalidação
- Métricas de hit/miss

✅ **Observabilidade Completa**
- Logging estruturado
- Métricas de performance
- Callback handlers customizados

✅ **Error Handling Robusto**
- Retry automático com backoff
- Tratamento de exceções personalizado
- Graceful degradation

✅ **Performance Otimizada**
- Async/await nativo
- Streaming responses
- Token optimization

## 🔧 PRÉ-REQUISITOS

### Dependências Necessárias:

```bash
# Instalar dependências otimizadas
pip install langchain-openai==0.1.23
pip install langchain-core==0.3.15
pip install langchain==0.3.3
pip install langgraph==0.2.28
pip install langchain-mcp-tools
```

### Estrutura de Diretórios:

```
langchain_optimizations/
├── optimized_agent_base.py      # Classe base otimizada
├── config_examples/             # Configurações de exemplo
│   ├── high_performance_agent.json
│   ├── creative_agent.json
│   └── neurohook_optimized.json
├── practical_examples.py        # Exemplos práticos
└── MIGRATION_GUIDE.md          # Este guia
```

## 🔄 MIGRAÇÃO PASSO A PASSO

### Passo 1: Backup do Agente Atual

```bash
# Fazer backup do agente original
cp domains/copywriters/agents/neurohook_ultra/neurohook_ultra_controller.py \
   domains/copywriters/agents/neurohook_ultra/neurohook_ultra_controller_backup.py
```

### Passo 2: Criar Configuração do Agente

```json
{
  "name": "neurohook_ultra_optimized",
  "model": "gpt-4o-mini",
  "temperature": 0.8,
  "max_tokens": 2500,
  "timeout": 60,
  "enable_memory": true,
  "memory_type": "buffer",
  "enable_cache": true,
  "cache_ttl": 3600,
  "log_level": "INFO",
  "enable_streaming": false,
  "max_retries": 3,
  "retry_delay": 1.0
}
```

### Passo 3: Implementar Classe Otimizada

```python
#!/usr/bin/env python3
"""
Neurohook Ultra - Versão Otimizada
"""

import asyncio
from typing import Dict, Any, List
from pathlib import Path
import sys

# Adicionar path das otimizações
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "langchain_optimizations"))

from optimized_agent_base import OptimizedAgentBase, AgentConfig

class NeurohookUltraOptimized(OptimizedAgentBase):
    """Versão otimizada do Neurohook Ultra"""
    
    def __init__(self, config_path: str = None):
        # Carregar configuração
        if config_path:
            config = self.load_config(config_path)
        else:
            config = AgentConfig(
                name="neurohook_ultra_optimized",
                temperature=0.8,
                max_tokens=2500,
                enable_memory=True,
                memory_type="buffer",
                enable_cache=True
            )
        
        super().__init__(config)
        
        # Configurar contexto específico
        if self.memory:
            self.memory.set_context("expertise", "neurohooks")
            self.memory.set_context("techniques", [
                "curiosity_gap", "social_proof", "scarcity", 
                "authority", "reciprocity", "commitment_consistency"
            ])
            self.memory.set_context("platforms", [
                "linkedin", "instagram", "facebook", "twitter", "tiktok"
            ])
    
    async def _process_core_logic(self, input_text: str, context: Dict) -> str:
        """Lógica otimizada para criação de neurohooks"""
        
        # Enriquecer prompt com contexto especializado
        techniques = self.memory.get_context('techniques') if self.memory else []
        platforms = self.memory.get_context('platforms') if self.memory else []
        
        enhanced_prompt = f"""
        Como especialista em neurohooks e psicologia da atenção, crie hooks magnéticos:
        
        CONTEXTO DA CONVERSA:
        {context.get('chat_history', 'Nova sessão')}
        
        SOLICITAÇÃO:
        {input_text}
        
        TÉCNICAS DISPONÍVEIS:
        {', '.join(techniques)}
        
        PLATAFORMAS OTIMIZADAS:
        {', '.join(platforms)}
        
        DIRETRIZES AVANÇADAS:
        1. 🧠 Use gatilhos neurológicos comprovados pela neurociência
        2. 🎯 Crie curiosity gaps irresistíveis que geram dopamina
        3. 📊 Aplique princípios de neurociência da atenção
        4. 🔄 Teste múltiplas variações para A/B testing
        5. 📱 Otimize para diferentes plataformas e formatos
        6. 💡 Inclua insights sobre por que cada hook funciona
        
        FORMATO DE RESPOSTA:
        Para cada hook, inclua:
        - O hook otimizado
        - Técnica neurológica utilizada
        - Platform-specific optimization
        - Variações para teste A/B
        
        NEUROHOOKS OTIMIZADOS:
        """
        
        if self.agent:
            response = await self.agent.ainvoke({"messages": [("user", enhanced_prompt)]})
            return response['messages'][-1].content
        else:
            from langchain.schema import HumanMessage
            messages = [HumanMessage(content=enhanced_prompt)]
            response = await self.llm.ainvoke(messages)
            return response.content
    
    async def create_hooks_for_platform(self, content_topic: str, platform: str, quantity: int = 5) -> str:
        """Método especializado para criação de hooks por plataforma"""
        
        platform_specs = {
            "linkedin": "Profissional, autoridade, networking",
            "instagram": "Visual, lifestyle, inspiracional",
            "facebook": "Comunidade, storytelling, emocional",
            "twitter": "Conciso, trending, viral",
            "tiktok": "Dinâmico, jovem, entertainment"
        }
        
        spec = platform_specs.get(platform.lower(), "Genérico")
        
        request = f"""
        Crie {quantity} neurohooks para {platform.upper()} sobre: {content_topic}
        
        Especificações da plataforma: {spec}
        
        Otimize para o algoritmo e audiência específica do {platform}.
        """
        
        return await self.process_input(request)
    
    def get_specialized_metrics(self) -> Dict[str, Any]:
        """Métricas especializadas para neurohooks"""
        base_metrics = self.get_metrics()
        
        # Adicionar métricas específicas
        specialized_metrics = {
            **base_metrics,
            "neurohook_techniques": self.memory.get_context('techniques') if self.memory else [],
            "supported_platforms": self.memory.get_context('platforms') if self.memory else [],
            "specialization": "neurohooks_psychology"
        }
        
        return specialized_metrics

# Função para uso direto (compatibilidade com código existente)
async def generate_neurohooks(prompt: str, platform: str = None) -> str:
    """Função de compatibilidade para uso direto"""
    
    config_path = Path(__file__).parent / "neurohook_optimized.json"
    agent = NeurohookUltraOptimized(str(config_path) if config_path.exists() else None)
    
    try:
        if platform:
            result = await agent.create_hooks_for_platform(prompt, platform)
        else:
            result = await agent.process_input(prompt)
        
        return result
    finally:
        agent.cleanup()

# Exemplo de uso
async def main():
    """Exemplo de uso do agente otimizado"""
    
    agent = NeurohookUltraOptimized()
    
    try:
        # Teste básico
        result = await agent.process_input(
            "Crie 3 hooks para um post sobre produtividade para empreendedores"
        )
        print("🎯 Hooks gerados:")
        print(result)
        
        # Teste especializado por plataforma
        linkedin_hooks = await agent.create_hooks_for_platform(
            "inteligência artificial no marketing", 
            "linkedin", 
            3
        )
        print("\n💼 Hooks para LinkedIn:")
        print(linkedin_hooks)
        
        # Mostrar métricas
        print("\n📊 Métricas do agente:")
        import json
        metrics = agent.get_specialized_metrics()
        print(json.dumps(metrics, indent=2, default=str))
        
    finally:
        agent.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

### Passo 4: Atualizar Imports e Dependências

```python
# No início do arquivo controller
import sys
from pathlib import Path

# Adicionar path das otimizações
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "langchain_optimizations"))

from optimized_agent_base import OptimizedAgentBase, AgentConfig
```

## 📊 EXEMPLOS DE MIGRAÇÃO POR TIPO DE AGENTE

### 1. Agente de Copywriting (Conversion Catalyst)

**Configuração Otimizada:**
```json
{
  "name": "conversion_catalyst_optimized",
  "model": "gpt-4o-mini",
  "temperature": 0.7,
  "max_tokens": 2500,
  "enable_memory": true,
  "memory_type": "buffer",
  "enable_cache": true,
  "cache_ttl": 1800,
  "log_level": "INFO",
  "max_retries": 3
}
```

**Contexto Especializado:**
```python
if self.memory:
    self.memory.set_context("expertise", "conversion_optimization")
    self.memory.set_context("techniques", [
        "social_proof", "urgency", "value_proposition",
        "objection_handling", "emotional_triggers"
    ])
    self.memory.set_context("conversion_elements", [
        "headlines", "subheadings", "cta_buttons", 
        "testimonials", "guarantees"
    ])
```

### 2. Agente de Analytics (ANALYTICSGPT)

**Configuração Otimizada:**
```json
{
  "name": "analytics_gpt_optimized",
  "model": "gpt-4o-mini",
  "temperature": 0.2,
  "max_tokens": 3000,
  "enable_memory": true,
  "memory_type": "summary",
  "enable_cache": true,
  "cache_ttl": 3600,
  "log_level": "DEBUG",
  "max_retries": 5
}
```

**Integração MCP:**
```python
from langchain_mcp_tools import convert_mcp_to_langchain_tools

async def initialize_with_mcp_tools(self):
    """Inicializar com ferramentas MCP para análise de dados"""
    mcp_servers = {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", str(Path.cwd())]
        }
    }
    
    tools, cleanup = await convert_mcp_to_langchain_tools(mcp_servers)
    self.tools.extend(tools)
    self._mcp_cleanup = cleanup
```

### 3. Agente de APIs (APIUnifyMaster)

**Configuração Otimizada:**
```json
{
  "name": "api_unify_master_optimized",
  "model": "gpt-4o-mini",
  "temperature": 0.1,
  "max_tokens": 2000,
  "enable_memory": true,
  "memory_type": "summary",
  "enable_cache": true,
  "cache_ttl": 7200,
  "log_level": "INFO",
  "max_retries": 5,
  "retry_delay": 2.0
}
```

## ⚙️ CONFIGURAÇÕES RECOMENDADAS POR CASO DE USO

### 🚀 Alta Performance (Produção)
```json
{
  "temperature": 0.3,
  "max_tokens": 1500,
  "enable_cache": true,
  "cache_ttl": 7200,
  "memory_type": "summary",
  "enable_streaming": true,
  "max_retries": 5,
  "retry_delay": 0.5
}
```

### 🎨 Criatividade Máxima
```json
{
  "temperature": 0.9,
  "max_tokens": 3000,
  "enable_cache": false,
  "memory_type": "buffer",
  "enable_streaming": false,
  "max_retries": 3,
  "retry_delay": 1.0
}
```

### 📊 Análise e Precisão
```json
{
  "temperature": 0.1,
  "max_tokens": 2500,
  "enable_cache": true,
  "cache_ttl": 3600,
  "memory_type": "summary",
  "max_retries": 5,
  "retry_delay": 2.0
}
```

## 🧪 TESTES E VALIDAÇÃO

### Script de Teste Automatizado:

```python
#!/usr/bin/env python3
"""
Script de teste para validar migração dos agentes
"""

import asyncio
import json
import time
from pathlib import Path

async def test_agent_migration(agent_class, config_path: str):
    """Testar migração de um agente"""
    
    print(f"🧪 Testando migração: {agent_class.__name__}")
    
    # Carregar agente otimizado
    agent = agent_class(config_path)
    
    # Testes básicos
    tests = [
        "Teste de funcionalidade básica",
        "Teste de memória - primeira mensagem",
        "Teste de memória - segunda mensagem relacionada",
        "Teste de cache - mesma query",
        "Teste de performance - query complexa"
    ]
    
    results = {}
    
    for i, test in enumerate(tests):
        start_time = time.time()
        
        try:
            if i == 1:
                await agent.process_input("Meu nome é João")
            elif i == 2:
                result = await agent.process_input("Qual é o meu nome?")
            else:
                result = await agent.process_input(f"Execute: {test}")
            
            duration = time.time() - start_time
            
            results[test] = {
                "status": "✅ PASSOU",
                "duration": f"{duration:.2f}s",
                "has_result": len(result) > 0 if 'result' in locals() else True
            }
            
        except Exception as e:
            results[test] = {
                "status": "❌ FALHOU",
                "error": str(e),
                "duration": f"{time.time() - start_time:.2f}s"
            }
    
    # Métricas finais
    metrics = agent.get_metrics()
    
    # Cleanup
    agent.cleanup()
    
    return {
        "agent": agent_class.__name__,
        "tests": results,
        "metrics": metrics
    }

async def run_migration_tests():
    """Executar todos os testes de migração"""
    
    # Lista de agentes para testar
    test_cases = [
        # Adicionar seus agentes aqui
        # (NeurohookUltraOptimized, "path/to/config.json"),
    ]
    
    all_results = []
    
    for agent_class, config_path in test_cases:
        result = await test_agent_migration(agent_class, config_path)
        all_results.append(result)
    
    # Salvar relatório
    with open("migration_test_report.json", "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    
    print("📊 Relatório de testes salvo em: migration_test_report.json")

if __name__ == "__main__":
    asyncio.run(run_migration_tests())
```

## 🔧 TROUBLESHOOTING

### Problemas Comuns e Soluções:

#### 1. **ImportError: No module named 'optimized_agent_base'**
```python
# Solução: Adicionar path correto
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "langchain_optimizations"))
```

#### 2. **Erro de Configuração JSON**
```bash
# Validar JSON
python -m json.tool config.json
```

#### 3. **Problemas de Memória**
```python
# Limpar memória periodicamente
if self.memory:
    self.memory.clear_memory()
```

#### 4. **Cache não funcionando**
```python
# Verificar configuração
print(f"Cache enabled: {self.config.enable_cache}")
print(f"Cache TTL: {self.config.cache_ttl}")
```

#### 5. **Performance degradada**
```python
# Ajustar configurações
config.max_tokens = 1500  # Reduzir tokens
config.temperature = 0.3  # Reduzir variabilidade
config.enable_streaming = True  # Ativar streaming
```

## 📈 MONITORAMENTO PÓS-MIGRAÇÃO

### Métricas para Acompanhar:

1. **Performance**
   - Tempo de resposta médio
   - Taxa de cache hit
   - Número de retries

2. **Qualidade**
   - Satisfação das respostas
   - Consistência com memória
   - Precisão técnica

3. **Recursos**
   - Uso de tokens
   - Consumo de memória
   - CPU utilizada

### Dashboard de Monitoramento:

```python
def generate_monitoring_dashboard(agents: List[OptimizedAgentBase]):
    """Gerar dashboard de monitoramento"""
    
    dashboard_data = {
        "timestamp": datetime.now().isoformat(),
        "agents": []
    }
    
    for agent in agents:
        metrics = agent.get_metrics()
        dashboard_data["agents"].append({
            "name": agent.config.name,
            "status": "active",
            "metrics": metrics
        })
    
    return dashboard_data
```

## 🎯 PRÓXIMOS PASSOS

1. **Migrar agentes prioritários** (neurohook_ultra, conversion_catalyst)
2. **Implementar testes automatizados**
3. **Configurar monitoramento**
4. **Otimizar baseado em métricas**
5. **Expandir para todos os agentes**

---

## 📞 SUPORTE

Para dúvidas ou problemas na migração:

1. Revisar logs detalhados
2. Verificar configurações JSON
3. Testar com configuração mínima
4. Consultar exemplos práticos

**Sucesso na migração! 🚀** 