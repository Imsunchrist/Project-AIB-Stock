"""
Stock Analysis Module - Finnhub Version
AI-powered stock analysis with Finnhub API (60 calls/min free!)
"""

import finnhub
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz, process
import warnings

warnings.filterwarnings('ignore')


class StockAdvisorFinnhub:
    """AI-powered stock analysis using Finnhub API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = finnhub.Client(api_key=api_key)
        
        self.company_symbols = {
            'apple': 'AAPL', 'microsoft': 'MSFT', 'google': 'GOOGL', 
            'alphabet': 'GOOGL', 'amazon': 'AMZN', 'tesla': 'TSLA',
            'meta': 'META', 'facebook': 'META', 'nvidia': 'NVDA',
            'netflix': 'NFLX', 'adobe': 'ADBE', 'salesforce': 'CRM',
            'oracle': 'ORCL', 'intel': 'INTC', 'amd': 'AMD',
            'cisco': 'CSCO', 'ibm': 'IBM', 'qualcomm': 'QCOM',
            'broadcom': 'AVGO', 'texas instruments': 'TXN',
            'paypal': 'PYPL', 'mastercard': 'MA', 'visa': 'V',
            'jpmorgan': 'JPM', 'bank of america': 'BAC',
            'wells fargo': 'WFC', 'goldman sachs': 'GS',
            'walmart': 'WMT', 'costco': 'COST', 'target': 'TGT',
            'home depot': 'HD', 'mcdonalds': 'MCD', 'nike': 'NKE',
            'starbucks': 'SBUX', 'coca cola': 'KO', 'pepsi': 'PEP'
        }
    
    def smart_symbol_lookup(self, company_query: str) -> str:
        """Fuzzy match company name to stock symbol"""
        query_lower = company_query.lower().strip()
        
        if query_lower in self.company_symbols:
            return self.company_symbols[query_lower]
        
        best_match = process.extractOne(
            query_lower, 
            self.company_symbols.keys(),
            scorer=fuzz.ratio
        )
        
        if best_match and best_match[1] > 70:
            return self.company_symbols[best_match[0]]
        
        return company_query.upper()
    
    def get_stock_data(self, symbol: str, days: int = 365) -> pd.DataFrame:
        """Fetch stock data from Finnhub"""
        try:
            print(f"Fetching data for {symbol} from Finnhub...")
            
            # Get historical data
            end_date = int(datetime.now().timestamp())
            start_date = int((datetime.now() - timedelta(days=days)).timestamp())
            
            res = self.client.stock_candles(symbol, 'D', start_date, end_date)
            
            if res['s'] != 'ok':
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame({
                'Open': res['o'],
                'High': res['h'],
                'Low': res['l'],
                'Close': res['c'],
                'Volume': res['v']
            }, index=pd.to_datetime(res['t'], unit='s'))
            
            return df
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def get_stock_quote(self, symbol: str) -> dict:
        """Get current stock quote"""
        try:
            quote = self.client.quote(symbol)
            
            if not quote or 'c' not in quote:
                return None
            
            return {
                'symbol': symbol,
                'price': quote['c'],  # Current price
                'change': quote['d'],  # Change
                'change_percent': quote['dp'],  # Change percent
                'high': quote['h'],  # Day high
                'low': quote['l'],  # Day low
                'open': quote['o'],  # Open price
                'previous_close': quote['pc']  # Previous close
            }
        except Exception as e:
            print(f"Error getting quote for {symbol}: {str(e)}")
            return None
    
    def get_company_profile(self, symbol: str) -> dict:
        """Get company information"""
        try:
            profile = self.client.company_profile2(symbol=symbol)
            return profile if profile else {}
        except:
            return {}
    
    def calculate_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators"""
        df = data.copy()
        
        try:
            # SMA
            df['SMA_20'] = df['Close'].rolling(window=20).mean()
            df['SMA_50'] = df['Close'].rolling(window=50).mean()
            df['SMA_200'] = df['Close'].rolling(window=200).mean()
            
            # RSI
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            # MACD
            exp1 = df['Close'].ewm(span=12, adjust=False).mean()
            exp2 = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = exp1 - exp2
            df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            
            # Bollinger Bands
            df['BB_Middle'] = df['Close'].rolling(window=20).mean()
            bb_std = df['Close'].rolling(window=20).std()
            df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
            df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
            
            # ATR
            high_low = df['High'] - df['Low']
            high_close = np.abs(df['High'] - df['Close'].shift())
            low_close = np.abs(df['Low'] - df['Close'].shift())
            ranges = pd.concat([high_low, high_close, low_close], axis=1)
            true_range = ranges.max(axis=1)
            df['ATR'] = true_range.rolling(14).mean()
            
            return df
            
        except Exception as e:
            print(f"Error calculating indicators: {str(e)}")
            return df
    
    def generate_signals(self, df: pd.DataFrame) -> dict:
        """Generate trading signals"""
        try:
            latest = df.iloc[-1]
            
            signals = {
                'buy_signals': [],
                'sell_signals': [],
                'neutral_signals': []
            }
            
            # SMA signals
            if pd.notna(latest['SMA_20']) and pd.notna(latest['SMA_50']):
                if latest['Close'] > latest['SMA_20'] > latest['SMA_50']:
                    signals['buy_signals'].append("Price above SMA20 and SMA50 (Bullish)")
                elif latest['Close'] < latest['SMA_20'] < latest['SMA_50']:
                    signals['sell_signals'].append("Price below SMA20 and SMA50 (Bearish)")
            
            # RSI signals
            if pd.notna(latest['RSI']):
                if latest['RSI'] < 30:
                    signals['buy_signals'].append(f"RSI oversold ({latest['RSI']:.1f})")
                elif latest['RSI'] > 70:
                    signals['sell_signals'].append(f"RSI overbought ({latest['RSI']:.1f})")
                else:
                    signals['neutral_signals'].append(f"RSI neutral ({latest['RSI']:.1f})")
            
            # MACD signals
            if pd.notna(latest['MACD']) and pd.notna(latest['Signal']):
                if latest['MACD'] > latest['Signal']:
                    signals['buy_signals'].append("MACD above signal line (Bullish)")
                else:
                    signals['sell_signals'].append("MACD below signal line (Bearish)")
            
            # Bollinger Bands
            if pd.notna(latest['BB_Upper']) and pd.notna(latest['BB_Lower']):
                if latest['Close'] > latest['BB_Upper']:
                    signals['sell_signals'].append("Price above upper Bollinger Band (Overbought)")
                elif latest['Close'] < latest['BB_Lower']:
                    signals['buy_signals'].append("Price below lower Bollinger Band (Oversold)")
            
            return signals
            
        except Exception as e:
            print(f"Error generating signals: {str(e)}")
            return {'buy_signals': [], 'sell_signals': [], 'neutral_signals': []}
    
    def analyze_stock(self, company_input: str) -> str:
        """Complete stock analysis with AI recommendations"""
        
        if not company_input or company_input.strip() == "":
            return "⚠️ Please enter a company name or stock symbol"
        
        symbol = self.smart_symbol_lookup(company_input)
        
        try:
            # Get current quote
            print(f"Analyzing {symbol} with Finnhub...")
            quote = self.get_stock_quote(symbol)
            
            if not quote:
                return f"""
## ❌ Unable to Fetch Data for {symbol}

### Possible Reasons:
1. **Invalid Stock Symbol** - Double-check the ticker
2. **Market Closed** - Try during market hours
3. **Stock Not Available** - Try US stocks (AAPL, MSFT, GOOGL)

### Suggestions:
**Try these verified symbols:**
- **US Stocks**: AAPL, MSFT, GOOGL, TSLA, AMZN, NVDA

**Or wait a minute and try again.**
"""
            
            # Get company profile
            profile = self.get_company_profile(symbol)
            
            # Get historical data
            data = self.get_stock_data(symbol, days=365)
            
            if data is None or data.empty:
                current_price = quote['price']
                change = quote['change']
                change_pct = quote['change_percent']
                
                return f"""
## 📊 {symbol} - Real-Time Quote

**Company:** {profile.get('name', symbol)}  
**Current Price:** ${current_price:.2f}  
**Change:** {'🟢' if change >= 0 else '🔴'} ${change:.2f} ({change_pct:+.2f}%)  
**Day High:** ${quote['high']:.2f}  
**Day Low:** ${quote['low']:.2f}  
**Previous Close:** ${quote['previous_close']:.2f}

**Industry:** {profile.get('finnhubIndustry', 'N/A')}  
**Market Cap:** ${profile.get('marketCapitalization', 0):.2f}B

---

*Powered by Finnhub | Real-time data*
"""
            
            # Calculate indicators
            df = self.calculate_technical_indicators(data)
            signals = self.generate_signals(df)
            
            # Extract metrics
            current_price = quote['price']
            change = quote['change']
            change_pct = quote['change_percent']
            
            year_high = df['High'].max()
            year_low = df['Low'].min()
            volatility = df['Close'].pct_change().std() * np.sqrt(252) * 100
            
            # Generate recommendation
            buy_score = len(signals['buy_signals'])
            sell_score = len(signals['sell_signals'])
            
            if buy_score > sell_score:
                recommendation = "BUY"
                confidence = min(90, 50 + (buy_score * 10))
                rec_emoji = "🟢"
            elif sell_score > buy_score:
                recommendation = "SELL"
                confidence = min(90, 50 + (sell_score * 10))
                rec_emoji = "🔴"
            else:
                recommendation = "HOLD"
                confidence = 50
                rec_emoji = "🟡"
            
            # Format analysis
            analysis = f"""
## 📊 Stock Analysis: {profile.get('name', symbol)} ({symbol})

### 📈 Current Price Information
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Current Price:** ${current_price:.2f}  
**Change:** {'🟢' if change >= 0 else '🔴'} ${change:.2f} ({change_pct:+.2f}%)  
**52-Week High:** ${year_high:.2f}  
**52-Week Low:** ${year_low:.2f}  
**Day Range:** ${quote['low']:.2f} - ${quote['high']:.2f}

### 🎯 AI Recommendation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Recommendation:** {rec_emoji} **{recommendation}**  
**Confidence:** {confidence}%

### 📊 Technical Indicators
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            
            latest = df.iloc[-1]
            if pd.notna(latest['RSI']):
                analysis += f"**RSI (14):** {latest['RSI']:.2f}\n"
            if pd.notna(latest['MACD']):
                analysis += f"**MACD:** {latest['MACD']:.2f}\n"
            if pd.notna(latest['Signal']):
                analysis += f"**Signal Line:** {latest['Signal']:.2f}\n"
            if pd.notna(latest['SMA_20']):
                analysis += f"**SMA 20:** ${latest['SMA_20']:.2f}\n"
            if pd.notna(latest['SMA_50']):
                analysis += f"**SMA 50:** ${latest['SMA_50']:.2f}\n"
            
            analysis += f"**Volatility:** {volatility:.2f}%\n"
            
            analysis += """
