# Pendle Finance MCP Agent

A Model Context Protocol (MCP) agent for interacting with Pendle Finance protocols. This agent provides programmatic access to Pendle's liquidity management, yield token operations, and swap functionality through a clean MCP interface.

## Overview

This project implements a comprehensive MCP server that wraps Pendle Finance's complex DeFi operations into callable tools. The agent handles everything from basic wallet operations to advanced liquidity management and yield token minting.

## Features

### Liquidity Management
- Add liquidity with dual SY/PT tokens
- Single token liquidity operations
- Remove liquidity from various pool types
- Support for different approximation parameters

### Yield Token Operations
- Mint PY tokens from SY tokens
- Redeem PY tokens back to SY
- Handle yield token addresses and calculations

### Swap Integration
- Support for multiple DEX integrations (KyberSwap, 1inch, Uniswap V2/V3, Curve, Balancer)
- Token input/output structures
- Swap data handling with external router calls

### Wallet Integration
- MetaMask wallet connection
- Private key management
- Balance checking and transaction signing
- Gas estimation and transaction building

## Architecture

The agent is built with a modular architecture:

- **`pendle.py`** - Core contract interaction logic (600+ lines)
- **`tools.py`** - MCP tool wrappers for all functions
- **`wallet.py`** - Wallet utilities and Web3 connection
- **`config.py`** - Network configuration and environment setup
- **`main.py`** - MCP server entry point

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

The agent is configured for Arbitrum Sepolia testnet. Create a `.env` file with:

```
RPC_URL=https://sepolia-rollup.arbitrum.io/rpc
WALLET_PRIVATE_KEY=your_private_key_here
PENDLE_CONTRACT_ADDRESS=TBD
```

## Usage

Start the MCP server:

```bash
python main.py
```

The server will expose all Pendle Finance operations as MCP tools that can be called programmatically.

## Network Configuration

**Arbitrum Sepolia Testnet:**
- Chain ID: 421614
- RPC URL: https://sepolia-rollup.arbitrum.io/rpc
- Block Explorer: https://sepolia.arbiscan.io/

## Data Structures

The agent implements several key data structures for Pendle operations:

### SwapType Enum
Maps to Pendle's supported swap types:
- NONE, KYBERSWAP, ONE_INCH, NATIVE
- UNISWAPV2, UNISWAPV3, CURVE, BALANCER

### ApproxParams
Handles swap approximation parameters:
- guessMin, guessMax, guessOffchain
- maxIteration, eps

### TokenInput/TokenOutput
Structures for token operations with proper type handling.

## Error Handling

The agent includes comprehensive error handling:
- `PendleError` - Base exception for Pendle operations
- `InvalidParametersError` - For invalid function parameters
- `InsufficientLiquidityError` - For liquidity-related errors
- `ContractError` - For contract interaction errors

## Current Status

The agent is configured for Arbitrum Sepolia testnet. Pendle Finance contracts are not yet deployed on this network, so the agent gracefully handles missing contracts and provides appropriate error messages.

## Project Structure

```
├── main.py              # MCP server entry point
├── config.py            # Network configuration
├── pendle.py            # Core Pendle functions (600+ lines)
├── tools.py             # MCP tool wrappers
├── wallet.py            # Wallet utilities
├── abi/                 # Contract ABIs
│   └── pendle_router_abi.json
├── tests/               # Unit tests
│   ├── test_tools.py
│   └── test_pendle_functions.py
└── requirements.txt     # Dependencies
```

## API Reference

### Core Functions

**Liquidity Management:**
- `add_liquidity_dual_sy_and_pt()` - Add liquidity with SY and PT tokens
- `add_liquidity_single_sy()` - Add liquidity with SY tokens only
- `add_liquidity_single_token()` - Add liquidity with single token
- `remove_liquidity_dual_sy_and_pt()` - Remove liquidity from dual pools
- `remove_liquidity_single_sy()` - Remove liquidity from SY pools
- `remove_liquidity_single_token()` - Remove liquidity from single token pools

**Yield Token Operations:**
- `mint_py_from_sy()` - Mint PY tokens from SY tokens
- `redeem_py_to_sy()` - Redeem PY tokens back to SY

**Utility Functions:**
- `create_approx_params()` - Create approximation parameters for swaps
- `create_swap_data()` - Create swap data structures
- `create_token_input()` - Create token input structures
- `create_token_output()` - Create token output structures

## Dependencies

- `web3` - Ethereum Web3 library
- `fastmcp` - Model Context Protocol framework
- `python-dotenv` - Environment variable management



