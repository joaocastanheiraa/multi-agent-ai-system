# 🚀 Guia Completo de Deploy do Multi-Agent AI System

## 1. **Opções de Deploy**

### 1.1. **Deploy Local (Desenvolvimento)**

```bash
# Executar testes primeiro
python test_system.py

# Executar deploy local
bash deploy_local.sh

# Ou usar o script Python
python scripts/deploy_and_test.py --local
```

### 1.2. **Deploy com Docker**

```bash
# Build da imagem
docker build -t multi-agent-system .

# Executar container
docker run -p 8001:8001 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -v $(pwd)/logs:/app/logs \
  multi-agent-system

# Ou usar o script
bash deploy_docker.sh
```

### 1.3. **Deploy com Docker Compose (Produção)**

```bash
# Subir todos os serviços
docker-compose up -d

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f multi-agent-system

# Parar serviços
docker-compose down
```

## 2. **Configuração de Ambiente**

### 2.1. **Variáveis de Ambiente Essenciais**

Copie `.env.example` para `.env` e configure:

```bash
# APIs
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=...

# MCP Server
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8001
MCP_DEBUG=false

# Database (opcional)
DATABASE_URL=postgresql://admin:admin123@postgres:5432/multiagent

# Redis (opcional)
REDIS_URL=redis://redis:6379

# Ambiente
ENV=production
LOG_LEVEL=INFO
PYTHONPATH=/app
```

### 2.2. **Configuração por Ambiente**

**Desenvolvimento:**
```bash
ENV=development
LOG_LEVEL=DEBUG
MCP_DEBUG=true
```

**Produção:**
```bash
ENV=production
LOG_LEVEL=INFO
MCP_DEBUG=false
```

## 3. **Scripts de Deploy Automatizado**

### 3.1. **Deploy Local**

```bash
#!/bin/bash
# deploy_local.sh

set -e

echo "🚀 Iniciando deploy local..."

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt -r requirements_mcp.txt

# Executar testes
python test_system.py

# Executar validação de migração
python scripts/validate_migration.py

# Iniciar MCP Server
cd mcp_integration
uvicorn mcp_server:app --host 0.0.0.0 --port 8001 --reload &
MCP_PID=$!

echo "✅ Deploy local concluído!"
echo "🌐 Servidor disponível em: http://localhost:8001"
echo "📖 Documentação da API: http://localhost:8001/docs"
echo "🛑 Para parar: kill $MCP_PID"
```

### 3.2. **Deploy Docker**

```bash
#!/bin/bash
# deploy_docker.sh

set -e

echo "🐳 Iniciando deploy Docker..."

# Build da imagem
docker build -t multi-agent-system:latest .

# Parar container existente (se houver)
docker stop multi-agent-system || true
docker rm multi-agent-system || true

# Executar novo container
docker run -d \
  --name multi-agent-system \
  -p 8001:8001 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/data:/app/data \
  --restart unless-stopped \
  multi-agent-system:latest

echo "✅ Deploy Docker concluído!"
echo "🌐 Servidor disponível em: http://localhost:8001"
```

## 4. **Monitoramento e Health Checks**

### 4.1. **Health Check Endpoint**

```bash
# Verificar status da aplicação
curl http://localhost:8001/health

# Resposta esperada:
{
  "status": "healthy",
  "version": "3.0.0",
  "agents": 14,
  "timestamp": "2025-01-XX"
}
```

### 4.2. **Dashboard de Monitoramento**

```bash
# Executar dashboard local
python monitor_dashboard.py

# Acesse: http://localhost:8002
```

### 4.3. **Logs e Debugging**

```bash
# Ver logs em tempo real
tail -f logs/mcp_server.log

# Docker logs
docker logs -f multi-agent-system

# Docker Compose logs
docker-compose logs -f multi-agent-system
```

## 5. **Configuração de Produção**

### 5.1. **Docker Compose para Produção**

```yaml
version: '3.8'

services:
  multi-agent-system:
    build: .
    ports:
      - "8001:8001"
    environment:
      - PYTHONPATH=/app
      - ENV=production
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    depends_on:
      - redis
      - postgres

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: multiagent
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-admin123}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
    depends_on:
      - multi-agent-system
    restart: unless-stopped

volumes:
  redis_data:
  postgres_data:
```

