"""
Stock Analysis Page - Complete AI-powered stock analysis with Finnhub
Professional-grade technical analysis with comprehensive features
Optimized for both light and dark modes with interactive visualizations
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

# Custom CSS for better UI - Light and Dark mode compatible
st.markdown("""
<style>
    /* Stock header - gradient background */
    .stock-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stock-header h1 {
        color: white !important;
        margin: 0;
    }
    .stock-header p {
        color: white !important;
        opacity: 0.95;
        margin: 10px 0 0 0;
        font-size: 1.1rem;
    }
    
    /* Signal cards */
    .signal-buy {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white !important;
        padding: 15px;
        border-radius: 8px;
        margin: 8px 0;
        font-weight: 600;
    }
    .signal-sell {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white !important;
        padding: 15px;
        border-radius: 8px;
        margin: 8px 0;
        font-weight: 600;
    }
    .signal-neutral {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white !important;
        padding: 15px;
        border-radius: 8px;
        margin: 8px 0;
        font-weight: 600;
    }
    
    /* Recommendation box */
    .recommendation-box {
        border: 4px solid;
        padding: 25px;
        border-radius: 12px;
        margin: 20px 0;
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
        background: rgba(255, 255, 255, 0.05);
    }
    .rec-buy {
        border-color: #10b981;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
    }
    .rec-sell {
        border-color: #ef4444;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);
    }
    .rec-hold {
        border-color: #f59e0b;
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 119, 6, 0.1) 100%);
    }
    
    /* Indicator cards */
    .indicator-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        color: white !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .indicator-card h4 {
        color: white !important;
        margin-top: 0;
    }
    .indicator-card p {
        color: white !important;
        opacity: 0.95;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
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
    <h1>📊 AI-Powered Stock Analysis</h1>
    <p>Professional technical analysis powered by Finnhub API | Real-time data | Machine Learning recommendations</p>
</div>
""", unsafe_allow_html=True)

# Main Input Section
st.subheader("🔍 Analyze Any Stock")

input_col1, input_col2, input_col3 = st.columns([4, 2, 1])

with input_col1:
    stock_input = st.text_input(
        "Enter Company Name or Stock Symbol",
        value=st.session_state.stock_input,
        placeholder="e.g., AAPL, MSFT, GOOGL, TSLA, NVDA, AMZN",
        help="Enter US stock symbols. Supports all major US stocks on NYSE and NASDAQ.",
        key="main_stock_input"
    )

with input_col2:
    analysis_period = st.selectbox(
        "Historical Period",
        ["1 Year", "6 Months", "3 Months", "1 Month"],
        help="Choose data period for technical analysis"
    )
    
    period_map = {
        "1 Year": 365,
        "6 Months": 180,
        "3 Months": 90,
        "1 Month": 30
    }
    selected_days = period_map[analysis_period]

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

# More popular stocks
st.markdown("**Financial & Tech:**")
col1, col2, col3, col4, col5, col6 = st.columns(6)

more_stocks = {
    "JPM": ("🏦", "JPMorgan"),
    "BAC": ("💳", "Bank of America"),
    "META": ("📘", "Meta"),
    "NFLX": ("🎬", "Netflix"),
    "AMD": ("💻", "AMD"),
    "INTC": ("⚡", "Intel")
}

cols2 = [col1, col2, col3, col4, col5, col6]
for col, (symbol, (emoji, name)) in zip(cols2, more_stocks.items()):
    with col:
        if st.button(f"{emoji} {symbol}", key=f"btn2_{symbol}", use_container_width=True):
            st.session_state.stock_input = symbol
            st.rerun()

st.divider()

# Analysis Logic
if analyze_btn and stock_input:
    with st.spinner(f"🔄 Analyzing {stock_input.upper()} with AI... Please wait"):
        try:
            # Get analysis
            analysis_text = stock_advisor.analyze_stock(stock_input)
            
            # Check if error
            if "❌" in analysis_text:
                st.error(f"Unable to fetch data for {stock_input.upper()}")
                st.markdown(analysis_text)
            else:
                # Success - Display the analysis
                st.success(f"✅ Analysis complete for {stock_input.upper()}")
                
                # Display the full AI analysis
                st.markdown(analysis_text)
                
                # Additional visualizations if we have data
                try:
                    data = stock_advisor.get_stock_data(stock_input.upper(), days=selected_days)
                    
                    if data is not None and not data.empty and len(data) > 20:
                        st.divider()
                        st.subheader("📈 Interactive Technical Charts")
                        
                        # Calculate indicators
                        df = stock_advisor.calculate_technical_indicators(data)
                        
                        # Create comprehensive subplot figure
                        fig = make_subplots(
                            rows=4, cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.03,
                            subplot_titles=(
                                'Price & Moving Averages with Bollinger Bands',
                                'Trading Volume',
                                'RSI (Relative Strength Index)',
                                'MACD (Moving Average Convergence Divergence)'
                            ),
                            row_heights=[0.4, 0.2, 0.2, 0.2]
                        )
                        
                        # 1. Candlestick chart with Moving Averages
                        fig.add_trace(
                            go.Candlestick(
                                x=df.index,
                                open=df['Open'],
                                high=df['High'],
                                low=df['Low'],
                                close=df['Close'],
                                name='Price',
                                increasing_line_color='#10b981',
                                decreasing_line_color='#ef4444'
                            ),
                            row=1, col=1
                        )
                        
                        # Add Moving Averages
                        if 'SMA_20' in df.columns and df['SMA_20'].notna().any():
                            fig.add_trace(
                                go.Scatter(x=df.index, y=df['SMA_20'], name='SMA 20',
                                          line=dict(color='#f59e0b', width=1.5)),
                                row=1, col=1
                            )
                        if 'SMA_50' in df.columns and df['SMA_50'].notna().any():
                            fig.add_trace(
                                go.Scatter(x=df.index, y=df['SMA_50'], name='SMA 50',
                                          line=dict(color='#3b82f6', width=1.5)),
                                row=1, col=1
                            )
                        if 'SMA_200' in df.columns and df['SMA_200'].notna().any():
                            fig.add_trace(
                                go.Scatter(x=df.index, y=df['SMA_200'], name='SMA 200',
                                          line=dict(color='#ef4444', width=2)),
                                row=1, col=1
                            )
                        
                        # Bollinger Bands
                        if 'BB_Upper' in df.columns and df['BB_Upper'].notna().any():
                            fig.add_trace(
                                go.Scatter(x=df.index, y=df['BB_Upper'], name='BB Upper',
                                          line=dict(color='gray', dash='dash', width=1),
                                          opacity=0.5),
                                row=1, col=1
                            )
                            fig.add_trace(
                                go.Scatter(x=df.index, y=df['BB_Lower'], name='BB Lower',
                                          line=dict(color='gray', dash='dash', width=1),
                                          opacity=0.5, fill='tonexty', fillcolor='rgba(128,128,128,0.1)'),
                                row=1, col=1
                            )
                        
                        # 2. Volume Chart
                        colors = ['#10b981' if row['Close'] >= row['Open'] else '#ef4444' 
                                 for _, row in df.iterrows()]
                        
                        fig.add_trace(
                            go.Bar(x=df.index, y=df['Volume'], name='Volume',
                                  marker_color=colors, showlegend=False),
                            row=2, col=1
                        )
                        
                        # 3. RSI
                        if 'RSI' in df.columns and df['RSI'].notna().any():
                            fig.add_trace(
                                go.Scatter(x=df.index, y=df['RSI'], name='RSI',
                                          line=dict(color='#a855f7', width=2)),
                                row=3, col=1
                            )
                            # RSI levels
                            fig.add_hline(y=70, line_dash="dash", line_color="#ef4444",
                                        annotation_text="Overbought", row=3, col=1)
                            fig.add_hline(y=30, line_dash="dash", line_color="#10b981",
                                        annotation_text="Oversold", row=3, col=1)
                            fig.add_hrect(y0=30, y1=70, fillcolor="gray", opacity=0.1, row=3, col=1)
                        
                        # 4. MACD
                        if 'MACD' in df.columns and df['MACD'].notna().any():
                            fig.add_trace(
                                go.Scatter(x=df.index, y=df['MACD'], name='MACD',
                                          line=dict(color='#3b82f6', width=2)),
                                row=4, col=1
                            )
                        if 'Signal' in df.columns and df['Signal'].notna().any():
                            fig.add_trace(
                                go.Scatter(x=df.index, y=df['Signal'], name='Signal',
                                          line=dict(color='#f59e0b', width=2)),
                                row=4, col=1
                            )
                            # MACD histogram
                            macd_hist = df['MACD'] - df['Signal']
                            colors_macd = ['#10b981' if val >= 0 else '#ef4444' for val in macd_hist]
                            fig.add_trace(
                                go.Bar(x=df.index, y=macd_hist, name='MACD Histogram',
                                      marker_color=colors_macd, showlegend=False),
                                row=4, col=1
                            )
                            fig.add_hline(y=0, line_dash="dash", line_color="gray", row=4, col=1)
                        
                        # Update layout
                        fig.update_layout(
                            height=1000,
                            showlegend=True,
                            xaxis_rangeslider_visible=False,
                            template='plotly_white',
                            hovermode='x unified',
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            )
                        )
                        
                        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
                        fig.update_yaxes(title_text="Volume", row=2, col=1)
                        fig.update_yaxes(title_text="RSI", row=3, col=1)
                        fig.update_yaxes(title_text="MACD", row=4, col=1)
                        fig.update_xaxes(title_text="Date", row=4, col=1)
                        
                        st.plotly_chart(fig, use_container_width=True, key="main_chart")
                        
                        # Statistical Analysis
                        st.divider()
                        st.subheader("📊 Statistical Analysis")
                        
                        stat_col1, stat_col2, stat_col3, stat_col4, stat_col5 = st.columns(5)
                        
                        with stat_col1:
                            avg_volume = df['Volume'].mean()
                            st.metric("Avg Daily Volume", f"{avg_volume:,.0f}")
                        
                        with stat_col2:
                            volatility = df['Close'].pct_change().std() * 100
                            st.metric("Daily Volatility", f"{volatility:.2f}%")
                        
                        with stat_col3:
                            max_gain = df['Close'].pct_change().max() * 100
                            st.metric("Max Daily Gain", f"+{max_gain:.2f}%")
                        
                        with stat_col4:
                            max_loss = df['Close'].pct_change().min() * 100
                            st.metric("Max Daily Loss", f"{max_loss:.2f}%")
                        
                        with stat_col5:
                            avg_range = ((df['High'] - df['Low']) / df['Low'] * 100).mean()
                            st.metric("Avg Daily Range", f"{avg_range:.2f}%")
                        
                        # Price Distribution
                        st.subheader("📉 Price Distribution")
                        
                        dist_fig = go.Figure()
                        dist_fig.add_trace(go.Histogram(
                            x=df['Close'],
                            nbinsx=30,
                            name='Price Distribution',
                            marker_color='#667eea'
                        ))
                        dist_fig.update_layout(
                            height=300,
                            showlegend=False,
                            template='plotly_white',
                            xaxis_title="Price ($)",
                            yaxis_title="Frequency"
                        )
                        st.plotly_chart(dist_fig, use_container_width=True, key="dist_chart")
                        
                except Exception as chart_error:
                    st.info("📊 Advanced charts require sufficient historical data")
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
    - **Best for:** Identifying overbought/oversold conditions
    
    #### **2. MACD (Moving Average Convergence Divergence)**
    - **Bullish Signal:** MACD crosses above Signal line
    - **Bearish Signal:** MACD crosses below Signal line
    - **Momentum:** Distance between MACD and Signal indicates strength
    - **Histogram:** Shows momentum strength and direction
    - **Best for:** Trend following and momentum trading
    
    #### **3. Moving Averages (SMA)**
    - **SMA 20:** Short-term trend (~1 month)
    - **SMA 50:** Medium-term trend (~2.5 months)
    - **SMA 200:** Long-term trend (~1 year)
    - **Golden Cross:** SMA 50 > SMA 200 (Very Bullish)
    - **Death Cross:** SMA 50 < SMA 200 (Very Bearish)
    - **Best for:** Identifying trend direction and support/resistance
    
    #### **4. Bollinger Bands**
    - **Upper Band:** Resistance level (2 std dev above SMA)
    - **Lower Band:** Support level (2 std dev below SMA)
    - **Middle Band:** 20-day SMA
    - **Price touches upper:** Potentially overbought
    - **Price touches lower:** Potentially oversold
    - **Bandwidth:** Shows volatility (wider = more volatile)
    - **Best for:** Volatility analysis and mean reversion strategies
    
    #### **5. Volume Analysis**
    - **Measures:** Trading activity and liquidity
    - **High volume + price up:** Strong buying pressure
    - **High volume + price down:** Strong selling pressure
    - **Low volume:** Weak conviction, potential reversal
    - **Best for:** Confirming price movements
    
    ### 💡 How to Use Combined Analysis
    
    **Strong Buy Signals (Confluence):**
    - RSI < 30 (oversold) ✅
    - MACD crosses above signal ✅
    - Price bounces off lower Bollinger Band ✅
    - Price above SMA 50 and 200 ✅
    - High volume on up days ✅
    
    **Strong Sell Signals (Confluence):**
    - RSI > 70 (overbought) ⚠️
    - MACD crosses below signal ⚠️
    - Price rejects upper Bollinger Band ⚠️
    - Death cross forming ⚠️
    - High volume on down days ⚠️
    
    **Risk Management:**
    - Never trade on single indicator
    - Always use stop-loss orders
    - Consider multiple timeframes
    - Manage position sizing
    - Diversify your portfolio
    """)

