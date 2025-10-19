from web3 import Web3
from config import RPC_URL, WALLET_PRIVATE_KEY, NETWORK_INFO

# Connect to Arbitrum Sepolia blockchain
web3 = Web3(Web3.HTTPProvider(RPC_URL))

def get_wallet_address():
    """Get wallet address from private key"""
    account = web3.eth.account.from_key(WALLET_PRIVATE_KEY)
    return account.address

def get_balance(address):
    """Get ETH balance for an address"""
    balance_wei = web3.eth.get_balance(address)
    return balance_wei / (10**18)  # Convert wei to ether
