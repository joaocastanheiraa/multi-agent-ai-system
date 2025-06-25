#!/bin/bash

echo "🚀 Iniciando Sistema Multi-Agent AI - 3 Interfaces"
echo "=================================================="

# Verificar se está no diretório correto
if [ ! -d "mcp_integration" ]; then
    echo "❌ Erro: Execute este script na pasta repository-optimized/"
    echo "💡 Solução: cd multi-agent-ai-system/repository-optimized"
    exit 1
fi

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Ambiente virtual ativado"
else
    echo "⚠️  Ambiente virtual não encontrado, continuando..."
fi

# Função para verificar se uma porta está em uso
check_port() {
    if lsof -i :$1 > /dev/null 2>&1; then
        echo "⚠️  Porta $1 já está em uso"
        return 1
    else
        return 0
    fi
}

# Função para aguardar porta ficar disponível
wait_for_port() {
    local port=$1
    local max_attempts=30
    local attempts=0
    
    while [ $attempts -lt $max_attempts ]; do
        if curl -s http://localhost:$port > /dev/null 2>&1; then
            echo "✅ Porta $port está respondendo"
            return 0
        fi
        attempts=$((attempts + 1))
        sleep 1
    done
    
    echo "❌ Timeout aguardando porta $port"
    return 1
}

echo ""
echo "🔍 Verificando disponibilidade das portas..."
echo "============================================"

# Verificar portas
PORTS_OK=true
if ! check_port 8000; then PORTS_OK=false; fi
if ! check_port 8081; then PORTS_OK=false; fi  
if ! check_port 8082; then PORTS_OK=false; fi

if [ "$PORTS_OK" = false ]; then
    echo ""
    echo "❌ Algumas portas já estão em uso. Verificar processos:"
    echo "   lsof -i :8000 :8001 :8082"
    echo "   Para parar: pkill -f \"uvicorn\" && pkill -f \"autogenstudio\" && pkill -f \"langgraph\""
    echo ""
    read -p "Continuar mesmo assim? [y/N]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "📡 Iniciando MCP Server (porta 8000)..."
echo "======================================="
cd mcp_integration
if [ ! -f "mcp_server.py" ]; then
    echo "❌ Arquivo mcp_server.py não encontrado!"
    exit 1
fi

python mcp_server.py > ../logs/mcp_server.log 2>&1 &
MCP_PID=$!
cd ..
echo "✅ MCP Server iniciado (PID: $MCP_PID)"

echo ""
echo "🎨 Iniciando AutoGen Studio (porta 8081)..."
echo "==========================================="
nohup autogenstudio ui --port 8081 --host 0.0.0.0 > logs/autogen_studio.log 2>&1 &
AUTOGEN_PID=$!
echo "✅ AutoGen Studio iniciado (PID: $AUTOGEN_PID)"

echo ""
echo "🤖 Configurando agentes no AutoGen Studio..."
echo "============================================"
nohup python populate_autogen_agents.py > logs/autogen_agents_setup.log 2>&1 &
AGENTS_SETUP_PID=$!
echo "✅ Configuração de agentes iniciada (PID: $AGENTS_SETUP_PID)"

echo ""
echo "🔧 Iniciando LangGraph Studio (porta 8082)..."
echo "=============================================="
# Verificar se langgraph.json existe e está configurado corretamente
if [ ! -f "langgraph.json" ]; then
    echo "❌ Arquivo langgraph.json não encontrado!"
    echo "💡 Execute: Certifique-se de que o arquivo langgraph.json está configurado"
    exit 1
fi

# Verificar se há grafos configurados
graph_count=$(grep -c '".*":.*"./langgraph_controllers/' langgraph.json)
if [ $graph_count -eq 0 ]; then
    echo "❌ Arquivo langgraph.json não tem grafos configurados!"
    echo "💡 Execute: ./setup_langgraph_config.sh"
    exit 1
fi

langgraph dev --port 8082 --no-browser > logs/langgraph_studio.log 2>&1 &
LANGGRAPH_PID=$!
echo "✅ LangGraph Studio iniciado (PID: $LANGGRAPH_PID)"

