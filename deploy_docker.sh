#!/bin/bash
echo "🐳 Deploy Docker Multi-Agent AI System v3.0"
echo "============================================"

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose não encontrado"
    exit 1
fi

# Build e start
echo "🔨 Building containers..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Verificar status
echo "📊 Verificando status..."
docker-compose ps

echo "✅ Deploy concluído!"
echo "🌐 Acesse: http://localhost:8001"
echo "📊 Logs: docker-compose logs -f"
echo "🛑 Para parar: docker-compose down"
