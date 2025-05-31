# Docker MCP - Changelog

## [0.2.0] - 2025-01-30

### 🎉 Novas Funcionalidades

#### Gerenciamento de Containers
- **stop-container**: Para containers em execução
- **start-container**: Inicia containers parados
- **remove-container**: Remove containers (com opção force)

#### Gerenciamento de Imagens
- **list-images**: Lista todas as imagens Docker locais
- **pull-image**: Baixa ou atualiza imagens do Docker Hub
- **remove-image**: Remove imagens não utilizadas

### 🔧 Melhorias
- **list-containers**: Agora mostra informações detalhadas
  - Portas mapeadas
  - Status detalhado (Up X hours, Exited (0))
  - Formato mais legível
  - Filtro opcional para mostrar apenas containers rodando

### 📚 Documentação
- Criada documentação completa em português
- Adicionados exemplos práticos
- FAQ com problemas comuns
- Guia de início rápido

## [0.1.0] - 2025-01-29

### 🎉 Versão Inicial

#### Funcionalidades Básicas
- **create-container**: Cria containers simples
- **deploy-compose**: Deploy com Docker Compose
- **list-containers**: Lista containers (básico)
- **get-logs**: Obtém logs de containers

#### Infraestrutura
- Suporte para macOS, Linux e Windows
- Integração com Claude Code via MCP
- Operações assíncronas
- Tratamento de erros

---

## Roadmap Futuro

### [0.3.0] - Planejado
- **list-volumes**: Gerenciamento de volumes
- **remove-volume**: Limpeza de volumes
- **compose-down**: Parar stacks Docker Compose
- Suporte para docker-compose.yml local

### [0.4.0] - Planejado
- **get-container-stats**: Estatísticas de recursos
- **container-exec**: Executar comandos em containers
- **image-build**: Construir imagens a partir de Dockerfile

### [1.0.0] - Planejado
- Suporte para Docker Swarm
- Integração com Docker Hub
- Suporte para Docker remoto (DOCKER_HOST)
- Interface web opcional