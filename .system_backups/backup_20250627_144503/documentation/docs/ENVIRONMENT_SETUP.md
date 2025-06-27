# 🌍 Guia Completo de Configuração de Ambiente

## 1. **Visão Geral**

Este guia cobre toda a configuração necessária para executar o Multi-Agent AI System em diferentes ambientes (desenvolvimento, teste, produção).

---

## 2. **Arquivos de Configuração**

### 2.1. **Estrutura de Arquivos**

```
repository-optimized/
├── .env                          # Variáveis locais (não commitado)
├── .env.example                  # Template de variáveis
├── .env.development             # Ambiente de desenvolvimento
├── .env.production              # Ambiente de produção (criptografado)
├── .env.test                    # Ambiente de teste
├── config/
│   ├── development.yml          # Configurações de dev
│   ├── production.yml           # Configurações de prod
│   └── test.yml                 # Configurações de teste
└── docker/
    ├── .env.docker              # Variáveis específicas Docker
    └── docker-compose.env       # Env para docker-compose
```

### 2.2. **Prioridade de Carregamento**

1. Variáveis de ambiente do sistema
2. `.env.{ENV}` (onde ENV = development, production, test)
3. `.env.local`
4. `.env`
5. Valores padrão no código

---

## 3. **Variáveis de Ambiente Essenciais**

### 3.1. **Template Base (.env.example)**

```bash
# ==============================================
# MULTI-AGENT AI SYSTEM - ENVIRONMENT CONFIG
# ==============================================

# Environment Type
ENV=development
NODE_ENV=development
PYTHON_ENV=development

# ==============================================
# API KEYS (OBRIGATÓRIAS)
# ==============================================

# OpenAI API (Principal)
OPENAI_API_KEY=sk-...
OPENAI_ORG_ID=org-...  # Optional

# Anthropic (Claude)
ANTHROPIC_API_KEY=sk-ant-...

# Google AI
GOOGLE_AI_API_KEY=...

# Perplexity (para research)
PERPLEXITY_API_KEY=pplx-...

# ==============================================
# MCP SERVER CONFIGURATION
# ==============================================

# Server Settings
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8001
MCP_DEBUG=false
MCP_LOG_LEVEL=INFO

# Performance
MCP_MAX_WORKERS=4
MCP_REQUEST_TIMEOUT=300
MCP_MAX_REQUESTS_PER_MINUTE=60

# ==============================================
# DATABASE CONFIGURATION
# ==============================================

# PostgreSQL (opcional)
DATABASE_URL=postgresql://admin:password@localhost:5432/multiagent
DB_HOST=localhost
DB_PORT=5432
DB_NAME=multiagent
DB_USER=admin
DB_PASSWORD=password
DB_SSL_MODE=prefer

# Redis (cache, opcional)
REDIS_URL=redis://localhost:6379
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# ==============================================
# SUPABASE CONFIGURATION
# ==============================================

# Para knowledge bases e embeddings
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...

# ==============================================
# LANGSMITH (MONITORING)
# ==============================================

LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=ls__...
LANGCHAIN_PROJECT=multi-agent-system

# ==============================================
# LOGGING & MONITORING
# ==============================================

LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=logs/app.log
ENABLE_METRICS=true
METRICS_PORT=9090

# ==============================================
# SECURITY
# ==============================================

# JWT Secret
JWT_SECRET=your-super-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION=24h

# API Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
RATE_LIMIT_PER_DAY=10000

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
CORS_METHODS=GET,POST,PUT,DELETE,OPTIONS
CORS_HEADERS=*

# ==============================================
# AGENT CONFIGURATION
# ==============================================

# Default Model Settings
DEFAULT_MODEL=gpt-4
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=2000

# Agent-specific configs
PARADIGM_ARCHITECT_MODEL=gpt-4
PAIN_DETECTOR_MODEL=gpt-3.5-turbo
NEUROHOOK_ULTRA_MODEL=gpt-4

# ==============================================
# EXTERNAL INTEGRATIONS
# ==============================================

# Hotmart API
HOTMART_CLIENT_ID=...
HOTMART_CLIENT_SECRET=...
HOTMART_WEBHOOK_SECRET=...

# Kiwify API
KIWIFY_API_KEY=...
KIWIFY_WEBHOOK_SECRET=...

# PerfectPay API
PERFECTPAY_API_KEY=...
PERFECTPAY_WEBHOOK_SECRET=...

# Payt API
PAYT_API_KEY=...
PAYT_WEBHOOK_SECRET=...

# ==============================================
# DEVELOPMENT SETTINGS
# ==============================================

# Debug Flags
DEBUG=false
VERBOSE=false
DEV_MODE=true
HOT_RELOAD=true

# Testing
RUN_TESTS_ON_START=false
MOCK_EXTERNAL_APIS=false
TEST_DATABASE_URL=postgresql://test:test@localhost:5432/multiagent_test

# ==============================================
# DEPLOYMENT SETTINGS
# ==============================================

# Docker
DOCKER_IMAGE_TAG=latest
DOCKER_REGISTRY=your-registry.com

# Kubernetes
K8S_NAMESPACE=multi-agent-system
K8S_CLUSTER=production

# Health Checks
HEALTH_CHECK_INTERVAL=30s
HEALTH_CHECK_TIMEOUT=5s
HEALTH_CHECK_RETRIES=3
```

