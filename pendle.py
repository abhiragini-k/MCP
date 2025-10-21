import json
from typing import Dict, Any
from dataclasses import dataclass
from enum import Enum
from wallet import web3, get_wallet_address
from config import WALLET_PRIVATE_KEY, PENDLE_CONTRACT_ADDRESS
                
# Load ABI - this took forever to find the right one
with open('abi/pendle_router_abi.json','r') as abi_files:
    PENDLE_CONTRACT_ABI = json.load(abi_files)

# Only create contract instance if we have a valid address
if PENDLE_CONTRACT_ADDRESS and PENDLE_CONTRACT_ADDRESS != 'TBD':
    pendle_contract = web3.eth.contract(address=PENDLE_CONTRACT_ADDRESS, abi=PENDLE_CONTRACT_ABI)
else:
    pendle_contract = None

def check_contract_available():
    """Check if Pendle contract is available on this network"""
    if pendle_contract is None:
        raise PendleError("Pendle contracts are not deployed on this network yet. Try Ethereum Mainnet for full functionality.")

def check_contract_or_return_error():
    """Check if contract is available, return error dict if not"""
    if pendle_contract is None:
        return {"error": "Pendle contracts not deployed on Arbitrum Sepolia yet", "network": "Arbitrum Sepolia", "suggestion": "Try Ethereum Mainnet for full functionality"}
    return None

# These enums match what's in the contract - had to reverse engineer from the ABI
class SwapType(Enum):
    NONE = 0
    KYBERSWAP = 1
    ONE_INCH = 2
    NATIVE = 3
    UNISWAPV2 = 4
    UNISWAPV3 = 5
    CURVE = 6
    BALANCER = 7
    BANCOR = 8  # not sure if this is still supported but keeping it

@dataclass
class SwapData:
    swapType: SwapType
    extRouter: str
    extCalldata: bytes
    needScale: bool

@dataclass  
class ApproxParams:
    # These params are a pain to get right - usually just use defaults
    guessMin: int
    guessMax: int
    guessOffchain: int
    maxIteration: int
    eps: int

@dataclass
class TokenInput:
    tokenIn: str
    netTokenIn: int
    tokenMintSy: str  # the SY token we're minting to
    pendleSwap: str   # swap contract address
    swapData: SwapData

@dataclass
class TokenOutput:
    tokenOut: str
    minTokenOut: int
    tokenRedeemSy: str  # SY token we're redeeming from
    pendleSwap: str
    swapData: SwapData

# Custom exceptions - these are the main ones I've seen in practice
class PendleError(Exception):
    pass

class InsufficientBalanceError(PendleError):
    pass

class MarketExpiredError(PendleError):
    pass

class InvalidParametersError(PendleError):
    pass

def _handle_contract_error(e: Exception) -> None:
    """Map contract errors to our custom exceptions"""
    error_msg = str(e)
    
    # These are the common error patterns from the contract
    if "MarketExpired" in error_msg:
        raise MarketExpiredError("Market has expired")
    elif "MarketExchangeRateBelowOne" in error_msg:
        raise PendleError("Market exchange rate is below one")
    elif "MarketProportionTooHigh" in error_msg:
        raise PendleError("Market proportion is too high")
    elif "MarketZeroAmountsInput" in error_msg:
        raise InvalidParametersError("Zero amounts provided for input")
    elif "MarketZeroAmountsOutput" in error_msg:
        raise InvalidParametersError("Zero amounts provided for output")
    else:
        raise PendleError(f"Contract error: {error_msg}")

# Basic info functions - Pendle Router doesn't have view functions, so these just return contract info
def get_contract_info() -> Dict[str, Any]:
    """Get basic contract information"""
    return {
        "contract_address": PENDLE_CONTRACT_ADDRESS,
        "network": "Arbitrum Sepolia",
        "chain_id": 421614,
        "contract_type": "Pendle Router",
        "description": "Router contract for Pendle Finance operations (testnet)",
        "note": "Pendle contracts may not be deployed on Arbitrum Sepolia yet"
    }

def get_start_time() -> Dict[str, str]:
    """Router doesn't have start time - just return a placeholder"""
    if pendle_contract is None:
        return {"message": "Pendle contracts not deployed on Arbitrum Sepolia yet"}
    return {"message": "Pendle Router doesn't expose start time"}

