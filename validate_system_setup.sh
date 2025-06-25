#!/bin/bash

echo "🔍 VALIDAÇÃO DO SISTEMA MULTI-AGENT AI"
echo "======================================"
echo ""

VALIDATION_PASSED=true

# Função para marcar falha
mark_failure() {
    VALIDATION_PASSED=false
    echo "❌ $1"
}

# Função para marcar sucesso
mark_success() {
    echo "✅ $1"
}

echo "📂 Verificando estrutura de diretórios..."
echo "========================================="

# Verificar diretórios essenciais
if [ -d "mcp_integration" ]; then
    mark_success "Diretório mcp_integration existe"
else
    mark_failure "Diretório mcp_integration não encontrado"
fi

if [ -d "langgraph_controllers" ]; then
    mark_success "Diretório langgraph_controllers existe"
else
    mark_failure "Diretório langgraph_controllers não encontrado"
fi

if [ -d "logs" ]; then
    mark_success "Diretório logs existe"
else
    echo "📝 Criando diretório logs..."
    mkdir -p logs
    mark_success "Diretório logs criado"
fi

if [ -d "venv" ]; then
    mark_success "Ambiente virtual existe"
else
    mark_failure "Ambiente virtual não encontrado - execute: python -m venv venv"
fi

echo ""
echo "📄 Verificando arquivos de configuração..."
echo "=========================================="

# Verificar arquivo langgraph.json
if [ -f "langgraph.json" ]; then
    # Contar número de grafos no arquivo
    graph_count=$(grep -c '".*":.*"./langgraph_controllers/' langgraph.json)
    if [ $graph_count -gt 0 ]; then
        mark_success "langgraph.json configurado com $graph_count grafos"
    else
        mark_failure "langgraph.json existe mas não tem grafos configurados"
    fi
else
    mark_failure "Arquivo langgraph.json não encontrado"
fi

# Verificar mcp_server.py
if [ -f "mcp_integration/mcp_server.py" ]; then
    mark_success "mcp_server.py encontrado"
else
    mark_failure "mcp_server.py não encontrado em mcp_integration/"
fi

# Verificar mcp_config.json
if [ -f "mcp_integration/mcp_config.json" ]; then
    mark_success "mcp_config.json encontrado"
else
    mark_failure "mcp_config.json não encontrado em mcp_integration/"
fi

echo ""
echo "🐍 Verificando dependências Python..."
echo "====================================="

if [ -d "venv" ]; then
    source venv/bin/activate
    
    # Verificar dependências essenciais
    if python -c "import fastapi" 2>/dev/null; then
        mark_success "FastAPI instalado"
    else
        mark_failure "FastAPI não instalado - execute: pip install fastapi"
    fi
    
    if python -c "import uvicorn" 2>/dev/null; then
        mark_success "Uvicorn instalado"
    else
        mark_failure "Uvicorn não instalado - execute: pip install uvicorn"
    fi
    
    if command -v langgraph >/dev/null 2>&1; then
        mark_success "LangGraph CLI instalado"
    else
        mark_failure "LangGraph CLI não instalado - execute: pip install langgraph-cli"
    fi
    
    if command -v autogenstudio >/dev/null 2>&1; then
        mark_success "AutoGen Studio instalado"
    else
        mark_failure "AutoGen Studio não instalado - execute: pip install autogenstudio"
    fi
else
    mark_failure "Ambiente virtual não encontrado - não é possível verificar dependências"
fi

echo ""
echo "🔧 Verificando controladores LangGraph..."
echo "========================================"

controller_count=0
if [ -d "langgraph_controllers" ]; then
    for controller in langgraph_controllers/*_controller.py; do
        if [ -f "$controller" ]; then
            controller_count=$((controller_count + 1))
        fi
    done
    
    if [ $controller_count -gt 0 ]; then
        mark_success "$controller_count controladores LangGraph encontrados"
    else
        mark_failure "Nenhum controlador LangGraph encontrado"
    fi
else
    mark_failure "Diretório langgraph_controllers não existe"
fi

echo ""
echo "🌐 Verificando portas disponíveis..."
echo "===================================="

# Verificar se as portas estão livres
check_port() {
    if lsof -i :$1 > /dev/null 2>&1; then
        echo "⚠️  Porta $1 está em uso (será necessário parar o processo)"
        return 1
    else
        mark_success "Porta $1 está disponível"
        return 0
    fi
}

check_port 8000  # MCP Server
check_port 8081  # AutoGen Studio  
check_port 8082  # LangGraph Studio

echo ""
echo "📋 RESULTADO DA VALIDAÇÃO"
echo "========================"

if [ "$VALIDATION_PASSED" = true ]; then
    echo "🎉 VALIDAÇÃO PASSOU! Sistema está pronto para uso."
    echo ""
    echo "🚀 Para iniciar o sistema, execute:"
    echo "   ./start_all_interfaces.sh"
    echo ""
    echo "🌐 URLs que estarão disponíveis:"
    echo "   AutoGen Studio:    http://localhost:8081"
    echo "   LangGraph Studio:  https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8082"
    echo "   MCP Server API:    http://localhost:8000"
    exit 0
else
    echo "❌ VALIDAÇÃO FALHOU! Corrija os problemas acima antes de continuar."
    echo ""
    echo "🔧 Comandos de correção comuns:"
    echo "   Criar ambiente virtual:     python -m venv venv"
    echo "   Ativar ambiente virtual:    source venv/bin/activate"
    echo "   Instalar dependências:      pip install -r requirements.txt"
    echo "   Instalar LangGraph CLI:     pip install langgraph-cli"
    echo "   Instalar AutoGen Studio:    pip install autogenstudio"
    exit 1
fi 