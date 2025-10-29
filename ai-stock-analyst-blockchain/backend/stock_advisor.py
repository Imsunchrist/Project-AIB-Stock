"""
Stock Analysis Module - AI-powered stock analysis with robust error handling
Enhanced with retry logic and comprehensive error handling for Yahoo Finance API
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz, process
import warnings
import time
import random
import json

warnings.filterwarnings('ignore')


class StockAdvisor:
    """AI-powered stock analysis and recommendation system with robust error handling"""
    
    def __init__(self):
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
            'starbucks': 'SBUX', 'coca cola': 'KO', 'pepsi': 'PEP',
            'reliance': 'RELIANCE.NS', 'tcs': 'TCS.NS', 'infosys': 'INFY.NS',
            'hdfc bank': 'HDFCBANK.NS', 'icici bank': 'ICICIBANK.NS',
            'wipro': 'WIPRO.NS', 'sbi': 'SBIN.NS', 'bharti airtel': 'BHARTIARTL.NS'
        }
    
    def smart_symbol_lookup(self, company_query: str) -> str:
        """Fuzzy match company name to stock symbol"""
        query_lower = company_query.lower().strip()
        
        # Direct match
        if query_lower in self.company_symbols:
            return self.company_symbols[query_lower]
        
        # Fuzzy match
        best_match = process.extractOne(
            query_lower, 
            self.company_symbols.keys(),
            scorer=fuzz.ratio
        )
        
        if best_match and best_match[1] > 70:
            return self.company_symbols[best_match[0]]
        
        # Return as-is if no match
        return company_query.upper()
    
    def safe_api_call(self, func, *args, max_retries=3, **kwargs):
        """Wrapper for API calls with retry logic and exponential backoff"""
        for attempt in range(max_retries):
            try:
                # Add small random delay to avoid rate limits
                if attempt > 0:
                    delay = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(delay)
                
                result = func(*args, **kwargs)
                return result
                
            except json.JSONDecodeError as e:
                print(f"JSON decode error on attempt {attempt + 1}: {str(e)}")
                if attempt == max_retries - 1:
                    return None
                    
            except Exception as e:
                print(f"API call failed on attempt {attempt + 1}: {str(e)}")
                if attempt == max_retries - 1:
                    return None
        
        return None
    
    def get_stock_data(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """Fetch stock data from yfinance with retry logic"""
        try:
            stock = yf.Ticker(symbol)
            data = self.safe_api_call(stock.history, period=period)
            
            if data is None or data.empty:
                print(f"No data returned for {symbol}")
                return None
            
            return data
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def get_stock_info(self, symbol: str) -> dict:
        """Get stock info with retry and fallback logic"""
        try:
            stock = yf.Ticker(symbol)
            info = self.safe_api_call(lambda: stock.info)
            
            if info and isinstance(info, dict) and len(info) > 0:
                return info
            
            # Fallback: try fast_info
            try:
                fast_info = stock.fast_info
                if fast_info:
                    return {
                        'regularMarketPrice': getattr(fast_info, 'last_price', None),
                        'marketCap': getattr(fast_info, 'market_cap', None),
                        'symbol': symbol,
                        'longName': symbol
                    }
            except:
                pass
            
            return None
            
        except Exception as e:
            print(f"Error fetching info for {symbol}: {str(e)}")
            return None
    
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
    
    def format_large_number(self, num):
        """Format large numbers for display"""
        if num is None or num == 'N/A':
            return 'N/A'
        
        try:
            num = float(num)
            if num >= 1_000_000_000_000:
                return f"${num/1_000_000_000_000:.2f}T"
            elif num >= 1_000_000_000:
                return f"${num/1_000_000_000:.2f}B"
            elif num >= 1_000_000:
                return f"${num/1_000_000:.2f}M"
            else:
                return f"${num:,.2f}"
        except:
            return str(num)
    
    def analyze_stock(self, company_input: str) -> str:
        """Complete stock analysis with AI recommendations and comprehensive error handling"""
        
        if not company_input or company_input.strip() == "":
            return "⚠️ Please enter a company name or stock symbol"
        
        symbol = self.smart_symbol_lookup(company_input)
        
        try:
            # Get stock info with retry
            print(f"Fetching info for {symbol}...")
            info = self.get_stock_info(symbol)
            
            # If info fetch fails, try alternative symbols
            if not info or len(info) == 0:
                alt_symbols = [
                    symbol,
                    symbol.upper(),
                    f"{symbol}.NS" if not symbol.endswith('.NS') else symbol.replace('.NS', ''),
                    f"{symbol}.BSE" if not symbol.endswith('.BSE') else symbol.replace('.BSE', '')
                ]
                
                for alt_symbol in alt_symbols:
                    if alt_symbol == symbol:
                        continue
                    print(f"Trying alternative symbol: {alt_symbol}")
                    info = self.get_stock_info(alt_symbol)
                    if info and len(info) > 0:
                        symbol = alt_symbol
                        break
            
            # If still no info, return helpful error
            if not info or len(info) == 0:
                return f"""
