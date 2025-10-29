import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
from backend.blockchain_integration import BlockchainPortfolioManager
import os


class PortfolioManager:
    """Traditional portfolio management (local storage)"""
    
    def __init__(self):
        self.user_portfolios = {}
    
    def add_investment(self, user_id: str, company: str, shares: float, 
                      purchase_price: float, purchase_date: str = None) -> str:
        """Add investment to user's portfolio"""
        if user_id not in self.user_portfolios:
            self.user_portfolios[user_id] = []
        
        if purchase_date is None:
            purchase_date = datetime.now().strftime("%Y-%m-%d")
        
        investment = {
            'company': company,
            'shares': float(shares),
            'purchase_price': float(purchase_price),
            'purchase_date': purchase_date,
            'investment_id': f"{company}_{datetime.now().timestamp()}"
        }
        
        self.user_portfolios[user_id].append(investment)
        
        return f"✅ Added {shares} shares of {company} at ${purchase_price} per share"
    
    def get_portfolio(self, user_id: str) -> List[Dict]:
        """Get user's portfolio"""
        return self.user_portfolios.get(user_id, [])
    
    def remove_investment(self, user_id: str, investment_id: str) -> str:
        """Remove investment from portfolio"""
        if user_id not in self.user_portfolios:
            return "❌ No portfolio found"
        
        portfolio = self.user_portfolios[user_id]
        initial_length = len(portfolio)
        
        self.user_portfolios[user_id] = [
            inv for inv in portfolio 
            if inv['investment_id'] != investment_id
        ]
        
        if len(self.user_portfolios[user_id]) < initial_length:
            return "✅ Investment removed successfully"
        else:
            return "❌ Investment not found"
    
    def calculate_portfolio_value(self, user_id: str, stock_advisor) -> Dict:
        """Calculate current portfolio value"""
        portfolio = self.get_portfolio(user_id)
        
        if not portfolio:
            return {
                'total_invested': 0,
                'current_value': 0,
                'gain_loss': 0,
                'gain_loss_pct': 0
            }
        
        total_invested = 0
        current_value = 0
        
        for investment in portfolio:
            invested = investment['shares'] * investment['purchase_price']
            total_invested += invested
            
            symbol = stock_advisor.smart_symbol_lookup(investment['company'])
            current_price = stock_advisor.get_current_price(symbol)
            
            if current_price > 0:
                current_value += investment['shares'] * current_price
            else:
                current_value += invested
        
        gain_loss = current_value - total_invested
        gain_loss_pct = (gain_loss / total_invested * 100) if total_invested > 0 else 0
        
        return {
            'total_invested': total_invested,
            'current_value': current_value,
            'gain_loss': gain_loss,
            'gain_loss_pct': gain_loss_pct
        }


class BlockchainPortfolioManagerEnhanced(PortfolioManager):
    """Enhanced portfolio manager with blockchain integration"""
    
    def __init__(self, blockchain_enabled: bool = False):
        super().__init__()
        self.blockchain_enabled = blockchain_enabled
        self.blockchain = None
        self.stock_advisor = None
        
        if blockchain_enabled:
            rpc_url = os.getenv('RPC_URL', 'http://127.0.0.1:8545')
            self.blockchain = BlockchainPortfolioManager(rpc_url)
    
    def set_stock_advisor(self, advisor):
        """Set stock advisor reference"""
        self.stock_advisor = advisor
    
    def connect_blockchain(self, private_key: str, contract_address: str, 
                          abi_path: str = None) -> str:
        """Initialize blockchain connection"""
        if not self.blockchain_enabled:
            return "❌ Blockchain not enabled"
        
        try:
            wallet_address = self.blockchain.connect_wallet(private_key)
            if not wallet_address:
                return "❌ Failed to connect wallet"
            
            success = self.blockchain.load_contract(contract_address, abi_path)
            
            if success:
                return f"""✅ **Blockchain Connected Successfully**

📍 **Wallet Address:** `{wallet_address}`
🔗 **Contract Address:** `{contract_address}`
⛓️ **Chain ID:** {self.blockchain.w3.eth.chain_id}
📦 **Block Number:** {self.blockchain.w3.eth.block_number}

🚀 Ready to track investments on blockchain!"""
            else:
                return "❌ Failed to load smart contract"
                
        except Exception as e:
            return f"❌ Connection failed: {str(e)}"
    
    def add_investment_blockchain(self, user_id: str, company: str, shares: float,
                                 purchase_price: float, purchase_date: str = None) -> str:
        """Add investment to both local and blockchain"""
        local_result = super().add_investment(user_id, company, shares, 
                                            purchase_price, purchase_date)
        
        if self.blockchain_enabled and self.blockchain.account and self.stock_advisor:
            symbol = self.stock_advisor.smart_symbol_lookup(company)
            if symbol:
                result = self.blockchain.add_investment_to_blockchain(
                    company, symbol, float(shares), float(purchase_price)
                )
                
                if result:
                    tx_hash, gas_used = result
                    return f"""{local_result}

🔗 **Blockchain Confirmation**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Transaction Hash: `{tx_hash}`
Gas Used: {gas_used}
✅ Investment permanently recorded on blockchain!"""
                else:
                    return f"{local_result}\n\n⚠️ Blockchain write failed (saved locally only)"
        
        return local_result
    
    def sync_from_blockchain(self, user_id: str) -> str:
        """Sync portfolio from blockchain"""
        if not self.blockchain_enabled or not self.blockchain.account:
            return "❌ Blockchain not connected"
        
        try:
            blockchain_investments = self.blockchain.get_my_investments()
            
            if not blockchain_investments:
                return "📭 No investments found on blockchain"
            
            self.user_portfolios[user_id] = []
            
            for inv in blockchain_investments:
                investment = {
                    'company': inv['company'],
                    'shares': inv['shares'],
                    'purchase_price': inv['purchase_price'],
                    'purchase_date': inv['purchase_date'],
                    'investment_id': f"{inv['company']}_{inv['timestamp']}",
                    'blockchain_id': inv['blockchain_id']
                }
                self.user_portfolios[user_id].append(investment)
            
            count = len(blockchain_investments)
            return f"""✅ **Blockchain Sync Complete**

📊 Synced {count} investment{'s' if count != 1 else ''}
🔐 All investments verified on blockchain
⏰ Last sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
            
        except Exception as e:
            return f"❌ Sync failed: {str(e)}"
    
    def get_blockchain_stats(self) -> str:
        """Get blockchain portfolio statistics"""
        if not self.blockchain_enabled or not self.blockchain.account:
            return "❌ Blockchain not connected"
        
        try:
            stats = self.blockchain.get_portfolio_stats()
            
            return f"""
📊 **Blockchain Portfolio Statistics**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Active Investments: {stats.get('active_count', 0)}
Total Invested: ${stats.get('total_invested', 0):.2f}
Wallet: `{stats.get('wallet_address', 'N/A')}`
Contract: `{stats.get('contract_address', 'N/A')}`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        except Exception as e:
            return f"❌ Error fetching stats: {str(e)}"