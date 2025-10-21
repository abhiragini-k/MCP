# Pendle Finance MCP Agent

This is an MCP agent that lets you interact with Pendle Finance directly. Think of it as your bridge to yield trading, liquidity management, and all the tokenized yield stuff that Pendle does across different blockchains.

## What This Actually Does

I built this because I wanted a clean way to interact with Pendle Finance without having to deal with all the complexity of their contracts directly. The agent gives you two main ways to interact:

1. **Direct contract calls** - When you want to talk straight to the smart contracts and get transaction hashes back
2. **Hosted SDK operations** - When you want the fancy stuff like optimal routing and zero price impact trades

Plus there's a bunch of market analysis tools to help you figure out what's actually worth your time.

## The Tools You Get

### Direct Contract Tools
These are the basic building blocks - they talk directly to Pendle's contracts:
- `add_liquidity_with_sy_and_pt` - Add liquidity using both SY and PT tokens
- `add_liquidity_with_sy_only` - Add liquidity with just SY tokens
- `mint_py_tokens` - Convert SY tokens to PY tokens
- `redeem_py_tokens` - Convert PY tokens back to SY tokens
- `fetch_symbol` - Get the symbol of a contract
- `fetch_start_time` - When a contract started
- `fetch_owner` - Who owns a contract
- `get_wallet_info` - Check your wallet address and balance

### Hosted SDK Tools
These use Pendle's hosted SDK for the more complex operations:
- `convert_swap` - Token swaps with optimal routing
- `convert_add_liquidity` - Add liquidity with automatic optimization
- `convert_add_liquidity_zpi` - Add liquidity with zero price impact
- `convert_remove_liquidity` - Remove liquidity optimally
- `convert_mint_pt_yt` - Mint PT & YT tokens
- `convert_redeem_pt_yt` - Redeem PT & YT tokens
- `convert_mint_sy` - Mint SY (Standardized Yield) tokens
- `convert_redeem_sy` - Redeem SY tokens
- `convert_rollover_pt` - Roll over PT tokens between markets

### Market Analysis Tools
For when you want to understand what's happening in the markets:
- `get_markets_batch` - Get markets from multiple chains at once
- `get_best_opportunities` - Find the best yield opportunities with filters
- `get_market_depth` - Analyze market depth and liquidity
- `simulate_strategy` - Test out investment strategies before committing
- `get_trending_markets` - See what markets are hot by volume
- `get_protocol_revenue` - Check protocol revenue stats

### Utility Tools
The helper functions that make everything work:
- `create_approximation_params` - Create approximation parameters
- `get_swap_types_names` - See what swap protocols are supported
- `get_contract_info` - Get comprehensive contract information
- `get_supported_chains` - See which chains are supported

## Getting Started

First, install the dependencies:
```bash
pip install -r requirements.txt
```

You'll need to create a `.env` file with your configuration:
```
RPC_URL=https://sepolia-rollup.arbitrum.io/rpc
WALLET_PRIVATE_KEY=your_private_key_here
```

To make sure everything is working, run the test:
```bash
python test_working.py
```

Then start the MCP server:
```bash
python main.py
```

## What's in This Project

Here's what each file does:

- `main.py` - The main MCP server that ties everything together
- `hybrid_tools.py` - All the MCP tools (30+ of them)
- `pendle.py` - Direct contract interactions
- `pendle_api_client.py` - Handles the hosted SDK API calls
- `wallet.py` - Wallet management stuff
- `config.py` - Configuration management
- `test_working.py` - Tests to make sure everything works
- `requirements.txt` - Python dependencies
- `abi/pendle_router_abi.json` - The smart contract ABI

## Who This Is For

- **Yield traders** who want to execute strategies across multiple chains
- **Liquidity providers** who need optimal routing for adding/removing liquidity
- **DeFi developers** building on top of Pendle Finance
- **Portfolio managers** who want to analyze and simulate yield strategies

## How It Works

The agent uses the MCP protocol to provide a standardized interface for AI agents. It combines direct contract calls with Pendle's hosted SDK to give you the best of both worlds. It supports 5 major blockchain networks and includes comprehensive error handling and gas optimization.