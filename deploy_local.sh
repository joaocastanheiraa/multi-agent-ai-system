#!/bin/bash
echo "🚀 Deploy Local Multi-Agent AI System v3.0"
echo "============================================"

# Verificar dependências
echo "📦 Verificando dependências..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado"
    exit 1
fi

if ! command -v pip &> /dev/null; then
    echo "❌ pip não encontrado"
    exit 1
fi

# Instalar dependências MCP
echo "📦 Instalando dependências MCP..."
pip install -r mcp_integration/requirements_mcp.txt

# Iniciar servidor MCP
echo "🚀 Iniciando servidor MCP..."
cd mcp_integration
python mcp_server.py &
MCP_PID=$!

echo "✅ Servidor MCP iniciado (PID: $MCP_PID)"
echo "🌐 Acesse: http://localhost:8001"
echo "📊 Agents: http://localhost:8001/agents"
echo "🔧 Tools: http://localhost:8001/tools"

# Salvar PID
echo $MCP_PID > mcp_server.pid

echo "🎉 Deploy concluído! Use 'kill $(cat mcp_server.pid)' para parar"
