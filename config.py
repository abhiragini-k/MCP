import os
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv('RPC_URL')
WALLET_PRIVATE_KEY = os.getenv('WALLET_PRIVATE_KEY')

