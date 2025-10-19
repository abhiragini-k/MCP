import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Arbitrum Sepolia Configuration
# This project is configured for Arbitrum Sepolia testnet
RPC_URL = os.getenv('RPC_URL', 'https://sepolia-rollup.arbitrum.io/rpc')
WALLET_PRIVATE_KEY = os.getenv('WALLET_PRIVATE_KEY')

# Network configuration for Arbitrum Sepolia
CHAIN_ID = 421614
PENDLE_CONTRACT_ADDRESS = os.getenv('PENDLE_CONTRACT_ADDRESS', 'TBD')  # Pendle not deployed on Arbitrum Sepolia yet

# Network info
NETWORK_INFO = {
    'name': 'Arbitrum Sepolia',
    'chain_id': 421614,
    'rpc_url': 'https://sepolia-rollup.arbitrum.io/rpc',
    'block_explorer': 'https://sepolia.arbiscan.io/',
    'currency_symbol': 'ETH',
    'is_testnet': True
}