## ❌ Unable to Fetch Data for {symbol}

### Possible Reasons:
1. **Invalid Stock Symbol** - Double-check the ticker
2. **Yahoo Finance API Issue** - Try again in 60 seconds
3. **Market Closed** - Some data may not be available
4. **Rate Limit** - Too many requests from this server

### Suggestions:
**Try these verified symbols:**
- **US Stocks**: AAPL, MSFT, GOOGL, TSLA, AMZN, NVDA
- **Indian Stocks**: RELIANCE.NS, TCS.NS, INFY.NS

**Or wait 1-2 minutes and try again.**

---
*If this persists, Yahoo Finance may be temporarily unavailable.*
"""
            
            # Get historical data
            print(f"Fetching historical data for {symbol}...")
            data = self.get_stock_data(symbol, period="1y")
            
            # If no historical data, show basic info only
            if data is None or data.empty:
                current_price = info.get('regularMarketPrice', info.get('currentPrice', 'N/A'))
                market_cap = self.format_large_number(info.get('marketCap', 'N/A'))
                
                return f"""
## 📊 {info.get('longName', symbol)} ({symbol})

### ⚠️ Limited Data Available

We can show basic information, but technical analysis requires historical data.

**Current Price:** ${current_price}  
**Market Cap:** {market_cap}  
**Sector:** {info.get('sector', 'N/A')}  
**Industry:** {info.get('industry', 'N/A')}

---

**Note:** Historical data temporarily unavailable. Try again in a few minutes for full analysis with technical indicators.
"""
            
            # Calculate technical indicators
            print(f"Calculating technical indicators...")
            df = self.calculate_technical_indicators(data)
            signals = self.generate_signals(df)
            
            # Extract key metrics
            current_price = df['Close'].iloc[-1]
            prev_close = df['Close'].iloc[-2] if len(df) > 1 else current_price
            change = current_price - prev_close
            change_pct = (change / prev_close) * 100
            
            year_high = df['High'].max()
            year_low = df['Low'].min()
            
            volatility = df['Close'].pct_change().std() * np.sqrt(252) * 100
            
            # Calculate recommendation
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
            
            # Format output
            analysis = f"""
## 📊 Stock Analysis: {info.get('longName', symbol)} ({symbol})

### 📈 Current Price Information
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Current Price:** ${current_price:.2f}  
**Change:** {'🟢' if change >= 0 else '🔴'} ${change:.2f} ({change_pct:+.2f}%)  
**52-Week High:** ${year_high:.2f}  
**52-Week Low:** ${year_low:.2f}

### 🎯 AI Recommendation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Recommendation:** {rec_emoji} **{recommendation}**  
**Confidence:** {confidence}%

### 📊 Technical Indicators
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            
            # Add technical indicators if available
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
            
            # Trading signals
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
            
            # Company info
            analysis += f"""
### ℹ️ Company Information
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Sector:** {info.get('sector', 'N/A')}  
**Industry:** {info.get('industry', 'N/A')}  
**Market Cap:** {self.format_large_number(info.get('marketCap', 'N/A'))}  
**P/E Ratio:** {info.get('trailingPE', 'N/A')}

---
*Analysis generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
            
            return analysis
            
        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)
            
            return f"""
## ❌ Analysis Error for {symbol}

**Error Type:** {error_type}  
**Details:** {error_msg}

### Troubleshooting Steps:
1. **Wait 60 seconds** and try again (likely rate limit)
2. **Verify symbol** is correct (e.g., AAPL, MSFT, TSLA)
3. **Try different stock** to test if issue is symbol-specific
4. **Check market hours** (US: 9:30 AM - 4:00 PM ET, Mon-Fri)

### Common Issues:
- **Rate Limiting:** Too many requests from shared servers
- **API Timeout:** Yahoo Finance slow to respond
- **Invalid Symbol:** Stock ticker doesn't exist
- **Market Closed:** Limited data outside trading hours

**Try these verified symbols:** AAPL, MSFT, GOOGL, NVDA, TSLA

---
*If problem persists, Yahoo Finance API may be temporarily unavailable.*
"""
    
    def get_current_price(self, symbol: str) -> float:
        """Get current stock price with retry logic"""
        try:
            stock = yf.Ticker(symbol)
            data = self.safe_api_call(stock.history, period="1d")
            
            if data is not None and not data.empty:
                return float(data['Close'].iloc[-1])
            
            # Fallback: try fast_info
            try:
                fast_info = stock.fast_info
                if fast_info and hasattr(fast_info, 'last_price'):
                    return float(fast_info.last_price)
            except:
                pass
            
            return 0.0
            
        except Exception as e:
            print(f"Error getting price for {symbol}: {str(e)}")
            return 0.0
