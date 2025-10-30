"""
AI Stock Analyst with Blockchain - Streamlit Version
Main entry point - Optimized for both light and dark modes
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
        'Get Help': 'https://github.com/TheBhoomikaM',
        'Report a bug': 'https://github.com/TheBhoomikaM',
        'About': '# AI Stock Analyst with Blockchain\nBuilt by TheBhoomikaM'
    }
)

# Custom CSS - Optimized for BOTH light and dark modes
st.markdown("""
<style>
    /* Main header gradient - visible in both modes */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    
    /* Subheader - blue color visible in both modes */
    .sub-header {
        text-align: center;
        color: #1f77b4 !important;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 600;
    }
    
    /* Info boxes - gradient background with white text */
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .info-box h3 {
        color: white !important;
        margin-top: 0;
        font-size: 1.3rem;
        font-weight: 700;
    }
    .info-box p {
        color: white !important;
        opacity: 0.95;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* Metrics - gradient background */
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border: none !important;
    }
    .stMetric label {
        color: white !important;
        font-weight: 600;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2rem !important;
        font-weight: bold !important;
    }
    .stMetric [data-testid="stMetricDelta"] {
        color: white !important;
    }
    
    /* Expander headers */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1.1rem;
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
        <p>AI-powered technical analysis with RSI, MACD, Bollinger Bands. Get buy/sell/hold recommendations with confidence scores from advanced machine learning models.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-box">
        <h3>💼 Portfolio Tracking</h3>
        <p>Manage your investments with real-time valuations. Store your portfolio on Ethereum blockchain for immutable, tamper-proof records.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-box">
        <h3>🔗 Blockchain Storage</h3>
        <p>Connect your wallet to store investments permanently on Sepolia testnet. Full ownership - your keys, your data, your control.</p>
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
        help="Major US stocks via Finnhub API"
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
        help="Ethereum Sepolia testnet"
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
    - Advanced technical indicators (RSI, MACD, Bollinger Bands)
    - Machine learning-powered buy/sell/hold recommendations
    - Confidence scoring (50-95%) based on signal strength
    - Support for 80+ major US companies
    - 60 API calls per minute - zero rate limiting!
    
    **💼 Portfolio Management**
    - Add, view, and track investments in real-time
    - Live portfolio valuation with current prices
    - Gain/loss tracking with detailed percentages
    - Historical purchase records on blockchain
    - Export functionality for tax purposes
    """)

with col2:
    st.markdown("""
    **🔗 Blockchain Integration**
    - Ethereum smart contract storage (Sepolia testnet)
    - Immutable investment records
    - Wallet connection with MetaMask support
    - Gas-optimized transactions
    - Transparent on-chain verification
    
    **📊 Advanced Analytics**
    - Interactive price charts with technical overlays
    - Volume analysis and trends
    - Volatility calculations
    - Market sentiment indicators
    - Company profile information
    - Real-time news integration
    """)

st.divider()

# How to use
st.subheader("🚀 How to Use")

with st.expander("1️⃣ Analyze Stocks (No wallet needed)", expanded=True):
    st.markdown("""
    - Navigate to **"📊 Stock Analysis"** page in left sidebar
    - Enter any company name or US stock symbol (e.g., "AAPL", "MSFT", "TSLA")
    - Click **"Analyze Stock"** button
    - View comprehensive AI recommendations with:
      - Buy/Sell/Hold recommendation with confidence score
      - Technical indicators (RSI, MACD, Moving Averages)
      - Trading signals with detailed explanations
      - Interactive charts and visualizations
    - **No wallet connection required!**
    - **No rate limiting** - powered by Finnhub with 60 calls/minute
    """)

with st.expander("2️⃣ Connect Your Wallet"):
    st.markdown("""
    - Get free testnet ETH from [Sepolia Faucet](https://sepoliafaucet.com/)
    - Open sidebar on the left
    - Enter your **testnet wallet private key** (NEVER use mainnet key!)
    - Click **"Connect Wallet"** button
    - See connection confirmation with:
      - Wallet address
      - Current ETH balance
      - Transaction count
    - Your wallet is now connected to blockchain features
    """)

with st.expander("3️⃣ Manage Portfolio on Blockchain"):
    st.markdown("""
    - Navigate to **"💼 Portfolio"** page
    - Connect wallet first (if not already connected)
    - Fill in investment details:
      - Company symbol (e.g., "AAPL", "MSFT")
      - Number of shares purchased
      - Purchase price per share
      - Purchase date
    - Click **"Add to Blockchain"** button
    - Transaction will be sent to Sepolia testnet (~10-30 seconds)
    - View your portfolio with:
      - Real-time current valuations
      - Profit/loss calculations
      - Performance metrics
      - Blockchain transaction links
    """)

st.divider()

# Blockchain info
st.subheader("🔗 Blockchain Information")

col1, col2 = st.columns(2)

with col1:
    contract_display = f"`{st.session_state.contract_address[:10]}...`" if st.session_state.contract_address else "Not configured"
    st.markdown(f"""
    **Network Details:**
    - **Network:** Sepolia Testnet (ETH)
    - **Chain ID:** 11155111
    - **Contract Address:** {contract_display}
    - **Explorer:** [View on Etherscan](https://sepolia.etherscan.io/address/{st.session_state.contract_address})
    - **Status:** ✅ Fully operational
    """)

with col2:
    st.markdown("""
    **Get Free Testnet ETH:**
    - [Alchemy Sepolia Faucet](https://www.alchemy.com/faucets/ethereum-sepolia)
    - [Sepolia Faucet](https://sepoliafaucet.com/)
    - [Infura Faucet](https://www.infura.io/faucet/sepolia)
    
    **⚠️ Security Reminders:**
    - This is TESTNET only - no real money
    - Never use mainnet private keys here
    - Testnet ETH has zero real-world value
    - Safe for learning and testing
    """)

st.divider()

# API Info
st.subheader("⚡ Data Provider Information")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Finnhub Stock API:**
    - **Provider:** Finnhub.io (Professional-grade)
    - **Rate Limit:** 60 calls/minute (free tier)
    - **Data Quality:** Real-time, institutional-grade
    - **Coverage:** All US stocks, real-time quotes
    - **Latency:** < 100ms average response time
    - **Status:** ✅ Active and reliable
    """)

with col2:
    st.markdown("""
    **Why Finnhub?**
    - ✅ No rate limiting issues (unlike Yahoo Finance)
    - ✅ Professional-grade data quality
    - ✅ Real-time quotes (not 15-min delayed)
    - ✅ Company profiles and fundamentals included
    - ✅ 99.9% uptime guarantee
    - ✅ Free tier generous enough for most users
    """)

st.divider()

# Footer
st.markdown("""
---
<div style='text-align: center'>
    <p><strong>AI Stock Analyst v2.0.0</strong> | Built with ❤️ by TheBhoomikaM</p>
    <p>Powered by Streamlit, Finnhub API, Web3.py, and Ethereum blockchain</p>
    <p>
        <a href="https://github.com/TheBhoomikaM" target="_blank">GitHub</a> • 
        <a href="https://sepolia.etherscan.io/address/{}" target="_blank">Smart Contract</a> • 
        <a href="https://finnhub.io" target="_blank">Finnhub API</a>
    </p>
    <p style='font-size: 0.8rem; color: #888; margin-top: 1rem;'>
        Disclaimer: This tool provides information for educational purposes only. 
        Not financial advice. Always do your own research and consult with financial advisors.
    </p>
</div>
""".format(st.session_state.contract_address), unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.header("🔗 Blockchain Connection")
    
    if not st.session_state.wallet_connected:
        st.info("Connect your wallet to use blockchain portfolio features")
        
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
    **📚 Quick Links:**
    - [Get Testnet ETH](https://sepoliafaucet.com/)
    - [View Contract](https://sepolia.etherscan.io)
    - [Finnhub API](https://finnhub.io)
    - [GitHub Repository](https://github.com/TheBhoomikaM)
    - [Documentation](https://docs.finnhub.io/)
    """)
