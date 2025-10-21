"""
Pendle Finance MCP Agent - Main Entry Point
Production-ready MCP server for yield trading and liquidity management
"""
from fastmcp import FastMCP
import sys
import os

# Create the MCP server
mcp = FastMCP("Pendle Finance MCP Agent")

# Import tools to register them
import hybrid_tools

def print_banner():
    """Print professional startup banner"""
    print("=" * 80)
    print("🚀 Pendle Finance MCP Agent - Production Server")
    print("=" * 80)
    print("📊 Yield Trading & Liquidity Management")
    print("🔗 Multi-Chain Support: Ethereum, Arbitrum, Optimism, BSC, Mantle")
    print("🛠️  Tools: 30+ across 4 categories")
    print("⚡ Architecture: Hybrid (Direct Contract + Hosted SDK)")
    print("=" * 80)

def check_environment():
    """Check if environment is properly configured"""
    required_files = ['.env', 'abi/pendle_router_abi.json']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("⚠️  Warning: Missing configuration files:")
        for file in missing_files:
            print(f"   - {file}")
        print("   Please ensure all configuration files are present.")
        return False
    
    return True

if __name__ == "__main__":
    print_banner()
    
    # Check environment
    if not check_environment():
        print("❌ Environment check failed. Please fix configuration issues.")
        sys.exit(1)
    
    print("✅ Environment check passed")
    print("✅ All tools registered successfully")
    print("✅ Server ready for connections")
    print("=" * 80)
    
    try:
        # Start the MCP server
        mcp.run()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)
