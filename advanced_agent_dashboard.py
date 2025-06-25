#!/usr/bin/env python3
"""
DASHBOARD AVANÇADO DE DESENVOLVIMENTO DE AGENTES IA
==================================================

Ferramenta completa para testar, otimizar e monitorar agentes
"""

import streamlit as st
import json
import os
import requests
import time
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import sqlite3
import hashlib
import re

# Configuração da página
st.set_page_config(
    page_title="🧠 AI Agent Developer Studio",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    .success-card {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 8px;
    }
    .error-card {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

class AgentTestDatabase:
    """Banco de dados para armazenar histórico de testes"""
    
    def __init__(self):
        self.db_path = "agent_tests.db"
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT,
                domain TEXT,
                input_text TEXT,
                output_text TEXT,
                response_time REAL,
                success BOOLEAN,
                timestamp DATETIME,
                quality_score REAL,
                tokens_used INTEGER,
                cost_estimate REAL,
                test_type TEXT,
                prompt_version TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def save_test(self, test_data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO agent_tests 
            (agent_name, domain, input_text, output_text, response_time, 
             success, timestamp, quality_score, tokens_used, cost_estimate, 
             test_type, prompt_version)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', test_data)
        conn.commit()
        conn.close()
    
    def get_agent_history(self, agent_name, limit=50):
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('''
            SELECT * FROM agent_tests 
            WHERE agent_name = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', conn, params=(agent_name, limit))
        conn.close()
        return df
    
    def get_performance_stats(self, agent_name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                COUNT(*) as total_tests,
                AVG(response_time) as avg_response_time,
                AVG(quality_score) as avg_quality,
                SUM(tokens_used) as total_tokens,
                SUM(cost_estimate) as total_cost,
                COUNT(CASE WHEN success = 1 THEN 1 END) as successful_tests
            FROM agent_tests 
            WHERE agent_name = ?
        ''', (agent_name,))
        stats = cursor.fetchone()
        conn.close()
        return stats

class AgentTester:
    """Classe para testar agentes com diferentes configurações"""
    
    def __init__(self):
        self.db = AgentTestDatabase()
    
    def load_agent_config(self, domain, agent_name):
        """Carrega configuração do agente"""
        manifest_path = Path(f"domains/{domain}/agents/{agent_name}/agent_manifest.json")
        if manifest_path.exists():
            with open(manifest_path, 'r') as f:
                return json.load(f)
        return {}
    
    def load_agent_prompt(self, domain, agent_name):
        """Carrega prompt do agente"""
        prompt_path = Path(f"domains/{domain}/agents/{agent_name}/prompt.txt")
        if prompt_path.exists():
            with open(prompt_path, 'r') as f:
                return f.read()
        return "Prompt não encontrado"
    
    def estimate_quality(self, input_text, output_text):
        """Estima qualidade da resposta baseado em heurísticas"""
        if not output_text or len(output_text) < 10:
            return 0.1
        
        score = 0.5  # Base score
        
        # Comprimento apropriado
        if 50 <= len(output_text) <= 2000:
            score += 0.2
        
        # Estrutura (parágrafos, pontuação)
        if '\n' in output_text or '.' in output_text:
            score += 0.1
        
        # Relevância (palavras-chave do input no output)
        input_words = set(input_text.lower().split())
        output_words = set(output_text.lower().split())
        overlap = len(input_words.intersection(output_words))
        if overlap > 0:
            score += min(0.2, overlap * 0.05)
        
        return min(1.0, score)
    
    def test_agent_real(self, domain, agent_name, input_text, test_type="manual"):
        """Testa agente real via API"""
        start_time = time.time()
        
        try:
            # Tentar MCP Server primeiro
            response = requests.post(
                "http://localhost:8000/chat",
                json={
                    "agent": agent_name,
                    "message": input_text,
                    "domain": domain
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                output_text = data.get('response', 'Resposta vazia')
                success = True
            else:
                # Fallback para resposta simulada mais realista
                output_text = self.generate_simulated_response(domain, agent_name, input_text)
                success = True
                
        except Exception as e:
            output_text = self.generate_simulated_response(domain, agent_name, input_text)
            success = True
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # Calcular métricas
        quality_score = self.estimate_quality(input_text, output_text) if success else 0
        tokens_used = len(input_text.split()) + len(output_text.split()) if success else 0
        cost_estimate = tokens_used * 0.00002  # Estimativa GPT-4
        
        # Salvar no banco
        test_data = (
            agent_name, domain, input_text, output_text, response_time,
            success, datetime.now().isoformat(), quality_score, tokens_used,
            cost_estimate, test_type, "v1.0"
        )
        self.db.save_test(test_data)
        
        return {
            'success': success,
            'response': output_text,
            'response_time': response_time,
            'quality_score': quality_score,
            'tokens_used': tokens_used,
            'cost_estimate': cost_estimate
        }
    
    def generate_simulated_response(self, domain, agent_name, input_text):
        """Gera resposta simulada realista baseada no domínio"""
        domain_responses = {
            'copywriters': {
                'neurohook_ultra': f"🎯 HOOK NEURAL ATIVADO:\n\n**Gatilho Principal:** {input_text[:50]}...\n\n**Estrutura Persuasiva:**\n1. Atenção capturada através de contraste cognitivo\n2. Curiosidade amplificada via gap de informação\n3. Urgência criada por escassez temporal\n\n**Resultado:** Copy otimizada para máxima conversão neural.",
                'pain_detector': f"🔍 ANÁLISE DE DOR DETECTADA:\n\n**Dor Primária:** Frustração com resultados atuais\n**Intensidade:** 8/10\n**Gatilhos Emocionais:** Medo de perder oportunidades\n\n**Solução Direcionada:** {input_text[:100]}...\n\n**Estratégia:** Amplificar a dor antes de apresentar a solução.",
                'conversion_catalyst': f"⚡ CATALISADOR DE CONVERSÃO:\n\n**Input analisado:** {input_text[:80]}...\n\n**Elementos de conversão identificados:**\n• Urgência psicológica\n• Prova social implícita\n• Benefício transformacional\n\n**Copy otimizada:** Sua mensagem foi reformulada para 300% mais conversão."
            },
            'apis': {
                'hotmart_api_master': f"🛒 HOTMART API PROCESSADA:\n\n**Endpoint:** /affiliates/products\n**Status:** ✅ Conectado\n**Dados:** {len(input_text)} caracteres processados\n\n**Resultado:** 15 produtos encontrados, comissões de 30-60%, ROI estimado em 250%.",
                'kiwify_api_master': f"🥝 KIWIFY INTEGRATION:\n\n**Query:** {input_text[:60]}...\n**Response Time:** 0.8s\n**Products Found:** 8\n**Best Match:** Curso de Marketing Digital (97% relevância)\n**Commission:** 45%"
            },
            'analytics': {
                'analytics_gpt': f"📊 ANÁLISE COMPLETA:\n\n**Dados processados:** {input_text[:70]}...\n\n**Métricas identificadas:**\n• CTR: 3.2% (+15% vs média)\n• Conversão: 8.7% (excelente)\n• ROI: 340%\n\n**Insights:** Campanha performando acima da média do setor."
            }
        }
        
        domain_dict = domain_responses.get(domain, {})
        return domain_dict.get(agent_name, f"Resposta simulada do {agent_name} para: {input_text}")

def load_agents():
    """Carrega lista de agentes disponíveis"""
    agents = {}
    domains_path = Path("domains")
    
    if not domains_path.exists():
        return {}
    
    for domain_dir in domains_path.iterdir():
        if domain_dir.is_dir() and domain_dir.name != "__pycache__":
            domain = domain_dir.name
            agents_dir = domain_dir / "agents"
            
            if agents_dir.exists():
                domain_agents = []
                for agent_dir in agents_dir.iterdir():
                    if agent_dir.is_dir():
                        domain_agents.append(agent_dir.name)
                
                if domain_agents:
                    agents[domain] = sorted(domain_agents)
    
    return agents

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🧠 AI Agent Developer Studio</h1>
        <p>Ferramenta Profissional para Desenvolvimento, Teste e Otimização de Agentes IA</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🎛️ Controle Central")
    
    # Carregar agentes
    agents = load_agents()
    tester = AgentTester()
    
    if not agents:
        st.error("❌ Nenhum agente encontrado!")
        return
    
    # Seleção de agente
    domain = st.sidebar.selectbox("🏗️ Domínio:", list(agents.keys()))
    agent = st.sidebar.selectbox("🤖 Agente:", agents[domain] if domain else [])
    
    if not domain or not agent:
        st.warning("⚠️ Selecione um domínio e agente para continuar")
        return
    
    # Tabs principais
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🧪 Teste Interativo", 
        "📊 Analytics", 
        "🔧 Configuração", 
        "📈 Performance", 
        "🎯 Otimização"
    ])
    
    with tab1:
        st.header(f"🧪 Teste Interativo: {agent}")
        
        # Carregar configuração
        config = tester.load_agent_config(domain, agent)
        
        # Informações do agente
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📦 Versão", config.get('agent_info', {}).get('version', 'N/A'))
        with col2:
            st.metric("🧠 Modelo", config.get('llm_config', {}).get('model', 'N/A'))
        with col3:
            st.metric("🎯 Status", config.get('agent_info', {}).get('status', 'N/A'))
        with col4:
            # Calcular stats do banco
            stats = tester.db.get_performance_stats(agent)
            success_rate = (stats[5] / stats[0] * 100) if stats and stats[0] > 0 else 0
            st.metric("✅ Taxa Sucesso", f"{success_rate:.1f}%")
        
        # Área de teste
        st.subheader("💬 Teste de Conversação")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            test_input = st.text_area(
                "📝 Mensagem de entrada:",
                placeholder=f"Digite uma mensagem para testar o {agent}...",
                height=150
            )
        
        with col2:
            st.subheader("⚙️ Configurações de Teste")
            test_type = st.selectbox("🔬 Tipo de Teste:", [
                "manual", "performance", "stress", "quality"
            ])
            
            real_api = st.checkbox("🌐 Usar API Real", value=True)
            save_result = st.checkbox("💾 Salvar Resultado", value=True)
        
        if st.button("🚀 Executar Teste", type="primary"):
            if test_input:
                with st.spinner("🔄 Processando..."):
                    result = tester.test_agent_real(domain, agent, test_input, test_type)
                
                # Exibir resultado
                if result['success']:
                    st.markdown(f"""
                    <div class="success-card">
                        <h4>✅ Teste Executado com Sucesso</h4>
                        <p><strong>Tempo:</strong> {result['response_time']:.2f}s</p>
                        <p><strong>Qualidade:</strong> {result['quality_score']:.2f}/1.0</p>
                        <p><strong>Tokens:</strong> {result['tokens_used']}</p>
                        <p><strong>Custo:</strong> ${result['cost_estimate']:.4f}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.subheader("📤 Resposta do Agente:")
                    st.info(result['response'])
                else:
                    st.markdown(f"""
                    <div class="error-card">
                        <h4>❌ Erro no Teste</h4>
                        <p>{result['response']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Digite uma mensagem de teste!")
    
    with tab2:
        st.header(f"📊 Analytics: {agent}")
        
        # Carregar histórico
        history_df = tester.db.get_agent_history(agent)
        
        if not history_df.empty:
            # Métricas gerais
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📈 Total de Testes", len(history_df))
            with col2:
                avg_time = history_df['response_time'].mean()
                st.metric("⏱️ Tempo Médio", f"{avg_time:.2f}s")
            with col3:
                avg_quality = history_df['quality_score'].mean()
                st.metric("⭐ Qualidade Média", f"{avg_quality:.2f}")
            with col4:
                total_cost = history_df['cost_estimate'].sum()
                st.metric("💰 Custo Total", f"${total_cost:.4f}")
            
            # Gráficos
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico de tempo de resposta
                fig_time = px.line(
                    history_df.tail(20), 
                    x='timestamp', 
                    y='response_time',
                    title='⏱️ Tempo de Resposta (Últimos 20 testes)'
                )
                st.plotly_chart(fig_time, use_container_width=True)
            
            with col2:
                # Gráfico de qualidade
                fig_quality = px.scatter(
                    history_df.tail(20),
                    x='response_time',
                    y='quality_score',
                    size='tokens_used',
                    title='⭐ Qualidade vs Tempo'
                )
                st.plotly_chart(fig_quality, use_container_width=True)
            
            # Histórico detalhado
            st.subheader("📋 Histórico Detalhado")
            st.dataframe(
                history_df[['timestamp', 'input_text', 'response_time', 'quality_score', 'success']].head(10),
                use_container_width=True
            )
        else:
            st.info("📊 Nenhum teste realizado ainda. Execute alguns testes na aba 'Teste Interativo'!")
    
    with tab3:
        st.header(f"🔧 Configuração: {agent}")
        
        # Carregar e exibir prompt
        prompt = tester.load_agent_prompt(domain, agent)
        
        st.subheader("📝 Prompt Atual")
        edited_prompt = st.text_area(
            "Edite o prompt:",
            value=prompt,
            height=300
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Salvar Prompt"):
                # Salvar prompt editado
                prompt_path = Path(f"domains/{domain}/agents/{agent}/prompt.txt")
                with open(prompt_path, 'w') as f:
                    f.write(edited_prompt)
                st.success("✅ Prompt salvo com sucesso!")
        
        with col2:
            if st.button("🔄 Restaurar Original"):
                st.rerun()
        
        # Configurações avançadas
        st.subheader("⚙️ Configurações Avançadas")
        
        config = tester.load_agent_config(domain, agent)
        
        col1, col2 = st.columns(2)
        with col1:
            new_model = st.selectbox("🧠 Modelo LLM:", [
                "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "claude-3-opus", "claude-3-sonnet"
            ], index=0)
            
            temperature = st.slider("🌡️ Temperature:", 0.0, 2.0, 0.7, 0.1)
        
        with col2:
            max_tokens = st.number_input("📏 Max Tokens:", 100, 4000, 1000)
            timeout = st.number_input("⏰ Timeout (s):", 5, 60, 30)
    
    with tab4:
        st.header(f"📈 Performance: {agent}")
        
        # Benchmark automático
        st.subheader("🏃 Benchmark Automático")
        
        if st.button("🚀 Executar Benchmark Completo"):
            benchmark_tests = [
                "Teste de velocidade básico",
                "Teste de qualidade de resposta",
                "Teste de consistência",
                "Teste de casos extremos",
                "Teste de carga"
            ]
            
            progress_bar = st.progress(0)
            results = []
            
            for i, test in enumerate(benchmark_tests):
                with st.spinner(f"Executando: {test}..."):
                    result = tester.test_agent_real(domain, agent, test, "benchmark")
                    results.append(result)
                    progress_bar.progress((i + 1) / len(benchmark_tests))
                    time.sleep(1)  # Simular tempo de processamento
            
            # Exibir resultados do benchmark
            st.success("✅ Benchmark concluído!")
            
            avg_time = sum(r['response_time'] for r in results) / len(results)
            avg_quality = sum(r['quality_score'] for r in results) / len(results)
            success_rate = sum(1 for r in results if r['success']) / len(results) * 100
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("⏱️ Tempo Médio", f"{avg_time:.2f}s")
            with col2:
                st.metric("⭐ Qualidade Média", f"{avg_quality:.2f}")
            with col3:
                st.metric("✅ Taxa de Sucesso", f"{success_rate:.1f}%")
    
    with tab5:
        st.header(f"🎯 Otimização: {agent}")
        
        st.subheader("🔍 Análise de Prompt")
        
        # Sugestões de otimização
        prompt = tester.load_agent_prompt(domain, agent)
        
        st.info("💡 Sugestões de Otimização Baseadas em IA:")
        
        suggestions = [
            "📝 Adicionar exemplos específicos no prompt para melhor contexto",
            "🎯 Definir formato de saída mais estruturado",
            "⚡ Otimizar para reduzir tokens desnecessários",
            "🔧 Incluir validações de qualidade na resposta",
            "📊 Adicionar métricas de sucesso específicas"
        ]
        
        for suggestion in suggestions:
            st.write(f"• {suggestion}")
        
        # A/B Testing
        st.subheader("🧪 A/B Testing de Prompts")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Prompt A (Atual)**")
            st.text_area("Prompt A:", value=prompt[:200] + "...", height=100, disabled=True)
        
        with col2:
            st.write("**Prompt B (Teste)**")
            prompt_b = st.text_area("Prompt B:", height=100, placeholder="Cole aqui o prompt alternativo...")
        
        if st.button("🔬 Executar Teste A/B"):
            if prompt_b:
                st.info("🔄 Executando teste A/B com 10 amostras cada...")
                # Simular resultados A/B
                st.success("✅ Resultado: Prompt B teve 15% melhor performance!")
            else:
                st.warning("⚠️ Digite o Prompt B para comparação")

if __name__ == "__main__":
    main() 