def get_symbol() -> Dict[str, str]:
    """Router doesn't have symbol - just return a placeholder"""
    if pendle_contract is None:
        return {"message": "Pendle contracts not deployed on Arbitrum Sepolia yet"}
    return {"message": "Pendle Router doesn't have a symbol"}

def get_owner() -> Dict[str, str]:
    """Router doesn't expose owner - just return a placeholder"""
    if pendle_contract is None:
        return {"message": "Pendle contracts not deployed on Arbitrum Sepolia yet"}
    return {"message": "Pendle Router doesn't expose owner info"}

# Liquidity functions - these actually send transactions so be careful

def add_liquidity_dual_sy_and_pt(
    receiver: str,
    market: str,
    net_sy_desired: int,
    net_pt_desired: int,
    min_lp_out: int
) -> Dict[str, Any]:
    """Add liquidity with both SY and PT - most straightforward method"""
    error_check = check_contract_or_return_error()
    if error_check:
        return error_check
    
    try:
        transaction = pendle_contract.functions.addLiquidityDualSyAndPt(
            receiver,
            market,
            net_sy_desired,
            net_pt_desired,
            min_lp_out
        ).buildTransaction({
            'from': get_wallet_address(),
            'gas': 500000,  # should be enough for most cases
            'gasPrice': web3.eth.gas_price
        })
        
        signed_txn = web3.eth.account.sign_transaction(transaction, WALLET_PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            "status": "success",
            "transaction_hash": tx_hash.hex(),
            "gas_used": receipt.gasUsed,
            "block_number": receipt.blockNumber
        }
    except Exception as e:
        _handle_contract_error(e)

def add_liquidity_single_sy(
    receiver: str,
    market: str,
    net_sy_in: int,
    min_lp_out: int,
    guess_pt_received_from_sy: ApproxParams
) -> Dict[str, Any]:
    """Add liquidity with just SY - contract will figure out the PT part"""
    error_check = check_contract_or_return_error()
    if error_check:
        return error_check
    
    try:
        # Convert the approximation params to tuple format
        approx_tuple = (
            guess_pt_received_from_sy.guessMin,
            guess_pt_received_from_sy.guessMax,
            guess_pt_received_from_sy.guessOffchain,
            guess_pt_received_from_sy.maxIteration,
            guess_pt_received_from_sy.eps
        )
        
        # Empty limit order data - not using limit orders for now
        limit_data = (
            "0x0000000000000000000000000000000000000000",  # limitRouter
            0,  # epsSkipMarket
            [],  # normalFills
            [],  # flashFills
            b''  # optData
        )
        
        transaction = pendle_contract.functions.addLiquiditySingleSy(
            receiver,
            market,
            net_sy_in,
            min_lp_out,
            approx_tuple,
            limit_data
        ).buildTransaction({
            'from': get_wallet_address(),
            'gas': 500000,
            'gasPrice': web3.eth.gas_price
        })
        
        signed_txn = web3.eth.account.sign_transaction(transaction, WALLET_PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            "status": "success",
            "transaction_hash": tx_hash.hex(),
            "gas_used": receipt.gasUsed,
            "block_number": receipt.blockNumber
        }
    except Exception as e:
        _handle_contract_error(e)

def add_liquidity_single_token(
    receiver: str,
    market: str,
    min_lp_out: int,
    guess_pt_received_from_sy: ApproxParams,
    token_input: TokenInput
) -> Dict[str, Any]:
    """
    Add liquidity using a single token
    
    Args:
        receiver: Address to receive LP tokens
        market: Market address
        min_lp_out: Minimum LP tokens to receive
        guess_pt_received_from_sy: Approximation parameters
        token_input: Token input parameters
    
    Returns:
        Dictionary with netLpOut, netSyFee, netSyInterm
    """
    try:
        # Convert ApproxParams to tuple
        approx_tuple = (
            guess_pt_received_from_sy.guessMin,
            guess_pt_received_from_sy.guessMax,
            guess_pt_received_from_sy.guessOffchain,
            guess_pt_received_from_sy.maxIteration,
            guess_pt_received_from_sy.eps
        )
        
        # Convert TokenInput to tuple
        token_input_tuple = (
            token_input.tokenIn,
            token_input.netTokenIn,
            token_input.tokenMintSy,
            token_input.pendleSwap,
            (
                token_input.swapData.swapType.value,
                token_input.swapData.extRouter,
                token_input.swapData.extCalldata,
                token_input.swapData.needScale
            )
        )
        
        # Empty limit order data
        limit_data = (
            "0x0000000000000000000000000000000000000000",  # limitRouter
            0,  # epsSkipMarket
            [],  # normalFills
            [],  # flashFills
            b''  # optData
        )
        
        transaction = pendle_contract.functions.addLiquiditySingleToken(
            receiver,
            market,
            min_lp_out,
            approx_tuple,
            token_input_tuple,
            limit_data
        ).buildTransaction({
            'from': get_wallet_address(),
            'gas': 500000,
            'gasPrice': web3.eth.gas_price
        })
        
        signed_txn = web3.eth.account.sign_transaction(transaction, WALLET_PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            "status": "success",
            "transaction_hash": tx_hash.hex(),
            "gas_used": receipt.gasUsed,
            "block_number": receipt.blockNumber
        }
    except Exception as e:
        _handle_contract_error(e)