### 5.2. **Configuração Nginx**

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream multi_agent_backend {
        server multi-agent-system:8001;
    }

    server {
        listen 80;
        server_name your-domain.com;

        location / {
            proxy_pass http://multi_agent_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /docs {
            proxy_pass http://multi_agent_backend/docs;
        }

        location /health {
            proxy_pass http://multi_agent_backend/health;
        }
    }
}
```

## 6. **Segurança**

### 6.1. **Variáveis Sensíveis**

```bash
# Usar secrets do Docker Swarm ou Kubernetes
echo "sk-..." | docker secret create openai_api_key -

# Ou usar .env com permissões restritas
chmod 600 .env
```

### 6.2. **Firewall e Acesso**

```bash
# Permitir apenas portas necessárias
ufw allow 80
ufw allow 443
ufw allow 8001  # apenas para desenvolvimento
```

## 7. **Backup e Recuperação**

### 7.1. **Backup de Dados**

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/$DATE"

mkdir -p $BACKUP_DIR

# Backup de configurações
cp -r domains/ $BACKUP_DIR/
cp -r knowledge_bases/ $BACKUP_DIR/
cp .env $BACKUP_DIR/

# Backup de banco (se usando PostgreSQL)
docker exec postgres pg_dump -U admin multiagent > $BACKUP_DIR/database.sql

echo "✅ Backup criado em: $BACKUP_DIR"
```

### 7.2. **Recuperação**

```bash
#!/bin/bash
# restore.sh

BACKUP_DIR=$1

if [ -z "$BACKUP_DIR" ]; then
    echo "Uso: ./restore.sh <diretório_backup>"
    exit 1
fi

# Restaurar configurações
cp -r $BACKUP_DIR/domains/ .
cp -r $BACKUP_DIR/knowledge_bases/ .
cp $BACKUP_DIR/.env .

# Restaurar banco
docker exec -i postgres psql -U admin multiagent < $BACKUP_DIR/database.sql

echo "✅ Recuperação concluída de: $BACKUP_DIR"
```

## 8. **Troubleshooting**

### 8.1. **Problemas Comuns**

**Erro de porta em uso:**
```bash
# Verificar processo usando a porta
lsof -i :8001

# Matar processo
kill -9 <PID>
```

**Erro de permissão:**
```bash
# Verificar permissões dos arquivos
ls -la .env

# Corrigir permissões
chmod 600 .env
chmod +x *.sh
```

**Container não inicia:**
```bash
# Ver logs detalhados
docker logs multi-agent-system

# Executar container interativo para debug
docker run -it --entrypoint /bin/bash multi-agent-system
```

### 8.2. **Comandos de Debug**

```bash
# Verificar status de todos os serviços
docker-compose ps

# Entrar no container
docker exec -it multi-agent-system bash

# Verificar conectividade
curl -v http://localhost:8001/health

# Verificar logs de aplicação
tail -f logs/*.log
```

## 9. **Escalabilidade**

### 9.1. **Deploy com Kubernetes**

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: multi-agent-system
spec:
  replicas: 3
  selector:
    matchLabels:
      app: multi-agent-system
  template:
    metadata:
      labels:
        app: multi-agent-system
    spec:
      containers:
      - name: multi-agent-system
        image: multi-agent-system:latest
        ports:
        - containerPort: 8001
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: openai-key
```

### 9.2. **Load Balancer**

```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: multi-agent-service
spec:
  selector:
    app: multi-agent-system
  ports:
  - port: 80
    targetPort: 8001
  type: LoadBalancer
```

## 10. **Comandos Úteis**

```bash
# Deploy completo
make deploy-prod

# Verificar saúde do sistema
make health-check

# Backup automático
make backup

# Atualizar sistema
make update

# Rollback
make rollback

# Limpar logs antigos
make clean-logs
```

---

**📋 Checklist de Deploy:**

- [ ] Configurar variáveis de ambiente
- [ ] Executar testes locais
- [ ] Verificar conectividade com APIs externas
- [ ] Configurar monitoramento
- [ ] Configurar backup
- [ ] Configurar SSL (produção)
- [ ] Configurar firewall
- [ ] Documentar URLs e credenciais
- [ ] Treinar equipe de operações

---

**🚨 Para emergências:**
1. Verificar health endpoint
2. Revisar logs recentes
3. Verificar recursos do sistema
4. Reiniciar serviços se necessário
5. Contatar equipe de desenvolvimento 