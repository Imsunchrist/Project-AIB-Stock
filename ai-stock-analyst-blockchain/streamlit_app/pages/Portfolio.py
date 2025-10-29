"""
Portfolio Management Page
Uses existing backend/portfolio_manager.py and backend/blockchain_integration.py
"""

import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime

# Add parent directory to import backend
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.stock_advisor import StockAdvisor
from backend.portfolio_manager import BlockchainPortfolioManagerEnhanced

# Page config
st.set_page_config(
    page_title="Portfolio Management",
    page_icon="💼",
    layout="wide"
)

# Initialize session state
if 'advisor' not in st.session_state:
    st.session_state.advisor = StockAdvisor()

if 'portfolio_manager' not in st.session_state:
    st.session_state.portfolio_manager = BlockchainPortfolioManagerEnhanced(blockchain_enabled=True)
    st.session_state.portfolio_manager.set_stock_advisor(st.session_state.advisor)

if 'wallet_connected' not in st.session_state:
    st.session_state.wallet_connected = False

if 'user_id' not in st.session_state:
    st.session_state.user_id = "streamlit_user"

# Header
st.title("💼 Portfolio Management")
st.markdown("Track your investments with real-time valuations and blockchain storage")

st.divider()

# Check wallet connection
if not st.session_state.wallet_connected:
    st.warning("⚠️ **Wallet not connected!** Connect your wallet in the sidebar (Home page) to add investments to blockchain.")
    st.info("💡 You can still view portfolio features below, but blockchain storage requires wallet connection.")
    st.divider()

# Add Investment Section
st.subheader("➕ Add New Investment")

