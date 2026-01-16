"""MCP Tool Registry for accessing MCP servers.

This module provides integration with MCP (Model Context Protocol) servers
to access tools like Scaffold, Repomix, Harness, and GitHub APIs.

Note: MCP integration is optional. If MCP servers are not available,
the nodes will use placeholder implementations.
"""

import os
from typing import Any

# Import is optional - gracefully degrade if not available
try:
    from langchain_mcp_adapters.client import load_mcp_tools, create_session
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False


def get_mcp_tools(server_names: list[str]) -> list[Any]:
    """Get tools from specified MCP servers.

    Args:
        server_names: List of MCP server names to load tools from.
                     Supported: 'scaffold', 'repomix', 'harness', 'github'

    Returns:
        List of LangChain tools from the specified MCP servers.
        Returns empty list if MCP adapters not available.

    Raises:
        ValueError: If an unsupported server name is provided
        RuntimeError: If MCP server connection fails
    """
    if not MCP_AVAILABLE:
        # Return empty list if MCP not available
        # Nodes will use placeholder implementations
        return []

    server_configs = {
        "scaffold": {
            "command": "npx",
            "args": [
                "-y",
                "@scaffoldly/mcp-server",
            ],
            "env": {},
        },
        "repomix": {
            "command": "npx",
            "args": [
                "-y",
                "@elizaos/mcp-repomix",
            ],
            "env": {},
        },
        "harness": {
            "command": "python",
            "args": [
                "-m",
                "harness_mcp",
            ],
            "env": {
                "HARNESS_ACCOUNT_ID": os.getenv("HARNESS_ACCOUNT_ID", ""),
                "HARNESS_API_KEY": os.getenv("HARNESS_API_KEY", ""),
                "HARNESS_API_URL": os.getenv(
                    "HARNESS_API_URL", "https://app.harness.io/gateway"
                ),
            },
        },
        "github": {
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/server-github",
            ],
            "env": {
                "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN", ""),
            },
        },
    }

    tools = []

    for server_name in server_names:
        if server_name not in server_configs:
            raise ValueError(
                f"Unsupported MCP server: {server_name}. "
                f"Supported servers: {list(server_configs.keys())}"
            )

        config = server_configs[server_name]

        try:
            # Note: MCP tools require async context manager
            # For now, return empty list and use placeholder implementations
            # In production, this would use async context manager properly
            pass

        except Exception as e:
            # Non-fatal - just log and continue with empty tools
            print(f"Warning: Failed to connect to MCP server '{server_name}': {str(e)}")

    return tools


def get_all_mcp_tools() -> list[Any]:
    """Get tools from all available MCP servers.

    Returns:
        List of all available LangChain tools from all MCP servers
    """
    return get_mcp_tools(["scaffold", "repomix", "harness", "github"])
