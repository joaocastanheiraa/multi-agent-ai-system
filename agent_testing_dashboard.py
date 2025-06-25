#!/usr/bin/env python3
"""
DASHBOARD DE TESTES E MONITORAMENTO DOS AGENTES
==============================================

Interface interativa para:
- Testar agentes individualmente
- Monitorar performance
- Otimizar prompts
- Visualizar métricas
- Integração com LangSmith
"""

import json
import time
import asyncio
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class AgentTestingDashboard:
    """Dashboard completo para testes e monitoramento"""
    
    def __init__(self):
        self.base_path = Path(".")
        self.domains_path = self.base_path / "domains"
        self.results_path = self.base_path / "test_results"
        self.results_path.mkdir(exist_ok=True)
        
        # URLs dos serviços
        self.mcp_server_url = "http://localhost:8000"
        self.langgraph_url = "http://localhost:8082"
        
    def load_available_agents(self) -> Dict[str, List[str]]:
        """Carrega todos os agentes disponíveis por domínio"""
        agents_by_domain = {}
        
        for domain_dir in self.domains_path.iterdir():
            if domain_dir.is_dir() and domain_dir.name != "__pycache__":
                domain = domain_dir.name
                agents_dir = domain_dir / "agents"
                
                if agents_dir.exists():
                    agents = []
                    for agent_dir in agents_dir.iterdir():
                        if agent_dir.is_dir():
                            agents.append(agent_dir.name)
                    
                    if agents:
                        agents_by_domain[domain] = sorted(agents)
        
        return agents_by_domain
    
    def load_agent_config(self, domain: str, agent_name: str) -> Optional[Dict[str, Any]]:
        """Carrega configuração de um agente"""
        manifest_path = self.domains_path / domain / "agents" / agent_name / "agent_manifest.json"
        
        if manifest_path.exists():
            with open(manifest_path, 'r') as f:
                return json.load(f)
        return None
    
    def test_agent_basic(self, domain: str, agent_name: str, test_input: str) -> Dict[str, Any]:
        """Executa teste básico de um agente"""
        start_time = time.time()
        
        try:
            # Tentar via MCP Server primeiro
            response = requests.post(
                f"{self.mcp_server_url}/agent/process",
                json={
                    "agent_name": agent_name,
                    "domain": domain,
                    "message": test_input,
                    "user_id": "dashboard_test"
                },
                timeout=30
            )
            
            execution_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "response": result,
                    "execution_time": execution_time,
                    "method": "mcp_server",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "execution_time": execution_time,
                    "method": "mcp_server",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                "success": False,
                "error": str(e),
                "execution_time": execution_time,
                "method": "mcp_server",
                "timestamp": datetime.now().isoformat()
            }
    
    def test_agent_langgraph(self, agent_name: str, test_input: str) -> Dict[str, Any]:
        """Testa agente via LangGraph"""
        start_time = time.time()
        
        try:
            # Converter nome do agente para formato LangGraph
            graph_id = agent_name.lower().replace(" ", "_").replace("|", "_")
            
            response = requests.post(
                f"{self.langgraph_url}/runs/stream",
                json={
                    "assistant_id": graph_id,
                    "input": {"message": test_input},
                    "config": {"configurable": {"thread_id": f"test_{int(time.time())}"}}
                },
                timeout=30
            )
            
            execution_time = time.time() - start_time
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "response": response.json(),
                    "execution_time": execution_time,
                    "method": "langgraph",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "execution_time": execution_time,
                    "method": "langgraph",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                "success": False,
                "error": str(e),
                "execution_time": execution_time,
                "method": "langgraph",
                "timestamp": datetime.now().isoformat()
            }
    
    def save_test_result(self, domain: str, agent_name: str, result: Dict[str, Any]):
        """Salva resultado do teste"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{domain}_{agent_name}_{timestamp}.json"
        filepath = self.results_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(result, f, indent=2)
    
    def load_test_history(self, domain: str = None, agent_name: str = None) -> List[Dict[str, Any]]:
        """Carrega histórico de testes"""
        results = []
        
        for result_file in self.results_path.glob("*.json"):
            try:
                with open(result_file, 'r') as f:
                    result = json.load(f)
                    
                # Extrair informações do nome do arquivo
                parts = result_file.stem.split('_')
                if len(parts) >= 3:
                    result['domain'] = parts[0]
                    result['agent_name'] = '_'.join(parts[1:-2])
                    
                    # Filtrar se necessário
                    if domain and result['domain'] != domain:
                        continue
                    if agent_name and result['agent_name'] != agent_name:
                        continue
                    
                    results.append(result)
                    
            except Exception as e:
                st.error(f"Erro carregando {result_file}: {e}")
        
        return sorted(results, key=lambda x: x.get('timestamp', ''), reverse=True)

def main():
    """Interface principal do Streamlit"""
    st.set_page_config(
        page_title="Dashboard de Agentes IA",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Dashboard de Testes e Monitoramento dos Agentes")
    st.markdown("---")
    
    dashboard = AgentTestingDashboard()
    
    # Sidebar para navegação
    st.sidebar.title("🎯 Navegação")
    page = st.sidebar.selectbox(
        "Escolha a página:",
        ["🧪 Teste Individual", "📊 Monitoramento", "📈 Análise de Performance", "⚙️ Configurações"]
    )
    
    if page == "🧪 Teste Individual":
        st.header("🧪 Teste Individual de Agentes")
        
        # Carregar agentes disponíveis
        agents_by_domain = dashboard.load_available_agents()
        
        if not agents_by_domain:
            st.error("❌ Nenhum agente encontrado! Verifique a estrutura de domínios.")
            return
        
        # Seleção de domínio e agente
        col1, col2 = st.columns(2)
        
        with col1:
            domain = st.selectbox("🏗️ Domínio:", list(agents_by_domain.keys()))
        
        with col2:
            agent = st.selectbox("🤖 Agente:", agents_by_domain[domain])
        
        # Carregar configuração do agente
        agent_config = dashboard.load_agent_config(domain, agent)
        
        if agent_config:
            st.subheader(f"📋 Configuração: {agent}")
            
            # Mostrar informações básicas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📦 Versão", agent_config.get('agent_info', {}).get('version', 'N/A'))
            
            with col2:
                st.metric("🎯 Status", agent_config.get('agent_info', {}).get('status', 'N/A'))
            
            with col3:
                model = agent_config.get('llm_config', {}).get('model', 'N/A')
                st.metric("🧠 Modelo", model)
            
            # Área de teste
            st.subheader("🧪 Executar Teste")
            
            test_input = st.text_area(
                "💬 Mensagem de teste:",
                placeholder=f"Digite uma mensagem para testar o {agent}...",
                height=100
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🚀 Testar via MCP Server", type="primary"):
                    if test_input:
                        with st.spinner("🔄 Executando teste..."):
                            result = dashboard.test_agent_basic(domain, agent, test_input)
                            dashboard.save_test_result(domain, agent, result)
                            
                            if result['success']:
                                st.success(f"✅ Teste executado em {result['execution_time']:.2f}s")
                                st.json(result['response'])
                            else:
                                st.error(f"❌ Erro: {result['error']}")
                    else:
                        st.warning("⚠️ Digite uma mensagem de teste!")
            
            with col2:
                if st.button("🔧 Testar via LangGraph"):
                    if test_input:
                        with st.spinner("🔄 Executando teste via LangGraph..."):
                            result = dashboard.test_agent_langgraph(agent, test_input)
                            dashboard.save_test_result(domain, agent, result)
                            
                            if result['success']:
                                st.success(f"✅ Teste LangGraph executado em {result['execution_time']:.2f}s")
                                st.json(result['response'])
                            else:
                                st.error(f"❌ Erro LangGraph: {result['error']}")
                    else:
                        st.warning("⚠️ Digite uma mensagem de teste!")
    
    elif page == "📊 Monitoramento":
        st.header("📊 Monitoramento em Tempo Real")
        
        # Status dos serviços
        st.subheader("🔍 Status dos Serviços")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            try:
                response = requests.get(f"{dashboard.mcp_server_url}/health", timeout=5)
                if response.status_code == 200:
                    st.success("✅ MCP Server - ATIVO")
                else:
                    st.error("❌ MCP Server - ERRO")
            except:
                st.error("❌ MCP Server - OFFLINE")
        
        with col2:
            try:
                response = requests.get("http://localhost:8081", timeout=5)
                if response.status_code == 200:
                    st.success("✅ AutoGen Studio - ATIVO")
                else:
                    st.error("❌ AutoGen Studio - ERRO")
            except:
                st.error("❌ AutoGen Studio - OFFLINE")
        
        with col3:
            try:
                response = requests.get(f"{dashboard.langgraph_url}", timeout=5)
                if response.status_code == 200:
                    st.success("✅ LangGraph Studio - ATIVO")
                else:
                    st.error("❌ LangGraph Studio - ERRO")
            except:
                st.error("❌ LangGraph Studio - OFFLINE")
        
        # Histórico de testes recentes
        st.subheader("📝 Histórico de Testes Recentes")
        
        recent_tests = dashboard.load_test_history()[:10]  # Últimos 10 testes
        
        if recent_tests:
            df = pd.DataFrame([{
                'Timestamp': test.get('timestamp', 'N/A'),
                'Domínio': test.get('domain', 'N/A'),
                'Agente': test.get('agent_name', 'N/A'),
                'Sucesso': '✅' if test.get('success', False) else '❌',
                'Tempo (s)': f"{test.get('execution_time', 0):.2f}",
                'Método': test.get('method', 'N/A')
            } for test in recent_tests])
            
            st.dataframe(df, use_container_width=True)
        else:
            st.info("📭 Nenhum teste executado ainda.")
    
    elif page == "📈 Análise de Performance":
        st.header("📈 Análise de Performance dos Agentes")
        
        # Carregar todos os testes
        all_tests = dashboard.load_test_history()
        
        if all_tests:
            # Converter para DataFrame
            df = pd.DataFrame(all_tests)
            
            # Métricas gerais
            st.subheader("📊 Métricas Gerais")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_tests = len(df)
                st.metric("🧪 Total de Testes", total_tests)
            
            with col2:
                success_rate = (df['success'].sum() / len(df)) * 100 if len(df) > 0 else 0
                st.metric("✅ Taxa de Sucesso", f"{success_rate:.1f}%")
            
            with col3:
                avg_time = df['execution_time'].mean() if len(df) > 0 else 0
                st.metric("⏱️ Tempo Médio", f"{avg_time:.2f}s")
            
            with col4:
                unique_agents = df['agent_name'].nunique() if 'agent_name' in df.columns else 0
                st.metric("🤖 Agentes Testados", unique_agents)
            
            # Gráficos
            if len(df) > 0:
                st.subheader("📈 Gráficos de Performance")
                
                # Gráfico de tempo de execução por agente
                if 'agent_name' in df.columns and 'execution_time' in df.columns:
                    fig_time = px.box(
                        df, 
                        x='agent_name', 
                        y='execution_time',
                        title="⏱️ Tempo de Execução por Agente"
                    )
                    fig_time.update_xaxes(tickangle=45)
                    st.plotly_chart(fig_time, use_container_width=True)
                
                # Gráfico de taxa de sucesso por domínio
                if 'domain' in df.columns:
                    success_by_domain = df.groupby('domain')['success'].mean().reset_index()
                    success_by_domain['success_rate'] = success_by_domain['success'] * 100
                    
                    fig_success = px.bar(
                        success_by_domain,
                        x='domain',
                        y='success_rate',
                        title="✅ Taxa de Sucesso por Domínio (%)"
                    )
                    st.plotly_chart(fig_success, use_container_width=True)
        else:
            st.info("📭 Nenhum dado de performance disponível ainda.")
    
    elif page == "⚙️ Configurações":
        st.header("⚙️ Configurações do Sistema")
        
        st.subheader("🔧 URLs dos Serviços")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("MCP Server URL", value=dashboard.mcp_server_url, disabled=True)
            st.text_input("LangGraph URL", value=dashboard.langgraph_url, disabled=True)
        
        with col2:
            st.text_input("AutoGen Studio URL", value="http://localhost:8081", disabled=True)
            st.text_input("LangSmith URL", value="https://smith.langchain.com", disabled=True)
        
        st.subheader("📁 Diretórios")
        st.text_input("Domínios", value=str(dashboard.domains_path), disabled=True)
        st.text_input("Resultados", value=str(dashboard.results_path), disabled=True)
        
        st.subheader("🧹 Limpeza")
        if st.button("🗑️ Limpar Resultados de Teste"):
            for file in dashboard.results_path.glob("*.json"):
                file.unlink()
            st.success("✅ Resultados de teste limpos!")

if __name__ == "__main__":
    main() 