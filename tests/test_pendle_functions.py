import pytest
from unittest.mock import Mock, patch
from pendle import (
    get_symbol, get_start_time, get_owner,
    add_liquidity_dual_sy_and_pt, add_liquidity_single_sy,
    remove_liquidity_dual_sy_and_pt, remove_liquidity_single_sy,
    mint_py_from_sy, redeem_py_to_sy,
    create_approx_params, create_swap_data, create_token_input, create_token_output,
    PendleError, MarketExpiredError, InvalidParametersError,
    SwapType, ApproxParams, TokenInput, TokenOutput, SwapData
)
from wallet import get_wallet_address, get_balance

class TestBasicContractInfo:
    """Test basic contract information functions"""
    
    def test_get_symbol_success(self):
        """Test getting contract symbol successfully"""
        with patch('pendle.pendle_contract') as mock_contract:
            mock_contract.functions.symbol.return_value.call.return_value = "PENDLE"
            result = get_symbol()
            assert result["symbol"] == "PENDLE"
    
    def test_get_start_time_success(self):
        """Test getting contract start time successfully"""
        with patch('pendle.pendle_contract') as mock_contract:
            mock_contract.functions.startTime.return_value.call.return_value = 1640995200
            result = get_start_time()
            assert result["start_time"] == 1640995200
    
    def test_get_owner_success(self):
        """Test getting contract owner successfully"""
        with patch('pendle.pendle_contract') as mock_contract:
            mock_contract.functions.owner.return_value.call.return_value = "0x1234567890123456789012345678901234567890"
            result = get_owner()
            assert result["owner"] == "0x1234567890123456789012345678901234567890"
    
    def test_get_symbol_error(self):
        """Test getting contract symbol with error"""
        with patch('pendle.pendle_contract') as mock_contract:
            mock_contract.functions.symbol.return_value.call.side_effect = Exception("Contract call failed")
            with pytest.raises(PendleError):
                get_symbol()

