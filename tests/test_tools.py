import pytest
from unittest.mock import Mock, patch
from tools import (
    fetch_symbol, fetch_start_time, fetch_owner, get_wallet_info,
    add_liquidity_with_sy_and_pt, add_liquidity_with_sy_only,
    remove_liquidity_to_sy_and_pt, remove_liquidity_to_sy_only,
    mint_py_tokens, redeem_py_tokens,
    create_approximation_params, get_swap_types_names,
    estimate_gas_for_liquidity_addition, get_contract_info
)
from pendle import (
    PendleError, MarketExpiredError, InvalidParametersError,
    create_approx_params, create_swap_data, SwapType
)

# Tests for the MCP tools - mostly just checking they call the right functions

class TestBasicContractInfo:
    """Test basic contract information functions"""
    
    def test_fetch_symbol(self):
        """Test fetching contract symbol"""
        with patch('pendle.get_symbol') as mock_get_symbol:
            mock_get_symbol.return_value = {"symbol": "PENDLE"}
            result = fetch_symbol()
            assert result["symbol"] == "PENDLE"
    
    def test_fetch_start_time(self):
        """Test fetching contract start time"""
        with patch('pendle.get_start_time') as mock_get_start_time:
            mock_get_start_time.return_value = {"start_time": 1640995200}
            result = fetch_start_time()
            assert result["start_time"] == 1640995200
    
    def test_fetch_owner(self):
        """Test fetching contract owner"""
        with patch('pendle.get_owner') as mock_get_owner:
            mock_get_owner.return_value = {"owner": "0x1234567890123456789012345678901234567890"}
            result = fetch_owner()
            assert result["owner"] == "0x1234567890123456789012345678901234567890"
    
    def test_get_wallet_info(self):
        """Test getting wallet information"""
        with patch('pendle.get_wallet_address') as mock_get_address, \
             patch('pendle.get_balance') as mock_get_balance:
            mock_get_address.return_value = "0x1234567890123456789012345678901234567890"
            mock_get_balance.return_value = 1.5
            result = get_wallet_info()
            assert result["address"] == "0x1234567890123456789012345678901234567890"
            assert result["balance"] == "1.5"

class TestLiquidityManagement:
    """Test liquidity management functions"""
    
    def test_add_liquidity_with_sy_and_pt_success(self):
        """Test successful liquidity addition with SY and PT"""
        with patch('pendle.add_liquidity_dual_sy_and_pt') as mock_add:
            mock_add.return_value = {
                "status": "success",
                "transaction_hash": "0xabcdef1234567890",
                "gas_used": 250000,
                "block_number": 12345
            }
            result = add_liquidity_with_sy_and_pt(
                "0x1234567890123456789012345678901234567890",
                "0x0987654321098765432109876543210987654321",
                1000000000000000000,  # 1 ETH in wei
                500000000000000000,   # 0.5 ETH in wei
                750000000000000000    # 0.75 ETH in wei
            )
            assert result["status"] == "success"
            assert result["transaction_hash"] == "0xabcdef1234567890"
    
    def test_add_liquidity_with_sy_and_pt_error(self):
        """Test liquidity addition with error handling"""
        with patch('pendle.add_liquidity_dual_sy_and_pt') as mock_add:
            mock_add.side_effect = MarketExpiredError("Market has expired")
            with pytest.raises(MarketExpiredError):
                add_liquidity_with_sy_and_pt(
                    "0x1234567890123456789012345678901234567890",
                    "0x0987654321098765432109876543210987654321",
                    1000000000000000000,
                    500000000000000000,
                    750000000000000000
                )
    
    def test_add_liquidity_with_sy_only(self):
        """Test liquidity addition with SY only"""
        with patch('pendle.add_liquidity_single_sy') as mock_add:
            mock_add.return_value = {
                "status": "success",
                "transaction_hash": "0xabcdef1234567890",
                "gas_used": 200000,
                "block_number": 12346
            }
            result = add_liquidity_with_sy_only(
                "0x1234567890123456789012345678901234567890",
                "0x0987654321098765432109876543210987654321",
                1000000000000000000,  # 1 ETH in wei
                500000000000000000,   # 0.5 ETH in wei
                0,                    # guess_min
                10**18,              # guess_max
                256                   # max_iteration
            )
            assert result["status"] == "success"
    
    def test_remove_liquidity_to_sy_and_pt(self):
        """Test removing liquidity to get SY and PT"""
        with patch('pendle.remove_liquidity_dual_sy_and_pt') as mock_remove:
            mock_remove.return_value = {
                "status": "success",
                "transaction_hash": "0xfedcba0987654321",
                "gas_used": 180000,
                "block_number": 12347
            }
            result = remove_liquidity_to_sy_and_pt(
                "0x1234567890123456789012345678901234567890",
                "0x0987654321098765432109876543210987654321",
                750000000000000000,   # LP tokens to remove
                400000000000000000,   # min SY out
                350000000000000000    # min PT out
            )
            assert result["status"] == "success"
    
    def test_remove_liquidity_to_sy_only(self):
        """Test removing liquidity to get SY only"""
        with patch('pendle.remove_liquidity_single_sy') as mock_remove:
            mock_remove.return_value = {
                "status": "success",
                "transaction_hash": "0xfedcba0987654321",
                "gas_used": 150000,
                "block_number": 12348
            }
            result = remove_liquidity_to_sy_only(
                "0x1234567890123456789012345678901234567890",
                "0x0987654321098765432109876543210987654321",
                500000000000000000,   # LP tokens to remove
                400000000000000000    # min SY out
            )
            assert result["status"] == "success"