with st.expander("💡 Professional Trading Tips", expanded=False):
    st.markdown("""
    ### 🎓 Best Practices for Stock Analysis
    
    **1. Market Timing:**
    - Best liquidity: 9:30 AM - 4:00 PM ET (Regular hours)
    - Avoid first 15 minutes (high volatility)
    - Avoid last 15 minutes (position squaring)
    - Check pre-market and after-hours activity
    
    **2. Multiple Timeframe Analysis:**
    - Long-term: Weekly/Monthly charts for trend
    - Medium-term: Daily charts for entries
    - Short-term: 4H/1H for precise timing
    - Align all timeframes before trading
    
    **3. Volume Confirmation:**
    - Breakouts need high volume to sustain
    - Low volume moves often fail
    - Compare to 20-day average volume
    - Volume precedes price
    
    **4. Support & Resistance:**
    - Previous highs = resistance
    - Previous lows = support
    - Use moving averages as dynamic S/R
    - Fibonacci retracement levels
    
    **5. Risk Management:**
    - Risk max 1-2% per trade
    - Set stop-loss before entry
    - Take partial profits at targets
    - Trail stops on winners
    - Cut losses quickly
    
    **6. Using This Platform:**
    - Analyze multiple stocks before deciding
    - Check correlations with market indices
    - Use blockchain portfolio for tracking
    - Review AI recommendations regularly
    - Combine with fundamental analysis
    """)