with st.expander("📝 Add Investment Form", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        company = st.text_input(
            "Company Name",
            placeholder="e.g., Apple, Microsoft, Tesla",
            help="Enter company name (we'll find the stock symbol automatically)"
        )
        shares = st.number_input(
            "Number of Shares",
            min_value=0.01,
            value=10.0,
            step=0.01,
            help="Number of shares purchased"
        )
    
    with col2:
        price = st.number_input(
            "Purchase Price per Share ($)",
            min_value=0.01,
            value=175.50,
            step=0.01,
            help="Price per share at time of purchase"
        )
        date = st.date_input(
            "Purchase Date",
            value=datetime.now(),
            help="Date when investment was made"
        )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        add_local_btn = st.button(
            "💾 Add Locally",
            type="secondary",
            use_container_width=True,
            help="Save to local session (temporary)"
        )
    
    with col2:
        add_blockchain_btn = st.button(
            "🔗 Add to Blockchain",
            type="primary",
            use_container_width=True,
            disabled=not st.session_state.wallet_connected,
            help="Save permanently on Ethereum blockchain (requires wallet)"
        )
    
    # Handle local addition
    if add_local_btn:
        if company and shares > 0 and price > 0:
            with st.spinner("Adding to local portfolio..."):
                try:
                    result = st.session_state.portfolio_manager.add_investment(
                        st.session_state.user_id,
                        company,
                        float(shares),
                        float(price),
                        date.strftime("%Y-%m-%d")
                    )
                    st.success(f"✅ {result}")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.error("❌ Please fill all fields with valid values")
    
    # Handle blockchain addition
    if add_blockchain_btn:
        if company and shares > 0 and price > 0:
            with st.spinner("Adding to blockchain... This may take 10-15 seconds"):
                try:
                    result = st.session_state.portfolio_manager.add_investment_blockchain(
                        st.session_state.user_id,
                        company,
                        float(shares),
                        float(price),
                        date.strftime("%Y-%m-%d")
                    )
                    st.success("✅ Investment added to blockchain!")
                    st.markdown(result)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Blockchain error: {str(e)}")
        else:
            st.error("❌ Please fill all fields with valid values")

st.divider()

# Portfolio Overview Section
st.subheader("📊 Current Holdings")

col1, col2 = st.columns([3, 1])

with col2:
    if st.button("🔄 Refresh Portfolio", use_container_width=True):
        st.rerun()

# Get portfolio data using YOUR existing methods
portfolio = st.session_state.portfolio_manager.get_portfolio(st.session_state.user_id)

if portfolio:
    # Calculate stats using YOUR existing method
    stats = st.session_state.portfolio_manager.calculate_portfolio_value(
        st.session_state.user_id,
        st.session_state.advisor
    )
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Invested",
            value=f"${stats['total_invested']:,.2f}",
            help="Total amount invested across all holdings"
        )
    
    with col2:
        st.metric(
            label="📈 Current Value",
            value=f"${stats['current_value']:,.2f}",
            help="Current market value of all holdings"
        )
    
    with col3:
        st.metric(
            label="💵 Gain/Loss",
            value=f"${stats['gain_loss']:,.2f}",
            delta=f"{stats['gain_loss_pct']:+.2f}%",
            delta_color="normal",
            help="Total profit or loss"
        )
    
    with col4:
        st.metric(
            label="📦 Holdings",
            value=len(portfolio),
            help="Number of different investments"
        )
    
    st.divider()
    
    # Holdings table
    st.subheader("📋 Detailed Holdings")
    
    holdings_data = []
    
    for idx, inv in enumerate(portfolio, 1):
        # Get current price using YOUR existing method
        symbol = st.session_state.advisor.smart_symbol_lookup(inv['company'])
        current_price = st.session_state.advisor.get_current_price(symbol)
        
        invested = inv['shares'] * inv['purchase_price']
        current_value = inv['shares'] * current_price if current_price > 0 else invested
        gain_loss = current_value - invested
        gain_loss_pct = (gain_loss / invested * 100) if invested > 0 else 0
        
        # Check if blockchain verified
        blockchain_badge = "🔗" if inv.get('blockchain_id') or inv.get('blockchain_verified') else "💾"
        
        holdings_data.append({
            "": blockchain_badge,
            "#": idx,
            "Company": inv['company'],
            "Symbol": symbol,
            "Shares": f"{inv['shares']:.2f}",
            "Buy Price": f"${inv['purchase_price']:.2f}",
            "Current Price": f"${current_price:.2f}",
            "Invested": f"${invested:,.2f}",
            "Current Value": f"${current_value:,.2f}",
            "Gain/Loss": f"${gain_loss:,.2f}",
            "G/L %": f"{gain_loss_pct:+.2f}%",
            "Date": inv['purchase_date']
        })
    
    df = pd.DataFrame(holdings_data)
    
    # Display table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "": st.column_config.TextColumn("", width="small"),
            "#": st.column_config.NumberColumn("#", width="small"),
            "G/L %": st.column_config.TextColumn("G/L %", width="small")
        }
    )
    
    st.caption("🔗 = Blockchain verified | 💾 = Local storage")
    
    # Sync from blockchain option
    if st.session_state.wallet_connected:
        st.divider()
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("🔄 Sync from Blockchain", use_container_width=True):
                with st.spinner("Syncing from blockchain..."):
                    try:
                        result = st.session_state.portfolio_manager.sync_from_blockchain(
                            st.session_state.user_id
                        )
                        st.success(result)
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Sync failed: {str(e)}")

else:
    st.info("📭 Your portfolio is empty. Add your first investment above!")
    
    st.markdown("""
    **Getting Started:**
    1. Enter company name (e.g., "Apple", "Microsoft")
    2. Enter number of shares and purchase price
    3. Choose storage method:
       - **Add Locally**: Temporary storage (this session only)
       - **Add to Blockchain**: Permanent storage (requires wallet connection)
    """)

st.divider()

# Portfolio tips
with st.expander("💡 Portfolio Management Tips"):
    st.markdown("""
    **Local vs Blockchain Storage:**
    - **Local Storage (💾)**: 
      - Stored in browser session
      - Lost when you close browser
      - Instant (no transaction fees)
      - Good for testing
    
    - **Blockchain Storage (🔗)**:
      - Permanently stored on Ethereum
      - Accessible from any device
      - Requires gas fees (~$0.50 on testnet)
      - Immutable and verifiable
    
    **Best Practices:**
    - Use blockchain for real investments
    - Use local storage for testing
    - Regularly sync from blockchain
    - Keep backup of investment details
    
    **Understanding Metrics:**
    - **Total Invested**: Sum of all purchase prices
    - **Current Value**: Real-time market valuation
    - **Gain/Loss**: Profit or loss amount
    - **G/L %**: Percentage return on investment
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #888;'>
    <p>💼 Portfolio powered by your investments | 🔗 Secured by Ethereum blockchain</p>
</div>
""", unsafe_allow_html=True)