---

## 4. **Configuração por Ambiente**

### 4.1. **Desenvolvimento (.env.development)**

```bash
# Development Environment
ENV=development
DEBUG=true
VERBOSE=true
MCP_DEBUG=true
HOT_RELOAD=true

# Local Services
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8001
DATABASE_URL=postgresql://dev:dev@localhost:5432/multiagent_dev
REDIS_URL=redis://localhost:6379/1

# Relaxed Security
CORS_ORIGINS=*
RATE_LIMIT_PER_MINUTE=1000

# Development Models (mais baratos)
DEFAULT_MODEL=gpt-3.5-turbo
PARADIGM_ARCHITECT_MODEL=gpt-3.5-turbo
PAIN_DETECTOR_MODEL=gpt-3.5-turbo

# Mock APIs para desenvolvimento
MOCK_EXTERNAL_APIS=true
RUN_TESTS_ON_START=true

# Development Logging
LOG_LEVEL=DEBUG
LOG_FORMAT=pretty
ENABLE_METRICS=false
```

### 4.2. **Produção (.env.production)**

```bash
# Production Environment
ENV=production
DEBUG=false
VERBOSE=false
MCP_DEBUG=false
DEV_MODE=false

# Production Services
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8001
DATABASE_URL=postgresql://prod_user:secure_password@db.internal:5432/multiagent_prod
REDIS_URL=redis://redis.internal:6379

# Security Settings
CORS_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
RATE_LIMIT_PER_MINUTE=60
JWT_SECRET=super-secure-production-secret-key

# Production Models
DEFAULT_MODEL=gpt-4
PARADIGM_ARCHITECT_MODEL=gpt-4
PAIN_DETECTOR_MODEL=gpt-3.5-turbo

# Production Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=/var/log/multiagent/app.log
ENABLE_METRICS=true

# Health Checks
HEALTH_CHECK_INTERVAL=30s
HEALTH_CHECK_TIMEOUT=10s
```

### 4.3. **Teste (.env.test)**

```bash
# Test Environment
ENV=test
DEBUG=true
VERBOSE=false

# Test Services
MCP_SERVER_PORT=8002
DATABASE_URL=postgresql://test:test@localhost:5432/multiagent_test
REDIS_URL=redis://localhost:6379/2

# Test Settings
MOCK_EXTERNAL_APIS=true
RUN_TESTS_ON_START=false
DEFAULT_MODEL=gpt-3.5-turbo

# Fast test execution
MCP_REQUEST_TIMEOUT=30
RATE_LIMIT_PER_MINUTE=10000

# Test Logging
LOG_LEVEL=ERROR
LOG_FORMAT=simple
ENABLE_METRICS=false
```

---

## 5. **Configuração de APIs**

### 5.1. **OpenAI**

```bash
# Standard API Key
OPENAI_API_KEY=sk-...

# Organization ID (opcional, para billing)
OPENAI_ORG_ID=org-...

# Custom Endpoint (para Azure OpenAI)
OPENAI_API_BASE=https://your-resource.openai.azure.com/
OPENAI_API_VERSION=2023-12-01-preview
OPENAI_API_TYPE=azure

# Rate Limiting
OPENAI_MAX_REQUESTS_PER_MINUTE=60
OPENAI_MAX_TOKENS_PER_MINUTE=150000
```

### 5.2. **Anthropic (Claude)**

```bash
# API Key
ANTHROPIC_API_KEY=sk-ant-...

# Custom Endpoint (se necessário)
ANTHROPIC_API_URL=https://api.anthropic.com

# Model Preferences
ANTHROPIC_DEFAULT_MODEL=claude-3-sonnet-20240229
ANTHROPIC_MAX_TOKENS=4000
```

