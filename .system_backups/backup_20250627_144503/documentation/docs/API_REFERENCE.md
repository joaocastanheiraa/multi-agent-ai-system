# 🌐 Referência Completa da API - MCP Server

## 1. **Visão Geral**

O MCP Server fornece uma API REST para interagir com todos os agentes do sistema Multi-Agent AI. A API está disponível em `http://localhost:8001` e inclui documentação interativa via Swagger.

**Base URL**: `http://localhost:8001`  
**Documentação Interativa**: `http://localhost:8001/docs`  
**Schema OpenAPI**: `http://localhost:8001/openapi.json`

---

## 2. **Autenticação**

### 2.1. **API Key (Opcional)**

Se configurada, use header de autenticação:

```bash
# Header de autenticação
Authorization: Bearer YOUR_API_KEY

# Exemplo com curl
curl -H "Authorization: Bearer YOUR_API_KEY" \
     http://localhost:8001/agents
```

### 2.2. **CORS**

A API suporta CORS para desenvolvimento frontend:

```python
# Headers permitidos
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: *
```

---

## 3. **Endpoints Principais**

### 3.1. **Health Check**

**GET** `/health`

Verifica status da aplicação.

```bash
curl http://localhost:8001/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "3.0.0",
  "agents": 14,
  "timestamp": "2025-01-16T10:30:00Z",
  "uptime": "2h 15m 30s",
  "memory_usage": "245MB",
  "cpu_usage": "15%"
}
```

### 3.2. **Listar Agentes**

**GET** `/agents`

Lista todos os agentes disponíveis.

```bash
curl http://localhost:8001/agents
```

**Response:**
```json
{
  "success": true,
  "data": {
    "count": 14,
    "agents": [
      {
        "id": "paradigm_architect",
        "name": "Paradigm Architect",
        "domain": "copywriters",
        "description": "Agente especializado em mudança de paradigmas",
        "status": "active",
        "version": "1.0.0",
        "capabilities": ["analysis", "paradigm_shift", "storytelling"],
        "endpoints": ["/process", "/analyze"]
      },
      {
        "id": "pain_detector",
        "name": "Pain Detector",
        "domain": "copywriters", 
        "description": "Detecção e análise de dores do cliente",
        "status": "active",
        "version": "1.0.0",
        "capabilities": ["pain_analysis", "emotion_detection"],
        "endpoints": ["/process", "/detect"]
      }
    ]
  }
}
```

### 3.3. **Detalhes de Agente Específico**

**GET** `/agents/{agent_id}`

Obter informações detalhadas de um agente.

```bash
curl http://localhost:8001/agents/paradigm_architect
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "paradigm_architect",
    "name": "Paradigm Architect",
    "domain": "copywriters",
    "description": "Agente especializado em mudança de paradigmas",
    "status": "active",
    "version": "1.0.0",
    "config": {
      "model": "gpt-4",
      "temperature": 0.7,
      "max_tokens": 2000
    },
    "capabilities": ["analysis", "paradigm_shift", "storytelling"],
    "endpoints": ["/process", "/analyze"],
    "schema": {
      "input": {
        "text": "string",
        "context": "string",
        "options": "object"
      },
      "output": {
        "result": "string",
        "analysis": "object",
        "metadata": "object"
      }
    },
    "examples": [
      {
        "input": {"text": "Produto caro", "context": "SaaS B2B"},
        "output": {"result": "Investimento estratégico em produtividade..."}
      }
    ]
  }
}
```

### 3.4. **Processar com Agente**

**POST** `/agent/{agent_id}/process`

Executar processamento principal do agente.

```bash
curl -X POST http://localhost:8001/agent/paradigm_architect/process \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Nosso produto é muito caro para o mercado",
    "context": "SaaS empresarial B2B", 
    "options": {
      "format": "detailed",
      "include_examples": true
    }
  }'
```

**Request Schema:**
```json
{
  "text": "string (required)",
  "context": "string (optional)",
  "options": {
    "format": "brief|detailed",
    "include_examples": "boolean",
    "tone": "professional|casual|persuasive",
    "length": "short|medium|long"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "result": "Em vez de 'caro', posicione como 'investimento estratégico em produtividade'...",
    "analysis": {
      "paradigm_shift": "cost -> investment",
      "emotional_trigger": "fear_of_loss",
      "reframing_strength": 8.5
    },
    "metadata": {
      "processing_time": "1.2s",
      "tokens_used": 450,
      "model": "gpt-4",
      "confidence": 0.92
    },
    "suggestions": [
      "Adicione case studies de ROI",
      "Compare com custo de não ter a solução",
      "Destaque economia de tempo/recursos"
    ]
  }
}
```

### 3.5. **Análise Específica**

**POST** `/agent/{agent_id}/analyze`

Executar análise especializada do agente.

