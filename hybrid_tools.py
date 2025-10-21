"""
Pendle Finance MCP Tools
Yield trading, liquidity management, and tokenized yield operations
"""
from fastmcp import FastMCP
from typing import Dict, Any, List
import asyncio
import json
from wallet import get_wallet_address, get_balance
from pendle import (
    get_symbol, get_start_time, get_owner,
    add_liquidity_dual_sy_and_pt, add_liquidity_single_sy, add_liquidity_single_token,
    remove_liquidity_dual_sy_and_pt, remove_liquidity_single_sy, remove_liquidity_single_token,
    mint_py_from_sy, redeem_py_to_sy,
    create_approx_params, create_swap_data, create_token_input, create_token_output,
    SwapType, ApproxParams, TokenInput, TokenOutput
)
from pendle_api_client import pendle_api

# Set up the MCP server
mcp = FastMCP("Pendle Finance MCP Agent")

# ========== ORIGINAL CONTRACT INTERACTION TOOLS ==========

# Basic contract info - safe to call anytime
@mcp.tool
def fetch_symbol() -> Dict[str, str]:
    """Get contract symbol"""
    return get_symbol()

@mcp.tool
def fetch_start_time() -> Dict[str, int]:
    """Get when the contract started"""
    return get_start_time()

@mcp.tool
def fetch_owner() -> Dict[str, str]:
    """Who owns this contract"""
    return get_owner()

@mcp.tool
def get_wallet_info() -> Dict[str, Any]:
    """Check your wallet address and ETH balance"""
    address = get_wallet_address()
    balance = get_balance(address)
    return {
        "address": address,
        "balance": str(balance)
    }

# Liquidity functions - these send real transactions!
@mcp.tool
def add_liquidity_with_sy_and_pt(
    receiver: str,
    market: str,
    net_sy_desired: int,
    net_pt_desired: int,
    min_lp_out: int
) -> Dict[str, Any]:
    """Add liquidity with both SY and PT tokens (Direct Contract)"""
    return add_liquidity_dual_sy_and_pt(
        receiver, market, net_sy_desired, net_pt_desired, min_lp_out
    )

@mcp.tool
def add_liquidity_with_sy_only(
    receiver: str,
    market: str,
    net_sy_in: int,
    min_lp_out: int,
    guess_min: int = 0,
    guess_max: int = 10**18,
    max_iteration: int = 256
) -> Dict[str, Any]:
    """Add liquidity with just SY tokens - contract figures out PT amount (Direct Contract)"""
    approx_params = create_approx_params(
        guess_min=guess_min,
        guess_max=guess_max,
        max_iteration=max_iteration
    )
    return add_liquidity_single_sy(
        receiver, market, net_sy_in, min_lp_out, approx_params
    )

@mcp.tool
def mint_py_tokens(
    receiver: str,
    yt_address: str,
    net_sy_in: int
) -> Dict[str, Any]:
    """Mint PY tokens from SY tokens (Direct Contract)"""
    return mint_py_from_sy(receiver, yt_address, net_sy_in)

@mcp.tool
def redeem_py_tokens(
    receiver: str,
    yt_address: str,
    net_py_in: int
) -> Dict[str, Any]:
    """Redeem PY tokens to SY tokens (Direct Contract)"""
    return redeem_py_to_sy(receiver, yt_address, net_py_in)

# ========== HOSTED SDK TOOLS (Hackathon-Winning Approach) ==========

