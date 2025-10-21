import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Network configuration
RPC_URL = os.getenv('RPC_URL', 'https://sepolia-rollup.arbitrum.io/rpc')
WALLET_PRIVATE_KEY = os.getenv('WALLET_PRIVATE_KEY')
PENDLE_CONTRACT_ADDRESS = os.getenv('PENDLE_CONTRACT_ADDRESS', 'TBD')

# Network info
NETWORK_INFO = {
    'name': 'Arbitrum Sepolia',
    'chain_id': 421614,
    'rpc_url': 'https://sepolia-rollup.arbitrum.io/rpc',
    'block_explorer': 'https://sepolia.arbiscan.io/',
    'currency_symbol': 'ETH',
    'is_testnet': True
}

