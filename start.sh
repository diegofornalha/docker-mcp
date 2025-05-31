#!/bin/bash
# Start Docker MCP Server

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Instalar dependências se necessário
if ! python -c "import mcp" 2>/dev/null; then
    echo "Instalando dependências..."
    pip install mcp httpx python-dotenv python-on-whales pyyaml
fi

# Executar o servidor
cd /Users/agents/.claude/docker-mcp
export PYTHONPATH="${PYTHONPATH}:./src"
python -m docker_mcp.server