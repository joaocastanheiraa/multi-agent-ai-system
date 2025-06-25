#!/bin/bash

echo "🔧 Configurando LangGraph Studio - Arquivo langgraph.json"
echo "========================================================="

# Backup do arquivo existente se houver
if [ -f "langgraph.json" ]; then
    echo "📋 Fazendo backup do langgraph.json existente..."
    cp langgraph.json langgraph.json.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ Backup criado: langgraph.json.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Criar o arquivo langgraph.json com configuração padrão
echo "📝 Criando arquivo langgraph.json com todos os grafos..."

cat > langgraph.json << 'EOF'
{
  "dependencies": [
    "./requirements.txt"
  ],
  "environment": ".env",
  "graphs": {
    "api_unify_master": "./langgraph_controllers/APIUnifyMaster_controller.py:APIUnifyMaster_graph",
    "conversion_catalyst": "./langgraph_controllers/conversion_catalyst_controller.py:conversion_catalyst_graph",
    "retention_architect": "./langgraph_controllers/retention_architect_controller.py:retention_architect_graph",
    "paradigm_architect": "./langgraph_controllers/paradigm_architect_controller.py:paradigm_architect_graph",
    "neurohook_ultra": "./langgraph_controllers/neurohook_ultra_controller.py:neurohook_ultra_graph",
    "pain_detector": "./langgraph_controllers/pain_detector_controller.py:pain_detector_graph",
    "metaphor_architect": "./langgraph_controllers/metaphor_architect_controller.py:metaphor_architect_graph",
    "analytics_gpt": "./langgraph_controllers/ANALYTICSGPT | Super Track_controller.py:ANALYTICSGPT_Super_Track_graph",
    "doc_rag_optimizer": "./langgraph_controllers/DocRAGOptimizer_controller.py:DocRAGOptimizer_graph",
    "hotmart_api_master": "./langgraph_controllers/HotmartAPIMaster_controller.py:HotmartAPIMaster_graph",
    "kiwify_api_master": "./langgraph_controllers/KiwifyAPIMaster_controller.py:KiwifyAPIMaster_graph",
    "perfectpay_api_master": "./langgraph_controllers/PerfectpayAPIMaster_controller.py:PerfectpayAPIMaster_graph",
    "payt_api_master": "./langgraph_controllers/PaytAPIMaster_controller.py:PaytAPIMaster_graph",
    "apis_input_output_mapper": "./langgraph_controllers/APIsImputOutputMapper_controller.py:APIsImputOutputMapper_graph"
  }
}
EOF

echo "✅ Arquivo langgraph.json criado com sucesso!"

# Verificar se os controladores existem
echo ""
echo "🔍 Verificando controladores disponíveis..."
echo "==========================================="

missing_controllers=0
total_controllers=0

for controller_path in $(grep -o '"./langgraph_controllers/[^"]*"' langgraph.json | tr -d '"'); do
    total_controllers=$((total_controllers + 1))
    if [ -f "$controller_path" ]; then
        echo "✅ $(basename "$controller_path")"
    else
        echo "❌ $(basename "$controller_path") - ARQUIVO NÃO ENCONTRADO"
        missing_controllers=$((missing_controllers + 1))
    fi
done

echo ""
echo "📊 RESUMO DA CONFIGURAÇÃO"
echo "========================"
echo "Total de grafos configurados: $total_controllers"
echo "Controladores encontrados: $((total_controllers - missing_controllers))"
echo "Controladores ausentes: $missing_controllers"

if [ $missing_controllers -eq 0 ]; then
    echo ""
    echo "🎉 CONFIGURAÇÃO PERFEITA!"
    echo "========================"
    echo "Todos os controladores foram encontrados."
    echo "O LangGraph Studio está pronto para uso."
    echo ""
    echo "🚀 Para testar, execute:"
    echo "   ./validate_system_setup.sh"
    echo "   ./start_all_interfaces.sh"
    echo ""
    echo "🌐 URL do LangGraph Studio:"
    echo "   https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8082"
else
    echo ""
    echo "⚠️  ATENÇÃO: Alguns controladores não foram encontrados."
    echo "O LangGraph Studio ainda funcionará, mas alguns grafos podem não estar disponíveis."
    echo ""
    echo "💡 Para gerar controladores ausentes, execute:"
    echo "   python scripts/transform_to_langgraph_clean.py"
fi 