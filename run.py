#!/usr/bin/env python3
"""
Docker MCP Server runner
"""
import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importar e executar
from docker_mcp import main

if __name__ == "__main__":
    main()