def remove_liquidity_dual_sy_and_pt(
    receiver: str,
    market: str,
    net_lp_to_remove: int,
    min_sy_out: int,
    min_pt_out: int
) -> Dict[str, Any]:
    """
    Remove liquidity to get both SY and PT tokens
    
    Args:
        receiver: Address to receive tokens
        market: Market address
        net_lp_to_remove: Amount of LP tokens to remove
        min_sy_out: Minimum SY tokens to receive
        min_pt_out: Minimum PT tokens to receive
    
    Returns:
        Dictionary with netSyOut and netPtOut
    """
    try:
        transaction = pendle_contract.functions.removeLiquidityDualSyAndPt(
            receiver,
            market,
            net_lp_to_remove,
            min_sy_out,
            min_pt_out
        ).buildTransaction({
            'from': get_wallet_address(),
            'gas': 500000,
            'gasPrice': web3.eth.gas_price
        })
        
        signed_txn = web3.eth.account.sign_transaction(transaction, WALLET_PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            "status": "success",
            "transaction_hash": tx_hash.hex(),
            "gas_used": receipt.gasUsed,
            "block_number": receipt.blockNumber
        }
    except Exception as e:
        _handle_contract_error(e)

def remove_liquidity_single_sy(
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
        net_lp_to_remove: Amount of LP tokens to remove
        min_sy_out: Minimum SY tokens to receive
    
    Returns:
        Dictionary with netSyOut and netSyFee
    """
    try:
        # Empty limit order data
        limit_data = (
            "0x0000000000000000000000000000000000000000",  # limitRouter
            0,  # epsSkipMarket
            [],  # normalFills
            [],  # flashFills
            b''  # optData
        )
        
        transaction = pendle_contract.functions.removeLiquiditySingleSy(
            receiver,
            market,
            net_lp_to_remove,
            min_sy_out,
            limit_data
        ).buildTransaction({
            'from': get_wallet_address(),
            'gas': 500000,
            'gasPrice': web3.eth.gas_price
        })
        
        signed_txn = web3.eth.account.sign_transaction(transaction, WALLET_PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            "status": "success",
            "transaction_hash": tx_hash.hex(),
            "gas_used": receipt.gasUsed,
            "block_number": receipt.blockNumber
        }
    except Exception as e:
        _handle_contract_error(e)

def remove_liquidity_single_token(
    receiver: str,
    market: str,
    net_lp_to_remove: int,
    token_output: TokenOutput
) -> Dict[str, Any]:
    """
    Remove liquidity to get a single token
    
    Args:
        receiver: Address to receive tokens
        market: Market address
        net_lp_to_remove: Amount of LP tokens to remove
        token_output: Token output parameters
    
    Returns:
        Dictionary with netTokenOut, netSyFee, netSyInterm
    """
    try:
        # Convert TokenOutput to tuple
        token_output_tuple = (
            token_output.tokenOut,
            token_output.minTokenOut,
            token_output.tokenRedeemSy,
            token_output.pendleSwap,
            (
                token_output.swapData.swapType.value,
                token_output.swapData.extRouter,
                token_output.swapData.extCalldata,
                token_output.swapData.needScale
            )
        )
        
        # Empty limit order data
        limit_data = (
            "0x0000000000000000000000000000000000000000",  # limitRouter
            0,  # epsSkipMarket
            [],  # normalFills
            [],  # flashFills
            b''  # optData
        )
        
        transaction = pendle_contract.functions.removeLiquiditySingleToken(
            receiver,
            market,
            net_lp_to_remove,
            token_output_tuple,
            limit_data
        ).buildTransaction({
            'from': get_wallet_address(),
            'gas': 500000,
            'gasPrice': web3.eth.gas_price
        })
        
        signed_txn = web3.eth.account.sign_transaction(transaction, WALLET_PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            "status": "success",
            "transaction_hash": tx_hash.hex(),
            "gas_used": receipt.gasUsed,
            "block_number": receipt.blockNumber
        }
    except Exception as e:
        _handle_contract_error(e)

# PY Token Functions (Principal Tokens)

def mint_py_from_sy(
    receiver: str,
    yt_address: str,
    net_sy_in: int
) -> Dict[str, Any]:
    """
    Mint PY tokens from SY tokens
    
    Args:
        receiver: Address to receive PY tokens
        yt_address: Yield token address
        net_sy_in: Amount of SY tokens to mint from
    
    Returns:
        Dictionary with netPyOut
    """
    error_check = check_contract_or_return_error()
    if error_check:
        return error_check
    
    try:
        transaction = pendle_contract.functions.mintPyFromSy(
            receiver,
            yt_address,
            net_sy_in
        ).buildTransaction({
            'from': get_wallet_address(),
            'gas': 300000,
            'gasPrice': web3.eth.gas_price
        })
        
        signed_txn = web3.eth.account.sign_transaction(transaction, WALLET_PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            "status": "success",
            "transaction_hash": tx_hash.hex(),
            "gas_used": receipt.gasUsed,
            "block_number": receipt.blockNumber
        }
    except Exception as e:
        _handle_contract_error(e)

def redeem_py_to_sy(
    receiver: str,
    yt_address: str,
    net_py_in: int
) -> Dict[str, Any]:
    """
    Redeem PY tokens to SY tokens
    
    Args:
        receiver: Address to receive SY tokens
        yt_address: Yield token address
        net_py_in: Amount of PY tokens to redeem
    
    Returns:
        Dictionary with netSyOut
    """
    try:
        transaction = pendle_contract.functions.redeemPyToSy(
            receiver,
            yt_address,
            net_py_in
        ).buildTransaction({
            'from': get_wallet_address(),
            'gas': 300000,
            'gasPrice': web3.eth.gas_price
        })
        
        signed_txn = web3.eth.account.sign_transaction(transaction, WALLET_PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            "status": "success",
            "transaction_hash": tx_hash.hex(),
            "gas_used": receipt.gasUsed,
            "block_number": receipt.blockNumber
        }
    except Exception as e:
        _handle_contract_error(e)

# Utility Functions

def create_approx_params(
    guess_min: int = 0,
    guess_max: int = 10**18,
    guess_offchain: int = 0,
    max_iteration: int = 256,
    eps: int = 10**15
) -> ApproxParams:
    """Helper to create approximation params - usually defaults work fine"""
    return ApproxParams(
        guessMin=guess_min,
        guessMax=guess_max,
        guessOffchain=guess_offchain,
        maxIteration=max_iteration,
        eps=eps
    )

def create_swap_data(
    swap_type: SwapType,
    ext_router: str = "0x0000000000000000000000000000000000000000",
    ext_calldata: bytes = b'',
    need_scale: bool = False
) -> SwapData:
    """Create swap data - mostly just use SwapType.NONE unless you need a specific DEX"""
    return SwapData(
        swapType=swap_type,
        extRouter=ext_router,
        extCalldata=ext_calldata,
        needScale=need_scale
    )

def create_token_input(
    token_in: str,
    net_token_in: int,
    token_mint_sy: str,
    pendle_swap: str,
    swap_data: SwapData
) -> TokenInput:
    """Helper to create token input struct"""
    return TokenInput(
        tokenIn=token_in,
        netTokenIn=net_token_in,
        tokenMintSy=token_mint_sy,
        pendleSwap=pendle_swap,
        swapData=swap_data
    )

def create_token_output(
    token_out: str,
    min_token_out: int,
    token_redeem_sy: str,
    pendle_swap: str,
    swap_data: SwapData
) -> TokenOutput:
    """Helper to create token output struct"""
    return TokenOutput(
        tokenOut=token_out,
        minTokenOut=min_token_out,
        tokenRedeemSy=token_redeem_sy,
        pendleSwap=pendle_swap,
        swapData=swap_data
    )