```bash
curl -X POST http://localhost:8001/agent/pain_detector/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Estou perdendo clientes para a concorrência",
    "analyze_type": "pain_depth"
  }'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "pain_level": 8,
    "pain_type": "business_threat",
    "emotional_state": "anxiety",
    "urgency": "high",
    "triggers": [
      "competitive_pressure",
      "revenue_loss",
      "market_share_erosion"
    ],
    "recommendations": [
      "Criar urgência com dados de mercado",
      "Focar em diferenciação única",
      "Ofereger garantias de resultados"
    ]
  }
}
```

---

## 4. **Endpoints por Domínio**

### 4.1. **Copywriters Domain**

**Agentes Disponíveis:**
- `paradigm_architect` - Mudança de paradigmas
- `pain_detector` - Detecção de dores
- `neurohook_ultra` - Criação de hooks neurológicos
- `metaphor_architect` - Construção de metáforas
- `conversion_catalyst` - Otimização de conversão
- `retention_architect` - Estratégias de retenção

**Endpoints Comuns:**
```bash
POST /agent/{agent_id}/process      # Processamento principal
POST /agent/{agent_id}/analyze      # Análise específica
POST /agent/{agent_id}/generate     # Geração de conteúdo
POST /agent/{agent_id}/optimize     # Otimização de copy
```

### 4.2. **APIs Domain**

**Agentes Disponíveis:**
- `hotmart_master` - Integração Hotmart
- `kiwify_master` - Integração Kiwify
- `perfectpay_master` - Integração PerfectPay
- `payt_master` - Integração Payt
- `api_unify_master` - Unificação de APIs

**Endpoints Comuns:**
```bash
POST /agent/{agent_id}/connect      # Conectar API
POST /agent/{agent_id}/sync         # Sincronizar dados
POST /agent/{agent_id}/webhook      # Configurar webhooks
GET  /agent/{agent_id}/status       # Status da conexão
```

### 4.3. **Analytics Domain**

**Agentes Disponíveis:**
- `super_track` - Analytics avançado

**Endpoints Comuns:**
```bash
POST /agent/super_track/track       # Rastrear evento
POST /agent/super_track/analyze     # Análise de dados
GET  /agent/super_track/report      # Relatórios
POST /agent/super_track/funnel      # Análise de funil
```

---

## 5. **Schemas de Request/Response**

### 5.1. **Schema Base de Request**

```json
{
  "text": "string (required)",
  "context": "string (optional)",
  "options": {
    "format": "brief|detailed|json",
    "language": "pt|en|es",
    "tone": "professional|casual|persuasive|urgent",
    "length": "short|medium|long",
    "include_examples": "boolean",
    "include_metadata": "boolean"
  },
  "metadata": {
    "user_id": "string",
    "session_id": "string",
    "timestamp": "string",
    "source": "string"
  }
}
```

### 5.2. **Schema Base de Response**

```json
{
  "success": "boolean",
  "data": {
    "result": "string|object",
    "analysis": "object (optional)",
    "metadata": {
      "processing_time": "string",
      "tokens_used": "number",
      "model": "string",
      "confidence": "number",
      "agent_version": "string"
    },
    "suggestions": "array (optional)",
    "next_actions": "array (optional)"
  },
  "error": {
    "code": "string",
    "message": "string",
    "details": "object"
  }
}
```

---

## 6. **Códigos de Status e Erros**

### 6.1. **Códigos de Sucesso**

- `200` - OK - Requisição processada com sucesso
- `201` - Created - Recurso criado com sucesso
- `202` - Accepted - Requisição aceita para processamento

### 6.2. **Códigos de Erro do Cliente**

- `400` - Bad Request - Dados de entrada inválidos
- `401` - Unauthorized - Falha na autenticação
- `403` - Forbidden - Acesso negado
- `404` - Not Found - Agente ou endpoint não encontrado
- `429` - Too Many Requests - Rate limit excedido

### 6.3. **Códigos de Erro do Servidor**

- `500` - Internal Server Error - Erro interno do servidor
- `502` - Bad Gateway - Erro na comunicação com agente
- `503` - Service Unavailable - Serviço temporariamente indisponível
- `504` - Gateway Timeout - Timeout na execução do agente

### 6.4. **Exemplos de Erros**

**400 - Bad Request:**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "O campo 'text' é obrigatório",
    "details": {
      "field": "text",
      "expected": "string",
      "received": "null"
    }
  }
}
```

**404 - Agent Not Found:**
```json
{
  "success": false,
  "error": {
    "code": "AGENT_NOT_FOUND",
    "message": "Agente 'invalid_agent' não encontrado",
    "details": {
      "agent_id": "invalid_agent",
      "available_agents": ["paradigm_architect", "pain_detector", "..."]
    }
  }
}
```

**500 - Processing Error:**
```json
{
  "success": false,
  "error": {
    "code": "PROCESSING_ERROR",
    "message": "Erro ao processar request com o agente",
    "details": {
      "agent_id": "paradigm_architect",
      "error_type": "model_timeout",
      "retry_after": 30
    }
  }
}
```

---

## 7. **Rate Limiting**

### 7.1. **Limites Padrão**

- **Requests por minuto**: 60
- **Requests por hora**: 1000
- **Requests por dia**: 10000

### 7.2. **Headers de Rate Limit**

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1642780800
```