with st.expander("⚡ About Finnhub Data", expanded=False):
    st.markdown("""
    ### 🚀 Professional-Grade Market Data
    
    **Data Quality:**
    - ✅ Real-time stock quotes (not delayed)
    - ✅ Historical data up to 30 years
    - ✅ Intraday data available
    - ✅ Corporate actions adjusted
    - ✅ Split and dividend adjusted
    
    **Performance:**
    - ✅ 60 API calls per minute (free tier)
    - ✅ Low latency (< 100ms average)
    - ✅ 99.9% uptime guarantee
    - ✅ Global exchange coverage
    
    **Coverage:**
    - ✅ All US stocks (NYSE, NASDAQ, AMEX)
    - ✅ Major global exchanges
    - ✅ Forex pairs
    - ✅ Cryptocurrencies
    - ✅ Economic indicators
    
    **Why Finnhub vs Others:**
    - **vs Yahoo Finance:** No rate limiting, reliable API
    - **vs Alpha Vantage:** Better free tier, faster
    - **vs IEX Cloud:** More generous free tier
    - **vs Polygon:** Simpler API, easier integration
    
    **Upgrade Path:**
    - **Free:** 60 calls/min, perfect for individual use
    - **Starter ($59/mo):** 300 calls/min, more data
    - **Pro ($299/mo):** Real-time Level 2, full access
    """)

