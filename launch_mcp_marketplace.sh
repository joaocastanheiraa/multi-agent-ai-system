#!/bin/bash

# 🛒 MCP MARKETPLACE - Script de Lançamento
# Configura automaticamente e inicia o marketplace de ferramentas MCP

echo "🛒 MCP MARKETPLACE - Sistema Inteligente de Ferramentas"
echo "=================================================="
echo ""

# Verificar se estamos no diretório correto
if [ ! -d "domains" ]; then
    echo "❌ Execute este script da raiz do projeto multi-agent-ai-system"
    exit 1
fi

# Função para verificar dependências
check_dependencies() {
    echo "🔍 Verificando dependências..."
    
    # Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 não encontrado"
        exit 1
    fi
    
    # Streamlit
    if ! python3 -c "import streamlit" 2>/dev/null; then
        echo "📦 Instalando streamlit..."
        pip install streamlit
    fi
    
    # Pandas
    if ! python3 -c "import pandas" 2>/dev/null; then
        echo "📦 Instalando pandas..."
        pip install pandas
    fi
    
    echo "✅ Dependências verificadas"
}

# Função para executar setup inicial
run_initial_setup() {
    echo ""
    echo "🚀 Executando setup inicial do MCP Marketplace..."
    
    # Criar diretórios necessários
    mkdir -p config examples/mcp_integration docs scripts
    
    # Executar setup automático
    if [ -f "scripts/setup_mcp_marketplace.py" ]; then
        echo "⚡ Configurando agentes automaticamente..."
        python3 scripts/setup_mcp_marketplace.py
    else
        echo "⚠️  Script de setup não encontrado, continuando..."
    fi
}

