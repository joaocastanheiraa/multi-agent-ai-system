# 📜 Referência Completa de Scripts

## 1. **Scripts de Migração**

### 1.1. **`run_migration_optimized.py`**

**Descrição**: Script principal para executar migração v3.0

```bash
# Migração completa
python scripts/run_migration_optimized.py --full

# Fases específicas
python scripts/run_migration_optimized.py --phases A,B,C

# Apenas validar pré-requisitos
python scripts/run_migration_optimized.py --validate

# Com debug verbose
python scripts/run_migration_optimized.py --full --verbose
```

**Opções:**
- `--full`: Executa todas as 7 fases
- `--phases`: Executa fases específicas (A,B,C,D,E,F,G)
- `--validate`: Apenas valida pré-requisitos
- `--verbose`: Output detalhado
- `--dry-run`: Simula execução sem fazer alterações

### 1.2. **`migrate_to_optimized.py`**

**Descrição**: Migração legada para repository-optimized

```bash
# Migração básica
python scripts/migrate_to_optimized.py

# Com backup automático
python scripts/migrate_to_optimized.py --backup

# Forçar sobrescrita
python scripts/migrate_to_optimized.py --force
```

### 1.3. **`validate_migration.py`**

**Descrição**: Validação completa do sistema migrado

```bash
# Validação completa
python scripts/validate_migration.py

# Validação específica
python scripts/validate_migration.py --check agents
python scripts/validate_migration.py --check knowledge
python scripts/validate_migration.py --check structure

# Com output detalhado
python scripts/validate_migration.py --verbose
```

**Verificações:**
- Estrutura de diretórios
- Integridade de agentes
- Knowledge bases
- Configurações
- Dependencies

## 2. **Scripts de LangGraph**

### 2.1. **`transform_to_langgraph_clean.py`**

**Descrição**: Converte agentes para controllers LangGraph

```bash
# Agente específico
python scripts/transform_to_langgraph_clean.py \
  --agent-dir domains/copywriters/agents/paradigm_architect

# Domínio completo
python scripts/transform_to_langgraph_clean.py --domain copywriters

# Todos os agentes
python scripts/transform_to_langgraph_clean.py --all

# Output customizado
python scripts/transform_to_langgraph_clean.py \
  --domain apis --output-dir ./custom_controllers
```

**Funcionalidades:**
- Extrai lógica de workflow de prompt.txt
- Gera StateGraph LangGraph
- Cria schemas TypedDict
- Implementa nodes e edges
- Adiciona error handling

### 2.2. **`controller_usage_examples.py`**

**Descrição**: Exemplos de uso dos controllers gerados

```bash
# Executar exemplos
python scripts/controller_usage_examples.py

# Exemplo específico
python scripts/controller_usage_examples.py --example paradigm_architect

# Testar controller
python scripts/controller_usage_examples.py --test conversion_catalyst
```

## 3. **Scripts de Deploy**

### 3.1. **`deploy_and_test.py`**

**Descrição**: Deploy completo com testes automatizados

```bash
# Deploy local
python scripts/deploy_and_test.py --local

# Deploy Docker
python scripts/deploy_and_test.py --docker

# Deploy produção
python scripts/deploy_and_test.py --production

# Apenas testes
python scripts/deploy_and_test.py --test-only

# Com monitoramento
python scripts/deploy_and_test.py --local --monitor
```

**Opções:**
- `--local`: Deploy em ambiente local
- `--docker`: Deploy com Docker
- `--production`: Configurações de produção
- `--test-only`: Apenas executa testes
- `--monitor`: Inicia monitoramento
- `--skip-tests`: Pula testes
- `--verbose`: Output detalhado

### 3.2. **`deploy_local.sh`**

**Descrição**: Script bash para deploy local rápido

```bash
# Deploy básico
bash deploy_local.sh

# Com debug
DEBUG=true bash deploy_local.sh

# Porta customizada
PORT=8002 bash deploy_local.sh
```

### 3.3. **`deploy_docker.sh`**

**Descrição**: Script bash para deploy Docker

