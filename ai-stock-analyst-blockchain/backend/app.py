import gradio as gr
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz, process
import warnings
import os
from dotenv import load_dotenv

warnings.filterwarnings('ignore')

from stock_advisor import StockAdvisor
from portfolio_manager import BlockchainPortfolioManagerEnhanced

load_dotenv()

print("🚀 AI Stock Analyst with Blockchain Integration Starting...")

blockchain_enabled = os.getenv('BLOCKCHAIN_ENABLED', 'False').lower() == 'true'
portfolio_manager = BlockchainPortfolioManagerEnhanced(blockchain_enabled=blockchain_enabled)
advisor = StockAdvisor()
portfolio_manager.set_stock_advisor(advisor)

USER_ID = "user123"


def analyze_stock_interface(company_input):
    """Interface function for stock analysis"""
    if not company_input or company_input.strip() == "":
        return "⚠️ Please enter a company name or stock symbol"
    
    return advisor.analyze_stock(company_input)


def add_investment_interface(company, shares, price, date):
    """Interface function for adding investment"""
    try:
        if not company or not shares or not price:
            return "⚠️ Please fill all fields"
        
        shares_float = float(shares)
        price_float = float(price)
        
        if shares_float <= 0 or price_float <= 0:
            return "⚠️ Shares and price must be positive numbers"
        
        if blockchain_enabled:
            result = portfolio_manager.add_investment_blockchain(
                USER_ID, company, shares_float, price_float, date
            )
        else:
            result = portfolio_manager.add_investment(
                USER_ID, company, shares_float, price_float, date
            )
        
        return result
        
    except ValueError:
        return "❌ Invalid number format for shares or price"
    except Exception as e:
        return f"❌ Error adding investment: {str(e)}"


def view_portfolio_interface():
    """Interface function for viewing portfolio"""
    portfolio = portfolio_manager.get_portfolio(USER_ID)
    
    if not portfolio:
        return "📭 Your portfolio is empty. Add some investments to get started!"
    
    stats = portfolio_manager.calculate_portfolio_value(USER_ID, advisor)
    
    output = f"""
## 💼 Your Investment Portfolio

### 📊 Portfolio Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Total Invested:** ${stats['total_invested']:,.2f}
**Current Value:** ${stats['current_value']:,.2f}
**Gain/Loss:** {'🟢' if stats['gain_loss'] >= 0 else '🔴'} ${stats['gain_loss']:,.2f} ({stats['gain_loss_pct']:+.2f}%)

### 📈 Individual Holdings
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    for idx, inv in enumerate(portfolio, 1):
        symbol = advisor.smart_symbol_lookup(inv['company'])
        current_price = advisor.get_current_price(symbol)
        
        invested = inv['shares'] * inv['purchase_price']
        current_value = inv['shares'] * current_price if current_price > 0 else invested
        gain_loss = current_value - invested
        gain_loss_pct = (gain_loss / invested * 100) if invested > 0 else 0
        
        blockchain_badge = "🔗" if 'blockchain_id' in inv else ""
        
        output += f"""
**{idx}. {inv['company']}** {blockchain_badge}
   Symbol: {symbol}
   Shares: {inv['shares']:.2f}
   Purchase Price: ${inv['purchase_price']:.2f}
   Current Price: ${current_price:.2f}
   Purchase Date: {inv['purchase_date']}
   Invested: ${invested:,.2f}
   Current Value: ${current_value:,.2f}
   {'🟢' if gain_loss >= 0 else '🔴'} Gain/Loss: ${gain_loss:,.2f} ({gain_loss_pct:+.2f}%)
   ID: `{inv['investment_id']}`

"""
    
    if blockchain_enabled:
        output += "\n🔗 Blockchain verified investments"
    
    output += f"\n*Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
    
    return output


def remove_investment_interface(investment_id):
    """Interface function for removing investment"""
    if not investment_id or investment_id.strip() == "":
        return "⚠️ Please enter an investment ID"
    
    result = portfolio_manager.remove_investment(USER_ID, investment_id.strip())
    return result


def compare_stocks_interface(stock1, stock2):
    """Interface function for comparing two stocks"""
    if not stock1 or not stock2:
        return "⚠️ Please enter both stock symbols"
    
    symbol1 = advisor.smart_symbol_lookup(stock1)
    symbol2 = advisor.smart_symbol_lookup(stock2)
    
    try:
        data1 = advisor.get_stock_data(symbol1, period="6mo")
        data2 = advisor.get_stock_data(symbol2, period="6mo")
        
        if data1 is None or data2 is None:
            return "❌ Unable to fetch data for one or both stocks"
        
        stock1_obj = yf.Ticker(symbol1)
        stock2_obj = yf.Ticker(symbol2)
        info1 = stock1_obj.info
        info2 = stock2_obj.info
        
        price1 = data1['Close'].iloc[-1]
        price2 = data2['Close'].iloc[-1]
        
        change1 = ((price1 - data1['Close'].iloc[0]) / data1['Close'].iloc[0]) * 100
        change2 = ((price2 - data2['Close'].iloc[0]) / data2['Close'].iloc[0]) * 100
        
        vol1 = data1['Close'].pct_change().std() * np.sqrt(252) * 100
        vol2 = data2['Close'].pct_change().std() * np.sqrt(252) * 100
        
        comparison = f"""