class TestLiquidityManagement:
    """Test liquidity management functions"""
    
    def test_add_liquidity_dual_sy_and_pt_success(self):
        """Test successful dual liquidity addition"""
        with patch('pendle.web3') as mock_web3, \
             patch('pendle.get_wallet_address') as mock_address:
            
            # Mock web3 components
            mock_web3.eth.gas_price = 20000000000  # 20 gwei
            mock_web3.eth.account.sign_transaction.return_value.rawTransaction = b'signed_tx'
            mock_web3.eth.send_raw_transaction.return_value = b'tx_hash'
            mock_web3.eth.wait_for_transaction_receipt.return_value = Mock(
                gasUsed=250000, blockNumber=12345
            )
            mock_address.return_value = "0x1234567890123456789012345678901234567890"
            
            result = add_liquidity_dual_sy_and_pt(
                "0x1234567890123456789012345678901234567890",
                "0x0987654321098765432109876543210987654321",
                1000000000000000000,  # 1 ETH in wei
                500000000000000000,   # 0.5 ETH in wei
                750000000000000000    # 0.75 ETH in wei
            )
            assert result["status"] == "success"
            assert result["gas_used"] == 250000
            assert result["block_number"] == 12345
    
    def test_add_liquidity_single_sy_success(self):
        """Test successful single SY liquidity addition"""
        with patch('pendle.web3') as mock_web3, \
             patch('pendle.get_wallet_address') as mock_address:
            
            # Mock web3 components
            mock_web3.eth.gas_price = 20000000000
            mock_web3.eth.account.sign_transaction.return_value.rawTransaction = b'signed_tx'
            mock_web3.eth.send_raw_transaction.return_value = b'tx_hash'
            mock_web3.eth.wait_for_transaction_receipt.return_value = Mock(
                gasUsed=200000, blockNumber=12346
            )
            mock_address.return_value = "0x1234567890123456789012345678901234567890"
            
            approx_params = create_approx_params()
            result = add_liquidity_single_sy(
                "0x1234567890123456789012345678901234567890",
                "0x0987654321098765432109876543210987654321",
                1000000000000000000,  # 1 ETH in wei
                500000000000000000,   # 0.5 ETH in wei
                approx_params
            )
            assert result["status"] == "success"
            assert result["gas_used"] == 200000
    
    def test_remove_liquidity_dual_sy_and_pt_success(self):
        """Test successful dual liquidity removal"""
        with patch('pendle.web3') as mock_web3, \
             patch('pendle.get_wallet_address') as mock_address:
            
            # Mock web3 components
            mock_web3.eth.gas_price = 20000000000
            mock_web3.eth.account.sign_transaction.return_value.rawTransaction = b'signed_tx'
            mock_web3.eth.send_raw_transaction.return_value = b'tx_hash'
            mock_web3.eth.wait_for_transaction_receipt.return_value = Mock(
                gasUsed=180000, blockNumber=12347
            )
            mock_address.return_value = "0x1234567890123456789012345678901234567890"
            
            result = remove_liquidity_dual_sy_and_pt(
                "0x1234567890123456789012345678901234567890",
                "0x0987654321098765432109876543210987654321",
                750000000000000000,   # LP tokens to remove
                400000000000000000,   # min SY out
                350000000000000000    # min PT out
            )
            assert result["status"] == "success"
            assert result["gas_used"] == 180000
    
    def test_remove_liquidity_single_sy_success(self):
        """Test successful single SY liquidity removal"""
        with patch('pendle.web3') as mock_web3, \
             patch('pendle.get_wallet_address') as mock_address:
            
            # Mock web3 components
            mock_web3.eth.gas_price = 20000000000
            mock_web3.eth.account.sign_transaction.return_value.rawTransaction = b'signed_tx'
            mock_web3.eth.send_raw_transaction.return_value = b'tx_hash'
            mock_web3.eth.wait_for_transaction_receipt.return_value = Mock(
                gasUsed=150000, blockNumber=12348
            )
            mock_address.return_value = "0x1234567890123456789012345678901234567890"
            
            result = remove_liquidity_single_sy(
                "0x1234567890123456789012345678901234567890",
                "0x0987654321098765432109876543210987654321",
                500000000000000000,   # LP tokens to remove
                400000000000000000    # min SY out
            )
            assert result["status"] == "success"
            assert result["gas_used"] == 150000

class TestPYTokenManagement:
    """Test PY token management functions"""
    
    def test_mint_py_from_sy_success(self):
        """Test successful PY minting from SY"""
        with patch('pendle.web3') as mock_web3, \
             patch('pendle.get_wallet_address') as mock_address:
            
            # Mock web3 components
            mock_web3.eth.gas_price = 20000000000
            mock_web3.eth.account.sign_transaction.return_value.rawTransaction = b'signed_tx'
            mock_web3.eth.send_raw_transaction.return_value = b'tx_hash'
            mock_web3.eth.wait_for_transaction_receipt.return_value = Mock(
                gasUsed=120000, blockNumber=12349
            )
            mock_address.return_value = "0x1234567890123456789012345678901234567890"
            
            result = mint_py_from_sy(
                "0x1234567890123456789012345678901234567890",
                "0x0987654321098765432109876543210987654321",
                1000000000000000000  # 1 ETH in wei
            )
            assert result["status"] == "success"
            assert result["gas_used"] == 120000
    
    def test_redeem_py_to_sy_success(self):
        """Test successful PY redemption to SY"""
        with patch('pendle.web3') as mock_web3, \
             patch('pendle.get_wallet_address') as mock_address:
            
            # Mock web3 components
            mock_web3.eth.gas_price = 20000000000
            mock_web3.eth.account.sign_transaction.return_value.rawTransaction = b'signed_tx'
            mock_web3.eth.send_raw_transaction.return_value = b'tx_hash'
            mock_web3.eth.wait_for_transaction_receipt.return_value = Mock(
                gasUsed=100000, blockNumber=12350
            )
            mock_address.return_value = "0x1234567890123456789012345678901234567890"
            
            result = redeem_py_to_sy(
                "0x1234567890123456789012345678901234567890",
                "0x0987654321098765432109876543210987654321",
                800000000000000000   # 0.8 ETH in wei
            )
            assert result["status"] == "success"
            assert result["gas_used"] == 100000