### 7.3. **Response 429 - Rate Limit**

```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit excedido",
    "details": {
      "limit": 60,
      "window": "1m",
      "retry_after": 30
    }
  }
}
```

---

## 8. **Webhooks**

### 8.1. **Configurar Webhook**

**POST** `/webhooks/configure`

```bash
curl -X POST http://localhost:8001/webhooks/configure \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://yourapp.com/webhook",
    "events": ["agent.completed", "agent.failed"],
    "secret": "your_webhook_secret"
  }'
```

### 8.2. **Payload do Webhook**

```json
{
  "event": "agent.completed",
  "timestamp": "2025-01-16T10:30:00Z",
  "agent_id": "paradigm_architect",
  "request_id": "req_123456",
  "data": {
    "input": {...},
    "output": {...},
    "metadata": {...}
  }
}
```

---

## 9. **SDKs e Bibliotecas**

### 9.1. **JavaScript/Node.js**

```javascript
const MultiAgentAPI = require('multi-agent-api');

const client = new MultiAgentAPI({
  baseURL: 'http://localhost:8001',
  apiKey: 'YOUR_API_KEY'
});

// Processar com agente
const result = await client.agents.paradigmArchitect.process({
  text: "Produto caro",
  context: "SaaS B2B",
  options: { format: "detailed" }
});

console.log(result.data.result);
```

### 9.2. **Python**

```python
from multi_agent_api import MultiAgentClient

client = MultiAgentClient(
    base_url="http://localhost:8001",
    api_key="YOUR_API_KEY"
)

# Processar com agente
result = client.agents.paradigm_architect.process(
    text="Produto caro",
    context="SaaS B2B",
    options={"format": "detailed"}
)

print(result.data.result)
```

### 9.3. **cURL Examples**

```bash
# Listar agentes
curl http://localhost:8001/agents

# Processar com Paradigm Architect
curl -X POST http://localhost:8001/agent/paradigm_architect/process \
  -H "Content-Type: application/json" \
  -d '{"text": "Produto caro", "context": "SaaS B2B"}'

# Detectar dor com Pain Detector
curl -X POST http://localhost:8001/agent/pain_detector/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Perdendo clientes", "analyze_type": "pain_depth"}'

# Health check
curl http://localhost:8001/health
```

---

## 10. **Monitoramento e Logs**

### 10.1. **Métricas da API**

**GET** `/metrics`

```json
{
  "requests_total": 1250,
  "requests_per_minute": 15.5,
  "average_response_time": "850ms",
  "error_rate": "2.1%",
  "active_connections": 8,
  "agents": {
    "paradigm_architect": {
      "requests": 350,
      "avg_time": "1.2s",
      "success_rate": "98.5%"
    }
  }
}
```

### 10.2. **Logs de Auditoria**

**GET** `/logs?agent={agent_id}&limit={limit}`

```json
{
  "logs": [
    {
      "timestamp": "2025-01-16T10:30:00Z",
      "level": "INFO",
      "agent_id": "paradigm_architect",
      "request_id": "req_123456",
      "message": "Request processed successfully",
      "duration": "1.2s",
      "status": "success"
    }
  ]
}
```

---

## 11. **Testes e Desenvolvimento**

### 11.1. **Ambiente de Testes**

```bash
# Iniciar em modo teste
MCP_ENV=test python mcp_integration/mcp_server.py

# URL de teste
http://localhost:8001/test
```

### 11.2. **Mock Responses**

```bash
# Habilitar mocks
curl -X POST http://localhost:8001/test/mock/enable

# Configurar mock response
curl -X POST http://localhost:8001/test/mock/agent/paradigm_architect \
  -H "Content-Type: application/json" \
  -d '{"result": "Mock response for testing"}'
```

### 11.3. **Performance Testing**

```bash
# Teste de carga com ab
ab -n 1000 -c 10 http://localhost:8001/health

# Teste de stress com curl
for i in {1..100}; do
  curl -X POST http://localhost:8001/agent/paradigm_architect/process \
    -H "Content-Type: application/json" \
    -d '{"text": "test"}' &
done
```

---

**📋 Quick Reference:**

- **Base URL**: `http://localhost:8001`
- **Docs**: `http://localhost:8001/docs`
- **Health**: `http://localhost:8001/health`
- **Agents**: `http://localhost:8001/agents`
- **Process**: `POST /agent/{id}/process`
- **Analyze**: `POST /agent/{id}/analyze`

**🔧 Development Tools:**

- Swagger UI para explorar API
- Postman collection disponível
- SDK Python e JavaScript
- Webhook testing endpoint
- Rate limiting configurável 