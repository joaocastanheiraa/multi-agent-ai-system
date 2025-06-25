#!/bin/bash

echo "🔥 GERENCIADOR DE INTEGRAÇÃO MCP-LANGCHAIN"
echo "=========================================="
echo ""

# Definir caminhos
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/venv"
MCP_INTEGRATION_DIR="$SCRIPT_DIR/mcp_integration"

# Função para ativar ambiente virtual
activate_venv() {
    if [ -f "$VENV_PATH/bin/activate" ]; then
        source "$VENV_PATH/bin/activate"
        echo "✅ Ambiente virtual ativado"
    else
        echo "❌ Ambiente virtual não encontrado em: $VENV_PATH"
        exit 1
    fi
}

# Função para verificar dependências
check_dependencies() {
    echo "🔍 Verificando dependências..."
    
    # Verificar Python
    if ! command -v python &> /dev/null; then
        echo "❌ Python não encontrado"
        exit 1
    fi
    
    # Verificar Node.js
    if ! command -v node &> /dev/null; then
        echo "⚠️  Node.js não encontrado - alguns servidores MCP podem não funcionar"
        echo "   Instale Node.js: https://nodejs.org/"
    else
        echo "✅ Node.js encontrado: $(node --version)"
    fi
    
    # Verificar pacotes Python
    activate_venv
    
    required_packages=("langchain-mcp-adapters" "langchain-mcp-tools" "langgraph" "langchain-openai")
    for package in "${required_packages[@]}"; do
        if pip show "$package" &> /dev/null; then
            echo "✅ $package instalado"
        else
            echo "❌ $package não encontrado"
            echo "   Instale com: pip install $package"
        fi
    done
}

# Função para instalar servidores MCP oficiais
install_mcp_servers() {
    echo "📦 Instalando servidores MCP oficiais..."
    
    # Servidores Node.js
    echo "   Instalando servidor filesystem..."
    npx -y @modelcontextprotocol/server-filesystem --version || echo "   ⚠️  Erro ao instalar servidor filesystem"
    
    echo "   Instalando servidor brave-search..."
    npx -y @modelcontextprotocol/server-brave-search --version || echo "   ⚠️  Erro ao instalar servidor brave-search"
    
    echo "✅ Servidores MCP instalados"
}

# Função para testar integração
test_integration() {
    echo "🧪 Testando integração MCP-LangChain..."
    
    activate_venv
    
    # Verificar variáveis de ambiente
    if [ -z "$OPENAI_API_KEY" ]; then
        echo "⚠️  OPENAI_API_KEY não configurada"
        echo "   Configure no arquivo .env ou como variável de ambiente"
        echo "   export OPENAI_API_KEY='sua-chave-aqui'"
        return 1
    fi
    
    # Executar teste
    cd "$SCRIPT_DIR"
    python "$MCP_INTEGRATION_DIR/official_mcp_langgraph_integration.py"
}

# Função para iniciar servidor MCP customizado
start_custom_server() {
    echo "🚀 Iniciando servidor MCP customizado..."
    
    activate_venv
    cd "$MCP_INTEGRATION_DIR"
    
    if [ -f "custom_mcp_server.py" ]; then
        echo "   Servidor rodando em modo stdio..."
        echo "   Para conectar, use: python custom_mcp_server.py"
        python custom_mcp_server.py
    else
        echo "❌ Servidor customizado não encontrado"
        echo "   Execute primeiro: $0 test"
    fi
}

# Função para mostrar exemplos de uso
show_examples() {
    echo "📚 EXEMPLOS DE USO DA INTEGRAÇÃO MCP"
    echo "=================================="
    echo ""
    echo "1. 🗂️  SERVIDOR FILESYSTEM (manipulação de arquivos):"
    echo "   - Liste arquivos no diretório"
    echo "   - Leia conteúdo de arquivos"
    echo "   - Crie e edite arquivos"
    echo ""
    echo "2. 🧮 SERVIDOR MATH (operações matemáticas):"
    echo "   - Calcule expressões complexas"
    echo "   - Resolva equações"
    echo "   - Operações estatísticas"
    echo ""
    echo "3. 🌤️  SERVIDOR WEATHER (clima simulado):"
    echo "   - Consulte clima de cidades"
    echo "   - Informações meteorológicas"
    echo ""
    echo "4. 🛠️  SERVIDOR CUSTOMIZADO:"
    echo "   - Informações do sistema"
    echo "   - Cálculos de Fibonacci"
    echo "   - Funcionalidades personalizadas"
    echo ""
    echo "💡 COMO USAR:"
    echo "   1. Configure OPENAI_API_KEY"
    echo "   2. Execute: $0 test"
    echo "   3. Integre aos seus agentes existentes"
}

