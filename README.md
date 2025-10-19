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

## How It Works

### Architecture Overview

The Pendle Finance MCP Agent operates as a Model Context Protocol (MCP) server that provides programmatic access to Pendle Finance's DeFi operations. Here's how the system works:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Client    │───▶│   MCP Server     │───▶│  Pendle Router  │
│  (Your App)     │    │  (This Agent)    │    │   Contract      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   Web3 Provider  │
                       │ (Arbitrum Sepolia)│
                       └──────────────────┘
```

### Core Components

1. **MCP Server (`main.py`)**: Entry point that starts the FastMCP server
2. **Tool Wrappers (`tools.py`)**: Exposes Pendle functions as MCP tools
3. **Core Logic (`pendle.py`)**: Direct contract interaction with Pendle Router
4. **Wallet Integration (`wallet.py`)**: Handles Web3 connection and wallet operations
5. **Configuration (`config.py`)**: Network settings and environment variables

### Data Flow

1. **Client Request**: MCP client calls a tool (e.g., `add_liquidity_with_sy_and_pt`)
2. **Tool Processing**: `tools.py` validates parameters and calls `pendle.py` functions
3. **Contract Interaction**: `pendle.py` builds and sends transactions to Pendle Router
4. **Blockchain Execution**: Transaction is executed on Arbitrum Sepolia
5. **Response**: Transaction hash and results are returned to the client

### Key Features

- **Direct Contract Interaction**: Uses actual Pendle Router ABI for on-chain operations
- **Comprehensive Error Handling**: Custom exceptions for different failure scenarios
- **Gas Optimization**: Built-in gas estimation and transaction optimization
- **Multi-DEX Support**: Integration with Uniswap, Curve, Balancer, and other DEXs
- **Flexible Parameters**: Support for complex approximation parameters and swap data

## Execution Guide

### Prerequisites

1. **Python 3.8+** installed
2. **Arbitrum Sepolia ETH** for gas fees (get from [Arbitrum Sepolia Faucet](https://faucet.quicknode.com/arbitrum/sepolia))
3. **Private Key** for wallet operations

### Step 1: Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd pendle-finance-mcp

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configuration

Create a `.env` file in the project root:

```bash
# .env file
RPC_URL=https://sepolia-rollup.arbitrum.io/rpc
WALLET_PRIVATE_KEY=your_private_key_here
PENDLE_CONTRACT_ADDRESS=TBD
```

**Important Notes:**
- Replace `your_private_key_here` with your actual private key (without 0x prefix)
- The project is configured for Arbitrum Sepolia testnet
- Pendle contracts may not be deployed on Arbitrum Sepolia yet

### Step 3: Running the MCP Server

```bash
# Start the MCP server
python main.py
```

The server will start and listen for MCP client connections. You should see output like:
```
Pendle Finance MCP Agent started
Listening for MCP connections...
```

### Step 4: Using the Agent

#### Option A: Direct Function Calls (for testing)

```python
# Example: Check wallet info
from tools import get_wallet_info
result = get_wallet_info()
print(result)
```

#### Option B: MCP Client Integration

```python
# Example MCP client usage
import asyncio
from mcp import ClientSession, StdioServerParameters

async def main():
    async with ClientSession(StdioServerParameters(
        command="python",
        args=["main.py"]
    )) as session:
        # Call a tool
        result = await session.call_tool(
            "add_liquidity_with_sy_and_pt",
            {
                "receiver": "0x...",
                "market": "0x...",
                "net_sy_desired": 1000000000000000000,  # 1 SY token
                "net_pt_desired": 1000000000000000000,  # 1 PT token
                "min_lp_out": 0
            }
        )
        print(result)

asyncio.run(main())
```

### Step 5: Available Operations

#### Liquidity Management
```bash
# Add liquidity with SY and PT tokens
add_liquidity_with_sy_and_pt(receiver, market, net_sy_desired, net_pt_desired, min_lp_out)

# Add liquidity with SY only
add_liquidity_with_sy_only(receiver, market, net_sy_in, min_lp_out)

# Remove liquidity
remove_liquidity_to_sy_and_pt(receiver, market, net_lp_to_remove, min_sy_out, min_pt_out)
```

#### PY Token Operations
```bash
# Mint PY tokens from SY
mint_py_tokens(receiver, yt_address, net_sy_in)

# Redeem PY tokens to SY
redeem_py_tokens(receiver, yt_address, net_py_in)
```

#### Utility Functions
```bash
# Check wallet info
get_wallet_info()

# Get contract information
get_contract_info()

# Create approximation parameters
create_approximation_params(guess_min, guess_max, max_iteration)
```

### Step 6: Testing

Run the test suite to verify everything works:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_tools.py

# Run with verbose output
python -m pytest tests/ -v
```

### Troubleshooting

#### Common Issues

1. **"Pendle contracts not deployed"**
   - This is expected on Arbitrum Sepolia
   - The agent gracefully handles missing contracts
   - Try Ethereum Mainnet for full functionality

2. **"Insufficient funds"**
   - Ensure you have Arbitrum Sepolia ETH for gas
   - Get testnet ETH from the faucet

3. **"Invalid private key"**
   - Check your `.env` file format
   - Ensure private key doesn't include 0x prefix

4. **"Connection refused"**
   - Verify RPC URL is correct
   - Check internet connection

#### Debug Mode

Enable debug logging by setting environment variable:
```bash
export PYTHONPATH=.
python -c "import logging; logging.basicConfig(level=logging.DEBUG); import main"
```

### Network Information

**Arbitrum Sepolia Testnet:**
- Chain ID: 421614
- RPC URL: https://sepolia-rollup.arbitrum.io/rpc
- Block Explorer: https://sepolia.arbiscan.io/
- Faucet: https://faucet.quicknode.com/arbitrum/sepolia

**For Production Use:**
- Switch to Ethereum Mainnet in `config.py`
- Update contract addresses
- Use mainnet RPC endpoints

## Dependencies

- `web3` - Ethereum Web3 library
- `fastmcp` - Model Context Protocol framework
- `python-dotenv` - Environment variable management