## 📊 Stock Comparison: {symbol1} vs {symbol2}

### 💰 Price Comparison
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
| Metric | {symbol1} | {symbol2} |
|--------|----------|----------|
| Current Price | ${price1:.2f} | ${price2:.2f} |
| 6-Month Return | {change1:+.2f}% | {change2:+.2f}% |
| Volatility | {vol1:.2f}% | {vol2:.2f}% |
| Market Cap | ${info1.get('marketCap', 0)/1e9:.2f}B | ${info2.get('marketCap', 0)/1e9:.2f}B |
| P/E Ratio | {info1.get('trailingPE', 'N/A')} | {info2.get('trailingPE', 'N/A')} |

### 🏢 Company Information
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**{symbol1}:** {info1.get('longName', 'N/A')}
Sector: {info1.get('sector', 'N/A')}
Industry: {info1.get('industry', 'N/A')}

**{symbol2}:** {info2.get('longName', 'N/A')}
Sector: {info2.get('sector', 'N/A')}
Industry: {info2.get('industry', 'N/A')}

### 🎯 Performance Winner
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        if change1 > change2:
            comparison += f"🏆 **{symbol1}** outperformed with {change1-change2:.2f}% higher returns"
        elif change2 > change1:
            comparison += f"🏆 **{symbol2}** outperformed with {change2-change1:.2f}% higher returns"
        else:
            comparison += "🤝 Both stocks performed equally"
        
        return comparison
        
    except Exception as e:
        return f"❌ Error comparing stocks: {str(e)}"


def search_stocks_interface(keyword):
    """Interface function for searching stocks"""
    if not keyword or keyword.strip() == "":
        return "⚠️ Please enter a search keyword"
    
    keyword_lower = keyword.lower()
    matches = []
    
    for company, symbol in advisor.company_symbols.items():
        if keyword_lower in company or keyword_lower in symbol.lower():
            matches.append(f"**{company.title()}** → {symbol}")
    
    if not matches:
        return f"❌ No stocks found matching '{keyword}'"
    
    result = f"## 🔍 Search Results for '{keyword}'\n\n"
    result += "\n".join(matches[:20])
    
    if len(matches) > 20:
        result += f"\n\n*Showing 20 of {len(matches)} results*"
    
    return result


def get_market_overview():
    """Get major market indices overview"""
    indices = {
        'S&P 500': '^GSPC',
        'Dow Jones': '^DJI',
        'NASDAQ': '^IXIC',
        'Russell 2000': '^RUT',
        'NIFTY 50': '^NSEI',
        'SENSEX': '^BSESN'
    }
    
    overview = "## 🌍 Market Overview\n\n"
    
    for name, symbol in indices.items():
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="2d")
            
            if not data.empty and len(data) >= 2:
                current = data['Close'].iloc[-1]
                previous = data['Close'].iloc[-2]
                change = current - previous
                change_pct = (change / previous) * 100
                
                emoji = "🟢" if change >= 0 else "🔴"
                overview += f"{emoji} **{name}:** {current:,.2f} ({change_pct:+.2f}%)\n"
        except:
            overview += f"⚠️ **{name}:** Data unavailable\n"
    
    overview += f"\n*Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
    
    return overview


def connect_blockchain_interface(private_key, contract_address):
    """Interface function for blockchain connection"""
    if not blockchain_enabled:
        return "❌ Blockchain integration is not enabled. Set BLOCKCHAIN_ENABLED=True in .env"
    
    if not private_key or not contract_address:
        return "⚠️ Please provide both private key and contract address"
    
    abi_path = os.path.join(os.path.dirname(__file__), 'contract_abi.json')
    
    result = portfolio_manager.connect_blockchain(
        private_key.strip(),
        contract_address.strip(),
        abi_path
    )
    
    return result


def sync_blockchain_interface():
    """Interface function for blockchain sync"""
    if not blockchain_enabled:
        return "❌ Blockchain not enabled"
    
    return portfolio_manager.sync_from_blockchain(USER_ID)


def get_blockchain_stats_interface():
    """Interface function for blockchain statistics"""
    if not blockchain_enabled:
        return "❌ Blockchain not enabled"
    
    return portfolio_manager.get_blockchain_stats()


