"""Week 4: expose Helios tools over MCP 2026-07-28 style JSON-RPC.

You do not need a full SDK. Implement a tiny stdio or HTTP handler that understands:

- tools/list  → { tools: [ { name, description, inputSchema } ] }
- tools/call  → { name, arguments } → { content: [ { type: "text", text: json } ] }

Read:
https://modelcontextprotocol.io/specification/2026-07-28/server/tools
https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture
"""

from __future__ import annotations

import json
from typing import Any

from react_eval_lab.tools import TOOL_SCHEMAS, execute_tool


def list_tools() -> dict[str, Any]:
    tools = []
    for schema in TOOL_SCHEMAS:
        fn = schema["function"]
        tools.append(
            {
                "name": fn["name"],
                "description": fn["description"],
                "inputSchema": fn["parameters"],
            }
        )
    return {"tools": tools}


def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    result = execute_tool(name, arguments)
    return {"content": [{"type": "text", "text": json.dumps(result)}], "isError": "error" in result}


def handle_rpc(request: dict[str, Any]) -> dict[str, Any]:
    """Implement JSON-RPC 2.0 dispatch for tools/list and tools/call.

    Expected request shape:
      {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
      {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "search", "arguments": {"query": "aurora"}}}
    """
    raise NotImplementedError("implement handle_rpc in src/react_eval_lab/mcp_server.py")
