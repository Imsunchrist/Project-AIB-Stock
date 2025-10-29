"""
Stock Analysis Page - AI-powered stock analysis
Uses existing backend/stock_advisor.py
"""

import streamlit as st
import sys
import os

# Add parent directory to import backend
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from backend.stock_advisor import StockAdvisor

# Page config
st.set_page_config(
    page_title="Stock Analysis",
    page_icon="📊",
    layout="wide"
)

# Initialize
if 'advisor' not in st.session_state:
    st.session_state.advisor = StockAdvisor()

# Header
st.title("📊 AI-Powered Stock Analysis")
st.markdown("Get real-time technical analysis and AI recommendations for any stock")

st.divider()

# Input section
col1, col2 = st.columns([3, 1])

with col1:
    stock_input = st.text_input(
        "Enter Company Name or Stock Symbol",
        placeholder="e.g., Apple, MSFT, Tesla, RELIANCE.NS",
        help="You can enter company name (Apple) or symbol (AAPL)"
    )

with col2:
    st.write("")  # Spacing
    st.write("")  # Spacing
    analyze_btn = st.button("🔍 Analyze Stock", type="primary", use_container_width=True)

# Analysis section
if analyze_btn and stock_input:
    with st.spinner(f"Analyzing {stock_input}... This may take 5-10 seconds"):
        # Use YOUR existing analyze_stock method
        analysis = st.session_state.advisor.analyze_stock(stock_input)
        
        if analysis:
            st.success(f"✅ Analysis complete for {stock_input}")
            
            # Display analysis using markdown
            st.markdown(analysis)
        else:
            st.error(f"❌ Unable to fetch data for {stock_input}")

elif analyze_btn:
    st.warning("⚠️ Please enter a company name or stock symbol")

# Tips section
st.divider()

with st.expander("💡 Tips for Better Analysis"):
    st.markdown("""
    **Supported Input Formats:**
    - Company name: "Apple", "Microsoft", "Tesla"
    - Stock symbol: "AAPL", "MSFT", "TSLA"
    - Indian stocks: "RELIANCE.NS", "TCS.NS", "INFY.NS"
    
    **Understanding Indicators:**
    - **RSI < 30**: Oversold (potential buy)
    - **RSI > 70**: Overbought (potential sell)
    - **MACD > Signal**: Bullish momentum
    - **Price > SMA20 > SMA50**: Strong uptrend
    
    **AI Recommendation:**
    - **BUY**: Multiple bullish signals
    - **HOLD**: Mixed or neutral signals
    - **SELL**: Multiple bearish signals
    - **Confidence**: 50-90% based on signal strength
    """)

# Example stocks
st.divider()
st.subheader("📌 Try These Popular Stocks")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Apple (AAPL)", use_container_width=True):
        st.session_state.stock_input = "AAPL"
        st.rerun()

with col2:
    if st.button("Microsoft (MSFT)", use_container_width=True):
        st.session_state.stock_input = "MSFT"
        st.rerun()

with col3:
    if st.button("Tesla (TSLA)", use_container_width=True):
        st.session_state.stock_input = "TSLA"
        st.rerun()

with col4:
    if st.button("Nvidia (NVDA)", use_container_width=True):
        st.session_state.stock_input = "NVDA"
        st.rerun()
