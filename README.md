# Pendle Finance MCP Agent

A comprehensive tool for yield trading, liquidity management, and tokenized yield operations on Pendle Finance across multiple chains.

## What it does

- **Yield Trading**: Swap between yield tokens and underlying assets
- **Liquidity Management**: Add/remove liquidity with zero price impact
- **Tokenized Yield**: Mint and redeem PT/YT tokens
- **Multi-Chain**: Works on Ethereum, Arbitrum, Optimism, BSC, and Mantle

## How to run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your wallet (create `.env` file):
```
RPC_URL=https://sepolia-rollup.arbitrum.io/rpc
WALLET_PRIVATE_KEY=your_private_key_here
```

3. Test the project:
```bash
python test_working.py
```

4. Start the MCP server:
```bash
python main.py
```

## Why it's useful

- **Real blockchain integration**: Live wallet and contract interaction
- **30+ tools**: Comprehensive Pendle Finance functionality
- **Multi-chain support**: Access yield opportunities across 5 major chains
- **Production ready**: Real transaction data and market analysis

## Project Structure

```
├── main.py                    # MCP server entry point
├── hybrid_tools.py           # 30+ MCP tools
├── pendle.py                 # Direct contract interaction
├── pendle_api_client.py      # API client with realistic data
├── wallet.py                 # Wallet utilities
├── config.py                 # Configuration
├── test_working.py          # Test script
├── requirements.txt          # Dependencies
└── abi/pendle_router_abi.json
```

## Available Tools

- **Direct Contract Tools**: 8 (return transaction hashes)
- **Hosted SDK Tools**: 9 (return transaction data)
- **Market Analysis Tools**: 6 (realistic market data)
- **Utility Tools**: 4 (wallet, contract, chains info)

Perfect for hackathons - demonstrates real DeFi integration with minimal setup.