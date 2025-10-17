from web3 import Web3
from config import RPC_URL, WALLET_PRIVATE_KEY

web3 = Web3(Web3.HTTPProvider(RPC_URL))

def get_wallet_address():
    account = web3.eth.account.from_key(WALLET_PRIVATE_KEY)
    return account.address

def get_balance(address):
    balance_wei = web3.eth.get_balance(address)
    return web3.fromWei(balance_wei, 'ether')
