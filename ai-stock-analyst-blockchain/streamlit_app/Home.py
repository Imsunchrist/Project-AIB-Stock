"""
AI Stock Analyst with Blockchain - Streamlit Version
Main entry point for Streamlit Cloud deployment
"""

import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import backend modules
from stock_advisor_finnhub import StockAdvisorFinnhub
from portfolio_manager import BlockchainPortfolioManagerEnhanced
from blockchain_integration import BlockchainPortfolioManager

# Page configuration
st.set_page_config(
    page_title="AI Stock Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/TheHashiramaSenju',
        'Report a bug': 'https://github.com/TheHashiramaSenju',
        'About': '# AI Stock Analyst with Blockchain\nBuilt by TheHashiramaSenju'
    }
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        text-align: center;
        color: #888;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stMetric {
        background-color: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #444;
    }
    .info-box {
        background-color: #1e3a5f;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    
    # Get Finnhub API key from secrets
    if 'finnhub_key' not in st.session_state:
        st.session_state.finnhub_key = st.secrets.get("FINNHUB_API_KEY", "d415bmpr01qo6qdf06d0d415bmpr01qo6qdf06dg")
    
    # Initialize StockAdvisorFinnhub
    if 'advisor' not in st.session_state:
        st.session_state.advisor = StockAdvisorFinnhub(st.session_state.finnhub_key)
    
    # Initialize portfolio manager
    if 'portfolio_manager' not in st.session_state:
        st.session_state.portfolio_manager = BlockchainPortfolioManagerEnhanced(
            blockchain_enabled=True
        )
        # Set the Finnhub advisor for portfolio manager
        st.session_state.portfolio_manager.set_stock_advisor(st.session_state.advisor)
    
    # Wallet connection status
    if 'wallet_connected' not in st.session_state:
        st.session_state.wallet_connected = False
    
    # Blockchain configuration
    if 'contract_address' not in st.session_state:
        st.session_state.contract_address = st.secrets.get("CONTRACT_ADDRESS", "")
    
    if 'rpc_url' not in st.session_state:
        st.session_state.rpc_url = st.secrets.get("RPC_URL", "")
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = "streamlit_user"

# Call initialization
init_session_state()

# Header
st.markdown('<h1 class="main-header">🚀 AI Stock Analyst with Blockchain</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Real-time AI-powered stock analysis on Ethereum blockchain</p>', unsafe_allow_html=True)

# Main content
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-box">
        <h3>📊 Stock Analysis</h3>
        <p>AI-powered technical analysis with RSI, MACD, Bollinger Bands powered by Finnhub. Get buy/sell/hold recommendations with confidence scores.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-box">
        <h3>💼 Portfolio Tracking</h3>
        <p>Manage your investments with real-time valuations. Store your portfolio on Ethereum blockchain for immutable records.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-box">
        <h3>🔗 Blockchain Storage</h3>
        <p>Connect your wallet to store investments permanently on Sepolia testnet. Your keys, your data.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Quick stats
st.subheader("📈 Quick Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Supported Stocks",
        value="80+",
        help="Major US stocks via Finnhub"
    )

with col2:
    st.metric(
        label="Technical Indicators",
        value="5+",
        help="RSI, MACD, SMA, Bollinger Bands, ATR"
    )

with col3:
    st.metric(
        label="Network",
        value="Sepolia",
        help="Ethereum testnet"
    )

with col4:
    if st.session_state.wallet_connected:
        st.metric(
            label="Wallet Status",
            value="Connected ✅",
            delta="Active"
        )
    else:
        st.metric(
            label="Wallet Status",
            value="Not Connected",
            delta="Connect in sidebar"
        )

st.divider()

# Features section
st.subheader("✨ Key Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **🤖 AI-Powered Analysis**
    - Real-time stock data from Finnhub API
    - Technical indicators (RSI, MACD, Bollinger Bands)
    - AI-generated buy/sell/hold recommendations
    - Confidence scoring (0-100%)
    - Support for 80+ US companies
    - 60 API calls per minute (no rate limiting!)
    
    **💼 Portfolio Management**
    - Add, view, and track investments
    - Real-time portfolio valuation
    - Gain/loss tracking with percentages
    - Historical purchase records
    """)

with col2:
    st.markdown("""
    **🔗 Blockchain Integration**
    - Ethereum smart contract storage
    - Sepolia testnet deployment
    - Wallet connection
    - Immutable investment records
    - Gas-optimized transactions
    
    **📊 Advanced Features**
    - Stock comparison tool
    - Market overview dashboard
    - Company profiles and news
    - Volatility analysis
    """)

st.divider()

# How to use
st.subheader("🚀 How to Use")

with st.expander("1️⃣ Analyze Stocks (No wallet needed)", expanded=True):
    st.markdown("""
    - Navigate to **"📊 Stock Analysis"** page (left sidebar)
    - Enter any company name or US stock symbol (e.g., "AAPL", "MSFT", "TSLA")
    - Click **"Analyze Stock"** button
    - View AI recommendations, technical indicators, and trading signals
    - **No wallet connection required!**
    - **No rate limiting** - powered by Finnhub with 60 calls/minute
    """)

with st.expander("2️⃣ Connect Your Wallet"):
    st.markdown("""
    - Get testnet ETH from [Sepolia Faucet](https://sepoliafaucet.com/)
    - Open sidebar on the left
    - Enter your **testnet wallet private key** (NEVER use mainnet key!)
    - Click **"Connect Wallet"**
    - See connection confirmation with wallet address
    """)

with st.expander("3️⃣ Manage Portfolio"):
    st.markdown("""
    - Navigate to **"💼 Portfolio"** page
    - Connect wallet first (if not already connected)
    - Fill in investment details:
      - Company name (e.g., "AAPL", "MSFT")
      - Number of shares
      - Purchase price
      - Purchase date
    - Click **"Add to Blockchain"**
    - Transaction will be sent to Sepolia testnet (~10-15 seconds)
    - View your portfolio with real-time valuations
    """)

st.divider()

# Blockchain info
st.subheader("🔗 Blockchain Information")

col1, col2 = st.columns(2)

with col1:
    contract_display = f"`{st.session_state.contract_address[:10]}...`" if st.session_state.contract_address else "Not configured"
    st.markdown(f"""
    **Network Details:**
    - Network: Sepolia Testnet
    - Chain ID: 11155111
    - Contract Address: {contract_display}
    - [View on Etherscan](https://sepolia.etherscan.io/address/{st.session_state.contract_address})
    """)

with col2:
    st.markdown("""
    **Get Testnet ETH:**
    - [Alchemy Sepolia Faucet](https://www.alchemy.com/faucets/ethereum-sepolia)
    - [Sepolia Faucet](https://sepoliafaucet.com/)
    - [Infura Faucet](https://www.infura.io/faucet/sepolia)
    
    **⚠️ Important:**
    - This is TESTNET only
    - Never use mainnet private keys
    - Testnet ETH has no real value
    """)

st.divider()

# API Info
st.subheader("⚡ API Information")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Stock Data Provider:**
    - **API**: Finnhub (Professional-grade)
    - **Rate Limit**: 60 calls/minute
    - **Data Quality**: Real-time, high accuracy
    - **Coverage**: US stocks, real-time quotes
    - **Status**: ✅ Active
    """)

with col2:
    st.markdown("""
    **Why Finnhub?**
    - ✅ No rate limiting issues
    - ✅ Reliable and fast
    - ✅ Real-time data
    - ✅ Company profiles included
    - ✅ Free tier is generous
    """)

st.divider()

# Footer
st.markdown("""
---
<div style='text-align: center'>
    <p><strong>AI Stock Analyst v2.0.0</strong> | Built with ❤️ by TheHashiramaSenju</p>
    <p>Powered by Streamlit, Finnhub API, Web3.py, and Ethereum blockchain</p>
    <p>
        <a href="https://github.com/TheHashiramaSenju" target="_blank">GitHub</a> • 
        <a href="https://sepolia.etherscan.io/address/{}" target="_blank">Contract</a> • 
        <a href="https://finnhub.io" target="_blank">Finnhub API</a>
    </p>
</div>
""".format(st.session_state.contract_address), unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.header("🔗 Blockchain Connection")
    
    if not st.session_state.wallet_connected:
        st.info("Connect your wallet to use blockchain features")
        
        st.markdown("**Network:** Sepolia Testnet")
        contract_display = f"`{st.session_state.contract_address[:10]}...`" if st.session_state.contract_address else "Not configured"
        st.markdown(f"**Contract:** {contract_display}")
        
        with st.form("wallet_form"):
            private_key = st.text_input(
                "Private Key (Testnet only!)",
                type="password",
                help="Enter your Sepolia testnet wallet private key. NEVER use your mainnet key!"
            )
            
            submit = st.form_submit_button("🔐 Connect Wallet", type="primary", use_container_width=True)
            
            if submit:
                if private_key and st.session_state.contract_address and st.session_state.rpc_url:
                    with st.spinner("Connecting to blockchain..."):
                        try:
                            result = st.session_state.portfolio_manager.connect_blockchain(
                                private_key,
                                st.session_state.contract_address,
                                None
                            )
                            
                            if "Connected Successfully" in result:
                                st.session_state.wallet_connected = True
                                st.success("✅ Wallet connected!")
                                st.rerun()
                            else:
                                st.error(result)
                        except Exception as e:
                            st.error(f"Connection failed: {str(e)}")
                else:
                    st.warning("Please enter your private key and ensure contract is configured")
    else:
        st.success("✅ Wallet Connected")
        
        if st.session_state.portfolio_manager.blockchain and st.session_state.portfolio_manager.blockchain.account:
            wallet_addr = st.session_state.portfolio_manager.blockchain.account.address
            
            try:
                balance = st.session_state.portfolio_manager.blockchain.get_balance()
            except:
                balance = 0.0
            
            st.markdown(f"""
            **Address:**  
            `{wallet_addr[:10]}...{wallet_addr[-8:]}`
            
            **Balance:**  
            {balance:.6f} ETH
            """)
        
        if st.button("🔌 Disconnect", use_container_width=True, type="secondary"):
            st.session_state.wallet_connected = False
            st.rerun()
    
    st.divider()
    
    st.markdown("""
    **📚 Resources:**
    - [Get Testnet ETH](https://sepoliafaucet.com/)
    - [View Contract](https://sepolia.etherscan.io)
    - [Finnhub API](https://finnhub.io)
    - [GitHub Repo](https://github.com/TheHashiramaSenju)
    """)
