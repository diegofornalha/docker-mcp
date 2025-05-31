# Docker MCP 🐳

> Gerencie containers Docker diretamente através do Claude usando o Model Context Protocol (MCP)

[![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.12+-green.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)

## ✨ O que é?

Docker MCP é um servidor MCP que permite ao Claude Code gerenciar todo o seu ambiente Docker através de comandos naturais. Esqueça comandos complexos - simplesmente diga ao Claude o que você quer fazer!

## 🚀 Funcionalidades (v0.3.0)

### Gerenciamento Completo de Containers
- ✅ Criar, listar, parar, iniciar e remover containers
- ✅ Visualizar logs e estatísticas em tempo real
- ✅ Monitorar uso de CPU, memória, rede e I/O

### Gerenciamento de Imagens
- ✅ Listar imagens locais
- ✅ Baixar novas imagens do Docker Hub
- ✅ Remover imagens não utilizadas

### Gerenciamento de Volumes
- ✅ Listar e remover volumes
- ✅ Filtrar volumes órfãos

### Docker Compose Aprimorado
- ✅ Deploy usando YAML inline ou arquivos locais
- ✅ Parar e remover stacks completas
- ✅ Opções para limpar volumes e imagens

## 📦 Instalação Rápida

```bash
# 1. Clone ou navegue até o diretório
cd /Users/agents/.claude/docker-mcp

# 2. Execute o setup
./setup.sh

# 3. Adicione ao Claude Code
claude mcp add docker-mcp -s user -- python3 /Users/agents/.claude/docker-mcp/run.py

# 4. Verifique
claude mcp list | grep docker-mcp
```

## 💬 Exemplos de Uso

### Criar um servidor web
```
"Crie um container nginx chamado meu-site na porta 8080"
```

### Monitorar recursos
```
"Mostre as estatísticas de CPU e memória do container database"
```

### Deploy com Docker Compose
```
"Faça deploy do arquivo docker-compose.yml em /Users/agents/projeto"
```

### Gerenciar imagens e volumes
```
"Liste todas as imagens Docker e remova as não utilizadas"
"Mostre todos os volumes e remova os órfãos"
```

### Parar e limpar stacks
```
"Pare o stack myapp e remova todos os volumes e imagens"
```

## 🛠️ Todas as Ferramentas Disponíveis

| Ferramenta | Descrição | Novo |
|------------|-----------|------|
| **create-container** | Cria e executa containers Docker | |
| **list-containers** | Lista containers com informações detalhadas | ✨ |
| **stop-container** | Para containers em execução | ✅ |
| **start-container** | Inicia containers parados | ✅ |
| **remove-container** | Remove containers (com opção force) | ✅ |
| **get-logs** | Obtém logs de containers | |
| **get-container-stats** | Mostra estatísticas de recursos em tempo real | ✅ |
| **list-images** | Lista todas as imagens Docker locais | ✅ |
| **pull-image** | Baixa imagens do Docker Hub | ✅ |
| **remove-image** | Remove imagens não utilizadas | ✅ |
| **list-volumes** | Lista todos os volumes Docker | ✅ |
| **remove-volume** | Remove volumes Docker | ✅ |
| **deploy-compose** | Deploy com Docker Compose (suporta arquivos locais) | ✨ |
| **compose-down** | Para e remove stacks Docker Compose | ✅ |

## 📋 Exemplos Detalhados

### 1. Ciclo de vida completo de um container
```bash
# Criar
"Crie um container postgres chamado db-prod com senha segura"

# Monitorar
"Mostre as estatísticas do container db-prod"

# Gerenciar
"Pare o container db-prod"
"Inicie o container db-prod"

# Limpar
"Remova o container db-prod"
```

### 2. Deploy de aplicação completa
```bash
# Deploy com arquivo local
"Faça deploy do docker-compose.yml em /Users/agents/myapp"

# Deploy com YAML inline
"Crie um stack WordPress com MySQL e Redis, use volumes persistentes"

# Parar e limpar
"Pare o stack myapp e remova volumes e imagens"
```

## 📚 Documentação

- [Documentação Completa](DOCKER-MCP-DOCS.md) - Guia detalhado com todos os recursos
- [Changelog](CHANGELOG.md) - Histórico de mudanças e novidades
- [Resumo das Melhorias](IMPROVEMENTS_SUMMARY.md) - O que foi adicionado na v0.3.0

## 🔧 Requisitos

- Python 3.12+
- Docker Desktop instalado e rodando
- Claude Code CLI
- macOS, Linux ou Windows (com Docker Desktop)

## 🏗️ Estrutura do Projeto

```
docker-mcp/
├── src/
│   └── docker_mcp/
│       ├── __init__.py
│       ├── server.py          # Servidor MCP (14 ferramentas)
│       ├── handlers.py        # Implementação das ferramentas
│       └── docker_executor.py # Executor Docker Compose
├── run.py                     # Script principal
├── setup.sh                   # Instalação automática
├── CHANGELOG.md              # Histórico de versões
├── DOCKER-MCP-DOCS.md        # Documentação completa
└── README.md                 # Este arquivo
```

## 🔧 Solução de Problemas

### Docker não encontrado
```bash
# macOS
brew install --cask docker

# Linux
curl -fsSL https://get.docker.com | sh
```

### Verificar se está rodando
```bash
ps aux | grep docker-mcp
claude mcp list | grep docker-mcp
```

### Ver logs
```bash
tail -f ~/Library/Logs/Claude/mcp-docker-mcp.log
```

## 🚀 Roadmap

### v0.4.0 (Em breve)
- [ ] container-exec - Executar comandos em containers
- [ ] image-build - Construir imagens de Dockerfile
- [ ] container-inspect - Informações detalhadas

### v0.5.0
- [ ] Gerenciamento de redes Docker
- [ ] Suporte para registries privados
- [ ] Healthchecks automáticos

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja o guia de desenvolvimento na [documentação completa](DOCKER-MCP-DOCS.md#desenvolvimento).

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

Encontrou um problema? Precisa de ajuda?

1. Consulte a [documentação completa](DOCKER-MCP-DOCS.md)
2. Verifique o [troubleshooting](DOCKER-MCP-DOCS.md#troubleshooting)
3. Use o comando: `"Liste containers e mostre logs de erros"`

---

Feito com ❤️ por Diego via Claude

**Versão**: 0.3.0 | **Última atualização**: 30/01/2025