# 🔧 Guia Completo do Makefile

## 1. **Visão Geral**

O Makefile automatiza tarefas comuns de setup, instalação e configuração dos agentes. Ele facilita a configuração de agentes individuais ou todos de uma vez, gerencia dependências e faz upload de embeddings.

---

## 2. **Comandos Disponíveis**

### 2.1. **Instalação e Setup**

#### `make install`
Instala todas as dependências necessárias.

```bash
make install
```

**O que faz:**
- Instala: `openai`, `supabase`, `python-dotenv`, `tqdm`, `pyyaml`, `colorama`, `requests`
- Verifica se todas as dependências foram instaladas corretamente

#### `make check`
Verifica se todas as dependências estão instaladas.

```bash
make check
```

**Verifica:**
- openai
- supabase  
- dotenv
- tqdm

#### `make dirs`
Cria diretórios necessários para o sistema.

```bash
make dirs
```

**Cria:**
- `data/embeddings/` - Para armazenar embeddings gerados
- `agents/` - Para configurações de agentes

---

## 3. **Configuração de Agentes Específicos**

### 3.1. **Retention Architect**

```bash
make agent-retention
```

**Script executado:** `./scripts/setup_retention_architect.sh`

**O que configura:**
- Estrutura de diretórios para retention_architect
- Knowledge base de retenção
- Embeddings específicos de retenção
- Configurações de prompt

### 3.2. **Pain Detector**

```bash
make agent-pain
```

**Script executado:** `./scripts/setup_pain_detector.sh`

**O que configura:**
- Estrutura para detecção de dores
- Base de conhecimento de pain points
- Embeddings de análise emocional
- Templates de detecção

### 3.3. **Paradigm Architect**

```bash
make agent-paradigm
```

**Script executado:** `./scripts/setup_paradigm_architect.sh`

**O que configura:**
- Framework de mudança de paradigmas
- Knowledge base de paradigmas
- Embeddings de storytelling
- Templates de reframing

### 3.4. **Metaphor Architect**

```bash
make agent-metaphor
```

**Script executado:** `./scripts/setup_metaphor_architect.sh`

**O que configura:**
- Biblioteca de metáforas
- Knowledge base criativa
- Embeddings de analogias
- Templates de comparação

### 3.5. **Conversion Catalyst**

```bash
make agent-conversion
```

**Script executado:** `./scripts/setup_conversion_catalyst.sh`

**O que configura:**
- Frameworks de conversão
- Knowledge base de CRO
- Embeddings de otimização
- Templates de urgência

---

## 4. **Comandos Combinados**

### 4.1. **Setup Completo**

```bash
make all
```

**Executa em sequência:**
1. `make agent-retention`
2. `make agent-pain`
3. `make agent-paradigm`
4. `make agent-metaphor`
5. `make agent-conversion`

**Resultado:** Todos os agentes configurados e prontos para uso.

---

## 5. **Upload de Embeddings**

### 5.1. **Upload Específico**

```bash
# Upload retention architect
make upload-retention

# Upload pain detector
make upload-pain

# Upload paradigm architect
make upload-paradigm

# Upload metaphor architect
make upload-metaphor

# Upload conversion catalyst
make upload-conversion
```

**O que faz:**
- Verifica se o arquivo de embeddings existe em `data/embeddings/`
- Executa `python scripts/upload_to_supabase.py` com o arquivo correspondente
- Faz upload para o Supabase configurado

### 5.2. **Estrutura de Arquivos de Embeddings**

```
data/embeddings/
├── retention-embedding-data.jsonl
├── pain-embedding-data.jsonl
├── paradigm-embedding-data.jsonl
├── metaphor-embedding-data.jsonl
└── conversion-embedding-data.jsonl
```

---

## 6. **Limpeza e Manutenção**

### 6.1. **Limpar Arquivos Temporários**

```bash
make clean
```

**Remove:**
- `*.log` - Arquivos de log
- `*.tmp` - Arquivos temporários
- `data/embeddings/*.progress` - Arquivos de progresso

---

## 7. **Workflows Práticos**

### 7.1. **Setup Inicial Completo**

```bash
# 1. Instalar dependências
make install

# 2. Verificar instalação
make check

# 3. Criar diretórios
make dirs

# 4. Configurar todos os agentes
make all

# 5. Upload de todos os embeddings
make upload-retention
make upload-pain
make upload-paradigm
make upload-metaphor
make upload-conversion
```

### 7.2. **Configurar Agente Específico**

```bash
# Exemplo: Configurar apenas o Paradigm Architect
make install
make check
make dirs
make agent-paradigm
make upload-paradigm
```

### 7.3. **Reconfigurar Sistema**

