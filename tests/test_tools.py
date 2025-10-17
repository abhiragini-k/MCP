import pytest
from tools import wallet_info, show_yield_tokens

def test_wallet_info():
    info = wallet_info()
    assert "address" in info
    assert float(info["balance"]) >= 0

def test_show_yield_tokens():
    tokens = show_yield_tokens()
    assert "yield_tokens" in tokens