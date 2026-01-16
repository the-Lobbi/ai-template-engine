"""MCP Tool Registry for accessing MCP servers.

This module provides integration with MCP (Model Context Protocol) servers
to access tools like Scaffold, Repomix, Harness, and GitHub APIs.
"""

import os
from typing import Any

from langchain_mcp_adapters.client import create_mcp_client_stdio


def get_mcp_tools(server_names: list[str]) -> list[Any]:
    """Get tools from specified MCP servers.

    Args:
        server_names: List of MCP server names to load tools from.
                     Supported: 'scaffold', 'repomix', 'harness', 'github'

    Returns:
        List of LangChain tools from the specified MCP servers

    Raises:
        ValueError: If an unsupported server name is provided
        RuntimeError: If MCP server connection fails
    """
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
            # Create MCP client for this server
            client = create_mcp_client_stdio(
                command=config["command"],
                args=config["args"],
                env=config.get("env", {}),
            )

            # Get tools from this server
            server_tools = client.get_tools()
            tools.extend(server_tools)

        except Exception as e:
            raise RuntimeError(
                f"Failed to connect to MCP server '{server_name}': {str(e)}"
            ) from e

    return tools


def get_all_mcp_tools() -> list[Any]:
    """Get tools from all available MCP servers.

    Returns:
        List of all available LangChain tools from all MCP servers
    """
    return get_mcp_tools(["scaffold", "repomix", "harness", "github"])
