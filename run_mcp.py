#!/usr/bin/env python3
"""
Docker MCP Server runner with proper virtual environment activation
"""
import sys
import os
import subprocess

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to virtual environment's python
venv_python = os.path.join(script_dir, 'venv', 'bin', 'python3')

# Check if venv exists
if not os.path.exists(venv_python):
    print("Error: Virtual environment not found. Run setup.sh first.", file=sys.stderr)
    sys.exit(1)

# Add src to Python path for the subprocess
env = os.environ.copy()
env['PYTHONPATH'] = os.path.join(script_dir, 'src')

# Execute the server using venv python
try:
    subprocess.run(
        [venv_python, '-m', 'docker_mcp.server'],
        env=env,
        cwd=script_dir
    )
except KeyboardInterrupt:
    print("\nShutting down gracefully...")
    sys.exit(0)
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)