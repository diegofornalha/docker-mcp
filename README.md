# Docker MCP 🐳

> Gerencie containers Docker diretamente através do Claude usando o Model Context Protocol (MCP)

## ✅ Instalação Correta

### Comando que FUNCIONA:
```bash
# 1. Navegue até o diretório
cd /root/.claude/docker-mcp

# 2. Execute o setup (se ainda não fez)
./setup.sh

# 3. Adicione ao Claude (USE ESTE COMANDO EXATO!)
claude mcp add docker-mcp -s user -- \
  /root/.claude/docker-mcp/venv/bin/python3 \
  /root/.claude/docker-mcp/docker_mcp_server.py

# 4. Verifique
mcp
```

### ⚠️ IMPORTANTE:
- **USE SEMPRE** o script `docker_mcp_server.py`
- **USE SEMPRE** o Python do venv: `/root/.claude/docker-mcp/venv/bin/python3`
- **NÃO USE** outros scripts run.py ou wrappers

## 🚀 Ferramentas Disponíveis (14 total)

- create-container
- list-containers
- stop-container
- start-container
- remove-container
- get-logs
- get-container-stats
- list-images
- pull-image
- remove-image
- list-volumes
- remove-volume
- deploy-compose
- compose-down

## 🔧 Solução de Problemas

### Se aparecer "docker-mcp: failed":
Veja o arquivo **`SOLUCAO_DEFINITIVA_DOCKER_MCP.md`**

### Para reinstalar:
```bash
claude mcp remove docker-mcp -s user
claude mcp add docker-mcp -s user -- /root/.claude/docker-mcp/venv/bin/python3 /root/.claude/docker-mcp/docker_mcp_server.py
```

## 📁 Arquivos Importantes

- `docker_mcp_server.py` - Script principal (USE ESTE!)
- `setup.sh` - Instalador de dependências
- `SOLUCAO_DEFINITIVA_DOCKER_MCP.md` - Solução para erros
- `src/` - Código fonte do servidor MCP

---
Versão: 0.3.0 | Status: ✅ Funcionando