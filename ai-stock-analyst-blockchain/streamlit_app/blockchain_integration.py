"""
Blockchain Integration Module - Complete Professional Implementation
Manages all blockchain interactions for portfolio tracking on Ethereum
Supports Sepolia testnet and mainnet with comprehensive error handling
"""

from web3 import Web3
from eth_account import Account
import json
import os
from typing import Optional, Dict, List, Tuple, Any
from datetime import datetime
import warnings
import time

warnings.filterwarnings('ignore')


class BlockchainPortfolioManager:
    """
    Complete blockchain portfolio management system
    Handles Web3 connections, wallet management, and smart contract interactions
    """
    
    def __init__(self, provider_url: str = "http://127.0.0.1:8545"):
        """
        Initialize blockchain connection
        
        Args:
            provider_url: RPC endpoint URL (Alchemy, Infura, local node, etc.)
        """
        self.provider_url = provider_url
        self.w3 = None
        self.contract_address = None
        self.contract = None
        self.account = None
        self.private_key = None
        self.connected = False
        self.chain_id = None
        self.network_name = None
        
        # Connection statistics
        self.connection_attempts = 0
        self.last_connection_time = None
        
        # Initialize connection
        self._connect_to_provider()
    
    def _connect_to_provider(self) -> bool:
        """
        Establish connection to blockchain provider with retry logic
        
        Returns:
            True if connection successful, False otherwise
        """
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                self.connection_attempts += 1
                
                # Initialize Web3 connection
                self.w3 = Web3(Web3.HTTPProvider(self.provider_url))
                
                # Test connection
                if self.w3.is_connected():
                    # Get network information
                    self.chain_id = self.w3.eth.chain_id
                    block_number = self.w3.eth.block_number
                    self.last_connection_time = datetime.now()
                    
                    # Determine network name
                    self.network_name = self._get_network_name(self.chain_id)
                    
                    print(f"✅ Connected to blockchain")
                    print(f"   Network: {self.network_name}")
                    print(f"   Chain ID: {self.chain_id}")
                    print(f"   Block Number: {block_number}")
                    print(f"   Provider: {self.provider_url}")
                    print(f"   Attempt: {attempt + 1}/{max_retries}")
                    
                    self.connected = True
                    return True
                else:
                    print(f"⚠️  Connection attempt {attempt + 1} failed - not connected")
                    
            except Exception as e:
                print(f"❌ Connection attempt {attempt + 1} error: {str(e)}")
            
            # Wait before retry (except on last attempt)
            if attempt < max_retries - 1:
                print(f"   Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
        
        print(f"❌ Failed to connect after {max_retries} attempts")
        self.connected = False
        return False
    
    def _get_network_name(self, chain_id: int) -> str:
        """
        Get human-readable network name from chain ID
        
        Args:
            chain_id: Ethereum chain ID
            
        Returns:
            Network name string
        """
        networks = {
            1: "Ethereum Mainnet",
            3: "Ropsten Testnet (Deprecated)",
            4: "Rinkeby Testnet (Deprecated)",
            5: "Goerli Testnet",
            11155111: "Sepolia Testnet",
            137: "Polygon Mainnet",
            80001: "Mumbai Testnet",
            56: "BSC Mainnet",
            97: "BSC Testnet"
        }
        return networks.get(chain_id, f"Unknown Network (Chain ID: {chain_id})")
    
    def reconnect(self) -> bool:
        """
        Attempt to reconnect to blockchain provider
        
        Returns:
            True if reconnection successful
        """
        print("\n🔄 Attempting to reconnect...")
        self.connected = False
        return self._connect_to_provider()
    
    def connect_wallet(self, private_key: str) -> Optional[str]:
        """
        Connect user wallet using private key with validation
        
        Args:
            private_key: Ethereum private key (with or without 0x prefix)
            
        Returns:
            Wallet address if successful, None otherwise
        """
        if not self.connected:
            print("❌ Not connected to blockchain provider")
            print("   Attempting to reconnect...")
            if not self.reconnect():
                return None
        
        try:
            # Normalize private key format
            if not private_key.startswith('0x'):
                private_key = '0x' + private_key
            
            # Validate private key length
            if len(private_key) != 66:  # 0x + 64 hex characters
                print(f"❌ Invalid private key length: {len(private_key)} (expected 66)")
                return None
            
            # Create account from private key
            self.private_key = private_key
            self.account = Account.from_key(private_key)
            
            # Get wallet balance
            balance = self.w3.eth.get_balance(self.account.address)
            balance_eth = self.w3.from_wei(balance, 'ether')
            
            # Get transaction count (nonce)
            tx_count = self.w3.eth.get_transaction_count(self.account.address)
            
            print(f"\n✅ Wallet Connected Successfully")
            print(f"   Network: {self.network_name}")
            print(f"   Address: {self.account.address}")
            print(f"   Balance: {balance_eth:.6f} ETH")
            print(f"   Transactions: {tx_count}")
            
            if balance == 0:
                print(f"   ⚠️  Warning: Zero balance - cannot send transactions")
                print(f"   Get testnet ETH from faucets:")
                if self.chain_id == 11155111:
                    print(f"   - https://sepoliafaucet.com/")
                    print(f"   - https://www.alchemy.com/faucets/ethereum-sepolia")
            
            return self.account.address
            
        except ValueError as e:
            print(f"❌ Invalid private key format: {str(e)}")
            self.account = None
            self.private_key = None
            return None
        except Exception as e:
            print(f"❌ Wallet connection failed: {str(e)}")
            self.account = None
            self.private_key = None
            return None
    
    def get_balance(self) -> float:
        """
        Get wallet balance in ETH
        
        Returns:
            Balance in ETH, 0.0 if error
        """
        try:
            if self.connected and self.account:
                balance_wei = self.w3.eth.get_balance(self.account.address)
                balance_eth = self.w3.from_wei(balance_wei, 'ether')
                return float(balance_eth)
            return 0.0
        except Exception as e:
            print(f"Error getting balance: {str(e)}")
            return 0.0
    
    def load_contract(self, contract_address: str, abi_path: str = None) -> bool:
        """
        Load and verify smart contract connection
        
        Args:
            contract_address: Deployed contract address
            abi_path: Path to ABI JSON file (optional)
            
        Returns:
            True if contract loaded successfully
        """
        if not self.connected:
            print("❌ Not connected to blockchain")
            return False
        
        try:
            # Convert to checksum address
            self.contract_address = Web3.to_checksum_address(contract_address)
            
            # Determine ABI path
            if abi_path is None:
                abi_path = os.path.join(os.path.dirname(__file__), 'contract_abi.json')
            
            # Check if ABI file exists
            if not os.path.exists(abi_path):
                print(f"❌ ABI file not found: {abi_path}")
                print(f"   Please ensure contract_abi.json is in the same directory")
                return False
            
            # Load ABI
            with open(abi_path, 'r') as f:
                contract_abi = json.load(f)
            
            # Create contract instance
            self.contract = self.w3.eth.contract(
                address=self.contract_address,
                abi=contract_abi
            )
            
            # Verify contract by calling read-only function
            try:
                counter = self.contract.functions.investmentCounter().call()
                
                print(f"\n✅ Contract Loaded Successfully")
                print(f"   Address: {self.contract_address}")
                print(f"   Network: {self.network_name}")
                print(f"   Total Investments: {counter}")
                print(f"   Etherscan: https://sepolia.etherscan.io/address/{self.contract_address}")
                
                return True
                
            except Exception as verify_error:
                print(f"⚠️  Contract loaded but verification failed")
                print(f"   Error: {str(verify_error)}")
                print(f"   Contract may not be deployed or ABI mismatch")
                return False
            
        except ValueError as e:
            print(f"❌ Invalid contract address: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Contract loading failed: {str(e)}")
            return False
    
    def add_investment_to_blockchain(
        self,
        company: str,
        symbol: str,
        shares: float,
        purchase_price: float
    ) -> Optional[Tuple[str, int, float]]:
        """
        Add investment to blockchain with comprehensive transaction handling
        
        Args:
            company: Company name
            symbol: Stock symbol
            shares: Number of shares (will be converted to uint)
            purchase_price: Purchase price per share (will be converted to uint)
            
        Returns:
            Tuple of (transaction_hash, gas_used, cost_in_eth) if successful, None otherwise
        """
        if not self.contract or not self.account:
            print("❌ Contract or wallet not connected")
            return None
        
        try:
            # Convert to contract-compatible format (multiply by 100 to preserve decimals)
            shares_uint = int(shares * 100)
            price_uint = int(purchase_price * 100)
            
            print(f"\n⏳ Preparing blockchain transaction...")
            print(f"   Company: {company}")
            print(f"   Symbol: {symbol}")
            print(f"   Shares: {shares} ({shares_uint} on-chain)")
            print(f"   Price: ${purchase_price} (${price_uint} on-chain)")
            
            # Estimate gas
            try:
                gas_estimate = self.contract.functions.addInvestment(
                    company,
                    symbol,
                    shares_uint,
                    price_uint
                ).estimate_gas({'from': self.account.address})
                
                print(f"   Estimated Gas: {gas_estimate}")
            except Exception as gas_error:
                print(f"   ⚠️  Gas estimation failed: {str(gas_error)}")
                gas_estimate = 300000  # Fallback gas limit
                print(f"   Using fallback gas: {gas_estimate}")
            
            # Get current gas price
            gas_price = self.w3.eth.gas_price
            gas_price_gwei = self.w3.from_wei(gas_price, 'gwei')
            print(f"   Gas Price: {gas_price_gwei:.2f} Gwei")
            
            # Calculate estimated cost
            estimated_cost = gas_estimate * gas_price
            estimated_cost_eth = self.w3.from_wei(estimated_cost, 'ether')
            print(f"   Estimated Cost: {estimated_cost_eth:.6f} ETH")
            
            # Check balance
            balance = self.w3.eth.get_balance(self.account.address)
            if balance < estimated_cost:
                balance_eth = self.w3.from_wei(balance, 'ether')
                print(f"   ❌ Insufficient balance: {balance_eth:.6f} ETH")
                print(f"   Required: {estimated_cost_eth:.6f} ETH")
                return None
            
            # Build transaction
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            
            transaction = self.contract.functions.addInvestment(
                company,
                symbol,
                shares_uint,
                price_uint
            ).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': int(gas_estimate * 1.2),  # Add 20% buffer
                'gasPrice': gas_price,
                'chainId': self.chain_id
            })
            
            # Sign transaction
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction,
                self.private_key
            )
            
            # Send transaction
            print(f"\n📤 Sending transaction...")
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            tx_hash_hex = tx_hash.hex()
            
            print(f"   Transaction Hash: {tx_hash_hex}")
            print(f"   View on Etherscan: https://sepolia.etherscan.io/tx/{tx_hash_hex}")
            print(f"   ⏳ Waiting for confirmation (may take 10-30 seconds)...")
            
            # Wait for transaction receipt with timeout
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            # Check transaction status
            if tx_receipt['status'] == 1:
                actual_cost = tx_receipt['gasUsed'] * gas_price
                actual_cost_eth = self.w3.from_wei(actual_cost, 'ether')
                
                print(f"\n   ✅ Transaction Confirmed!")
                print(f"   Block Number: {tx_receipt['blockNumber']}")
                print(f"   Gas Used: {tx_receipt['gasUsed']}")
                print(f"   Actual Cost: {actual_cost_eth:.6f} ETH")
                
                return (tx_hash_hex, tx_receipt['gasUsed'], actual_cost_eth)
            else:
                print(f"\n   ❌ Transaction Failed")
                print(f"   Block: {tx_receipt['blockNumber']}")
                return None
                
        except Exception as e:
            print(f"\n❌ Blockchain transaction error: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            return None
    
    def get_my_investments(self) -> List[Dict[str, Any]]:
        """
        Fetch all active investments from blockchain with detailed information
        
        Returns:
            List of investment dictionaries with complete data
        """
        if not self.contract or not self.account:
            print("❌ Contract or wallet not connected")
            return []
        
        try:
            print(f"\n⏳ Fetching investments from blockchain...")
            print(f"   Wallet: {self.account.address}")
            
            # Get all investment IDs for this wallet
            investment_ids = self.contract.functions.getMyInvestmentIds().call({
                'from': self.account.address
            })
            
            total_count = len(investment_ids)
            print(f"   Found {total_count} total investment(s)")
            
            if total_count == 0:
                print(f"   No investments found on blockchain")
                return []
            
            investments = []
            active_count = 0
            
            # Fetch each investment
            for idx, inv_id in enumerate(investment_ids, 1):
                try:
                    print(f"   Fetching {idx}/{total_count}...", end='\r')
                    
                    # Call contract to get investment data
                    inv_data = self.contract.functions.getInvestment(inv_id).call({
                        'from': self.account.address
                    })
                    
                    # Parse investment data (only active investments)
                    if inv_data[5]:  # Check if active
                        active_count += 1
                        
                        investment = {
                            'blockchain_id': int(inv_id),
                            'company': inv_data[0],
                            'symbol': inv_data[1],
                            'shares': float(inv_data[2]) / 100,  # Convert back from uint
                            'purchase_price': float(inv_data[3]) / 100,  # Convert back from uint
                            'timestamp': int(inv_data[4]),
                            'purchase_date': datetime.fromtimestamp(inv_data[4]).strftime("%Y-%m-%d"),
                            'purchase_datetime': datetime.fromtimestamp(inv_data[4]).strftime("%Y-%m-%d %H:%M:%S"),
                            'active': inv_data[5],
                            'total_cost': (float(inv_data[2]) / 100) * (float(inv_data[3]) / 100)
                        }
                        
                        investments.append(investment)
                
                except Exception as e:
                    print(f"\n   ⚠️  Error fetching investment {inv_id}: {str(e)}")
                    continue
            
            print(f"\n   ✅ Retrieved {active_count} active investment(s)")
            
            # Sort by timestamp (newest first)
            investments.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return investments
            
        except Exception as e:
            print(f"❌ Error fetching investments: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            return []
    
    def remove_investment_from_blockchain(self, investment_id: int) -> Optional[str]:
        """
        Remove (deactivate) investment from blockchain
        
        Args:
            investment_id: Blockchain investment ID
            
        Returns:
            Transaction hash if successful, None otherwise
        """
        if not self.contract or not self.account:
            print("❌ Contract or wallet not connected")
            return None
        
        try:
            print(f"\n⏳ Removing investment #{investment_id} from blockchain...")
            
            # Estimate gas
            gas_estimate = self.contract.functions.removeInvestment(
                investment_id
            ).estimate_gas({'from': self.account.address})
            
            # Build transaction
            transaction = self.contract.functions.removeInvestment(
                investment_id
            ).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': int(gas_estimate * 1.2),
                'gasPrice': self.w3.eth.gas_price,
                'chainId': self.chain_id
            })
            
            # Sign and send
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction,
                self.private_key
            )
            
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            print(f"   Transaction sent: {tx_hash.hex()}")
            print(f"   Waiting for confirmation...")
            
            # Wait for receipt
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            if tx_receipt['status'] == 1:
                print(f"   ✅ Investment removed successfully")
                print(f"   TX: {tx_hash.hex()}")
                return tx_hash.hex()
            else:
                print(f"   ❌ Removal transaction failed")
                return None
                
        except Exception as e:
            print(f"❌ Error removing investment: {str(e)}")
            return None
    
    def get_portfolio_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive portfolio statistics from blockchain
        
        Returns:
            Dictionary with portfolio statistics
        """
        if not self.contract or not self.account:
            return {
                'error': 'Contract or wallet not connected',
                'connected': False
            }
        
        try:
            # Get active investment count
            active_count = self.contract.functions.getActiveInvestmentCount().call({
                'from': self.account.address
            })
            
            # Get total invested amount
            total_invested = self.contract.functions.getTotalInvested().call({
                'from': self.account.address
            })
            
            # Get wallet balance
            balance = self.w3.eth.get_balance(self.account.address)
            balance_eth = self.w3.from_wei(balance, 'ether')
            
            return {
                'connected': True,
                'active_count': int(active_count),
                'total_invested': float(total_invested) / 10000,  # Convert from uint
                'wallet_address': self.account.address,
                'wallet_balance': float(balance_eth),
                'contract_address': self.contract_address,
                'network': self.network_name,
                'chain_id': self.chain_id
            }
            
        except Exception as e:
            print(f"Error getting stats: {str(e)}")
            return {
                'error': str(e),
                'connected': True
            }
    
    def verify_transaction(self, tx_hash: str) -> Dict[str, Any]:
        """
        Verify and get detailed information about a blockchain transaction
        
        Args:
            tx_hash: Transaction hash (with or without 0x prefix)
            
        Returns:
            Dictionary with transaction details
        """
        if not self.connected:
            return {'confirmed': False, 'error': 'Not connected to blockchain'}
        
        try:
            # Normalize hash
            if not tx_hash.startswith('0x'):
                tx_hash = '0x' + tx_hash
            
            # Get transaction receipt
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            
            # Get transaction details
            tx = self.w3.eth.get_transaction(tx_hash)
            
            # Get block timestamp
            block = self.w3.eth.get_block(receipt['blockNumber'])
            timestamp = datetime.fromtimestamp(block['timestamp'])
            
            # Calculate cost
            gas_cost = receipt['gasUsed'] * tx['gasPrice']
            cost_eth = self.w3.from_wei(gas_cost, 'ether')
            
            return {
                'confirmed': receipt['status'] == 1,
                'block_number': receipt['blockNumber'],
                'block_timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                'gas_used': receipt['gasUsed'],
                'gas_price_gwei': self.w3.from_wei(tx['gasPrice'], 'gwei'),
                'transaction_cost_eth': float(cost_eth),
                'transaction_hash': tx_hash,
                'from_address': receipt['from'],
                'to_address': receipt['to'],
                'etherscan_url': f"https://sepolia.etherscan.io/tx/{tx_hash}"
            }
            
        except Exception as e:
            return {
                'confirmed': False,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def get_connection_info(self) -> str:
        """
        Get formatted connection information for display
        
        Returns:
            Formatted string with connection details
        """
        if not self.connected:
            return "❌ Not connected to blockchain"
        
        info = f"""
🔗 **Blockchain Connection Status**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Network:** {self.network_name}
**Chain ID:** {self.chain_id}
**Provider:** {self.provider_url}
**Block Number:** {self.w3.eth.block_number}
**Connection Time:** {self.last_connection_time.strftime("%Y-%m-%d %H:%M:%S") if self.last_connection_time else 'N/A'}
"""
        
        if self.account:
            balance = self.w3.eth.get_balance(self.account.address)
            balance_eth = self.w3.from_wei(balance, 'ether')
            tx_count = self.w3.eth.get_transaction_count(self.account.address)
            
            info += f"""
**Wallet Address:** `{self.account.address}`
**Balance:** {balance_eth:.6f} ETH
**Transaction Count:** {tx_count}
"""
        
        if self.contract_address:
            info += f"""
**Contract Address:** `{self.contract_address}`
**Etherscan:** https://sepolia.etherscan.io/address/{self.contract_address}
"""
        
        info += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        return info
    
    def disconnect(self):
        """Safely disconnect from blockchain and clear sensitive data"""
        print("\n🔌 Disconnecting from blockchain...")
        
        self.account = None
        self.private_key = None
        self.contract = None
        self.connected = False
        
        print("   ✅ Disconnected successfully")
