# Docker MCP Server

Servidor MCP (Model Context Protocol) para gerenciar containers Docker através do Claude.

## Instalação

1. Execute o script de configuração:
```bash
./setup.sh
```

2. Adicione ao arquivo `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "docker": {
      "command": "/Users/agents/.claude/docker-mcp/start.sh"
    }
  }
}
```

3. Reinicie o Claude Desktop

## Ferramentas Disponíveis

### 1. `create-container`
Cria e executa um container Docker simples.

Parâmetros:
- `image`: Imagem Docker (obrigatório)
- `name`: Nome do container
- `ports`: Mapeamento de portas (ex: {"80": "8080"})
- `environment`: Variáveis de ambiente

### 2. `deploy-compose`
Deploy de um stack Docker Compose.

Parâmetros:
- `compose_yaml`: Conteúdo do arquivo docker-compose.yml
- `project_name`: Nome do projeto

### 3. `list-containers`
Lista todos os containers Docker (rodando e parados).

### 4. `get-logs`
Obtém logs de um container específico.

Parâmetros:
- `container_name`: Nome do container

## Exemplos de Uso

### Criar um container Nginx:
```
Crie um container nginx na porta 8080
```

### Deploy de uma aplicação com Docker Compose:
```
Faça deploy de uma aplicação WordPress com MySQL
```

### Ver logs de um container:
```
Mostre os logs do container nginx
```

## Requisitos

- Python 3.12+
- Docker Desktop instalado e rodando
- macOS (testado) ou Linux

## Solução de Problemas

Se o servidor não iniciar:
1. Verifique se o Docker está rodando: `docker info`
2. Verifique os logs em: `~/Library/Logs/Claude/mcp*.log`
3. Execute manualmente: `./start.sh` para ver erros

## Estrutura

```
docker-mcp/
├── src/
│   └── docker_mcp/
│       ├── __init__.py
│       ├── server.py          # Servidor MCP principal
│       ├── handlers.py        # Handlers das ferramentas
│       └── docker_executor.py # Executor de comandos Docker
├── pyproject.toml
├── start.sh                   # Script de inicialização
├── setup.sh                   # Script de instalação
└── README.md
```