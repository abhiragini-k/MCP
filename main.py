from fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("Pendle Finance MCP Agent")

# Import tools to register them
import hybrid_tools

if __name__ == "__main__":
    print("🚀 Starting Pendle Finance MCP Agent...")
    print("📊 Supports yield trading, liquidity management, and tokenized yield")
    print("🔗 Works with Ethereum, Arbitrum, Optimism, BSC, and Mantle")
    print("=" * 60)
    
    # Start the MCP server
    mcp.run()
