#!/usr/bin/env python3
"""Test MCP server initialization"""
import json
import subprocess
import sys

# Test initialization request
init_request = {
    "jsonrpc": "2.0",
    "method": "initialize",
    "params": {
        "protocolVersion": "0.1.0",
        "capabilities": {}
    },
    "id": 1
}

# Start the server
proc = subprocess.Popen(
    [sys.executable, "/Users/agents/.claude/docker-mcp/run_mcp.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

try:
    # Send initialization request
    proc.stdin.write(json.dumps(init_request) + "\n")
    proc.stdin.flush()
    
    # Read response
    response = proc.stdout.readline()
    print("Response:", response)
    
    if response:
        data = json.loads(response)
        print("Parsed:", json.dumps(data, indent=2))
    else:
        print("No response received")
        stderr = proc.stderr.read()
        if stderr:
            print("Stderr:", stderr)
            
except Exception as e:
    print(f"Error: {e}")
finally:
    proc.terminate()