class TestDataStructures:
    """Test data structure creation functions"""
    
    def test_create_approx_params_default(self):
        """Test creating approximation parameters with defaults"""
        params = create_approx_params()
        assert params.guessMin == 0
        assert params.guessMax == 10**18
        assert params.guessOffchain == 0
        assert params.maxIteration == 256
        assert params.eps == 10**15
    
    def test_create_approx_params_custom(self):
        """Test creating approximation parameters with custom values"""
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
    
    def test_create_token_input(self):
        """Test creating token input"""
        swap_data = create_swap_data(SwapType.NONE)
        token_input = create_token_input(
            "0x1111111111111111111111111111111111111111",
            1000000000000000000,
            "0x2222222222222222222222222222222222222222",
            "0x3333333333333333333333333333333333333333",
            swap_data
        )
        assert token_input.tokenIn == "0x1111111111111111111111111111111111111111"
        assert token_input.netTokenIn == 1000000000000000000
        assert token_input.tokenMintSy == "0x2222222222222222222222222222222222222222"
        assert token_input.pendleSwap == "0x3333333333333333333333333333333333333333"
        assert token_input.swapData == swap_data
    
    def test_create_token_output(self):
        """Test creating token output"""
        swap_data = create_swap_data(SwapType.CURVE)
        token_output = create_token_output(
            "0x4444444444444444444444444444444444444444",
            500000000000000000,
            "0x5555555555555555555555555555555555555555",
            "0x6666666666666666666666666666666666666666",
            swap_data
        )
        assert token_output.tokenOut == "0x4444444444444444444444444444444444444444"
        assert token_output.minTokenOut == 500000000000000000
        assert token_output.tokenRedeemSy == "0x5555555555555555555555555555555555555555"
        assert token_output.pendleSwap == "0x6666666666666666666666666666666666666666"
        assert token_output.swapData == swap_data

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
    
    def test_contract_error_handling(self):
        """Test contract error handling"""
        from pendle import _handle_contract_error
        
        # Test MarketExpired error
        with pytest.raises(MarketExpiredError):
            _handle_contract_error(Exception("MarketExpired"))
        
        # Test InvalidParameters error
        with pytest.raises(InvalidParametersError):
            _handle_contract_error(Exception("MarketZeroAmountsInput"))
        
        # Test generic Pendle error
        with pytest.raises(PendleError):
            _handle_contract_error(Exception("SomeOtherError"))

class TestWalletFunctions:
    """Test wallet-related functions"""
    
    def test_get_wallet_address(self):
        """Test getting wallet address"""
        with patch('pendle.web3') as mock_web3:
            mock_web3.eth.account.from_key.return_value.address = "0x1234567890123456789012345678901234567890"
            result = get_wallet_address()
            assert result == "0x1234567890123456789012345678901234567890"
    
    def test_get_balance(self):
        """Test getting wallet balance"""
        with patch('pendle.web3') as mock_web3:
            mock_web3.eth.get_balance.return_value = 1500000000000000000  # 1.5 ETH in wei
            mock_web3.fromWei.return_value = 1.5
            result = get_balance("0x1234567890123456789012345678901234567890")
            assert result == 1.5

class TestSwapTypeEnum:
    """Test SwapType enum"""
    
    def test_swap_type_values(self):
        """Test swap type enum values"""
        assert SwapType.NONE.value == 0
        assert SwapType.KYBERSWAP.value == 1
        assert SwapType.ONE_INCH.value == 2
        assert SwapType.NATIVE.value == 3
        assert SwapType.UNISWAPV2.value == 4
        assert SwapType.UNISWAPV3.value == 5
        assert SwapType.CURVE.value == 6
        assert SwapType.BALANCER.value == 7
        assert SwapType.BANCOR.value == 8
    
    def test_swap_type_creation(self):
        """Test creating swap types from values"""
        assert SwapType(0) == SwapType.NONE
        assert SwapType(1) == SwapType.KYBERSWAP
        assert SwapType(5) == SwapType.UNISWAPV3
        assert SwapType(6) == SwapType.CURVE
