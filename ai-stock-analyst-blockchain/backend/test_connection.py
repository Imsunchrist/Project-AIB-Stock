from blockchain_integration import BlockchainPortfolioManager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

rpc_url = os.getenv('RPC_URL')
contract_address = os.getenv('CONTRACT_ADDRESS')

print(f"✅ Configuration loaded:")
print(f"   RPC: {rpc_url}")
print(f"   Contract: {contract_address}")
print(f"\n🔗 Testing blockchain connection...")

blockchain = BlockchainPortfolioManager(rpc_url)
if blockchain.connected:
    print(f"✅ Connected to Sepolia!")
    print(f"   Chain ID: {blockchain.w3.eth.chain_id}")
    print(f"   Block: {blockchain.w3.eth.block_number}")
else:
    print("❌ Connection failed!")