# Função para atualizar configuração
update_config() {
    echo "⚙️  Atualizando configuração MCP..."
    
    # Criar arquivo de configuração MCP
    cat > "$SCRIPT_DIR/mcp_config.json" << EOF
{
    "servers": {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
            "transport": "stdio"
        },
        "brave-search": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-brave-search"],
            "transport": "stdio",
            "env": {
                "BRAVE_API_KEY": "sua-chave-brave-aqui"
            }
        },
        "custom": {
            "command": "python",
            "args": ["mcp_integration/custom_mcp_server.py"],
            "transport": "stdio"
        }
    }
}
EOF
    
    echo "✅ Configuração MCP atualizada em: mcp_config.json"
}

# Função para mostrar status
show_status() {
    echo "📊 STATUS DA INTEGRAÇÃO MCP"
    echo "=========================="
    echo ""
    
    # Status do ambiente
    if [ -f "$VENV_PATH/bin/activate" ]; then
        echo "✅ Ambiente virtual: OK"
    else
        echo "❌ Ambiente virtual: NÃO ENCONTRADO"
    fi
    
    # Status das dependências
    activate_venv &> /dev/null
    if pip show langchain-mcp-adapters &> /dev/null; then
        echo "✅ Adaptadores MCP: OK"
    else
        echo "❌ Adaptadores MCP: NÃO INSTALADOS"
    fi
    
    # Status do Node.js
    if command -v node &> /dev/null; then
        echo "✅ Node.js: $(node --version)"
    else
        echo "❌ Node.js: NÃO ENCONTRADO"
    fi
    
    # Status das variáveis de ambiente
    if [ -n "$OPENAI_API_KEY" ]; then
        echo "✅ OPENAI_API_KEY: CONFIGURADA"
    else
        echo "⚠️  OPENAI_API_KEY: NÃO CONFIGURADA"
    fi
    
    echo ""
    echo "📁 Arquivos de integração:"
    if [ -f "$MCP_INTEGRATION_DIR/official_mcp_langgraph_integration.py" ]; then
        echo "✅ Script principal: OK"
    else
        echo "❌ Script principal: NÃO ENCONTRADO"
    fi
    
    if [ -f "$SCRIPT_DIR/mcp_config.json" ]; then
        echo "✅ Configuração MCP: OK"
    else
        echo "⚠️  Configuração MCP: NÃO ENCONTRADA"
    fi
}

# Menu principal
case "$1" in
    "check")
        check_dependencies
        ;;
    "install")
        install_mcp_servers
        ;;
    "test")
        test_integration
        ;;
    "server")
        start_custom_server
        ;;
    "examples")
        show_examples
        ;;
    "config")
        update_config
        ;;
    "status")
        show_status
        ;;
    *)
        echo "🔥 GERENCIADOR DE INTEGRAÇÃO MCP-LANGCHAIN"
        echo "=========================================="
        echo ""
        echo "Comandos disponíveis:"
        echo "  check     - Verificar dependências"
        echo "  install   - Instalar servidores MCP oficiais"
        echo "  test      - Testar integração completa"
        echo "  server    - Iniciar servidor MCP customizado"
        echo "  examples  - Mostrar exemplos de uso"
        echo "  config    - Atualizar configuração MCP"
        echo "  status    - Mostrar status da integração"
        echo ""
        echo "Uso: $0 <comando>"
        echo ""
        echo "Exemplos:"
        echo "  $0 check    # Verificar se tudo está configurado"
        echo "  $0 test     # Executar teste completo"
        echo "  $0 examples # Ver exemplos de uso"
        ;;
esac 