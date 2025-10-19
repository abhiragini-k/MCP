from fastmcp import FastMCP
from typing import Dict, Any
from wallet import get_wallet_address, get_balance
from pendle import (
    get_symbol, get_start_time, get_owner,
    add_liquidity_dual_sy_and_pt, add_liquidity_single_sy, add_liquidity_single_token,
    remove_liquidity_dual_sy_and_pt, remove_liquidity_single_sy, remove_liquidity_single_token,
    mint_py_from_sy, redeem_py_to_sy,
    create_approx_params, create_swap_data, create_token_input, create_token_output,
    SwapType, ApproxParams, TokenInput, TokenOutput
)

# Set up the MCP server
mcp = FastMCP("Pendle Finance MCP Agent")

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
    """Add liquidity with both SY and PT tokens"""
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
    """Add liquidity with just SY tokens - contract figures out PT amount"""
    approx_params = create_approx_params(
        guess_min=guess_min,
        guess_max=guess_max,
        max_iteration=max_iteration
    )
    return add_liquidity_single_sy(
        receiver, market, net_sy_in, min_lp_out, approx_params
    )

@mcp.tool
def add_liquidity_with_token(
    receiver: str,
    market: str,
    min_lp_out: int,
    token_in: str,
    net_token_in: int,
    token_mint_sy: str,
    pendle_swap: str,
    swap_type: int = 0,
    guess_min: int = 0,
    guess_max: int = 10**18
) -> Dict[str, Any]:
    """Add liquidity with any token - gets converted to SY first"""
    swap_data = create_swap_data(SwapType(swap_type))
    token_input = create_token_input(
        token_in, net_token_in, token_mint_sy, pendle_swap, swap_data
    )
    approx_params = create_approx_params(guess_min=guess_min, guess_max=guess_max)
    
    return add_liquidity_single_token(
        receiver, market, min_lp_out, approx_params, token_input
    )

@mcp.tool
def remove_liquidity_to_sy_and_pt(
    receiver: str,
    market: str,
    net_lp_to_remove: int,
    min_sy_out: int,
    min_pt_out: int
) -> Dict[str, Any]:
    """Remove liquidity and get back both SY and PT tokens"""
    return remove_liquidity_dual_sy_and_pt(
        receiver, market, net_lp_to_remove, min_sy_out, min_pt_out
    )

@mcp.tool
def remove_liquidity_to_sy_only(
    receiver: str,
    market: str,
    net_lp_to_remove: int,
    min_sy_out: int
) -> Dict[str, Any]:
    """
    Remove liquidity to get SY tokens only
    
    Args:
        receiver: Address to receive SY tokens
        market: Market address
        net_lp_to_remove: Amount of LP tokens to remove (in wei)
        min_sy_out: Minimum SY tokens to receive (in wei)
    
    Returns:
        Transaction result with hash and gas usage
    """
    return remove_liquidity_single_sy(
        receiver, market, net_lp_to_remove, min_sy_out
    )

@mcp.tool
def remove_liquidity_to_token(
    receiver: str,
    market: str,
    net_lp_to_remove: int,
    token_out: str,
    min_token_out: int,
    token_redeem_sy: str,
    pendle_swap: str,
    swap_type: int = 0
) -> Dict[str, Any]:
    """
    Remove liquidity to get a single token
    
    Args:
        receiver: Address to receive tokens
        market: Market address
        net_lp_to_remove: Amount of LP tokens to remove (in wei)
        token_out: Output token address
        min_token_out: Minimum output tokens to receive (in wei)
        token_redeem_sy: Token to redeem SY to
        pendle_swap: Pendle swap contract address
        swap_type: Type of swap (0=NONE, 1=KYBERSWAP, 2=ONE_INCH, etc.)
    
    Returns:
        Transaction result with hash and gas usage
    """
    swap_data = create_swap_data(SwapType(swap_type))
    token_output = create_token_output(
        token_out, min_token_out, token_redeem_sy, pendle_swap, swap_data
    )
    
    return remove_liquidity_single_token(
        receiver, market, net_lp_to_remove, token_output
    )

# PY Token Management Tools

@mcp.tool
def mint_py_tokens(
    receiver: str,
    yt_address: str,
    net_sy_in: int
) -> Dict[str, Any]:
    """
    Mint PY tokens from SY tokens
    
    Args:
        receiver: Address to receive PY tokens
        yt_address: Yield token address
        net_sy_in: Amount of SY tokens to mint from (in wei)
    
    Returns:
        Transaction result with hash and gas usage
    """
    return mint_py_from_sy(receiver, yt_address, net_sy_in)

@mcp.tool
def redeem_py_tokens(
    receiver: str,
    yt_address: str,
    net_py_in: int
) -> Dict[str, Any]:
    """
    Redeem PY tokens to SY tokens
    
    Args:
        receiver: Address to receive SY tokens
        yt_address: Yield token address
        net_py_in: Amount of PY tokens to redeem (in wei)
    
    Returns:
        Transaction result with hash and gas usage
    """
    return redeem_py_to_sy(receiver, yt_address, net_py_in)

# Utility Tools

@mcp.tool
def create_approximation_params(
    guess_min: int = 0,
    guess_max: int = 10**18,
    guess_offchain: int = 0,
    max_iteration: int = 256,
    eps: int = 10**15
) -> Dict[str, int]:
    """
    Create approximation parameters for complex calculations
    
    Args:
        guess_min: Minimum guess value (default: 0)
        guess_max: Maximum guess value (default: 10^18)
        guess_offchain: Offchain guess value (default: 0)
        max_iteration: Maximum iterations (default: 256)
        eps: Epsilon value for precision (default: 10^15)
    
    Returns:
        Dictionary with approximation parameters
    """
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

# Helper functions
@mcp.tool
def estimate_gas_for_liquidity_addition(
    market: str,
    net_sy_desired: int,
    net_pt_desired: int
) -> Dict[str, int]:
    """Estimate gas cost before sending transaction"""
    try:
        gas_estimate = pendle_contract.functions.addLiquidityDualSyAndPt(
            get_wallet_address(),
            market,
            net_sy_desired,
            net_pt_desired,
            0  # min_lp_out
        ).estimateGas({'from': get_wallet_address()})
        
        return {
            "estimated_gas": gas_estimate,
            "estimated_gas_with_buffer": int(gas_estimate * 1.2)
        }
    except Exception as e:
        return {"error": str(e)}

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
            "network": "Ethereum Mainnet"
        }
    except Exception as e:
        return {"error": str(e)}
