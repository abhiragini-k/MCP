from fastmcp import mcp
from wallet import get_wallet_address, get_balance
from pendle import get_yield_tokens, tokenize_asset

@mcp.tool
def wallet_info()->dict:
    """Get wallet address and balance."""
    address = get_wallet_address()
    balance = get_balance()
    return {"address":address, "balance":balance}

@mcp.tool
def show_yield_tokens()->dict:
    """Fetch Pendle yield token position for wallet."""
    tokens = get_yield_tokens()
    return tokens

@mcp.tool
def run_tokenization(asset_id: str)->dict:
    """Tokenize asset with Pendle for specified ID."""
    result = tokenize_asset(asset_id)
    return result