### 5.3. **Supabase (Knowledge Bases)**

```bash
# Project URL
SUPABASE_URL=https://your-project.supabase.co

# Public Anon Key (para cliente)
SUPABASE_ANON_KEY=eyJ...

# Service Role Key (para servidor)
SUPABASE_SERVICE_ROLE_KEY=eyJ...

# Database Direct Connection
SUPABASE_DB_URL=postgresql://postgres:password@db.supabase.co:5432/postgres
```

---

## 6. **Configuração de Segurança**

### 6.1. **Secrets Management**

**Para Desenvolvimento:**
```bash
# Usar .env local
cp .env.example .env
# Editar .env com suas chaves
```

**Para Produção (Docker):**
```bash
# Usar Docker Secrets
echo "sk-..." | docker secret create openai_api_key -
echo "sk-ant-..." | docker secret create anthropic_api_key -

# docker-compose.yml
secrets:
  openai_api_key:
    external: true
  anthropic_api_key:
    external: true
```

**Para Kubernetes:**
```bash
# Usar Kubernetes Secrets
kubectl create secret generic api-keys \
  --from-literal=openai-api-key="sk-..." \
  --from-literal=anthropic-api-key="sk-ant-..."
```

### 6.2. **Criptografia de Arquivos**

```bash
# Criptografar .env.production
gpg --symmetric --cipher-algo AES256 .env.production

# Descriptografar para uso
gpg --decrypt .env.production.gpg > .env.production
```

### 6.3. **Permissões de Arquivo**

```bash
# Proteger arquivos de ambiente
chmod 600 .env*
chmod 600 config/*.yml

# Verificar permissões
ls -la .env*
```

---

## 7. **Docker Configuration**

### 7.1. **Docker Compose Environment**

```yaml
# docker-compose.yml
version: '3.8'

services:
  multi-agent-system:
    build: .
    environment:
      - ENV=production
      - MCP_SERVER_PORT=8001
    env_file:
      - .env.production
    secrets:
      - openai_api_key
      - anthropic_api_key
    volumes:
      - ./logs:/app/logs
    ports:
      - "8001:8001"

secrets:
  openai_api_key:
    file: ./secrets/openai_api_key.txt
  anthropic_api_key:
    file: ./secrets/anthropic_api_key.txt
```

### 7.2. **Dockerfile Environment**

```dockerfile
FROM python:3.11-slim

# Environment defaults
ENV ENV=production
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

CMD ["python", "mcp_integration/mcp_server.py"]
```

---

## 8. **Validação de Configuração**

### 8.1. **Script de Validação**

```python
#!/usr/bin/env python3
# scripts/validate_env.py

import os
import sys
from typing import List, Tuple

def check_required_vars() -> List[Tuple[str, bool]]:
    """Verifica variáveis obrigatórias"""
    required = [
        'OPENAI_API_KEY',
        'MCP_SERVER_PORT',
        'ENV'
    ]
    
    results = []
    for var in required:
        value = os.getenv(var)
        results.append((var, bool(value)))
    
    return results

def check_optional_vars() -> List[Tuple[str, bool]]:
    """Verifica variáveis opcionais"""
    optional = [
        'ANTHROPIC_API_KEY',
        'SUPABASE_URL',
        'REDIS_URL',
        'DATABASE_URL'
    ]
    
    results = []
    for var in optional:
        value = os.getenv(var)
        results.append((var, bool(value)))
    
    return results

def validate_api_keys():
    """Valida formato das API keys"""
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key and not openai_key.startswith('sk-'):
        print(f"⚠️  OPENAI_API_KEY parece inválida")
    
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    if anthropic_key and not anthropic_key.startswith('sk-ant-'):
        print(f"⚠️  ANTHROPIC_API_KEY parece inválida")

def main():
    print("🔍 Validando configuração de ambiente...\n")
    
    # Variáveis obrigatórias
    print("📋 Variáveis Obrigatórias:")
    required_results = check_required_vars()
    for var, exists in required_results:
        status = "✅" if exists else "❌"
        print(f"  {status} {var}")
    
    # Variáveis opcionais
    print("\n📋 Variáveis Opcionais:")
    optional_results = check_optional_vars()
    for var, exists in optional_results:
        status = "✅" if exists else "⚠️ "
        print(f"  {status} {var}")
    
    # Validação adicional
    print("\n🔐 Validação de API Keys:")
    validate_api_keys()
    
    # Resultado final
    missing_required = [var for var, exists in required_results if not exists]
    if missing_required:
        print(f"\n❌ Variáveis obrigatórias faltando: {', '.join(missing_required)}")
        sys.exit(1)
    else:
        print(f"\n✅ Configuração básica válida!")

if __name__ == "__main__":
    main()
```

