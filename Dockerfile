FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y     git     curl     && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY mcp_integration/requirements_mcp.txt requirements_mcp.txt
COPY requirements.txt requirements.txt

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements_mcp.txt
RUN pip install --no-cache-dir -r requirements.txt || echo "Main requirements optional"

# Copiar código
COPY . .

# Expor porta
EXPOSE 8001

# Comando padrão
CMD ["python", "mcp_integration/mcp_server.py"]