def get_blockchain_connection_info():
    """Get blockchain connection status"""
    if not blockchain_enabled:
        return "❌ Blockchain integration disabled"
    
    if portfolio_manager.blockchain and portfolio_manager.blockchain.connected:
        return portfolio_manager.blockchain.get_connection_info()
    else:
        return "⚠️ Not connected to blockchain. Please connect your wallet."


with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="cyan",
        neutral_hue="slate"
    ),
    title="AI Stock Analyst + Blockchain",
    css="""
        .gradio-container {max-width: 1400px !important}
        .output-markdown {font-size: 15px}
        .tab-nav button {font-size: 16px; font-weight: 600}
    """
) as demo:
    
    gr.Markdown("""
    # 🚀 AI Stock Analyst with Blockchain Integration
    ### Powered by Machine Learning & Decentralized Technology
    
    Analyze stocks, manage your portfolio, and track investments on the blockchain!
    """)
    
    with gr.Tabs():
        
        with gr.Tab("📊 Stock Analysis"):
            gr.Markdown("### Get AI-powered analysis and recommendations for any stock")
            
            with gr.Row():
                with gr.Column(scale=2):
                    stock_input = gr.Textbox(
                        label="Enter Company Name or Stock Symbol",
                        placeholder="e.g., Apple, MSFT, Tesla, RELIANCE.NS",
                        lines=1
                    )
                    analyze_btn = gr.Button("🔍 Analyze Stock", variant="primary", size="lg")
                
                with gr.Column(scale=1):
                    gr.Markdown("""
                    **Tips:**
                    - Enter company name (Apple) or symbol (AAPL)
                    - Indian stocks: Add .NS (RELIANCE.NS)
                    - US stocks work directly (TSLA)
                    """)
            
            stock_output = gr.Markdown(label="Analysis Results")
            analyze_btn.click(
                fn=analyze_stock_interface,
                inputs=stock_input,
                outputs=stock_output
            )
        
        with gr.Tab("💼 Portfolio Management"):
            gr.Markdown("### Manage your investment portfolio")
            
            with gr.Tabs():
                with gr.Tab("➕ Add Investment"):
                    with gr.Row():
                        with gr.Column():
                            company_input = gr.Textbox(
                                label="Company Name",
                                placeholder="e.g., Apple, Microsoft"
                            )
                            shares_input = gr.Number(
                                label="Number of Shares",
                                value=1,
                                minimum=0.01
                            )
                        with gr.Column():
                            price_input = gr.Number(
                                label="Purchase Price per Share ($)",
                                value=100,
                                minimum=0.01
                            )
                            date_input = gr.Textbox(
                                label="Purchase Date (YYYY-MM-DD)",
                                value=datetime.now().strftime("%Y-%m-%d")
                            )
                    
                    add_btn = gr.Button("➕ Add to Portfolio", variant="primary", size="lg")
                    add_output = gr.Markdown()
                    
                    add_btn.click(
                        fn=add_investment_interface,
                        inputs=[company_input, shares_input, price_input, date_input],
                        outputs=add_output
                    )
                
                with gr.Tab("👁️ View Portfolio"):
                    view_btn = gr.Button("🔄 Refresh Portfolio", variant="secondary", size="lg")
                    portfolio_output = gr.Markdown()
                    
                    view_btn.click(
                        fn=view_portfolio_interface,
                        outputs=portfolio_output
                    )
                    
                    demo.load(fn=view_portfolio_interface, outputs=portfolio_output)
                
                with gr.Tab("🗑️ Remove Investment"):
                    gr.Markdown("Get the Investment ID from 'View Portfolio' tab")
                    
                    remove_id_input = gr.Textbox(
                        label="Investment ID",
                        placeholder="Paste investment ID here"
                    )
                    remove_btn = gr.Button("🗑️ Remove Investment", variant="stop")
                    remove_output = gr.Markdown()
                    
                    remove_btn.click(
                        fn=remove_investment_interface,
                        inputs=remove_id_input,
                        outputs=remove_output
                    )
        
        with gr.Tab("⚖️ Compare Stocks"):
            gr.Markdown("### Compare two stocks side-by-side")
            
            with gr.Row():
                stock1_input = gr.Textbox(
                    label="First Stock",
                    placeholder="e.g., AAPL"
                )
                stock2_input = gr.Textbox(
                    label="Second Stock",
                    placeholder="e.g., MSFT"
                )
            
            compare_btn = gr.Button("⚖️ Compare Stocks", variant="primary", size="lg")
            compare_output = gr.Markdown()
            
            compare_btn.click(
                fn=compare_stocks_interface,
                inputs=[stock1_input, stock2_input],
                outputs=compare_output
            )
        
        with gr.Tab("🔍 Search Stocks"):
            gr.Markdown("### Search for stocks in our database")
            
            search_input = gr.Textbox(
                label="Search Keyword",
                placeholder="e.g., tech, bank, auto"
            )
            search_btn = gr.Button("🔍 Search", variant="primary", size="lg")
            search_output = gr.Markdown()
            
            search_btn.click(
                fn=search_stocks_interface,
                inputs=search_input,
                outputs=search_output
            )
        
        with gr.Tab("🌍 Market Overview"):
            gr.Markdown("### Global market indices at a glance")
            
            market_btn = gr.Button("🔄 Refresh Market Data", variant="secondary", size="lg")
            market_output = gr.Markdown()
            
            market_btn.click(fn=get_market_overview, outputs=market_output)
            demo.load(fn=get_market_overview, outputs=market_output)
        
        if blockchain_enabled:
            with gr.Tab("🔗 Blockchain"):
                gr.Markdown("""
                ### Decentralized Portfolio Tracking
                Connect your wallet to store investments on the blockchain
                """)
                
                with gr.Tabs():
                    with gr.Tab("🔐 Connect Wallet"):
                        gr.Markdown("""
                        **⚠️ Security Warning:**
                        - Never share your private key
                        - Use testnet for testing
                        - Keep your keys secure
                        """)
                        
                        with gr.Row():
                            with gr.Column():
                                private_key_input = gr.Textbox(
                                    label="Private Key",
                                    placeholder="0x...",
                                    type="password"
                                )
                                contract_address_input = gr.Textbox(
                                    label="Contract Address",
                                    placeholder="0x...",
                                    value=os.getenv('CONTRACT_ADDRESS', '')
                                )
                                connect_btn = gr.Button("🔗 Connect Blockchain", variant="primary")
                            
                            with gr.Column():
                                connection_status = gr.Markdown()
                        
                        connect_btn.click(
                            fn=connect_blockchain_interface,
                            inputs=[private_key_input, contract_address_input],
                            outputs=connection_status
                        )
                    
                    with gr.Tab("🔄 Sync Portfolio"):
                        gr.Markdown("Sync your portfolio from the blockchain")
                        
                        sync_btn = gr.Button("🔄 Sync from Blockchain", variant="secondary", size="lg")
                        sync_output = gr.Markdown()
                        
                        sync_btn.click(
                            fn=sync_blockchain_interface,
                            outputs=sync_output
                        )
                    
                    with gr.Tab("📊 Blockchain Stats"):
                        stats_btn = gr.Button("📊 Get Statistics", variant="secondary", size="lg")
                        stats_output = gr.Markdown()
                        
                        stats_btn.click(
                            fn=get_blockchain_stats_interface,
                            outputs=stats_output
                        )
                    
                    with gr.Tab("ℹ️ Connection Info"):
                        info_btn = gr.Button("ℹ️ Check Connection", variant="secondary", size="lg")
                        info_output = gr.Markdown()
                        
                        info_btn.click(
                            fn=get_blockchain_connection_info,
                            outputs=info_output
                        )
        
        with gr.Tab("ℹ️ About"):
            gr.Markdown("""
            ## About This Application
            
            ### Features
            - 🤖 AI-powered stock analysis with technical indicators
            - 💼 Portfolio management and tracking
            - ⚖️ Stock comparison tools
            - 🔍 Stock search database
            - 🌍 Real-time market overview
            - 🔗 Blockchain integration for decentralized tracking
            
            ### Technical Indicators
            - RSI (Relative Strength Index)
            - MACD (Moving Average Convergence Divergence)
            - SMA (Simple Moving Averages)
            - Bollinger Bands
            - ATR (Average True Range)
            
            ### Data Sources
            - Yahoo Finance API
            - Real-time market data
            - Ethereum blockchain
            
            ### Developer
            **GitHub:** TheHashiramaSenju
            **Version:** 1.0.0
            
            ---
            
            *Built with Gradio, yfinance, Web3.py, and Hardhat*
            """)
    
    gr.Markdown("""
    ---
    © 2025 AI Stock Analyst | Built with ❤️ by TheHashiramaSenju
    """)


if __name__ == "__main__":
    port = int(os.getenv('GRADIO_PORT', 7860))
    share = os.getenv('GRADIO_SHARE', 'False').lower() == 'true'
    
    print(f"\n{'='*50}")
    print(f"🚀 Starting AI Stock Analyst")
    print(f"{'='*50}")
    print(f"📡 Port: {port}")
    print(f"🌐 Share: {share}")
    print(f"🔗 Blockchain: {'Enabled' if blockchain_enabled else 'Disabled'}")
    print(f"{'='*50}\n")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=share,
        show_error=True
    )