### 🎪 Trading Signals
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
            
            if signals['buy_signals']:
                analysis += "**🟢 Buy Signals:**\n"
                for signal in signals['buy_signals']:
                    analysis += f"  • {signal}\n"
                analysis += "\n"
            
            if signals['sell_signals']:
                analysis += "**🔴 Sell Signals:**\n"
                for signal in signals['sell_signals']:
                    analysis += f"  • {signal}\n"
                analysis += "\n"
            
            if signals['neutral_signals']:
                analysis += "**🟡 Neutral Signals:**\n"
                for signal in signals['neutral_signals']:
                    analysis += f"  • {signal}\n"
                analysis += "\n"
            
            # Add company info
            if profile:
                analysis += f"""
### ℹ️ Company Information
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Industry:** {profile.get('finnhubIndustry', 'N/A')}  
**Market Cap:** ${profile.get('marketCapitalization', 0):.2f}B  
**Country:** {profile.get('country', 'N/A')}  
**IPO Date:** {profile.get('ipo', 'N/A')}  
**Website:** {profile.get('weburl', 'N/A')}
"""
            
            analysis += f"""
---
*Analysis powered by Finnhub | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | Real-time data*
"""
            
            return analysis
            
        except Exception as e:
            return f"""
## ❌ Analysis Error for {symbol}

**Error:** {str(e)}

**Troubleshooting:**
- Verify stock symbol is correct (US stocks only)
- Check if market is open
- Try again in a few seconds

**Try these verified symbols:** AAPL, MSFT, GOOGL, NVDA, TSLA
"""
    
    def get_current_price(self, symbol: str) -> float:
        """Get current stock price"""
        try:
            quote = self.get_stock_quote(symbol)
            return quote['price'] if quote else 0.0
        except:
            return 0.0
