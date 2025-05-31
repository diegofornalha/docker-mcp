#!/bin/bash
# Setup Docker MCP Server

echo "🐳 Configurando Docker MCP Server..."

# Criar ambiente virtual
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
echo "Instalando dependências..."
pip install --upgrade pip
pip install httpx mcp python-dotenv python-on-whales pyyaml

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker não está instalado. Instale o Docker Desktop primeiro."
    exit 1
fi

# Verificar se Docker está rodando
if ! docker info &> /dev/null; then
    echo "⚠️  Docker não está em execução. Inicie o Docker Desktop."
    exit 1
fi

echo "✅ Docker MCP configurado com sucesso!"
echo ""
echo "Para iniciar o servidor:"
echo "  ./start.sh"
echo ""
echo "Para adicionar ao Claude, adicione isto ao seu claude_desktop_config.json:"
echo '{
  "docker": {
    "command": "/root/.claude/docker-mcp/start.sh"
  }
}'