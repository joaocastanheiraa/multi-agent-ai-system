# 🔧 MCP MARKETPLACE - Solução de Problemas

## ❌ Problemas Comuns e Soluções

### 1. `ModuleNotFoundError: No module named 'config'`

**Problema:** Python não consegue encontrar o módulo `config`.

**Soluções:**

#### Opção A: Usar o launcher fornecido
```bash
# Use o launcher que resolve automaticamente os imports
python3 run_mcp_ui.py
```

#### Opção B: Executar do diretório correto
```bash
# Certifique-se de estar na raiz do projeto
cd /caminho/para/multi-agent-ai-system
python3 -c "from config import MCPMarketplace; print('✅ Funcionando!')"
```

#### Opção C: Adicionar ao PYTHONPATH
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python3 config/mcp_marketplace_ui.py
```

### 2. `ModuleNotFoundError: No module named 'autogen_ext'`

**Problema:** AutoGen MCP extension não está instalada.

**Solução:**
```bash
# Instalar AutoGen MCP
pip install -U 'autogen-ext[mcp]'

# Ou instalar versão completa
pip install -U 'autogen-ext[all]'
```

### 3. `ModuleNotFoundError: No module named 'autogen_agentchat'`

**Problema:** AutoGen core não está instalado.

**Solução:**
```bash
# Instalar AutoGen core
pip install -U 'autogen-agentchat'

# Verificar versão
python3 -c "import autogen_agentchat; print(autogen_agentchat.__version__)"
```

### 4. `ModuleNotFoundError: No module named 'streamlit'`

**Problema:** Streamlit não está instalado.

**Solução:**
```bash
# Instalar Streamlit
pip install streamlit

# Verificar instalação
streamlit --version
```

### 5. Interface Streamlit não abre

**Problema:** Erro ao executar a interface web.

**Soluções:**

#### Opção A: Usar launcher personalizado
```bash
python3 run_mcp_ui.py
```

#### Opção B: Executar diretamente
```bash
streamlit run config/mcp_marketplace_ui.py
```

#### Opção C: Verificar porta
```bash
# Se porta 8501 estiver ocupada
streamlit run config/mcp_marketplace_ui.py --server.port 8502
```

## 🧪 Diagnóstico Automático

### Executar Teste Completo
```bash
# Testar todos os imports e dependências
python3 test_mcp_imports.py

# Ou via launcher
./launch_mcp_marketplace.sh
# Escolher opção 8: Testar Imports e Dependências
```

### Verificar Estrutura de Arquivos
```bash
# Verificar se todos os arquivos estão presentes
ls -la config/
ls -la examples/mcp_integration/
ls -la scripts/
```

## 📦 Instalação Completa de Dependências

### Dependências Mínimas
```bash
# Core do MCP Marketplace (funciona sem AutoGen)
pip install streamlit pandas
```

### Dependências Completas
```bash
# Funcionalidade completa com AutoGen MCP
pip install streamlit pandas
pip install -U 'autogen-ext[mcp]'
pip install -U 'autogen-agentchat'
```

### Dependências Opcionais
```bash
# Para servidores MCP específicos
pip install mcp-server-fetch
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @playwright/mcp@latest
```

## 🐳 Usando Docker (Alternativa)

Se você tem problemas persistentes com Python, use Docker:

```bash
# Criar Dockerfile simples
cat > Dockerfile << EOF
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install streamlit pandas
RUN pip install -U 'autogen-ext[mcp]' 'autogen-agentchat'

EXPOSE 8501

CMD ["streamlit", "run", "config/mcp_marketplace_ui.py", "--server.address", "0.0.0.0"]
EOF

# Build e run
docker build -t mcp-marketplace .
docker run -p 8501:8501 mcp-marketplace
```

## 🔍 Verificações Passo a Passo

### 1. Verificar Python
```bash
python3 --version
# Deve ser Python 3.8+
```

### 2. Verificar Estrutura
```bash
find . -name "*.py" | grep -E "(mcp_marketplace|test_mcp)" | head -5
# Deve mostrar os arquivos criados
```

### 3. Verificar Imports Básicos
```bash
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from config import MCPMarketplace
    print('✅ Config OK')
except Exception as e:
    print(f'❌ Config Error: {e}')
"
```

### 4. Verificar Streamlit
```bash
python3 -c "
import streamlit
import pandas
print('✅ UI Dependencies OK')
"
```

## 🚑 Modo de Recuperação

Se nada funcionar, use o modo básico:

### 1. Marketplace Básico (Sem AutoGen)
```python
# Criar versão mínima para testar
import json

# Dados básicos do marketplace
marketplace_data = {
    "servers": [
        {"id": "fetch_official", "name": "Fetch MCP", "category": "Web"},
        {"id": "filesystem_official", "name": "Filesystem MCP", "category": "System"}
    ]
}

print("🛒 Marketplace Básico Funcionando!")
print(f"Servidores: {len(marketplace_data['servers'])}")
```

### 2. Interface Mínima
```python
# Criar interface mínima com Streamlit
import streamlit as st

st.title("🛒 MCP Marketplace (Modo Básico)")
st.write("Interface funcionando sem AutoGen")

servers = ["Fetch MCP", "Filesystem MCP", "GitHub MCP"]
selected = st.multiselect("Selecione servidores:", servers)
st.write(f"Selecionados: {selected}")
```

## 📞 Suporte

### Comandos de Diagnóstico Úteis
```bash
# Informações do sistema
python3 --version
pip list | grep -E "(autogen|streamlit|pandas)"
which python3
echo $PYTHONPATH

# Testar imports individualmente
python3 -c "import config; print('Config OK')"
python3 -c "import streamlit; print('Streamlit OK')"
python3 -c "import pandas; print('Pandas OK')"
```

### Logs e Debug
```bash
# Executar com logs detalhados
PYTHONPATH=. python3 -v config/mcp_marketplace_ui.py 2>&1 | head -20

# Debug do Streamlit
streamlit run config/mcp_marketplace_ui.py --logger.level=debug
```

## ✅ Verificação Final

Após resolver os problemas, execute:

```bash
# Teste completo
python3 test_mcp_imports.py

# Se tudo estiver OK, launch normal
./launch_mcp_marketplace.sh
```

---

💡 **Dica:** Comece sempre com o teste de imports (`python3 test_mcp_imports.py`) para identificar rapidamente o problema. 