# Função para mostrar status
show_status() {
    echo ""
    echo "📊 STATUS DO SISTEMA:"
    echo "===================="
    
    # Contar agentes descobertos
    if [ -d "domains" ]; then
        agent_count=$(find domains -name "agent_manifest.json" | wc -l)
        echo "🤖 Agentes descobertos: $agent_count"
    fi
    
    # Verificar se marketplace foi configurado
    if [ -f "config/mcp_marketplace_config.json" ]; then
        echo "✅ Marketplace configurado"
    else
        echo "⚠️  Marketplace não configurado ainda"
    fi
    
    # Verificar exemplos
    if [ -d "examples/mcp_integration" ]; then
        example_count=$(ls examples/mcp_integration/*.py 2>/dev/null | wc -l)
        echo "📋 Exemplos criados: $example_count"
    fi
}

# Função para mostrar menu principal
show_menu() {
    echo ""
    echo "🎯 OPÇÕES DISPONÍVEIS:"
    echo "====================="
    echo "1. 🌐 Abrir Interface Visual (Streamlit)"
    echo "2. 🔧 Executar Setup Automático"
    echo "3. 🧠 Testar NeuroHook Ultra com MCP"
    echo "4. 📋 Ver Exemplos de Integração"
    echo "5. 📊 Mostrar Status do Sistema"
    echo "6. 🛠️ Instalar Servidores MCP"
    echo "7. 📖 Ver Documentação"
    echo "8. 🧪 Testar Imports e Dependências"
    echo "9. ❌ Sair"
    echo ""
}

# Função para abrir interface Streamlit
launch_streamlit_ui() {
    echo "🌐 Abrindo interface visual do MCP Marketplace..."
    echo "📱 Acesse: http://localhost:8501"
    echo ""
    echo "💡 Para parar, pressione Ctrl+C"
    echo ""
    
    # Verificar se arquivo existe
    if [ -f "run_mcp_ui.py" ]; then
        python3 run_mcp_ui.py
    elif [ -f "config/mcp_marketplace_ui.py" ]; then
        # Fallback para streamlit direto
        streamlit run config/mcp_marketplace_ui.py
    else
        echo "❌ Interface UI não encontrada"
        echo "💡 Execute a opção 2 primeiro para criar os arquivos"
    fi
}

# Função para testar NeuroHook
test_neurohook() {
    echo "🧠 Testando NeuroHook Ultra com MCP..."
    
    if [ -f "examples/mcp_integration/neurohook_ultra_mcp_controller.py" ]; then
        python3 examples/mcp_integration/neurohook_ultra_mcp_controller.py
    else
        echo "❌ Exemplo do NeuroHook não encontrado"
        echo "💡 Execute a opção 2 primeiro"
    fi
}

# Função para mostrar exemplos
show_examples() {
    echo "📋 EXEMPLOS DE INTEGRAÇÃO MCP:"
    echo "=============================="
    
    if [ -d "examples/mcp_integration" ]; then
        echo "📂 Localização: examples/mcp_integration/"
        echo ""
        echo "📄 Arquivos disponíveis:"
        ls -la examples/mcp_integration/*.py 2>/dev/null | while read line; do
            filename=$(echo $line | awk '{print $NF}')
            echo "  📄 $filename"
        done
        
        echo ""
        echo "🚀 Para executar um exemplo:"
        echo "cd examples/mcp_integration"
        echo "python3 <nome_do_arquivo.py>"
    else
        echo "❌ Nenhum exemplo encontrado"
        echo "💡 Execute a opção 2 primeiro"
    fi
}

# Função para instalar servidores MCP
install_mcp_servers() {
    echo "🛠️ INSTALAÇÃO DE SERVIDORES MCP:"
    echo "==============================="
    
    if [ -f "scripts/install_mcp_servers.sh" ]; then
        echo "📦 Executando script de instalação..."
        chmod +x scripts/install_mcp_servers.sh
        ./scripts/install_mcp_servers.sh
    else
        echo "❌ Script de instalação não encontrado"
        echo "💡 Execute a opção 2 primeiro para gerar o script"
    fi
}

# Função para testar imports
test_imports() {
    echo "🧪 TESTANDO IMPORTS E DEPENDÊNCIAS:"
    echo "=================================="
    
    if [ -f "test_mcp_imports.py" ]; then
        python3 test_mcp_imports.py
        
        echo ""
        echo "💡 DICAS PARA RESOLVER PROBLEMAS:"
        echo "  • AutoGen MCP: pip install -U 'autogen-ext[mcp]'"
        echo "  • AutoGen Core: pip install -U 'autogen-agentchat'"
        echo "  • Streamlit: pip install streamlit"
        echo "  • Pandas: pip install pandas"
    else
        echo "❌ Arquivo de teste não encontrado"
        echo "💡 Execute a opção 2 primeiro"
    fi
}

# Função para mostrar documentação
show_documentation() {
    echo "📖 DOCUMENTAÇÃO MCP MARKETPLACE:"
    echo "================================"
    
    echo "📚 Documentos disponíveis:"
    
    if [ -f "docs/MCP_MARKETPLACE_SETUP_REPORT.md" ]; then
        echo "  📄 docs/MCP_MARKETPLACE_SETUP_REPORT.md - Relatório de setup"
    fi
    
    echo ""
    echo "🌐 Links úteis:"
    echo "  • Documentação AutoGen MCP: https://microsoft.github.io/autogen/stable/reference/python/autogen_ext.tools.mcp.html"
    echo "  • Artigo Victor Dibia: https://newsletter.victordibia.com/p/how-to-use-mcp-anthropic-mcp-tools"
    echo "  • Repositório MCP: https://github.com/modelcontextprotocol"
    echo ""
    
    if [ -f "docs/MCP_MARKETPLACE_SETUP_REPORT.md" ]; then
        echo "📖 Quer ver o relatório de setup? (s/n)"
        read -r response
        if [[ "$response" =~ ^[Ss] ]]; then
            cat docs/MCP_MARKETPLACE_SETUP_REPORT.md
        fi
    fi
}

# Função principal
main() {
    # Verificar dependências
    check_dependencies
    
    # Mostrar status inicial
    show_status
    
    # Loop principal
    while true; do
        show_menu
        echo -n "🔢 Escolha uma opção (1-9): "
        read -r choice
        
        case $choice in
            1)
                launch_streamlit_ui
                ;;
            2)
                run_initial_setup
                ;;
            3)
                test_neurohook
                ;;
            4)
                show_examples
                ;;
            5)
                show_status
                ;;
            6)
                install_mcp_servers
                ;;
            7)
                show_documentation
                ;;
            8)
                test_imports
                ;;
            9)
                echo "👋 Até logo!"
                exit 0
                ;;
            *)
                echo "❌ Opção inválida. Tente novamente."
                ;;
        esac
        
        echo ""
        echo "⏸️  Pressione Enter para continuar..."
        read -r
    done
}

# Verificar se script está sendo executado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi 