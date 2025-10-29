"""
Stock Analysis Page - Complete AI-powered stock analysis with Finnhub
Professional-grade technical analysis with comprehensive features
"""

import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add parent directory to import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stock_advisor_finnhub import StockAdvisorFinnhub

# Page config
st.set_page_config(
    page_title="Stock Analysis - AI Stock Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .signal-buy {
        background-color: #10b981;
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .signal-sell {
        background-color: #ef4444;
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .signal-neutral {
        background-color: #f59e0b;
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .recommendation-box {
        border: 3px solid;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
    }
    .rec-buy {
        border-color: #10b981;
        background-color: rgba(16, 185, 129, 0.1);
    }
    .rec-sell {
        border-color: #ef4444;
        background-color: rgba(239, 68, 68, 0.1);
    }
    .rec-hold {
        border-color: #f59e0b;
        background-color: rgba(245, 158, 11, 0.1);
    }
    .indicator-card {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #3b82f6;
    }
    .stock-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize stock advisor from session state or create new
if 'advisor' in st.session_state:
    stock_advisor = st.session_state.advisor
else:
    # Fallback: create new instance with API key from secrets
    api_key = st.secrets.get("FINNHUB_API_KEY", "d415bmpr01qo6qdf06d0d415bmpr01qo6qdf06dg")
    stock_advisor = StockAdvisorFinnhub(api_key)
    st.session_state.advisor = stock_advisor

# Initialize session state for stock input
if 'stock_input' not in st.session_state:
    st.session_state.stock_input = ""

# Header Section
st.markdown("""
<div class="stock-header">
    <h1 style="margin: 0;">📊 AI-Powered Stock Analysis</h1>
    <p style="margin: 10px 0 0 0; font-size: 1.1rem;">
        Professional technical analysis powered by Finnhub API | Real-time data | 60 calls/minute
    </p>
</div>
""", unsafe_allow_html=True)

# Main Input Section
st.subheader("🔍 Analyze Any Stock")

input_col1, input_col2, input_col3 = st.columns([4, 2, 1])

with input_col1:
    stock_input = st.text_input(
        "Enter Company Name or Stock Symbol",
        value=st.session_state.stock_input,
        placeholder="e.g., AAPL, MSFT, GOOGL, TSLA, NVDA",
        help="Enter US stock symbols. Supports all major US stocks.",
        key="main_stock_input"
    )

with input_col2:
    analysis_type = st.selectbox(
        "Analysis Type",
        ["Complete Analysis", "Quick Quote", "Technical Only"],
        help="Choose analysis depth"
    )

with input_col3:
    st.write("")  # Spacing
    st.write("")  # Spacing
    analyze_btn = st.button("🚀 Analyze", type="primary", use_container_width=True)

# Quick access buttons for popular stocks
st.markdown("### 🔥 Popular Stocks")
quick_col1, quick_col2, quick_col3, quick_col4, quick_col5, quick_col6 = st.columns(6)

popular_stocks = {
    "AAPL": ("🍎", "Apple"),
    "MSFT": ("🖥️", "Microsoft"),
    "GOOGL": ("🔍", "Google"),
    "TSLA": ("🚗", "Tesla"),
    "NVDA": ("🎮", "Nvidia"),
    "AMZN": ("📦", "Amazon")
}

cols = [quick_col1, quick_col2, quick_col3, quick_col4, quick_col5, quick_col6]
for col, (symbol, (emoji, name)) in zip(cols, popular_stocks.items()):
    with col:
        if st.button(f"{emoji} {symbol}", key=f"quick_{symbol}", use_container_width=True):
            st.session_state.stock_input = symbol
            st.rerun()

st.divider()

# Analysis Logic
if analyze_btn and stock_input:
    with st.spinner(f"🔄 Analyzing {stock_input.upper()} with Finnhub AI... Please wait"):
        try:
            # Get analysis
            analysis_text = stock_advisor.analyze_stock(stock_input)
            
            # Check if error
            if "❌" in analysis_text:
                st.error(f"Unable to fetch data for {stock_input.upper()}")
                st.markdown(analysis_text)
            else:
                # Success - Parse and display beautifully
                st.success(f"✅ Analysis complete for {stock_input.upper()}")
                
                # Display the analysis
                st.markdown(analysis_text)
                
                # Additional visualizations if we have data
                try:
                    data = stock_advisor.get_stock_data(stock_input.upper(), days=365)
                    
                    if data is not None and not data.empty:
                        st.divider()
                        st.subheader("📈 Interactive Price Charts")
                        
                        # Calculate indicators
                        df = stock_advisor.calculate_technical_indicators(data)
                        
                        # Create subplots
                        fig = make_subplots(
                            rows=3, cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.05,
                            subplot_titles=('Price & Moving Averages', 'RSI', 'MACD'),
                            row_heights=[0.5, 0.25, 0.25]
                        )
                        
                        # Candlestick chart
                        fig.add_trace(
                            go.Candlestick(
                                x=df.index,
                                open=df['Open'],
                                high=df['High'],
                                low=df['Low'],
                                close=df['Close'],
                                name='Price'
                            ),
                            row=1, col=1
                        )
                        
                        # Add SMA lines
                        if 'SMA_20' in df.columns:
                            fig.add_trace(
                                go.Scatter(x=df.index, y=df['SMA_20'], name='SMA 20', line=dict(color='orange', width=1)),
                                row=1, col=1
                            )
                        if 'SMA_50' in df.columns:
                            fig.add_trace(
                                go.Scatter(x=df.index, y=df['SMA_50'], name='SMA 50', line=dict(color='blue', width=1)),
                                row=1, col=1
                            )
                        if 'SMA_200' in df.columns:
                            fig.add_trace(
                                go.Scatter(x=df.index, y=df['SMA_200'], name='SMA 200', line=dict(color='red', width=1)),
                                row=1, col=1
                            )
                        
                        # Bollinger Bands
                        if 'BB_Upper' in df.columns:
                            fig.add_trace(
                                go.Scatter(x=df.index, y=df['BB_Upper'], name='BB Upper', line=dict(color='gray', dash='dash', width=1)),
                                row=1, col=1
                            )
                            fig.add_trace(
                                go.Scatter(x=df.index, y=df['BB_Lower'], name='BB Lower', line=dict(color='gray', dash='dash', width=1)),
                                row=1, col=1
                            )
                        
                        # RSI
                        if 'RSI' in df.columns:
                            fig.add_trace(
                                go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='purple', width=2)),
                                row=2, col=1
                            )
                            # Add RSI levels
                            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
                            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
                        
                        # MACD
                        if 'MACD' in df.columns and 'Signal' in df.columns:
                            fig.add_trace(
                                go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='blue', width=2)),
                                row=3, col=1
                            )
                            fig.add_trace(
                                go.Scatter(x=df.index, y=df['Signal'], name='Signal', line=dict(color='orange', width=2)),
                                row=3, col=1
                            )
                            fig.add_hline(y=0, line_dash="dash", line_color="gray", row=3, col=1)
                        
                        # Update layout
                        fig.update_layout(
                            height=900,
                            showlegend=True,
                            xaxis_rangeslider_visible=False,
                            template='plotly_dark',
                            hovermode='x unified'
                        )
                        
                        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
                        fig.update_yaxes(title_text="RSI", row=2, col=1)
                        fig.update_yaxes(title_text="MACD", row=3, col=1)
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Volume chart
                        st.subheader("📊 Volume Analysis")
                        
                        volume_fig = go.Figure()
                        
                        # Color bars based on price change
                        colors = ['red' if row['Close'] < row['Open'] else 'green' for _, row in df.iterrows()]
                        
                        volume_fig.add_trace(
                            go.Bar(
                                x=df.index,
                                y=df['Volume'],
                                name='Volume',
                                marker_color=colors
                            )
                        )
                        
                        volume_fig.update_layout(
                            height=300,
                            showlegend=False,
                            template='plotly_dark',
                            yaxis_title="Volume"
                        )
                        
                        st.plotly_chart(volume_fig, use_container_width=True)
                        
                        # Statistics
                        st.divider()
                        st.subheader("📈 Historical Statistics")
                        
                        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
                        
                        with stat_col1:
                            avg_volume = df['Volume'].mean()
                            st.metric("Avg Volume", f"{avg_volume:,.0f}")
                        
                        with stat_col2:
                            volatility = df['Close'].pct_change().std() * 100
                            st.metric("Daily Volatility", f"{volatility:.2f}%")
                        
                        with stat_col3:
                            max_gain = df['Close'].pct_change().max() * 100
                            st.metric("Max Daily Gain", f"{max_gain:.2f}%")
                        
                        with stat_col4:
                            max_loss = df['Close'].pct_change().min() * 100
                            st.metric("Max Daily Loss", f"{max_loss:.2f}%")
                        
                except Exception as chart_error:
                    st.info("📊 Basic charts unavailable - showing text analysis only")
                    print(f"Chart error: {chart_error}")
                
        except Exception as e:
            st.error(f"❌ Error analyzing {stock_input.upper()}: {str(e)}")
            st.info("💡 Please try again or choose a different stock")

elif analyze_btn:
    st.warning("⚠️ Please enter a stock symbol")

# Educational Section
st.divider()

with st.expander("📚 Understanding Technical Indicators", expanded=False):
    st.markdown("""
    ### 🎯 Key Technical Indicators Explained
    
    #### **1. RSI (Relative Strength Index)**
    - **Range:** 0-100
    - **Oversold:** RSI < 30 → Potential buying opportunity
    - **Overbought:** RSI > 70 → Potential selling opportunity
    - **Neutral:** RSI 30-70 → Market in balance
    
    #### **2. MACD (Moving Average Convergence Divergence)**
    - **Bullish Signal:** MACD crosses above Signal line
    - **Bearish Signal:** MACD crosses below Signal line
    - **Momentum:** Distance between MACD and Signal indicates strength
    
    #### **3. Moving Averages (SMA)**
    - **SMA 20:** Short-term trend (1 month)
    - **SMA 50:** Medium-term trend (2.5 months)
    - **SMA 200:** Long-term trend (1 year)
    - **Golden Cross:** SMA 50 crosses above SMA 200 (Bullish)
    - **Death Cross:** SMA 50 crosses below SMA 200 (Bearish)
    
    #### **4. Bollinger Bands**
    - **Upper Band:** Resistance level
    - **Lower Band:** Support level
    - **Price touches upper:** Potentially overbought
    - **Price touches lower:** Potentially oversold
    
    #### **5. ATR (Average True Range)**
    - **Measures:** Price volatility
    - **High ATR:** High volatility, larger price swings
    - **Low ATR:** Low volatility, smaller price movements
    
    ### 💡 How to Use This Information
    
    **For Buying:**
    - RSI < 30 (oversold)
    - MACD crosses above signal
    - Price near lower Bollinger Band
    - Multiple indicators confirm
    
    **For Selling:**
    - RSI > 70 (overbought)
    - MACD crosses below signal
    - Price near upper Bollinger Band
    - Multiple indicators confirm
    
    **Risk Management:**
    - Never rely on single indicator
    - Consider multiple timeframes
    - Use stop-loss orders
    - Diversify your portfolio
    """)

with st.expander("💡 Tips for Better Stock Analysis", expanded=False):
    st.markdown("""
    ### 🎓 Professional Tips
    
    **1. Stock Selection:**
    - Focus on liquid stocks (high trading volume)
    - Research company fundamentals
    - Check recent news and earnings
    - Understand the industry
    
    **2. Timing Your Trades:**
    - Best during market hours (9:30 AM - 4:00 PM ET)
    - Avoid first and last 30 minutes (high volatility)
    - Check pre-market and after-hours trends
    
    **3. Using Our Platform:**
    - Analyze multiple stocks before deciding
    - Check analysis during different market conditions
    - Use the blockchain portfolio feature to track investments
    - Compare similar stocks in same sector
    
    **4. Risk Management:**
    - Never invest more than you can afford to lose
    - Set stop-loss levels (typically 5-10% below entry)
    - Take profits at predetermined targets
    - Diversify across sectors
    
    **5. Data Reliability:**
    - Powered by Finnhub (professional-grade API)
    - Real-time quotes (no 15-minute delay)
    - 60 API calls per minute (no rate limiting)
    - Institutional-quality data
    """)

with st.expander("⚡ About Our Data Source - Finnhub", expanded=False):
    st.markdown("""
    ### 🚀 Why Finnhub?
    
    **Data Quality:**
    - ✅ Real-time stock quotes
    - ✅ Historical data (up to 30 years)
    - ✅ Company profiles and financials
    - ✅ News and sentiment analysis
    
    **Performance:**
    - ✅ 60 API calls per minute (free tier)
    - ✅ No rate limiting issues
    - ✅ Low latency responses
    - ✅ 99.9% uptime
    
    **Coverage:**
    - ✅ All US stocks (NYSE, NASDAQ)
    - ✅ Major global exchanges
    - ✅ Forex and Crypto
    - ✅ Economic indicators
    
    **Previous Issues with Yahoo Finance:**
    - ❌ Constant rate limiting (429 errors)
    - ❌ Unreliable during high traffic
    - ❌ Unofficial API (can break anytime)
    - ❌ 15-minute delayed data
    
    **Upgrade Path:**
    - Current: Free tier (60 calls/min)
    - Pro: $59/month (300 calls/min)
    - More features in paid tiers
    """)

# Sidebar - Market Overview
with st.sidebar:
    st.header("📊 Market Overview")
    
    try:
        # Get major indices quotes
        indices = {
            "S&P 500": "^GSPC",
            "Dow Jones": "^DJI",
            "NASDAQ": "^IXIC"
        }
        
        st.markdown("### 📈 Major Indices")
        
        for name, symbol in indices.items():
            try:
                quote = stock_advisor.get_stock_quote(symbol)
                if quote:
                    st.metric(
                        name,
                        f"${quote['price']:.2f}",
                        f"{quote['change']:.2f} ({quote['change_percent']:.2f}%)"
                    )
            except:
                pass
        
    except:
        st.info("Market data loading...")
    
    st.divider()
    
    st.markdown("""
    ### 🔥 Trending Sectors
    
    **Technology** 📱  
    AAPL, MSFT, GOOGL, NVDA
    
    **Electric Vehicles** 🚗  
    TSLA, RIVN, LCID
    
    **Finance** 💰  
    JPM, BAC, GS, MS
    
    **Healthcare** 🏥  
    JNJ, PFE, UNH, ABBV
    """)
    
    st.divider()
    
    st.markdown("""
    ### 📚 Quick Links
    
    - [Finnhub Dashboard](https://finnhub.io/dashboard)
    - [Market News](https://finnhub.io/news)
    - [Economic Calendar](https://finnhub.io/calendar)
    - [Stock Screener](https://finnhub.io/stock-screener)
    """)

# Footer
st.divider()
st.markdown("""
---
<div style='text-align: center; padding: 20px;'>
    <p style='font-size: 0.9rem; color: #888;'>
        <strong>Powered by Finnhub API</strong> | Real-time Stock Data | Professional-Grade Analysis
    </p>
    <p style='font-size: 0.8rem; color: #666;'>
        Data provided for informational purposes only. Not financial advice. 
        Always consult with a financial advisor before making investment decisions.
    </p>
</div>
""", unsafe_allow_html=True)