```bash
# Deploy básico
bash deploy_docker.sh

# Rebuild forçado
REBUILD=true bash deploy_docker.sh

# Tag customizada
TAG=v1.0.0 bash deploy_docker.sh
```

## 4. **Scripts de Setup**

### 4.1. **`setup_mcp_integration.py`**

**Descrição**: Configuração do servidor MCP

```bash
# Setup básico
python scripts/setup_mcp_integration.py

# Com configuração customizada
python scripts/setup_mcp_integration.py --port 8001

# Modo debug
python scripts/setup_mcp_integration.py --debug

# Configurar todos os agentes
python scripts/setup_mcp_integration.py --all-agents
```

### 4.2. **`setup_autogen_complete.py`**

**Descrição**: Configuração completa do AutoGen

```bash
# Setup completo
python scripts/setup_autogen_complete.py

# Domínio específico
python scripts/setup_autogen_complete.py --domain copywriters

# Com templates
python scripts/setup_autogen_complete.py --with-templates
```

### 4.3. **`setup_rag_system.py`**

**Descrição**: Configuração do sistema RAG

```bash
# Setup básico
python scripts/setup_rag_system.py

# Com embeddings
python scripts/setup_rag_system.py --generate-embeddings

# Banco específico
python scripts/setup_rag_system.py --db supabase
```

## 5. **Scripts de Migração de Domínios**

### 5.1. **`create_domain_manifests.py`**

**Descrição**: Cria manifests para domínios

```bash
# Todos os domínios
python scripts/create_domain_manifests.py

# Domínio específico
python scripts/create_domain_manifests.py --domain copywriters

# Forçar atualização
python scripts/create_domain_manifests.py --force
```

### 5.2. **`migrate_knowledge_bases.py`**

**Descrição**: Migra knowledge bases para nova estrutura

```bash
# Migração completa
python scripts/migrate_knowledge_bases.py

# Domínio específico
python scripts/migrate_knowledge_bases.py --domain copywriters

# Verificar apenas
python scripts/migrate_knowledge_bases.py --dry-run
```

### 5.3. **`migrate_copywriters_main.py`**

**Descrição**: Migração específica de copywriters

```bash
# Migração completa
python scripts/migrate_copywriters_main.py

# Com backup
python scripts/migrate_copywriters_main.py --backup

# Agente específico
python scripts/migrate_copywriters_main.py --agent paradigm_architect
```

### 5.4. **`migrate_apis_domain.py`**

**Descrição**: Migração específica de APIs

```bash
# Migração completa
python scripts/migrate_apis_domain.py

# API específica
python scripts/migrate_apis_domain.py --api hotmart_master
```

### 5.5. **`migrate_analytics_knowledge.py`**

**Descrição**: Migração de knowledge base de analytics

```bash
# Migração completa
python scripts/migrate_analytics_knowledge.py

# Verificar estrutura
python scripts/migrate_analytics_knowledge.py --validate
```

## 6. **Scripts de Teste**

### 6.1. **`test_neurohook.py`**

**Descrição**: Testes específicos do Neurohook Ultra

```bash
# Teste completo
python scripts/test_neurohook.py

# Teste específico
python scripts/test_neurohook.py --test hooks_generation

# Com output detalhado
python scripts/test_neurohook.py --verbose
```

### 6.2. **`task_4_1_demo.py`**

**Descrição**: Demo da Task 4.1

```bash
# Executar demo
python scripts/task_4_1_demo.py

# Com dados específicos
python scripts/task_4_1_demo.py --data sample_data.json
```

### 6.3. **`task_4_1_test.py`**

**Descrição**: Testes da Task 4.1

```bash
# Executar testes
python scripts/task_4_1_test.py

# Testes específicos
python scripts/task_4_1_test.py --suite basic
```

## 7. **Scripts de Otimização (Placeholders)**

### 7.1. **`transform_architecture.py`**

**Descrição**: Transformação de arquitetura (Fase B)

```bash
# Execução completa
python scripts/transform_architecture.py

# Componente específico
python scripts/transform_architecture.py --component agents
```

### 7.2. **`setup_rag_optimized.py`**