### 8.2. **Comando de Validação**

```bash
# Validar ambiente atual
python scripts/validate_env.py

# Validar ambiente específico
ENV=production python scripts/validate_env.py

# Validar com arquivo específico
python -c "
import os
from dotenv import load_dotenv
load_dotenv('.env.production')
exec(open('scripts/validate_env.py').read())
"
```

---

## 9. **Troubleshooting**

### 9.1. **Problemas Comuns**

**Erro: "API key not found"**
```bash
# Verificar se .env está sendo carregado
python -c "import os; print(os.getenv('OPENAI_API_KEY'))"

# Verificar arquivo .env
cat .env | grep OPENAI_API_KEY

# Verificar permissões
ls -la .env
```

**Erro: "Port already in use"**
```bash
# Verificar porta em uso
lsof -i :8001

# Mudar porta
export MCP_SERVER_PORT=8002
```

**Erro: "Database connection failed"**
```bash
# Testar conexão
python -c "
import os
import psycopg2
try:
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    print('✅ Database connection OK')
except Exception as e:
    print(f'❌ Database error: {e}')
"
```

### 9.2. **Debug de Configuração**

```bash
# Ver todas as variáveis carregadas
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
for key, value in sorted(os.environ.items()):
    if any(x in key.upper() for x in ['API', 'KEY', 'SECRET', 'PASSWORD', 'TOKEN']):
        print(f'{key}=***masked***')
    elif key.startswith(('MCP_', 'ENV', 'DEBUG')):
        print(f'{key}={value}')
"

# Testar carregamento de .env
python -c "
from dotenv import load_dotenv
import os
print('Before:', os.getenv('DEBUG'))
load_dotenv('.env.development')
print('After:', os.getenv('DEBUG'))
"
```

---

## 10. **Scripts de Setup**

### 10.1. **Setup Automático**

```bash
#!/bin/bash
# scripts/setup_env.sh

ENV_TYPE=${1:-development}

echo "🚀 Configurando ambiente: $ENV_TYPE"

# Copiar template apropriado
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Arquivo .env criado a partir do template"
    else
        echo "❌ Template .env.example não encontrado"
        exit 1
    fi
fi

# Definir permissões
chmod 600 .env*
echo "✅ Permissões de segurança aplicadas"

# Validar configuração
python scripts/validate_env.py

echo "✅ Setup de ambiente concluído!"
echo "📝 Edite o arquivo .env com suas credenciais"
```

### 10.2. **Setup para Produção**

```bash
#!/bin/bash
# scripts/setup_production.sh

echo "🔒 Configurando ambiente de produção..."

# Verificar se secrets existem
if [ ! -d "secrets" ]; then
    mkdir secrets
    chmod 700 secrets
fi

# Prompt para API keys
read -s -p "OpenAI API Key: " OPENAI_KEY
echo "$OPENAI_KEY" > secrets/openai_api_key.txt

read -s -p "Anthropic API Key: " ANTHROPIC_KEY
echo "$ANTHROPIC_KEY" > secrets/anthropic_api_key.txt

# Proteger secrets
chmod 600 secrets/*

# Criar .env.production
cat > .env.production << EOF
ENV=production
DEBUG=false
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8001
LOG_LEVEL=INFO
CORS_ORIGINS=https://yourdomain.com
EOF

echo "✅ Ambiente de produção configurado!"
echo "🔐 API keys armazenadas em secrets/"
```

---

**🚀 Quick Setup:**

```bash
# Setup desenvolvimento
bash scripts/setup_env.sh development

# Setup produção
bash scripts/setup_production.sh

# Validar configuração
python scripts/validate_env.py

# Testar conexões
python scripts/test_connections.py
```

**📋 Checklist de Configuração:**

- [ ] Copiar .env.example para .env
- [ ] Configurar API keys obrigatórias
- [ ] Definir ambiente (development/production)
- [ ] Configurar banco de dados (se usar)
- [ ] Configurar Redis (se usar)
- [ ] Validar configuração
- [ ] Testar conexões
- [ ] Proteger permissões de arquivos 