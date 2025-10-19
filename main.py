from fastmcp import FastMCP
import asyncio

# Create the MCP server
mcp = FastMCP("Pendle Finance Hybrid MCP Agent")

# Import tools to register them
import hybrid_tools

if __name__ == "__main__":
    # Start the MCP server
    mcp.run()
