from fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("Pendle Finance MCP Agent")

# Import tools to register them
import tools

if __name__ == "__main__":
    # Start the MCP server
    mcp.run()
