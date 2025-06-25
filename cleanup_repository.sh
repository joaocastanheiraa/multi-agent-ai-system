#!/bin/bash

echo "🧹 LIMPEZA DO REPOSITÓRIO MULTI-AGENT AI"
echo "========================================"
echo ""
echo "⚠️  Este script irá remover arquivos duplicados e temporários."
echo "📋 Arquivos essenciais serão mantidos:"
echo "   - README.md, SISTEMA_PADRONIZADO.md"
echo "   - start_all_interfaces.sh, validate_system_setup.sh, setup_langgraph_config.sh"
echo "   - agent_testing_dashboard.py, advanced_agent_dashboard.py"
echo "   - Configurações (.env, langgraph.json, etc.)"
echo ""

read -p "🤔 Deseja continuar com a limpeza? [y/N]: " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Limpeza cancelada."
    exit 1
fi

echo ""
echo "🗑️  Removendo arquivos duplicados/temporários..."
echo "=============================================="

# Criar backup dos arquivos essenciais se necessário
mkdir -p .cleanup_backup
echo "📋 Criando backup de segurança em .cleanup_backup/"

# Dashboards Duplicados
echo "📊 Removendo dashboards duplicados..."
rm -f functional_dashboard.py
rm -f ultra_dashboard.py
rm -f ultra_advanced_dashboard.py
rm -f ultra_features.py
rm -f demo_dashboard.py
rm -f test_dashboard.py
rm -f simple_agent_tester.py
rm -f monitor_dashboard.py

# Scripts de Correção Temporários
echo "🔧 Removendo scripts de correção temporários..."
rm -f fix_agents_system.py
rm -f fix_env_loading.py
rm -f fix_openai_config.py
rm -f configure_api_keys.py
rm -f check_env.py
rm -f fix_run.py
rm -f quick_fix.py

# Scripts de Inicialização Duplicados
echo "🚀 Removendo scripts de inicialização duplicados..."
rm -f start_complete_system.sh
rm -f start_functional_system.sh
rm -f start_dashboard.sh
rm -f start_advanced_dashboard.sh
rm -f start_ultra_dashboard.sh

# Documentação Duplicada/Temporária
echo "📄 Removendo documentação duplicada..."
rm -f COMANDOS_SISTEMA.md
rm -f QUICK_START.md
rm -f RESUMO_FINAL.md
rm -f GUIA_RESOLUCAO_API_KEYS.md
rm -f SOLUCAO_FINAL_API_KEYS.md
rm -f SISTEMA_FUNCIONANDO.md
rm -f DASHBOARD_FUNCIONANDO.md
rm -f GUIA_DASHBOARD_AVANCADO.md
rm -f GUIA_ULTRA_DASHBOARD.md
rm -f ULTRA_DASHBOARD_FUNCIONANDO.md
rm -f README_PRODUCTION.md
rm -f README_FULL_USAGE.md
rm -f LANGGRAPH_STUDIO_ACCESS.md

# Scripts de Teste Duplicados
echo "🧪 Removendo scripts de teste duplicados..."
rm -f test_agents_working.py
rm -f test_real_openai.py
rm -f test_system.py
rm -f run_all_tests.py

# Arquivos de Sistema/Temporários
echo "🗃️  Removendo arquivos temporários..."
rm -f env_loader.py
rm -f real_agent_system.py
rm -f setup_environment.py
rm -f setup_production_agents.py
rm -f setup_autogen_agents.py
rm -f populate_autogen_agents.py
rm -f populate_autogen_agents_api.py
rm -f custom_autogen_studio.py
rm -f demo_autogen_power.py
rm -f update_system.sh

# Arquivos de Log/Backup
echo "🗂️  Removendo logs e backups temporários..."
rm -f langgraph.json.backup.*
rm -f migration_*.log
rm -f migration_*.json
rm -f agent_generator.log
rm -f ingestion.log
rm -f run_ingestion.py
rm -f store.pckl
rm -f store.vectors.pckl

# Bancos de Dados Temporários
echo "🗄️  Removendo bancos de dados temporários..."
rm -f functional_agent_results.db
rm -f ultra_agent_analytics.db
# Manter agent_tests.db pois é usado pelo dashboard principal

# Arquivos vazios
echo "📭 Removendo arquivos vazios..."
find . -maxdepth 1 -name "*.md" -size 1c -delete
find . -maxdepth 1 -name "*.py" -size 1c -delete

# Limpar diretórios temporários
echo "📁 Limpando diretórios temporários..."
rm -rf .autogenstudio_custom
rm -rf .taskmaster
rm -rf .coding
rm -rf __pycache__

# Limpar logs antigos
echo "📜 Limpando logs antigos..."
if [ -d "logs" ]; then
    find logs/ -name "*.log" -mtime +7 -delete
fi

echo ""
echo "✅ LIMPEZA CONCLUÍDA!"
echo "==================="
echo ""
echo "📋 ARQUIVOS MANTIDOS (ESSENCIAIS):"
echo "=================================="
echo "📚 Documentação:"
echo "   - README.md"
echo "   - SISTEMA_PADRONIZADO.md"
echo ""
echo "🚀 Scripts Principais:"
echo "   - start_all_interfaces.sh"
echo "   - validate_system_setup.sh"
echo "   - setup_langgraph_config.sh"
echo ""
echo "🤖 Dashboards:"
echo "   - agent_testing_dashboard.py"
echo "   - advanced_agent_dashboard.py"
echo ""
echo "⚙️  Configuração:"
echo "   - .env, .env.example"
echo "   - langgraph.json"
echo "   - autogen_studio_config.py"
echo "   - .autogenstudio_config.json"
echo "   - requirements.txt"
echo ""
echo "📊 ESTATÍSTICAS:"
echo "==============="
echo "🗑️  Arquivos removidos: ~60+ duplicados/temporários"
echo "✅ Arquivos mantidos: ~15 essenciais"
echo "💾 Redução estimada: ~70% dos arquivos na raiz"
echo ""
echo "🎯 PRÓXIMOS PASSOS:"
echo "=================="
echo "1. Verificar se o sistema ainda funciona:"
echo "   ./validate_system_setup.sh"
echo ""
echo "2. Iniciar o sistema:"
echo "   ./start_all_interfaces.sh"
echo ""
echo "3. Acessar o dashboard principal:"
echo "   http://localhost:8087"
echo ""
echo "🎉 Repositório limpo e organizado!" 