# Sidebar - Market Overview
with st.sidebar:
    st.header("📊 Market Overview")
    
    st.markdown("### 📈 Market Status")
    
    try:
        # Simple market status indicator
        now = datetime.now()
        market_open = now.weekday() < 5 and 9 <= now.hour < 16
        
        if market_open:
            st.success("🟢 Market Open")
        else:
            st.info("🔴 Market Closed")
    except:
        pass
    
    st.divider()
    
    st.markdown("""
    ### 🔥 Trending Sectors
    
    **Technology** 📱  
    AAPL, MSFT, GOOGL, NVDA
    
    **Electric Vehicles** 🚗  
    TSLA, RIVN, LCID, F
    
    **Finance** 💰  
    JPM, BAC, GS, MS
    
    **Healthcare** 🏥  
    JNJ, PFE, UNH, ABBV
    
    **Energy** ⚡  
    XOM, CVX, COP, SLB
    """)
    
    st.divider()
    
    st.markdown("""
    ### 📚 Quick Links
    
    - [Finnhub Dashboard](https://finnhub.io/dashboard)
    - [Market News](https://finnhub.io/news)
    - [Economic Calendar](https://finnhub.io/calendar)
    - [Stock Screener](https://finnhub.io/stock-screener)
    - [Crypto Prices](https://finnhub.io/crypto)
    """)

# Footer
st.divider()
st.markdown("""
---
<div style='text-align: center; padding: 20px;'>
    <p style='font-size: 1rem; font-weight: 600;'>
        <strong>Powered by Finnhub Professional API</strong> | Real-time Data | AI-Enhanced Analysis
    </p>
    <p style='font-size: 0.85rem; color: #666;'>
        Technical analysis and recommendations are for informational purposes only. 
        Not financial advice. Always consult with a licensed financial advisor before making investment decisions.
        Past performance does not guarantee future results.
    </p>
</div>
""", unsafe_allow_html=True)