class TestPYTokenManagement:
    """Test PY token management functions"""
    
    def test_mint_py_tokens(self):
        """Test minting PY tokens from SY"""
        with patch('pendle.mint_py_from_sy') as mock_mint:
            mock_mint.return_value = {
                "status": "success",
                "transaction_hash": "0x1111222233334444",
                "gas_used": 120000,
                "block_number": 12349
            }
            result = mint_py_tokens(
                "0x1234567890123456789012345678901234567890",
                "0x0987654321098765432109876543210987654321",
                1000000000000000000  # 1 ETH in wei
            )
            assert result["status"] == "success"
    
    def test_redeem_py_tokens(self):
        """Test redeeming PY tokens to SY"""
        with patch('pendle.redeem_py_to_sy') as mock_redeem:
            mock_redeem.return_value = {
                "status": "success",
                "transaction_hash": "0x5555666677778888",
                "gas_used": 100000,
                "block_number": 12350
            }
            result = redeem_py_tokens(
                "0x1234567890123456789012345678901234567890",
                "0x0987654321098765432109876543210987654321",
                800000000000000000   # 0.8 ETH in wei
            )
            assert result["status"] == "success"

class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_create_approximation_params_default(self):
        """Test creating approximation parameters with defaults"""
        result = create_approximation_params()
        assert result["guess_min"] == 0
        assert result["guess_max"] == 10**18
        assert result["guess_offchain"] == 0
        assert result["max_iteration"] == 256
        assert result["eps"] == 10**15
    
    def test_create_approximation_params_custom(self):
        """Test creating approximation parameters with custom values"""
        result = create_approximation_params(
            guess_min=100,
            guess_max=1000000,
            guess_offchain=50000,
            max_iteration=128,
            eps=10**12
        )
        assert result["guess_min"] == 100
        assert result["guess_max"] == 1000000
        assert result["guess_offchain"] == 50000
        assert result["max_iteration"] == 128
        assert result["eps"] == 10**12
    
    def test_get_swap_types_names(self):
        """Test getting swap types names"""
        result = get_swap_types_names()
        assert result["NONE"] == 0
        assert result["KYBERSWAP"] == 1
        assert result["ONE_INCH"] == 2
        assert result["UNISWAPV3"] == 5
        assert result["CURVE"] == 6
        assert len(result) == 9  # All swap types
    
    def test_estimate_gas_for_liquidity_addition(self):
        """Test gas estimation for liquidity addition"""
        with patch('pendle.pendle_contract') as mock_contract, \
             patch('pendle.get_wallet_address') as mock_address:
            mock_address.return_value = "0x1234567890123456789012345678901234567890"
            mock_contract.functions.addLiquidityDualSyAndPt.return_value.estimateGas.return_value = 250000
            
            result = estimate_gas_for_liquidity_addition(
                "0x0987654321098765432109876543210987654321",
                1000000000000000000,
                500000000000000000
            )
            assert result["estimated_gas"] == 250000
            assert result["estimated_gas_with_buffer"] == 300000
    
    def test_estimate_gas_for_liquidity_addition_error(self):
        """Test gas estimation with error"""
        with patch('pendle.pendle_contract') as mock_contract:
            mock_contract.functions.addLiquidityDualSyAndPt.return_value.estimateGas.side_effect = Exception("Gas estimation failed")
            
            result = estimate_gas_for_liquidity_addition(
                "0x0987654321098765432109876543210987654321",
                1000000000000000000,
                500000000000000000
            )
            assert "error" in result
            assert "Gas estimation failed" in result["error"]
    
    def test_get_contract_info_success(self):
        """Test getting contract info successfully"""
        with patch('pendle.get_symbol') as mock_symbol, \
             patch('pendle.get_start_time') as mock_start_time, \
             patch('pendle.get_owner') as mock_owner:
            mock_symbol.return_value = {"symbol": "PENDLE"}
            mock_start_time.return_value = {"start_time": 1640995200}
            mock_owner.return_value = {"owner": "0x1234567890123456789012345678901234567890"}
            
            result = get_contract_info()
            assert result["contract_address"] == "0x888888888889758F76e7103c6CbF23ABbF58F946"
            assert result["symbol"] == "PENDLE"
            assert result["start_time"] == 1640995200
            assert result["owner"] == "0x1234567890123456789012345678901234567890"
            assert result["network"] == "Ethereum Mainnet"
    
    def test_get_contract_info_error(self):
        """Test getting contract info with error"""
        with patch('pendle.get_symbol') as mock_symbol:
            mock_symbol.side_effect = Exception("Contract call failed")
            
            result = get_contract_info()
            assert "error" in result
            assert "Contract call failed" in result["error"]

