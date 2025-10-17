from wallet import web3, get_wallet_address
from config import WALLET_PRIVATE_KEY


#to do 
PENDLE_CONTRACT_ADDRESS = "0x..."
PENDLE_CONTRACT_ABI = [...]

def get_yield_tokens():
    contract = web3.eth.contract(address=PENDLE_CONTRACT_ADDRESS, abi=PENDLE_CONTRACT_ABI)
    address = get_wallet_address()
    #Use contract functions to fetch yield tokens for the address
    #Example: contract.functions.balanceOf(address).call()
    return {'yield_tokens':"example"}

def tokenize_asset(assey_id):
    contract = web3.eth.contract(address=PENDLE_CONTRACT_ADDRESS, abi=PENDLE_CONTRACT_ABI)
    acct = web3.eth.account.from_key(WALLET_PRIVATE_KEY)
    #Build , sign, and send transaction
    #Example code:
    txn = contract.functions.tokenize(asset_id).build_transaction({
        'from': acct.address,
        'nonce': web3.eth.get_transaction_count(acct.address)
    })
    signed = acct.sign_transaction(txn)
    tx_harsh = web3.eth.send_raw_transaction(signed.rawTransaction)
    return {"tx_hash":tx_hash.hex()}