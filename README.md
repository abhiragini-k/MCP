# Pendle Finance MCP Agent

Hey! This is my Pendle Finance MCP agent that I built for interacting with Pendle protocols. It's set up for Arbitrum Sepolia testnet right now.

## What I Built

I spent a lot of time analyzing the Pendle Router ABI and building out all the core functionality. Here's what I implemented:

### Core Features
- **Liquidity Management**: Add/remove liquidity for SY, PT, and single tokens
- **PY Token Operations**: Mint PY from SY and redeem PY back to SY
- **Swap Functions**: Handle different swap types (KyberSwap, 1inch, Uniswap, etc.)
- **Wallet Integration**: Connect to MetaMask and manage wallet operations
- **Error Handling**: Custom exceptions for contract errors and invalid parameters

### What I Actually Coded
- **Data Structures**: Built proper Python classes for complex Solidity types (SwapType, ApproxParams, TokenInput, TokenOutput, SwapData)
- **Contract Interaction**: Functions to build, sign, and send transactions to the Pendle Router
- **MCP Tools**: Wrapped everything as MCP tools so you can interact with it through the protocol
- **Testing**: Created comprehensive unit tests for all the functions
- **Network Support**: Set up for Arbitrum Sepolia with proper error handling for missing contracts

### The Hard Parts
- **ABI Analysis**: Had to reverse engineer the complex Pendle Router ABI to understand all the function signatures
- **Data Structure Mapping**: Converting Solidity structs to Python dataclasses was tricky
- **Error Handling**: Pendle has specific error codes that needed custom exception handling
- **Transaction Building**: Getting the gas estimation and transaction signing right took some trial and error

## Quick Start

### 1. Set up your .env file
Create a `.env` file in the root directory with:
```
RPC_URL=https://sepolia-rollup.arbitrum.io/rpc
WALLET_PRIVATE_KEY=your_private_key_here
PENDLE_CONTRACT_ADDRESS=TBD
```

**Important:** Don't commit your `.env` file to git! It has your private key.

### 2. Get some test tokens
You'll need test ETH for gas fees. Try these faucets:
- **Chainlink Faucet**: https://faucets.chain.link/arbitrum-sepolia (gives you 0.5 ETH)
- **Alchemy Faucet**: https://www.alchemy.com/faucets/arbitrum-sepolia (0.1 ETH daily)

### 3. Run it
```bash
python main.py
```

## Network Setup

**Arbitrum Sepolia Testnet:**
- Chain ID: 421614
- RPC URL: https://sepolia-rollup.arbitrum.io/rpc
- Block Explorer: https://sepolia.arbiscan.io/

### MetaMask Setup
Add this network to your MetaMask:
- **Network Name**: Arbitrum Sepolia
- **RPC URL**: https://sepolia-rollup.arbitrum.io/rpc
- **Chain ID**: 421614
- **Currency Symbol**: ETH
- **Block Explorer**: https://sepolia.arbiscan.io/

## Testing Your Setup

Before you start using the MCP tools, make sure everything works:

```bash
# Check your wallet connection
python -c "from wallet import get_wallet_address, get_balance; addr = get_wallet_address(); print('Wallet:', addr, 'Balance:', get_balance(addr))"

# Check contract info
python -c "from pendle import get_contract_info; print(get_contract_info())"
```

## Important Notes

**Pendle contracts aren't deployed on Arbitrum Sepolia yet** - so you can test basic Web3 stuff and wallet operations, but the actual Pendle functions will give you an error message. That's totally normal!

If you want to test the full Pendle functionality, you'd need to switch to Ethereum mainnet, but then you'd need real ETH for gas fees.

## Project Structure

```
├── main.py              # MCP server entry point
├── config.py            # Network configuration (Arbitrum Sepolia setup)
├── pendle.py            # Core Pendle functions (600+ lines of contract interaction)
├── tools.py             # MCP tool wrappers (all functions exposed as tools)
├── wallet.py            # Wallet utilities (MetaMask integration)
├── abi/                 # Contract ABIs
│   └── pendle_router_abi.json  # The actual Pendle Router ABI
├── tests/               # Unit tests
│   ├── test_tools.py    # MCP tool tests
│   └── test_pendle_functions.py  # Core function tests
└── requirements.txt     # Dependencies
```

## Technical Details

### Functions I Implemented
- `add_liquidity_dual_sy_and_pt()` - Add liquidity with both SY and PT
- `add_liquidity_single_sy()` - Add liquidity with just SY
- `add_liquidity_single_token()` - Add liquidity with a single token
- `remove_liquidity_dual_sy_and_pt()` - Remove liquidity from dual pools
- `remove_liquidity_single_sy()` - Remove liquidity from SY pools
- `remove_liquidity_single_token()` - Remove liquidity from single token pools
- `mint_py_from_sy()` - Mint PY tokens from SY
- `redeem_py_to_sy()` - Redeem PY tokens back to SY
- Plus all the helper functions for creating parameters and handling swaps

### Data Structures I Built
- `SwapType` enum - Maps to Pendle's swap types
- `ApproxParams` dataclass - For swap approximation parameters
- `TokenInput` dataclass - Token input structure
- `TokenOutput` dataclass - Token output structure
- `SwapData` dataclass - Complete swap data structure

### Error Handling
- `PendleError` - Base exception for Pendle operations
- `InvalidParametersError` - For invalid function parameters
- `InsufficientLiquidityError` - For liquidity-related errors
- `ContractError` - For contract interaction errors

## Dependencies

Just run:
```bash
pip install -r requirements.txt
```

## Troubleshooting

**"Contract not found" errors?** 
- That's expected on Arbitrum Sepolia since Pendle isn't deployed there yet

**"Insufficient funds" errors?**
- Get more test tokens from the faucets

**"Network mismatch" errors?**
- Make sure your MetaMask is on Arbitrum Sepolia network
- Check your RPC URL in the .env file

## What I Learned Building This

This was actually a pretty complex project! Here's what I figured out along the way:

### The Pendle Router is Complex
- It's not just a simple DEX - it handles yield tokens, principal tokens, and all kinds of complex DeFi operations
- The ABI has tons of functions for different liquidity scenarios
- Getting the parameter structures right was crucial

### MCP Integration
- Had to wrap all the functions as MCP tools with proper descriptions
- Made sure error handling works through the MCP protocol
- Tested that the tools actually work when called through MCP

### Network Challenges
- Pendle isn't deployed on Arbitrum Sepolia yet (which makes sense - it's a complex protocol)
- Had to build graceful error handling for missing contracts
- Set up proper network configuration for when contracts do get deployed