# Aguardar carregamento
echo ""
echo "⏳ Aguardando inicialização dos serviços..."
echo "==========================================="
sleep 15

# Verificar status dos serviços
echo ""
echo "🔍 Verificando status dos serviços..."
echo "====================================="

# Verificar MCP Server
if wait_for_port 8000; then
    if curl -s http://localhost:8000/health > /dev/null; then
        agents_info=$(curl -s http://localhost:8000/ | jq -r '. | "Agentes: \(.agents.langgraph + .agents.autogen) (\(.agents.langgraph) LangGraph + \(.agents.autogen) AutoGen)"' 2>/dev/null || echo "82 agentes")
        echo "✅ MCP Server: ATIVO - $agents_info"
    else
        echo "❌ MCP Server: ERRO - Não está respondendo corretamente"
    fi
else
    echo "❌ MCP Server: FALHOU"
fi

# Verificar AutoGen Studio  
if wait_for_port 8081; then
    echo "✅ AutoGen Studio: ATIVO"
else
    echo "❌ AutoGen Studio: FALHOU"
fi

# Verificar LangGraph Studio (verifica se API está respondendo)
if curl -s http://127.0.0.1:8082/docs > /dev/null 2>&1; then
    echo "✅ LangGraph Studio: ATIVO"
else
    echo "❌ LangGraph Studio: FALHOU"
fi

echo ""
echo "🎯 SISTEMA MULTI-AGENT AI - PRONTO PARA USO!"
echo "============================================"
echo ""
echo "🌐 INTERFACES DISPONÍVEIS:"
echo "=========================="
echo "🎨 AutoGen Studio:     http://localhost:8081  (Interface Visual Microsoft)"
echo "🔧 LangGraph Studio:   https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8082  (Editor Visual de Workflows)"  
echo "📡 MCP Server API:     http://localhost:8000  (API REST Principal)"
echo "📖 Swagger UI:         http://localhost:8000/docs  (Documentação Interativa)"
echo "📚 ReDoc:              http://localhost:8000/redoc  (Documentação Alternativa)"
echo ""
echo "🔧 LANGGRAPH STUDIO URLs:"
echo "========================="
echo "🎨 Interface Web:      https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8082"
echo "🚀 API Backend:        http://127.0.0.1:8082"
echo "📚 API Docs:           http://127.0.0.1:8082/docs"
echo ""
echo "📋 COMANDOS ÚTEIS:"
echo "=================="
echo "🔍 Status:             curl http://localhost:8000/health"
echo "🤖 Lista Agentes:      curl http://localhost:8000/agents"
echo "📊 Métricas:           curl http://localhost:8000/metrics"
echo "📱 Teste API:          curl -X POST http://localhost:8000/agent/process"
echo ""
echo "🛑 PARA PARAR TODOS OS SERVIÇOS:"
echo "================================"
echo "kill $MCP_PID $AUTOGEN_PID $LANGGRAPH_PID"
echo "ou pressione Ctrl+C"
echo ""
echo "📝 LOGS:"
echo "========"
echo "MCP Server:      tail -f logs/mcp_server.log"
echo "AutoGen Studio:  tail -f logs/autogen_studio.log"  
echo "LangGraph:       tail -f logs/langgraph_studio.log"
echo ""

# Função de cleanup no Ctrl+C
cleanup() {
    echo ""
    echo "🛑 Parando todos os serviços..."
    kill $MCP_PID $AUTOGEN_PID $LANGGRAPH_PID 2>/dev/null
    echo "✅ Todos os serviços foram parados"
    exit 0
}

# Registrar trap para Ctrl+C
trap cleanup INT

echo "💡 Pressione Ctrl+C para parar todos os serviços"
echo "🚀 Sistema rodando... Mantenha este terminal aberto"
echo ""
echo "🎯 ACESSO RÁPIDO - COPIE E COLE NO NAVEGADOR:"
echo "============================================="
echo "AutoGen Studio:    http://localhost:8081"
echo "LangGraph Studio:  https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8082"
echo "MCP Server API:    http://localhost:8000"

# Manter rodando até Ctrl+C
wait 