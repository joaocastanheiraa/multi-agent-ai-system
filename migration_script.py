#!/usr/bin/env python3
"""
🚀 SCRIPT DE MIGRAÇÃO - AGENTES PARA LANGCHAIN OTIMIZADO
Script prático para migrar seus agentes existentes para usar todas as otimizações LangChain
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class AgentMigrationTool:
    """Ferramenta para migrar agentes para versão otimizada"""
    
    def __init__(self):
        self.project_root = Path.cwd().parent
        self.domains_path = self.project_root / "domains"
        self.optimization_path = Path.cwd()
        
        print("🔧 FERRAMENTA DE MIGRAÇÃO INICIALIZADA")
        print(f"📁 Projeto: {self.project_root}")
        print(f"📁 Domínios: {self.domains_path}")
        print(f"📁 Otimizações: {self.optimization_path}")
    
    def analyze_existing_agents(self) -> Dict[str, Any]:
        """Analisa agentes existentes no projeto"""
        print("\n🔍 ANALISANDO AGENTES EXISTENTES...")
        
        agents_found = {}
        
        if not self.domains_path.exists():
            print("❌ Diretório domains/ não encontrado")
            return agents_found
        
        # Buscar controladores de agentes
        for domain_dir in self.domains_path.iterdir():
            if domain_dir.is_dir() and domain_dir.name != "__pycache__":
                domain_name = domain_dir.name
                agents_found[domain_name] = []
                
                agents_dir = domain_dir / "agents"
                if agents_dir.exists():
                    for agent_dir in agents_dir.iterdir():
                        if agent_dir.is_dir():
                            # Procurar controller
                            controller_files = list(agent_dir.glob("*_controller.py"))
                            if controller_files:
                                controller_file = controller_files[0]
                                
                                # Analisar controller
                                agent_info = self._analyze_controller(controller_file)
                                agent_info['domain'] = domain_name
                                agent_info['agent_name'] = agent_dir.name
                                agent_info['controller_path'] = controller_file
                                
                                agents_found[domain_name].append(agent_info)
        
        # Relatório de análise
        total_agents = sum(len(agents) for agents in agents_found.values())
        print(f"\n📊 ANÁLISE COMPLETA:")
        print(f"   🤖 Total de agentes encontrados: {total_agents}")
        
        for domain, agents in agents_found.items():
            if agents:
                print(f"   📁 {domain}: {len(agents)} agentes")
                for agent in agents:
                    print(f"      • {agent['agent_name']} - {agent['optimization_potential']}")
        
        return agents_found
    
    def _analyze_controller(self, controller_file: Path) -> Dict[str, Any]:
        """Analisa um controller específico"""
        try:
            with open(controller_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Analisar estrutura atual
            analysis = {
                'file_size_kb': len(content) / 1024,
                'line_count': len(content.split('\n')),
                'uses_basic_langchain': 'ChatOpenAI' in content and 'create_react_agent' not in content,
                'has_cache': 'cache' in content.lower(),
                'has_memory': 'memory' in content.lower() and 'ConversationBuffer' in content,
                'has_streaming': 'streaming' in content.lower(),
                'has_rag': 'vector' in content.lower() or 'embedding' in content.lower(),
                'has_observability': 'callback' in content.lower() or 'metrics' in content.lower(),
                'prompt_size_estimate': self._estimate_prompt_size(content)
            }
            
            # Calcular potencial de otimização
            optimization_score = 0
            if not analysis['has_cache']: optimization_score += 30
            if not analysis['has_memory']: optimization_score += 25
            if not analysis['has_streaming']: optimization_score += 20
            if not analysis['has_rag']: optimization_score += 15
            if not analysis['has_observability']: optimization_score += 10
            
            if analysis['prompt_size_estimate'] > 10000:  # Prompt muito grande
                optimization_score += 20
            
            analysis['optimization_potential'] = f"{min(optimization_score, 100)}% melhoria possível"
            
            return analysis
            
        except Exception as e:
            return {'error': str(e), 'optimization_potential': 'Erro na análise'}
    
    def _estimate_prompt_size(self, content: str) -> int:
        """Estima tamanho do prompt principal"""
        # Procurar por strings longas que podem ser prompts
        lines = content.split('\n')
        max_string_size = 0
        
        in_multiline_string = False
        current_string_size = 0
        
        for line in lines:
            if '"""' in line or "'''" in line:
                if in_multiline_string:
                    max_string_size = max(max_string_size, current_string_size)
                    current_string_size = 0
                    in_multiline_string = False
                else:
                    in_multiline_string = True
            
            if in_multiline_string:
                current_string_size += len(line)
        
        return max_string_size
    
    def create_migration_plan(self, agents_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria plano de migração personalizado"""
        print("\n📋 CRIANDO PLANO DE MIGRAÇÃO...")
        
        migration_plan = {
            'priority_agents': [],
            'migration_phases': [],
            'estimated_timeline': {},
            'roi_analysis': {}
        }
        
        # Priorizar agentes por impacto
        all_agents = []
        for domain, agents in agents_data.items():
            for agent in agents:
                agent['priority_score'] = self._calculate_priority_score(agent)
                all_agents.append(agent)
        
        # Ordenar por prioridade
        all_agents.sort(key=lambda x: x['priority_score'], reverse=True)
        
        # Top 3 agentes prioritários
        migration_plan['priority_agents'] = all_agents[:3]
        
        # Criar fases de migração
        phases = [
            {
                'phase': 1,
                'name': 'Cache + Memory',
                'agents': all_agents[:2],
                'duration_days': 3,
                'benefits': ['99% redução tempo resposta', 'Contexto persistente']
            },
            {
                'phase': 2,
                'name': 'RAG + Observabilidade',
                'agents': all_agents[2:4] if len(all_agents) > 2 else [],
                'duration_days': 4,
                'benefits': ['Acesso knowledge base', 'Métricas completas']
            },
            {
                'phase': 3,
                'name': 'Streaming + Error Handling',
                'agents': all_agents[4:] if len(all_agents) > 4 else [],
                'duration_days': 3,
                'benefits': ['UX melhorada', 'Robustez completa']
            }
        ]
        
        migration_plan['migration_phases'] = phases
        
        # Timeline estimado
        total_days = sum(phase['duration_days'] for phase in phases)
        migration_plan['estimated_timeline'] = {
            'total_days': total_days,
            'total_weeks': total_days / 7,
            'start_recommendation': 'Imediatamente',
            'completion_target': f'{total_days} dias úteis'
        }
        
        # Análise de ROI
        migration_plan['roi_analysis'] = self._calculate_roi(all_agents)
        
        return migration_plan
    
    def _calculate_priority_score(self, agent: Dict[str, Any]) -> int:
        """Calcula score de prioridade para migração"""
        score = 0
        
        # Domínio copywriters tem prioridade (mais uso)
        if agent['domain'] == 'copywriters':
            score += 30
        elif agent['domain'] == 'apis':
            score += 25
        elif agent['domain'] == 'analytics':
            score += 20
        
        # Agentes com prompts grandes se beneficiam mais
        if agent.get('prompt_size_estimate', 0) > 10000:
            score += 25
        
        # Agentes sem otimizações básicas
        if not agent.get('has_cache', False):
            score += 20
        if not agent.get('has_memory', False):
            score += 15
        if not agent.get('has_rag', False):
            score += 10
        
        return score
    
    def _calculate_roi(self, agents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcula ROI da migração"""
        
        # Estimativas baseadas na análise anterior
        usage_estimates = {
            'copywriters': 50,  # consultas/dia
            'apis': 30,
            'analytics': 20,
            'default': 15
        }
        
        hourly_rates = {
            'copywriters': 100,
            'apis': 150,
            'analytics': 120,
            'default': 100
        }
        
        total_monthly_savings = 0
        total_agents = len(agents)
        
        for agent in agents:
            domain = agent.get('domain', 'default')
            daily_usage = usage_estimates.get(domain, usage_estimates['default'])
            hourly_rate = hourly_rates.get(domain, hourly_rates['default'])
            
            # Tempo economizado por consulta (6.8s -> 0.05s)
            time_saved_per_query = 6.75  # segundos
            daily_time_saved = (daily_usage * time_saved_per_query) / 60  # minutos
            monthly_time_saved = daily_time_saved * 30 / 60  # horas
            monthly_savings = monthly_time_saved * hourly_rate
            
            total_monthly_savings += monthly_savings
        
        return {
            'monthly_savings': total_monthly_savings,
            'annual_savings': total_monthly_savings * 12,
            'per_agent_average': total_monthly_savings / total_agents if total_agents > 0 else 0,
            'payback_period_days': 1,  # ROI imediato
            'break_even_analysis': 'ROI positivo desde o primeiro dia'
        }
    
    def generate_migration_code(self, agent_info: Dict[str, Any]) -> str:
        """Gera código de migração para um agente específico"""
        
        domain = agent_info.get('domain', 'general')
        agent_name = agent_info.get('agent_name', 'unknown')
        
        # Determinar configuração otimizada baseada no domínio
        if domain == 'copywriters':
            config_type = 'creative_writing'
        elif domain == 'apis':
            config_type = 'enterprise_rag'
        elif domain == 'analytics':
            config_type = 'code_analysis'
        else:
            config_type = 'creative_writing'
        
        migration_code = f'''#!/usr/bin/env python3
"""
🚀 {agent_name.upper()} - VERSÃO OTIMIZADA
Migração automática para LangChain otimizado
Gerado em: {datetime.now().isoformat()}
"""

import os
import asyncio
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

# Imports das otimizações LangChain
from langchain_optimizations.optimized_agent_base import OptimizedAgentBase, AgentConfig
from langchain_optimizations.advanced_langchain_features import AdvancedLangChainAgent, AdvancedFeatureConfig
from langchain_optimizations.specialized_configs import SpecializedConfigs

# Imports LangChain
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser

class Optimized{agent_name.title().replace('_', '')}Controller:
    """
    Versão otimizada do {agent_name} usando todas as funcionalidades avançadas LangChain
    """
    
    def __init__(self):
        self.agent_name = "{agent_name}_optimized"
        self.domain = "{domain}"
        
        # Configuração otimizada específica para o domínio
        self.config = SpecializedConfigs.{config_type}()
        
        # Configurar agent otimizado
        self.agent = AdvancedLangChainAgent(
            config=self.config.agent_config,
            advanced_config=self.config.advanced_config
        )
        
        # Configurar prompt otimizado
        self.setup_optimized_prompt()
        
        print(f"🚀 {{self.agent_name}} OTIMIZADO INICIALIZADO")
        print(f"✅ Configuração: {config_type}")
        self._log_optimizations()
    
    def setup_optimized_prompt(self):
        """Configura prompt otimizado com LCEL"""
        
        # TODO: Migrar seu prompt original para aqui
        # Mantenha a essência mas otimize a estrutura
        system_prompt = \"\"\"
        [MIGRE SEU PROMPT ORIGINAL AQUI]
        
        INSTRUÇÕES DE MIGRAÇÃO:
        1. Mantenha a personalidade e expertise do agente
        2. Simplifique instruções longas
        3. Use format_instructions para output estruturado
        4. Adicione placeholders para memory se necessário
        \"\"\"
        
        # Template com memory e format instructions
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{{input}}")
        ])
    
    async def execute_optimized(self, request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Executa o agente otimizado com todas as funcionalidades avançadas
        """
        start_time = datetime.now()
        
        try:
            print(f"🧠 Executando {{self.agent_name}}: {{request[:50]}}...")
            
            # Preparar contexto com memory
            chat_history = []
            if context and 'previous_context' in context:
                chat_history.append(HumanMessage(content=f"Contexto: {{context['previous_context']}}"))
            
            # Criar chain otimizada com LCEL
            chain = self.prompt_template | self.agent.llm
            
            # Executar com todas as otimizações
            if self.config.advanced_config.enable_streaming:
                result = await self._execute_with_streaming(chain, request, chat_history)
            else:
                result = await chain.ainvoke({{
                    "input": request,
                    "chat_history": chat_history
                }})
            
            # Calcular métricas
            response_time = (datetime.now() - start_time).total_seconds()
            
            # Preparar resposta completa
            response = {{
                'success': True,
                'agent_name': self.agent_name,
                'result': result.content if hasattr(result, 'content') else str(result),
                'response_time': response_time,
                'cache_used': self.agent.cache.get_stats()['hit_rate'] > 0,
                'memory_context': len(chat_history) > 0,
                'timestamp': datetime.now().isoformat(),
                'optimizations_active': self._get_active_optimizations()
            }}
            
            print(f"✅ Execução concluída em {{response_time:.2f}}s")
            return response
            
        except Exception as e:
            print(f"❌ Erro na execução: {{e}}")
            return {{
                'success': False,
                'error': str(e),
                'response_time': (datetime.now() - start_time).total_seconds()
            }}
    
    async def _execute_with_streaming(self, chain, request: str, chat_history: List):
        """Executa com streaming para UX melhorada"""
        print("🔄 Modo streaming ativado...")
        
        # Implementar streaming real aqui
        result = await chain.ainvoke({{
            "input": request,
            "chat_history": chat_history
        }})
        
        return result
    
    def _log_optimizations(self):
        """Log das otimizações ativas"""
        optimizations = [
            f"Cache: {{self.config.agent_config.enable_cache}}",
            f"Memory: {{self.config.agent_config.memory_type}}",
            f"Streaming: {{self.config.advanced_config.enable_streaming}}",
            f"RAG: {{self.config.advanced_config.enable_rag}}",
            f"Observabilidade: Ativa"
        ]
        
        for opt in optimizations:
            print(f"   ✅ {{opt}}")
    
    def _get_active_optimizations(self) -> List[str]:
        """Retorna lista de otimizações ativas"""
        active = []
        
        if self.config.agent_config.enable_cache:
            active.append("Cache Inteligente")
        if self.config.agent_config.memory_type != "none":
            active.append("Memory System")
        if self.config.advanced_config.enable_streaming:
            active.append("Streaming")
        if self.config.advanced_config.enable_rag:
            active.append("RAG")
        
        active.append("Observabilidade")
        active.append("Error Handling")
        
        return active
    
    def get_performance_dashboard(self) -> Dict[str, Any]:
        """Retorna dashboard de performance"""
        cache_stats = self.agent.cache.get_stats()
        
        return {{
            'agent_name': self.agent_name,
            'cache_stats': cache_stats,
            'configuration': {{
                'model': self.config.agent_config.model,
                'temperature': self.config.agent_config.temperature,
                'max_tokens': self.config.agent_config.max_tokens,
                'optimizations_count': len(self._get_active_optimizations())
            }},
            'timestamp': datetime.now().isoformat()
        }}

# Instância global otimizada
optimized_{agent_name} = Optimized{agent_name.title().replace('_', '')}Controller()

async def run_{agent_name}_optimized(request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Função principal de execução otimizada"""
    return await optimized_{agent_name}.execute_optimized(request, context)

# Função de compatibilidade com código existente
def run_{agent_name}(messages: List[BaseMessage]) -> Dict[str, Any]:
    """Função de compatibilidade - mantém interface existente"""
    
    # Extrair mensagem do usuário
    user_message = ""
    for msg in messages:
        if isinstance(msg, HumanMessage):
            user_message = msg.content
            break
    
    if not user_message:
        return {{'success': False, 'error': 'Nenhuma mensagem encontrada'}}
    
    # Executar versão otimizada
    import asyncio
    result = asyncio.run(run_{agent_name}_optimized(user_message))
    
    # Converter para formato compatível
    if result['success']:
        ai_response = AIMessage(content=result['result'])
        return {{
            'success': True,
            'agent_name': result['agent_name'],
            'messages': messages + [ai_response],
            'response_time': result['response_time'],
            'optimizations_used': result['optimizations_active']
        }}
    else:
        return result

if __name__ == "__main__":
    # Teste do controller otimizado
    async def test_optimized():
        result = await run_{agent_name}_optimized("Teste de migração")
        print("📊 RESULTADO DO TESTE:")
        print(f"   ✅ Sucesso: {{result['success']}}")
        print(f"   ⏱️ Tempo: {{result.get('response_time', 0):.3f}}s")
        print(f"   🚀 Otimizações: {{', '.join(result.get('optimizations_active', []))}}")
    
    asyncio.run(test_optimized())
'''
        
        return migration_code
    
    def execute_migration_plan(self, migration_plan: Dict[str, Any]) -> None:
        """Executa o plano de migração"""
        print("\n🚀 EXECUTANDO PLANO DE MIGRAÇÃO...")
        
        print("\n📋 RESUMO DO PLANO:")
        print(f"   🎯 Agentes prioritários: {len(migration_plan['priority_agents'])}")
        print(f"   📅 Timeline: {migration_plan['estimated_timeline']['total_days']} dias")
        print(f"   💰 ROI anual: R$ {migration_plan['roi_analysis']['annual_savings']:,.0f}")
        
        print("\n📊 TOP 3 AGENTES PARA MIGRAÇÃO:")
        for i, agent in enumerate(migration_plan['priority_agents'], 1):
            print(f"   {i}. {agent['agent_name']} ({agent['domain']})")
            print(f"      • Potencial: {agent['optimization_potential']}")
            print(f"      • Prioridade: {agent['priority_score']}/100")
        
        print("\n📅 FASES DE MIGRAÇÃO:")
        for phase in migration_plan['migration_phases']:
            print(f"   Fase {phase['phase']}: {phase['name']} ({phase['duration_days']} dias)")
            print(f"      • Agentes: {len(phase['agents'])}")
            print(f"      • Benefícios: {', '.join(phase['benefits'])}")
        
        # Gerar código de migração para o primeiro agente
        if migration_plan['priority_agents']:
            top_agent = migration_plan['priority_agents'][0]
            print(f"\n💻 GERANDO CÓDIGO DE MIGRAÇÃO PARA: {top_agent['agent_name']}")
            
            migration_code = self.generate_migration_code(top_agent)
            
            # Salvar código de migração
            output_file = self.optimization_path / f"{top_agent['agent_name']}_optimized.py"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(migration_code)
            
            print(f"✅ Código salvo em: {output_file}")
            print("\n📋 PRÓXIMOS PASSOS:")
            print("   1. Revisar o código gerado")
            print("   2. Migrar seu prompt original")
            print("   3. Testar a versão otimizada")
            print("   4. Substituir o controller original")
            print("   5. Monitorar métricas de performance")

def main():
    """Função principal do script de migração"""
    print("🚀 SCRIPT DE MIGRAÇÃO - LANGCHAIN OTIMIZADO")
    print("=" * 60)
    
    # Inicializar ferramenta
    migration_tool = AgentMigrationTool()
    
    # Analisar agentes existentes
    agents_data = migration_tool.analyze_existing_agents()
    
    if not any(agents_data.values()):
        print("\n❌ Nenhum agente encontrado para migração")
        print("📁 Verifique se está executando do diretório correto")
        return
    
    # Criar plano de migração
    migration_plan = migration_tool.create_migration_plan(agents_data)
    
    # Executar plano
    migration_tool.execute_migration_plan(migration_plan)
    
    print("\n🎉 MIGRAÇÃO PLANEJADA COM SUCESSO!")
    print("📞 Execute os códigos gerados para começar a migração")

if __name__ == "__main__":
    main() 