@mcp.tool
async def convert_swap(
    chainId: int,
    marketAddress: str,
    receiver: str,
    tokenIn: str,
    tokenOut: str,
    amountIn: str,
    slippage: float = 0.005
) -> Dict[str, Any]:
    """Swap tokens using Pendle Hosted SDK (returns transaction data)"""
    try:
        result = await pendle_api.convert_swap(
            chain_id=chainId,
            market_address=marketAddress,
            receiver=receiver,
            token_in=tokenIn,
            token_out=tokenOut,
            amount_in=amountIn,
            slippage=slippage
        )
        return {
            "status": "success",
            "message": "🔄 Swap Transaction Ready",
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool
async def convert_add_liquidity(
    chainId: int,
    marketAddress: str,
    receiver: str,
    tokenIn: str,
    amountIn: str,
    slippage: float = 0.005
) -> Dict[str, Any]:
    """Add liquidity using Hosted SDK Convert API"""
    try:
        result = await pendle_api.convert_add_liquidity(
            chain_id=chainId,
            market_address=marketAddress,
            receiver=receiver,
            token_in=tokenIn,
            amount_in=amountIn,
            slippage=slippage
        )
        return {
            "status": "success",
            "message": "💧 Add Liquidity Transaction Ready",
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool
async def convert_add_liquidity_zpi(
    chainId: int,
    marketAddress: str,
    receiver: str,
    tokenIn: str,
    amountIn: str,
    slippage: float = 0.005
) -> Dict[str, Any]:
    """Add liquidity with Zero Price Impact (ZPI)"""
    try:
        result = await pendle_api.convert_add_liquidity_zpi(
            chain_id=chainId,
            market_address=marketAddress,
            receiver=receiver,
            token_in=tokenIn,
            amount_in=amountIn,
            slippage=slippage
        )
        return {
            "status": "success",
            "message": "💧 Add Liquidity (ZPI) Transaction Ready",
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool
async def convert_remove_liquidity(
    chainId: int,
    marketAddress: str,
    receiver: str,
    amountLp: str,
    tokenOut: str,
    slippage: float = 0.005
) -> Dict[str, Any]:
    """Remove liquidity using Hosted SDK"""
    try:
        result = await pendle_api.convert_remove_liquidity(
            chain_id=chainId,
            market_address=marketAddress,
            receiver=receiver,
            amount_lp=amountLp,
            token_out=tokenOut,
            slippage=slippage
        )
        return {
            "status": "success",
            "message": "💸 Remove Liquidity Transaction Ready",
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool
async def convert_mint_pt_yt(
    chainId: int,
    marketAddress: str,
    receiver: str,
    tokenIn: str,
    amountIn: str,
    slippage: float = 0.005
) -> Dict[str, Any]:
    """Mint PT & YT tokens using Hosted SDK"""
    try:
        result = await pendle_api.convert_mint_pt_yt(
            chain_id=chainId,
            market_address=marketAddress,
            receiver=receiver,
            token_in=tokenIn,
            amount_in=amountIn,
            slippage=slippage
        )
        return {
            "status": "success",
            "message": "🪙 Mint PT & YT Transaction Ready",
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool
async def convert_redeem_pt_yt(
    chainId: int,
    marketAddress: str,
    receiver: str,
    amountPt: str,
    tokenOut: str,
    slippage: float = 0.005
) -> Dict[str, Any]:
    """Redeem PT & YT tokens using Hosted SDK"""
    try:
        result = await pendle_api.convert_redeem_pt_yt(
            chain_id=chainId,
            market_address=marketAddress,
            receiver=receiver,
            amount_pt=amountPt,
            token_out=tokenOut,
            slippage=slippage
        )
        return {
            "status": "success",
            "message": "💰 Redeem PT & YT Transaction Ready",
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool
async def convert_mint_sy(
    chainId: int,
    syAddress: str,
    receiver: str,
    tokenIn: str,
    amountIn: str,
    slippage: float = 0.005
) -> Dict[str, Any]:
    """Mint SY (Standardized Yield) tokens using Hosted SDK"""
    try:
        result = await pendle_api.convert_mint_sy(
            chain_id=chainId,
            sy_address=syAddress,
            receiver=receiver,
            token_in=tokenIn,
            amount_in=amountIn,
            slippage=slippage
        )
        return {
            "status": "success",
            "message": "🏭 Mint SY Transaction Ready",
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool
async def convert_redeem_sy(
    chainId: int,
    syAddress: str,
    receiver: str,
    amountSy: str,
    tokenOut: str,
    slippage: float = 0.005
) -> Dict[str, Any]:
    """Redeem SY tokens using Hosted SDK"""
    try:
        result = await pendle_api.convert_redeem_sy(
            chain_id=chainId,
            sy_address=syAddress,
            receiver=receiver,
            amount_sy=amountSy,
            token_out=tokenOut,
            slippage=slippage
        )
        return {
            "status": "success",
            "message": "🔓 Redeem SY Transaction Ready",
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool
async def convert_rollover_pt(
    chainId: int,
    fromMarket: str,
    toMarket: str,
    receiver: str,
    amountPt: str,
    slippage: float = 0.005
) -> Dict[str, Any]:
    """Roll over PT tokens from one market to another using Hosted SDK"""
    try:
        result = await pendle_api.convert_rollover_pt(
            chain_id=chainId,
            from_market=fromMarket,
            to_market=toMarket,
            receiver=receiver,
            amount_pt=amountPt,
            slippage=slippage
        )
        return {
            "status": "success",
            "message": "🔄 Rollover PT Transaction Ready",
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool
async def convert_add_liquidity_dual(
    chainId: int,
    marketAddress: str,
    receiver: str,
    amountToken: str,
    amountPt: str,
    slippage: float = 0.005
) -> Dict[str, Any]:
    """Add dual-sided liquidity (token + PT) using Hosted SDK"""
    try:
        result = await pendle_api.convert_add_liquidity_dual(
            chain_id=chainId,
            market_address=marketAddress,
            receiver=receiver,
            amount_token=amountToken,
            amount_pt=amountPt,
            slippage=slippage
        )
        return {
            "status": "success",
            "message": "💎 Add Dual Liquidity Transaction Ready",
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool
async def convert_remove_liquidity_dual(
    chainId: int,
    marketAddress: str,
    receiver: str,
    amountLp: str,
    slippage: float = 0.005
) -> Dict[str, Any]:
    """Remove liquidity to both token and PT using Hosted SDK"""
    try:
        result = await pendle_api.convert_remove_liquidity_dual(
            chain_id=chainId,
            market_address=marketAddress,
            receiver=receiver,
            amount_lp=amountLp,
            slippage=slippage
        )
        return {
            "status": "success",
            "message": "💎 Remove Dual Liquidity Transaction Ready",
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool
async def convert_transfer_liquidity(
    chainId: int,
    fromMarket: str,
    toMarket: str,
    receiver: str,
    amountLp: str,
    slippage: float = 0.005
) -> Dict[str, Any]:
    """Transfer liquidity between markets using Hosted SDK"""
    try:
        result = await pendle_api.convert_transfer_liquidity(
            chain_id=chainId,
            from_market=fromMarket,
            to_market=toMarket,
            receiver=receiver,
            amount_lp=amountLp,
            slippage=slippage
        )
        return {
            "status": "success",
            "message": "🔀 Transfer Liquidity Transaction Ready",
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool
async def convert_transfer_liquidity_zpi(
    chainId: int,
    fromMarket: str,
    toMarket: str,
    receiver: str,
    amountLp: str,
    slippage: float = 0.005
) -> Dict[str, Any]:
    """Transfer liquidity with Zero Price Impact using Hosted SDK"""
    try:
        result = await pendle_api.convert_transfer_liquidity_zpi(
            chain_id=chainId,
            from_market=fromMarket,
            to_market=toMarket,
            receiver=receiver,
            amount_lp=amountLp,
            slippage=slippage
        )
        return {
            "status": "success",
            "message": "🔀 Transfer Liquidity (ZPI) Transaction Ready",
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ========== OPTIMIZED API TOOLS (Market Analysis & Opportunities) ==========

@mcp.tool
async def get_markets_batch(
    chainIds: List[int],
    limit: int = 20
) -> Dict[str, Any]:
    """Batch fetch markets from multiple chains (optimized with caching)"""
    try:
        result = await pendle_api.get_markets_batch(
            chain_ids=chainIds,
            limit=limit
        )
        return {
            "status": "success",
            "message": f"📊 Multi-Chain Markets ({result['totalChains']} chains)",
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool
async def get_best_opportunities(
    chainId: int,
    minLiquidity: float = 100000
) -> Dict[str, Any]:
    """Find best yield opportunities with liquidity filters"""
    try:
        result = await pendle_api.get_best_opportunities(
            chain_id=chainId,
            min_liquidity=minLiquidity
        )
        return {
            "status": "success",
            "message": f"🎯 Best Yield Opportunities ({result['count']} found)",
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool
async def get_market_depth(
    marketAddress: str,
    chainId: int
) -> Dict[str, Any]:
    """Get market depth and liquidity distribution"""
    try:
        result = await pendle_api.get_market_depth(
            market_address=marketAddress,
            chain_id=chainId
        )
        return {
            "status": "success",
            "message": "📈 Market Depth Analysis",
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool
async def simulate_strategy(
    marketAddress: str,
    chainId: int,
    investment: float,
    strategy: str
) -> Dict[str, Any]:
    """Simulate investment strategies with multiple scenarios"""
    try:
        result = await pendle_api.simulate_strategy(
            market_address=marketAddress,
            chain_id=chainId,
            investment=investment,
            strategy=strategy
        )
        return {
            "status": "success",
            "message": "🎲 Strategy Simulation",
            "data": result,
            "note": "Shows optimistic, expected, and pessimistic scenarios"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool
async def get_trending_markets(
    chainId: int,
    period: str = "24h"
) -> Dict[str, Any]:
    """Get trending markets by volume growth"""
    try:
        result = await pendle_api.get_trending_markets(
            chain_id=chainId,
            period=period
        )
        return {
            "status": "success",
            "message": "🔥 Trending Markets",
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool
async def get_protocol_revenue(
    chainId: int = None
) -> Dict[str, Any]:
    """Get protocol revenue statistics"""
    try:
        result = await pendle_api.get_protocol_revenue(
            chain_id=chainId
        )
        return {
            "status": "success",
            "message": "💵 Protocol Revenue",
            "data": result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ========== UTILITY TOOLS ==========

@mcp.tool
def create_approximation_params(
    guess_min: int = 0,
    guess_max: int = 10**18,
    guess_offchain: int = 0,
    max_iteration: int = 256,
    eps: int = 10**15
) -> Dict[str, int]:
    """Create approximation parameters for complex calculations"""
    params = create_approx_params(
        guess_min, guess_max, guess_offchain, max_iteration, eps
    )
    return {
        "guess_min": params.guessMin,
        "guess_max": params.guessMax,
        "guess_offchain": params.guessOffchain,
        "max_iteration": params.maxIteration,
        "eps": params.eps
    }

@mcp.tool
def get_swap_types_names() -> Dict[str, int]:
    """Get list of supported swap protocols"""
    return {
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

@mcp.tool
def get_contract_info() -> Dict[str, Any]:
    """Get all the basic contract info at once"""
    try:
        symbol = get_symbol()
        start_time = get_start_time()
        owner = get_owner()
        
        return {
            "contract_address": "0x888888888889758F76e7103c6CbF23ABbF58F946",
            "symbol": symbol.get("symbol", "Unknown"),
            "start_time": start_time.get("start_time", 0),
            "owner": owner.get("owner", "Unknown"),
            "network": "Ethereum Mainnet",
            "note": "Hybrid implementation with both direct contract and hosted SDK support"
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool
def get_supported_chains() -> Dict[str, int]:
    """Get list of supported chains for hosted SDK operations"""
    return {
        "ethereum": 1,
        "arbitrum": 42161,
        "optimism": 10,
        "bsc": 56,
        "mantle": 5000
    }
