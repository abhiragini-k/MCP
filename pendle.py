import json
from wallet import web3, get_wallet_address
from config import WALLET_PRIVATE_KEY


#to do => done
PENDLE_CONTRACT_ADDRESS = "0x888888888889758F76e7103c6CbF23ABbF58F946"
                
#To load contract ABI from the saved JSON file
with open('abi/pendle_router_abi.json','r') as abi_files:
    PENDLE_CONTRACT_ABI = json.load(abi_files)

pendle_contract = web3.eth.contract(address=PENDLE_CONTRACT_ADDRESS, abi = PENDLE_CONTRACT_ABI)

# Function: Query yield tokens (update the function name after ABI inspection)
def get_yield_tokens():
    """Fetch yield tokens or user-related token info"""
    address = get_wallet_address()
    # Example: Suppose ABI exposes 'balanceOf' for yield tokens
    # Replace 'balanceOf' and 'yieldTokenAddress' after examining the actual ABI!
    # yield_token_address = "0x..."  # The actual YT token address
    # balance = contract.functions.balanceOf(address, yield_token_address).call()
    # For now, leave a placeholder or parse based on your ABI
    return {'yield_tokens': "example"}  # Replace this after ABI check

# Function: Tokenize an asset (function name and args must match ABI!)
def tokenize_asset(assey_id):
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