class TestDataStructures:
    """Test data structure creation functions"""
    
    def test_create_approx_params(self):
        """Test creating approximation parameters"""
        params = create_approx_params(
            guess_min=100,
            guess_max=1000000,
            guess_offchain=50000,
            max_iteration=128,
            eps=10**12
        )
        assert params.guessMin == 100
        assert params.guessMax == 1000000
        assert params.guessOffchain == 50000
        assert params.maxIteration == 128
        assert params.eps == 10**12
    
    def test_create_swap_data(self):
        """Test creating swap data"""
        swap_data = create_swap_data(
            SwapType.UNISWAPV3,
            ext_router="0x1234567890123456789012345678901234567890",
            ext_calldata=b"test_data",
            need_scale=True
        )
        assert swap_data.swapType == SwapType.UNISWAPV3
        assert swap_data.extRouter == "0x1234567890123456789012345678901234567890"
        assert swap_data.extCalldata == b"test_data"
        assert swap_data.needScale == True

class TestErrorHandling:
    """Test error handling scenarios"""
    
    def test_market_expired_error(self):
        """Test market expired error handling"""
        error = MarketExpiredError("Market has expired")
        assert str(error) == "Market has expired"
        assert isinstance(error, PendleError)
    
    def test_invalid_parameters_error(self):
        """Test invalid parameters error handling"""
        error = InvalidParametersError("Invalid parameters provided")
        assert str(error) == "Invalid parameters provided"
        assert isinstance(error, PendleError)
    
    def test_pendle_error(self):
        """Test base Pendle error handling"""
        error = PendleError("Generic Pendle error")
        assert str(error) == "Generic Pendle error"