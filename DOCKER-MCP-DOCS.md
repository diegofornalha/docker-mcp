# Docker MCP - Documentação Completa

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Instalação](#instalação)
3. [Configuração](#configuração)
4. [Ferramentas Disponíveis](#ferramentas-disponíveis)
5. [Exemplos de Uso](#exemplos-de-uso)
6. [Arquitetura](#arquitetura)
7. [Troubleshooting](#troubleshooting)
8. [Desenvolvimento](#desenvolvimento)

## 🔍 Visão Geral

O Docker MCP é um servidor Model Context Protocol que permite ao Claude interagir com Docker e Docker Compose diretamente. Com ele, você pode:

- Criar e gerenciar containers Docker
- Deploy de aplicações usando Docker Compose
- Visualizar logs de containers
- Listar containers em execução

### Características

- ✅ Suporte completo ao Docker e Docker Compose
- ✅ Compatível com macOS, Linux e Windows
- ✅ Integração nativa com Claude Code
- ✅ Operações assíncronas para melhor performance
- ✅ Tratamento de erros robusto

## 📦 Instalação

### Pré-requisitos

- Python 3.12 ou superior
- Docker Desktop instalado e em execução
- Claude Code CLI (`claude`)

### Instalação Rápida

1. **Configure o ambiente**:
```bash
cd /Users/agents/.claude/docker-mcp
./setup.sh
```

2. **Adicione ao Claude Code**:
```bash
claude mcp add docker-mcp -s user -- python3 /Users/agents/.claude/docker-mcp/run.py
```

3. **Verifique a instalação**:
```bash
claude mcp list | grep docker-mcp
```

### Instalação Manual

Se preferir instalar manualmente:

```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install httpx mcp python-dotenv python-on-whales pyyaml

# Adicionar ao Claude
claude mcp add docker-mcp -s user -- python3 /Users/agents/.claude/docker-mcp/run.py
```

## ⚙️ Configuração

### Estrutura de Arquivos

```
docker-mcp/
├── src/
│   └── docker_mcp/
│       ├── __init__.py         # Ponto de entrada do módulo
│       ├── server.py           # Servidor MCP principal
│       ├── handlers.py         # Handlers das ferramentas
│       └── docker_executor.py  # Executor de comandos Docker
├── pyproject.toml              # Configuração do projeto
├── run.py                      # Script runner principal
├── start.sh                    # Script de inicialização
├── setup.sh                    # Script de instalação
└── DOCKER-MCP-DOCS.md         # Esta documentação
```

### Variáveis de Ambiente

Você pode configurar o comportamento através de variáveis de ambiente:

```bash
# Timeout padrão para comandos Docker (em segundos)
export DOCKER_COMMAND_TIMEOUT=300

# Caminho customizado para o Docker (se não estiver no PATH)
export DOCKER_PATH=/usr/local/bin/docker
```

## 🛠️ Ferramentas Disponíveis

### 1. create-container

Cria e executa um container Docker simples.

**Parâmetros**:
- `image` (obrigatório): Imagem Docker a usar
- `name`: Nome do container
- `ports`: Mapeamento de portas (objeto)
- `environment`: Variáveis de ambiente (objeto)

**Exemplo de uso no Claude**:
```
Crie um container nginx chamado "web-server" na porta 8080
```

**Parâmetros JSON equivalentes**:
```json
{
  "image": "nginx:latest",
  "name": "web-server",
  "ports": {
    "80": "8080"
  }
}
```

### 2. deploy-compose

Faz deploy de um stack completo usando Docker Compose.

**Parâmetros**:
- `compose_yaml` (obrigatório): Conteúdo do arquivo docker-compose.yml
- `project_name` (obrigatório): Nome do projeto

**Exemplo de uso no Claude**:
```
Faça deploy de uma aplicação WordPress com MySQL usando Docker Compose
```

### 3. list-containers

Lista todos os containers Docker (rodando e parados).

**Parâmetros**: Nenhum

**Exemplo de uso no Claude**:
```
Liste todos os containers Docker
```

**Resposta típica**:
```json
[
  {
    "id": "abc123...",
    "name": "web-server",
    "image": "nginx:latest",
    "status": "running",
    "ports": "0.0.0.0:8080->80/tcp"
  }
]
```

### 4. get-logs

Obtém os logs mais recentes de um container específico.

**Parâmetros**:
- `container_name` (obrigatório): Nome do container

**Exemplo de uso no Claude**:
```
Mostre os logs do container web-server
```

## 📚 Exemplos de Uso

### Exemplo 1: Deploy de Aplicação Web Simples

**Comando para Claude**:
```
Crie um container nginx servindo uma página estática na porta 3000
```

**O que acontece**:
1. Claude usa `create-container` com nginx
2. Mapeia porta 80 do container para 3000 do host
3. Container é criado e iniciado

### Exemplo 2: Stack WordPress Completo

**Comando para Claude**:
```
Faça deploy de um WordPress com banco de dados MySQL, 
configure senhas seguras e exponha na porta 8080
```

**O que acontece**:
1. Claude gera um docker-compose.yml
2. Configura WordPress e MySQL com senhas
3. Usa `deploy-compose` para fazer o deploy
4. Stack completo rodando em minutos

### Exemplo 3: Debugging de Container

**Comando para Claude**:
```
Meu container "api-server" está com erro. 
Mostre os logs e me ajude a debugar
```

**O que acontece**:
1. Claude usa `get-logs` para obter logs
2. Analisa os erros encontrados
3. Sugere soluções baseadas nos logs

### Exemplo 4: Gerenciamento de Múltiplos Containers

**Comando para Claude**:
```
Liste todos os containers e pare os que não estão sendo usados
```

**O que acontece**:
1. Claude usa `list-containers`
2. Identifica containers inativos
3. Sugere quais podem ser removidos

## 🏗️ Arquitetura

### Fluxo de Comunicação

```
Claude → MCP Protocol → docker-mcp → Docker Engine
                              ↓
                        docker_executor.py
                              ↓
                     Docker CLI/Docker Compose
```

### Componentes Principais

#### server.py
- Implementa o protocolo MCP
- Define as ferramentas disponíveis
- Gerencia a comunicação com Claude

#### handlers.py
- Contém a lógica de cada ferramenta
- Valida parâmetros
- Formata respostas

#### docker_executor.py
- Abstrai diferenças entre plataformas
- Executa comandos Docker de forma segura
- Gerencia timeouts e erros

### Segurança

- Validação de todos os parâmetros de entrada
- Sanitização de comandos Docker
- Timeouts para prevenir travamentos
- Logs detalhados para auditoria

## 🔧 Troubleshooting

### Problema: "Docker não encontrado"

**Solução**:
1. Verifique se Docker está instalado: `docker --version`
2. Certifique-se que Docker Desktop está rodando
3. Se necessário, configure o PATH:
   ```bash
   export DOCKER_PATH=/usr/local/bin/docker
   ```

### Problema: "Permissão negada"

**Solução**:
1. No Linux, adicione seu usuário ao grupo docker:
   ```bash
   sudo usermod -aG docker $USER
   ```
2. Faça logout e login novamente

### Problema: "Container não inicia"

**Diagnóstico**:
```
Use o comando "mostre os logs do container [nome]" no Claude
```

### Logs do MCP

Para debug avançado, verifique os logs:
```bash
# Logs do Claude
tail -f ~/Library/Logs/Claude/mcp-docker-mcp.log

# Executar servidor manualmente para ver erros
python3 /Users/agents/.claude/docker-mcp/run.py
```

## 👨‍💻 Desenvolvimento

### Adicionando Novas Ferramentas

1. **Defina a ferramenta em server.py**:
```python
types.Tool(
    name="nova-ferramenta",
    description="Descrição da ferramenta",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {"type": "string"}
        },
        "required": ["param1"]
    }
)
```

2. **Implemente o handler em handlers.py**:
```python
@staticmethod
async def handle_nova_ferramenta(arguments: Dict[str, Any]) -> List[types.TextContent]:
    # Implementação aqui
    return [types.TextContent(type="text", text="Resultado")]
```

3. **Adicione ao switch em server.py**:
```python
elif name == "nova-ferramenta":
    return await DockerHandlers.handle_nova_ferramenta(arguments)
```

### Testando Localmente

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar servidor em modo debug
python3 run.py

# Em outro terminal, envie comandos MCP de teste
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python3 run.py
```

### Contribuindo

1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit suas mudanças: `git commit -am 'Add nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📝 Notas Adicionais

### Performance

- Operações assíncronas para não bloquear Claude
- Timeouts configuráveis para comandos longos
- Cache de resultados quando apropriado

### Compatibilidade

- **macOS**: Totalmente compatível
- **Linux**: Totalmente compatível
- **Windows**: Compatível com Docker Desktop
- **WSL2**: Recomendado para Windows

### Limitações Conhecidas

1. Não suporta Docker Swarm (apenas Docker e Compose)
2. Limite de 100 linhas de logs por vez
3. Não manipula imagens Docker diretamente (use CLI)

### Roadmap

- [ ] Suporte para Docker Swarm
- [ ] Gerenciamento de imagens
- [ ] Métricas de containers
- [ ] Integração com Docker Hub
- [ ] Suporte para Kubernetes

## 🆘 Suporte

Para problemas ou dúvidas:

1. Verifique esta documentação
2. Consulte os logs em `~/Library/Logs/Claude/`
3. Execute o servidor manualmente para debug
4. Abra uma issue no repositório

---

**Versão**: 0.1.0  
**Última atualização**: Janeiro 2025  
**Autor**: Diego (via Claude)  
**Licença**: MIT