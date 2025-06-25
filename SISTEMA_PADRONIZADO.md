# 🎯 SISTEMA MULTI-AGENT AI - CONFIGURAÇÃO PADRONIZADA

## ✅ NUNCA MAIS TERÁ ERROS!

Este sistema foi padronizado para funcionar perfeitamente sempre. Siga os passos abaixo:

## 🚀 INICIALIZAÇÃO RÁPIDA (3 COMANDOS)

```bash
# 1. Validar sistema
./validate_system_setup.sh

# 2. Configurar LangGraph (se necessário)
./setup_langgraph_config.sh

# 3. Iniciar todas as interfaces
./start_all_interfaces.sh
```

## 🌐 URLS PADRONIZADAS (COPIE E COLE)

### ✅ URLs Que SEMPRE Funcionam:

```
🎨 AutoGen Studio:    http://localhost:8081
🔧 LangGraph Studio:  https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8082
📡 MCP Server API:    http://localhost:8000
📚 API Docs:          http://127.0.0.1:8082/docs
```

## 🔧 SCRIPTS PADRONIZADOS

### 1. `validate_system_setup.sh`
**O que faz:** Verifica se tudo está configurado corretamente
**Quando usar:** Antes de iniciar o sistema pela primeira vez ou após mudanças

```bash
./validate_system_setup.sh
```

### 2. `setup_langgraph_config.sh`  
**O que faz:** Configura automaticamente o arquivo `langgraph.json` com todos os grafos
**Quando usar:** Se o LangGraph Studio não iniciar ou se quiser reconfigurar

```bash
./setup_langgraph_config.sh
```

### 3. `start_all_interfaces.sh`
**O que faz:** Inicia todas as 3 interfaces (MCP Server + AutoGen Studio + LangGraph Studio)
**Quando usar:** Para iniciar o sistema completo

```bash
./start_all_interfaces.sh
```

## 🎯 GRAFOS CONFIGURADOS (14 GRAFOS)

O sistema está configurado com **14 grafos LangGraph**:

1. `api_unify_master` - Unificação de APIs
2. `conversion_catalyst` - Catalisador de Conversão
3. `retention_architect` - Arquiteto de Retenção  
4. `paradigm_architect` - Arquiteto de Paradigmas
5. `neurohook_ultra` - Ganchos Neurológicos
6. `pain_detector` - Detector de Dores
7. `metaphor_architect` - Arquiteto de Metáforas
8. `analytics_gpt` - Analytics GPT
9. `doc_rag_optimizer` - Otimizador de RAG
10. `hotmart_api_master` - API Master Hotmart
11. `kiwify_api_master` - API Master Kiwify
12. `perfectpay_api_master` - API Master Perfectpay
13. `payt_api_master` - API Master Payt
14. `apis_input_output_mapper` - Mapeador Input/Output APIs

## 🛡️ VALIDAÇÕES AUTOMÁTICAS

O sistema agora inclui validações automáticas que verificam:

- ✅ Estrutura de diretórios
- ✅ Arquivos de configuração
- ✅ Dependências Python
- ✅ Controladores LangGraph
- ✅ Disponibilidade de portas
- ✅ Configuração do `langgraph.json`

## 🔄 FLUXO DE TRABALHO PADRÃO

### Primeira vez:
```bash
# 1. Validar sistema
./validate_system_setup.sh

# 2. Se houver problemas, corrigir e validar novamente
# 3. Configurar LangGraph
./setup_langgraph_config.sh

# 4. Iniciar sistema
./start_all_interfaces.sh
```

### Uso diário:
```bash
# Apenas este comando:
./start_all_interfaces.sh
```

## 🚨 SOLUÇÃO DE PROBLEMAS

### Problema: "LangGraph Studio não abre"
**Solução:**
```bash
./setup_langgraph_config.sh
./start_all_interfaces.sh
```

### Problema: "Porta já está em uso"  
**Solução:**
```bash
pkill -f "uvicorn" && pkill -f "autogenstudio" && pkill -f "langgraph"
./start_all_interfaces.sh
```

### Problema: "Dependências não encontradas"
**Solução:**
```bash
source venv/bin/activate
pip install -r requirements.txt
pip install langgraph-cli autogenstudio
./validate_system_setup.sh
```

### Problema: "Arquivo langgraph.json inválido"
**Solução:**
```bash
./setup_langgraph_config.sh
```

## 📋 CHECKLIST DE FUNCIONAMENTO

Após executar `./start_all_interfaces.sh`, você deve ver:

- ✅ MCP Server: ATIVO - Agentes: 82 (14 LangGraph + 68 AutoGen)
- ✅ AutoGen Studio: ATIVO  
- ✅ LangGraph Studio: ATIVO

## 🎉 GARANTIA DE FUNCIONAMENTO

Com este sistema padronizado:

1. **✅ URLs sempre corretas** - Não há mais confusão sobre qual URL usar
2. **✅ Configuração automática** - Scripts configuram tudo automaticamente  
3. **✅ Validação prévia** - Sistema verifica tudo antes de iniciar
4. **✅ Solução de problemas** - Comandos claros para qualquer problema
5. **✅ Backup automático** - Configurações são sempre salvas

## 🚀 COMANDOS DE EMERGÊNCIA

Se algo der errado, use estes comandos na ordem:

```bash
# 1. Parar tudo
pkill -f "uvicorn" && pkill -f "autogenstudio" && pkill -f "langgraph"

# 2. Reconfigurar
./setup_langgraph_config.sh

# 3. Validar
./validate_system_setup.sh

# 4. Iniciar
./start_all_interfaces.sh
```

---

**🎯 RESULTADO:** Sistema Multi-Agent AI 100% funcional e padronizado! 