#!/bin/bash
# Setup Docker MCP Server (Método Legado - Python Local)

echo "🐳 Configurando Docker MCP Server (Método Legado)..."
echo "⚠️  NOTA: Considere usar o método Docker com ./setup.sh"

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
pip install -r requirements.txt

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker não está instalado. Instale o Docker primeiro."
    exit 1
fi

# Verificar se Docker está rodando
if ! docker info &> /dev/null; then
    echo "⚠️  Docker não está em execução. Inicie o Docker."
    exit 1
fi

echo "✅ Docker MCP configurado com sucesso (método legado)!"
echo ""
echo "Para adicionar ao Claude:"
echo "  claude mcp add docker-mcp -s user -- $PWD/venv/bin/python3 $PWD/docker_mcp_server.py"