```bash
# Limpar tudo e reconfigurar
make clean
make all
```

---

## 8. **Dependências dos Scripts**

### 8.1. **Scripts de Setup Esperados**

O Makefile espera que existam os seguintes scripts em `./scripts/`:

- `setup_retention_architect.sh`
- `setup_pain_detector.sh`
- `setup_paradigm_architect.sh`
- `setup_metaphor_architect.sh`
- `setup_conversion_catalyst.sh`
- `upload_to_supabase.py`

### 8.2. **Estrutura Esperada**

```
project/
├── Makefile
├── scripts/
│   ├── setup_retention_architect.sh
│   ├── setup_pain_detector.sh
│   ├── setup_paradigm_architect.sh
│   ├── setup_metaphor_architect.sh
│   ├── setup_conversion_catalyst.sh
│   └── upload_to_supabase.py
├── data/
│   └── embeddings/
└── agents/
```

---

## 9. **Variáveis de Configuração**

### 9.1. **Variáveis do Makefile**

```makefile
SHELL=/bin/bash
```

### 9.2. **Variáveis de Ambiente Suportadas**

```bash
# Para upload para Supabase
export SUPABASE_URL="your-supabase-url"
export SUPABASE_KEY="your-supabase-key"

# Para configuração OpenAI
export OPENAI_API_KEY="your-openai-key"

# Para debug
export DEBUG=true
export VERBOSE=true
```

---

## 10. **Troubleshooting**

### 10.1. **Problemas Comuns**

**Erro: "Algumas dependências estão faltando"**
```bash
# Solução
make install
make check
```

**Erro: "Arquivo de embeddings não encontrado"**
```bash
# Verificar se o agente foi configurado primeiro
make agent-retention
# Depois fazer upload
make upload-retention
```

**Erro: "Script não encontrado"**
```bash
# Verificar se os scripts existem
ls -la scripts/setup_*.sh

# Dar permissão de execução se necessário
chmod +x scripts/*.sh
```

### 10.2. **Debug**

```bash
# Executar com debug
DEBUG=true make agent-paradigm

# Ver saída detalhada
VERBOSE=true make all

# Executar step by step
make install && make check && make dirs && make agent-paradigm
```

---

## 11. **Customização**

### 11.1. **Adicionar Novo Agente**

Para adicionar um novo agente ao Makefile:

```makefile
# Adicionar target
agent-novo-agente: check dirs
	@./scripts/setup_novo_agente.sh

# Adicionar upload
upload-novo-agente: check
	@if [ -f "data/embeddings/novo-agente-embedding-data.jsonl" ]; then \
		python scripts/upload_to_supabase.py data/embeddings/novo-agente-embedding-data.jsonl; \
	else \
		echo "❌ Arquivo de embeddings para novo-agente não encontrado. Execute 'make agent-novo-agente' primeiro."; \
	fi

# Adicionar ao target 'all'
all: agent-retention agent-pain agent-paradigm agent-metaphor agent-conversion agent-novo-agente
```

### 11.2. **Targets Personalizados**

```makefile
# Setup de desenvolvimento
dev-setup: install check dirs agent-paradigm agent-pain
	@echo "✅ Setup de desenvolvimento concluído!"

# Setup de produção
prod-setup: install check dirs all
	@echo "✅ Setup de produção concluído!"

# Backup de embeddings
backup-embeddings:
	@mkdir -p backup/$(shell date +%Y%m%d)
	@cp -r data/embeddings/ backup/$(shell date +%Y%m%d)/
	@echo "✅ Backup criado em backup/$(shell date +%Y%m%d)/"
```

---

## 12. **Integração com CI/CD**

### 12.1. **GitHub Actions**

```yaml
# .github/workflows/setup.yml
name: Setup Agents
on: [push]

jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: make install
    - name: Check dependencies
      run: make check
    - name: Setup all agents
      run: make all
```

### 12.2. **Docker Integration**

```dockerfile
# Dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY . .

# Usar Makefile para setup
RUN make install
RUN make check
RUN make dirs
RUN make all

CMD ["python", "app.py"]
```

---

**🚀 Quick Commands:**

```bash
# Setup completo
make install && make all

# Verificar sistema
make check

# Agente específico
make agent-paradigm && make upload-paradigm

# Limpeza
make clean

# Debug
DEBUG=true make agent-pain
```

**📋 Checklist de Setup:**

- [ ] `make install` - Instalar dependências
- [ ] `make check` - Verificar instalação
- [ ] `make dirs` - Criar diretórios
- [ ] `make all` - Configurar agentes
- [ ] `make upload-*` - Fazer upload embeddings
- [ ] Verificar logs de erro
- [ ] Testar agentes configurados 