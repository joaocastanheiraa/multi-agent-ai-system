#!/usr/bin/env python3
"""
🎨 MCP MARKETPLACE UI - Interface Visual para Gestão de Ferramentas
Interface web interativa para descobrir, configurar e gerenciar ferramentas MCP
"""

import asyncio
import streamlit as st
import pandas as pd
from typing import Dict, List
import json
from pathlib import Path

# Import do nosso marketplace
try:
    from .mcp_marketplace import MCPMarketplace, MCPServer, AgentToolConfig
except ImportError:
    # Fallback para import absoluto quando executado diretamente
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from mcp_marketplace import MCPMarketplace, MCPServer, AgentToolConfig

class MCPMarketplaceUI:
    """Interface visual para o MCP Marketplace"""
    
    def __init__(self):
        self.marketplace = MCPMarketplace()
        self.setup_page_config()
    
    def setup_page_config(self):
        """Configuração da página Streamlit"""
        st.set_page_config(
            page_title="🛒 MCP Marketplace",
            page_icon="🛒",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def render_header(self):
        """Renderiza o cabeçalho da aplicação"""
        st.title("🛒 MCP Marketplace")
        st.markdown("""
        **Sistema Inteligente de Ferramentas para Agentes AutoGen**
        
        Descubra, configure e gerencie ferramentas MCP (Model Context Protocol) 
        para todos os seus agentes de forma visual e intuitiva.
        """)
        
        # Métricas rápidas
        col1, col2, col3, col4 = st.columns(4)
        
        total_servers = len(self.marketplace.official_servers)
        configured_agents = len(self.marketplace.agent_configs)
        categories = len(set(s.category for s in self.marketplace.official_servers))
        
        with col1:
            st.metric("🛠️ Servidores Disponíveis", total_servers)
        with col2:
            st.metric("🤖 Agentes Configurados", configured_agents)
        with col3:
            st.metric("📂 Categorias", categories)
        with col4:
            # Contar ferramentas total estimada
            total_tools = sum(len(s.tools_preview) for s in self.marketplace.official_servers)
            st.metric("⚡ Ferramentas Totais", f"~{total_tools}")
    
    def render_sidebar(self):
        """Renderiza sidebar com navegação"""
        st.sidebar.title("📋 Navegação")
        
        # Modo de visualização
        view_mode = st.sidebar.selectbox(
            "🔍 Modo de Visualização",
            ["🛒 Catálogo de Ferramentas", "🤖 Configurar Agentes", "📊 Status dos Agentes", "⚙️ Configurações Avançadas"]
        )
        
        # Filtros
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🔽 Filtros")
        
        # Filtro por domínio
        domains = ["Todos"] + list(set(
            domain for server in self.marketplace.official_servers 
            for domain in server.supported_domains
        ))
        selected_domain = st.sidebar.selectbox("🎯 Domínio", domains)
        
        # Filtro por categoria
        categories = ["Todas"] + list(set(s.category for s in self.marketplace.official_servers))
        selected_category = st.sidebar.selectbox("📂 Categoria", categories)
        
        # Filtro por rating
        min_rating = st.sidebar.slider("⭐ Rating Mínimo", 1, 5, 3)
        
        return view_mode, selected_domain, selected_category, min_rating
    
    def render_catalog_view(self, domain_filter: str, category_filter: str, min_rating: int):
        """Renderiza o catálogo de ferramentas MCP"""
        st.markdown("## 🛒 Catálogo de Ferramentas MCP")
        
        # Aplicar filtros
        filtered_servers = self.marketplace.official_servers
        
        if domain_filter != "Todos":
            filtered_servers = [
                s for s in filtered_servers 
                if domain_filter in s.supported_domains
            ]
        
        if category_filter != "Todas":
            filtered_servers = [
                s for s in filtered_servers 
                if s.category == category_filter
            ]
        
        filtered_servers = [
            s for s in filtered_servers 
            if s.performance_rating >= min_rating
        ]
        
        # Organizar por categoria
        catalog = {}
        for server in filtered_servers:
            if server.category not in catalog:
                catalog[server.category] = []
            catalog[server.category].append(server)
        
        # Renderizar cada categoria
        for category, servers in catalog.items():
            st.markdown(f"### 📂 {category}")
            
            for server in servers:
                self._render_server_card(server)
    
    def _render_server_card(self, server: MCPServer):
        """Renderiza um card de servidor MCP"""
        with st.expander(f"⚡ {server.name} {'⭐' * server.performance_rating}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**{server.description}**")
                st.markdown(f"🏷️ **Categoria:** {server.category}")
                st.markdown(f"🔒 **Segurança:** {server.security_level.title()}")
                
                # Domínios suportados
                domains_badges = " ".join([f"`{d}`" for d in server.supported_domains])
                st.markdown(f"🎯 **Domínios:** {domains_badges}")
                
                # Ferramentas preview
                tools_preview = ", ".join(server.tools_preview[:5])
                if len(server.tools_preview) > 5:
                    tools_preview += f" (+{len(server.tools_preview) - 5} mais)"
                st.markdown(f"🛠️ **Ferramentas:** {tools_preview}")
                
                # Requisitos
                if server.requirements:
                    req_text = ", ".join(server.requirements)
                    st.markdown(f"📋 **Requisitos:** {req_text}")
            
            with col2:
                # Status do servidor
                if server.id in [config.enabled_servers for config in self.marketplace.agent_configs.values()]:
                    st.success("✅ Ativo em alguns agentes")
                else:
                    st.info("💤 Não configurado")
                
                # Botões de ação
                if st.button(f"📖 Documentação", key=f"doc_{server.id}"):
                    st.markdown(f"[📖 Abrir documentação]({server.documentation_url})")
                
                if st.button(f"💾 Comandos de Instalação", key=f"install_{server.id}"):
                    st.code(server.install_command)
                
                # Configuração rápida
                st.markdown("**⚡ Configuração Rápida:**")
                agents_list = list(self.marketplace.agent_configs.keys()) + ["Novo agente..."]
                selected_agent = st.selectbox(
                    "Agente", 
                    agents_list, 
                    key=f"agent_{server.id}"
                )
                
                if st.button(f"🔧 Ativar para {selected_agent}", key=f"activate_{server.id}"):
                    if selected_agent != "Novo agente...":
                        # Lógica para ativar servidor para o agente
                        self._activate_server_for_agent(server.id, selected_agent)
    
    def render_agent_config_view(self):
        """Renderiza a view de configuração de agentes"""
        st.markdown("## 🤖 Configurar Agentes")
        
        # Descobrir agentes existentes do sistema
        agents_data = self._discover_existing_agents()
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### 📋 Agentes Descobertos")
            
            selected_agent = None
            for domain, agents in agents_data.items():
                st.markdown(f"**🎯 {domain.title()}**")
                for agent in agents:
                    is_configured = agent in self.marketplace.agent_configs
                    status_icon = "✅" if is_configured else "⚪"
                    
                    if st.button(f"{status_icon} {agent}", key=f"select_{agent}"):
                        selected_agent = agent
                        st.session_state.selected_agent = agent
        
        with col2:
            if 'selected_agent' in st.session_state:
                self._render_agent_configuration_panel(st.session_state.selected_agent, agents_data)
    
    def _render_agent_configuration_panel(self, agent_name: str, agents_data: Dict[str, List[str]]):
        """Renderiza painel de configuração para um agente específico"""
        st.markdown(f"### ⚙️ Configurar {agent_name}")
        
        # Descobrir domínio do agente
        agent_domain = None
        for domain, agents in agents_data.items():
            if agent_name in agents:
                agent_domain = domain
                break
        
        if not agent_domain:
            st.error("❌ Não foi possível determinar o domínio do agente")
            return
        
        # Carregar configuração existente
        current_config = self.marketplace.agent_configs.get(agent_name)
        
        st.markdown(f"🎯 **Domínio:** {agent_domain}")
        
        # Servidores recomendados para o domínio
        recommended_servers = self.marketplace.get_recommended_tools_for_domain(agent_domain)
        
        st.markdown("### 🎯 Servidores Recomendados para este Domínio")
        
        selected_servers = []
        
        for server in recommended_servers:
            is_enabled = current_config and server.id in current_config.enabled_servers
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"⚡ **{server.name}**")
                st.markdown(f"🔹 {server.description}")
            
            with col2:
                rating_stars = "⭐" * server.performance_rating
                st.markdown(f"{rating_stars}")
            
            with col3:
                enabled = st.checkbox(
                    "Ativar", 
                    value=is_enabled,
                    key=f"{agent_name}_{server.id}"
                )
                if enabled:
                    selected_servers.append(server.id)
        
        # Configurações customizadas
        st.markdown("### ⚙️ Configurações Avançadas")
        
        custom_config = {}
        if current_config and current_config.custom_config:
            custom_config = current_config.custom_config
        
        # Editor JSON para configurações
        config_json = st.text_area(
            "📝 Configurações Personalizadas (JSON)",
            value=json.dumps(custom_config, indent=2),
            height=150
        )
        
        # Botão salvar
        if st.button(f"💾 Salvar Configuração para {agent_name}"):
            try:
                parsed_config = json.loads(config_json) if config_json.strip() else {}
                
                self.marketplace.configure_agent_tools(
                    agent_name=agent_name,
                    domain=agent_domain,
                    enabled_servers=selected_servers,
                    custom_config=parsed_config
                )
                
                st.success(f"✅ Configuração salva para {agent_name}!")
                st.experimental_rerun()
                
            except json.JSONDecodeError:
                st.error("❌ Erro no JSON das configurações personalizadas")
            except Exception as e:
                st.error(f"❌ Erro ao salvar: {e}")
        
        # Prévia do código de integração
        if selected_servers:
            st.markdown("### 📋 Código de Integração")
            integration_code = self.marketplace.generate_agent_integration_code(agent_name)
            st.code(integration_code, language="python")
    
    def render_status_view(self):
        """Renderiza view de status dos agentes"""
        st.markdown("## 📊 Status dos Agentes")
        
        if not self.marketplace.agent_configs:
            st.info("🔍 Nenhum agente configurado ainda. Use a aba 'Configurar Agentes' para começar.")
            return
        
        # Tabela de status
        status_data = []
        for agent_name, config in self.marketplace.agent_configs.items():
            status_data.append({
                "🤖 Agente": agent_name,
                "🎯 Domínio": config.domain,
                "⚡ Servidores Ativos": len(config.enabled_servers),
                "🛠️ Ferramentas Desabilitadas": len(config.disabled_tools),
                "📅 Última Atualização": config.last_updated[:10] if config.last_updated else "N/A"
            })
        
        df = pd.DataFrame(status_data)
        st.dataframe(df, use_container_width=True)
        
        # Gráficos de status
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Servidores por Domínio")
            domain_counts = {}
            for config in self.marketplace.agent_configs.values():
                domain_counts[config.domain] = domain_counts.get(config.domain, 0) + len(config.enabled_servers)
            
            if domain_counts:
                st.bar_chart(domain_counts)
        
        with col2:
            st.markdown("### 📈 Popularidade dos Servidores")
            server_counts = {}
            for config in self.marketplace.agent_configs.values():
                for server_id in config.enabled_servers:
                    server_counts[server_id] = server_counts.get(server_id, 0) + 1
            
            if server_counts:
                st.bar_chart(server_counts)
    
    def render_advanced_config_view(self):
        """Renderiza configurações avançadas"""
        st.markdown("## ⚙️ Configurações Avançadas")
        
        # Exportar/Importar configurações
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📤 Exportar Configurações")
            
            domain_to_export = st.selectbox(
                "Selecionar Domínio",
                ["Todos"] + list(set(config.domain for config in self.marketplace.agent_configs.values()))
            )
            
            if st.button("📤 Exportar"):
                if domain_to_export == "Todos":
                    export_data = {
                        "all_domains": True,
                        "agent_configs": self.marketplace.agent_configs,
                        "export_date": pd.Timestamp.now().isoformat()
                    }
                else:
                    export_data = self.marketplace.export_domain_configuration(domain_to_export)
                
                st.download_button(
                    label="💾 Download Configurações",
                    data=json.dumps(export_data, indent=2, default=str),
                    file_name=f"mcp_config_{domain_to_export.lower()}.json",
                    mime="application/json"
                )
        
        with col2:
            st.markdown("### 📥 Comandos de Instalação")
            
            all_enabled_servers = set()
            for config in self.marketplace.agent_configs.values():
                all_enabled_servers.update(config.enabled_servers)
            
            if all_enabled_servers:
                install_commands = self.marketplace.get_installation_commands(list(all_enabled_servers))
                
                st.markdown("**📋 Comandos para instalar todos os servidores ativos:**")
                st.code("\n".join(install_commands), language="bash")
            else:
                st.info("ℹ️ Nenhum servidor ativo para gerar comandos de instalação")
        
        # Reset e limpeza
        st.markdown("---")
        st.markdown("### 🧹 Manutenção")
        
        col3, col4 = st.columns(2)
        
        with col3:
            if st.button("🗑️ Limpar Cache", help="Remove cache de sessões MCP"):
                self.marketplace.server_cache.clear()
                st.success("✅ Cache limpo!")
        
        with col4:
            if st.button("⚠️ Reset Configurações", help="Remove todas as configurações de agentes"):
                if st.checkbox("✅ Confirmo que quero resetar tudo"):
                    self.marketplace.agent_configs.clear()
                    self.marketplace._save_configs()
                    st.success("🔄 Configurações resetadas!")
                    st.experimental_rerun()
    
    def _discover_existing_agents(self) -> Dict[str, List[str]]:
        """Descobre agentes existentes no sistema"""
        agents_data = {}
        
        # Ler dos domains
        domains_path = Path("domains")
        if domains_path.exists():
            for domain_path in domains_path.iterdir():
                if domain_path.is_dir() and domain_path.name != "__pycache__":
                    domain_name = domain_path.name
                    agents_path = domain_path / "agents"
                    
                    if agents_path.exists():
                        agents_data[domain_name] = []
                        for agent_path in agents_path.iterdir():
                            if agent_path.is_dir():
                                # Verificar se tem manifest
                                manifest_path = agent_path / "agent_manifest.json"
                                if manifest_path.exists():
                                    try:
                                        with open(manifest_path, 'r', encoding='utf-8') as f:
                                            manifest = json.load(f)
                                        agents_data[domain_name].append(manifest.get("agent_name", agent_path.name))
                                    except:
                                        agents_data[domain_name].append(agent_path.name)
        
        return agents_data
    
    def _activate_server_for_agent(self, server_id: str, agent_name: str):
        """Ativa um servidor MCP para um agente específico"""
        try:
            current_config = self.marketplace.agent_configs.get(agent_name)
            
            if current_config:
                if server_id not in current_config.enabled_servers:
                    current_config.enabled_servers.append(server_id)
                    self.marketplace._save_configs()
                    st.success(f"✅ {server_id} ativado para {agent_name}!")
                else:
                    st.info(f"ℹ️ {server_id} já está ativo para {agent_name}")
            else:
                # Descobrir domínio do agente
                agents_data = self._discover_existing_agents()
                agent_domain = None
                for domain, agents in agents_data.items():
                    if agent_name in agents:
                        agent_domain = domain
                        break
                
                if agent_domain:
                    self.marketplace.configure_agent_tools(
                        agent_name=agent_name,
                        domain=agent_domain,
                        enabled_servers=[server_id]
                    )
                    st.success(f"✅ {agent_name} configurado com {server_id}!")
                else:
                    st.error(f"❌ Não foi possível determinar o domínio para {agent_name}")
        
        except Exception as e:
            st.error(f"❌ Erro ao ativar servidor: {e}")
    
    def run(self):
        """Executa a interface do marketplace"""
        self.render_header()
        
        # Sidebar
        view_mode, domain_filter, category_filter, min_rating = self.render_sidebar()
        
        # Conteúdo principal baseado no modo
        if view_mode == "🛒 Catálogo de Ferramentas":
            self.render_catalog_view(domain_filter, category_filter, min_rating)
        elif view_mode == "🤖 Configurar Agentes":
            self.render_agent_config_view()
        elif view_mode == "📊 Status dos Agentes":
            self.render_status_view()
        elif view_mode == "⚙️ Configurações Avançadas":
            self.render_advanced_config_view()

def main():
    """Função principal para executar a UI"""
    app = MCPMarketplaceUI()
    app.run()

if __name__ == "__main__":
    main() 