**Descrição**: Setup RAG otimizado (Fase C)

```bash
# Setup completo
python scripts/setup_rag_optimized.py

# Com configuração avançada
python scripts/setup_rag_optimized.py --advanced
```

### 7.3. **`setup_agents_optimized.py`**

**Descrição**: Setup de agentes otimizado (Fase D)

```bash
# Setup completo
python scripts/setup_agents_optimized.py

# Agentes específicos
python scripts/setup_agents_optimized.py --agents paradigm_architect,pain_detector
```

### 7.4. **`setup_interfaces_optimized.py`**

**Descrição**: Setup de interfaces otimizado (Fase E)

```bash
# Setup completo
python scripts/setup_interfaces_optimized.py

# Interface específica
python scripts/setup_interfaces_optimized.py --interface rest
```

### 7.5. **`deploy_optimized.py`**

**Descrição**: Deploy otimizado (Fase G)

```bash
# Deploy completo
python scripts/deploy_optimized.py

# Ambiente específico
python scripts/deploy_optimized.py --env production
```

### 7.6. **`validate_optimized.py`**

**Descrição**: Validação otimizada (Fase F)

```bash
# Validação completa
python scripts/validate_optimized.py

# Validação específica
python scripts/validate_optimized.py --check performance
```

## 8. **Combinações Comuns de Scripts**

### 8.1. **Setup Completo do Zero**

```bash
# 1. Migração inicial
python scripts/run_migration_optimized.py --full

# 2. Transformar para LangGraph
python scripts/transform_to_langgraph_clean.py --all

# 3. Setup MCP
python scripts/setup_mcp_integration.py --all-agents

# 4. Setup AutoGen
python scripts/setup_autogen_complete.py

# 5. Deploy e teste
python scripts/deploy_and_test.py --local --monitor
```

### 8.2. **Desenvolvimento de Novo Agente**

```bash
# 1. Validar estrutura
python scripts/validate_migration.py --check agents

# 2. Criar controller LangGraph
python scripts/transform_to_langgraph_clean.py --agent-dir domains/copywriters/agents/novo_agente

# 3. Testar controller
python scripts/controller_usage_examples.py --test novo_agente

# 4. Deploy local
python scripts/deploy_and_test.py --local
```

### 8.3. **Debug e Troubleshooting**

```bash
# 1. Validação completa
python scripts/validate_migration.py --verbose

# 2. Testar específico
python scripts/test_neurohook.py --verbose

# 3. Deploy com logs
python scripts/deploy_and_test.py --local --verbose

# 4. Verificar controllers
python scripts/controller_usage_examples.py
```

## 9. **Variáveis de Ambiente para Scripts**

```bash
# Debug geral
export DEBUG=true

# Verbose para todos os scripts
export VERBOSE=true

# Porta customizada
export MCP_SERVER_PORT=8001

# Diretório de output
export OUTPUT_DIR=./custom_output

# Configuração específica
export AGENT_CONFIG=./custom_config.json

# Pular testes
export SKIP_TESTS=true
```

## 10. **Logs e Outputs**

### Arquivos de Log Gerados:
- `migration.log` - Logs de migração
- `migration_orchestrator.log` - Logs do orquestrador
- `deploy.log` - Logs de deploy
- `test_results.log` - Resultados de testes
- `langgraph_conversion.log` - Logs de conversão

### Arquivos de Relatório:
- `migration_status.json` - Status da migração
- `migration_report.json` - Relatório detalhado
- `validation_report.json` - Relatório de validação
- `test_report.json` - Relatório de testes

### Diretórios de Output:
- `migration_reports/` - Relatórios de migração
- `test_reports/` - Relatórios de teste
- `langgraph_controllers/` - Controllers gerados
- `logs/` - Logs diversos

---

**🔧 Comandos Úteis:**

```bash
# Ver todos os scripts disponíveis
ls -la scripts/

# Executar com log personalizado
python scripts/script.py 2>&1 | tee custom.log

# Executar em background
nohup python scripts/script.py &

# Matar processos
pkill -f "python scripts/"

# Verificar status
ps aux | grep "python scripts/"
``` 