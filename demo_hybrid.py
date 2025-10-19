"""
Demo script for Pendle Finance Hybrid MCP Agent
Shows both direct contract and hosted SDK approaches
"""
import asyncio
import json
from hybrid_tools import mcp
from pendle_api_client import pendle_api

async def demo_hosted_sdk():
    """Demo hosted SDK operations"""
    print("Hosted SDK Demo")
    print("=" * 50)
    
    try:
        # Get best opportunities on Ethereum
        opportunities = await pendle_api.get_best_opportunities(chain_id=1, min_liquidity=1000000)
        print(f"Found {opportunities['count']} opportunities on Ethereum")
        
        if opportunities['opportunities']:
            best = opportunities['opportunities'][0]
            print(f"Best opportunity: {best['market']}")
            print(f"   APY: {best['apy']}")
            print(f"   Liquidity: {best['liquidity']}")
            print(f"   Risk Score: {best['riskScore']}")
        
        # Get multi-chain markets
        markets = await pendle_api.get_markets_batch([1, 42161, 10], limit=5)
        print(f"\nMulti-chain markets: {markets['totalChains']} chains")
        
        for market in markets['markets'][:3]:
            print(f"   {market['name']} on {market['chain']} - {market['lpAPY']}")
            
    except Exception as e:
        print(f"Error: {e}")

def demo_direct_contract():
    """Demo direct contract operations"""
    print("\nDirect Contract Demo")
    print("=" * 50)
    
    try:
        # Get wallet info
        from wallet import get_wallet_address, get_balance
        address = get_wallet_address()
        balance = get_balance(address)
        
        print(f"Wallet: {address}")
        print(f"Balance: {balance} ETH")
        
        # Get contract info
        from pendle import get_contract_info
        info = get_contract_info()
        print(f"Contract: {info['contract_address']}")
        print(f"Network: {info['network']}")
        
    except Exception as e:
        print(f"Error: {e}")

def demo_utility_functions():
    """Demo utility functions"""
    print("\nUtility Functions Demo")
    print("=" * 50)
    
    try:
        # Get supported chains
        chains = {
            "ethereum": 1,
            "arbitrum": 42161,
            "optimism": 10,
            "bsc": 56,
            "mantle": 5000
        }
        print("Supported Chains:")
        for name, chain_id in chains.items():
            print(f"   {name}: {chain_id}")
        
        # Get swap types
        swap_types = {
            "NONE": 0,
            "KYBERSWAP": 1,
            "ONE_INCH": 2,
            "NATIVE": 3,
            "UNISWAPV2": 4,
            "UNISWAPV3": 5,
            "CURVE": 6,
            "BALANCER": 7,
            "BANCOR": 8
        }
        print(f"\nSupported Swap Types: {len(swap_types)}")
        for name, value in list(swap_types.items())[:5]:
            print(f"   {name}: {value}")
        
    except Exception as e:
        print(f"Error: {e}")

async def main():
    """Run all demos"""
    print("Pendle Finance Hybrid MCP Agent Demo")
    print("=" * 60)
    
    # Demo hosted SDK (async)
    await demo_hosted_sdk()
    
    # Demo direct contract (sync)
    demo_direct_contract()
    
    # Demo utility functions (sync)
    demo_utility_functions()
    
    print("\nDemo completed!")
    print("\nTo start the MCP server: python main.py")
    print("See README.md for full documentation")

if __name__ == "__main__":
    asyncio.run(main())
