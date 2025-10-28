import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz, process
import warnings
warnings.filterwarnings('ignore')


class StockAdvisor:
    """AI-powered stock analysis and recommendation system"""
    
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
            'morgan stanley': 'MS', 'citigroup': 'C',
            'walmart': 'WMT', 'costco': 'COST', 'target': 'TGT',
            'home depot': 'HD', 'mcdonalds': 'MCD', 'nike': 'NKE',
            'starbucks': 'SBUX', 'coca cola': 'KO', 'pepsi': 'PEP',
            'procter gamble': 'PG', 'johnson johnson': 'JNJ',
            'pfizer': 'PFE', 'merck': 'MRK', 'abbvie': 'ABBV',
            'exxon': 'XOM', 'chevron': 'CVX', 'conocophillips': 'COP',
            'boeing': 'BA', 'lockheed martin': 'LMT', 'ge': 'GE',
            'caterpillar': 'CAT', '3m': 'MMM', 'honeywell': 'HON',
            'uber': 'UBER', 'lyft': 'LYFT', 'airbnb': 'ABNB',
            'spotify': 'SPOT', 'snap': 'SNAP', 'twitter': 'TWTR',
            'pinterest': 'PINS', 'zoom': 'ZM', 'shopify': 'SHOP',
            'square': 'SQ', 'docusign': 'DOCU', 'twilio': 'TWLO',
            'reliance': 'RELIANCE.NS', 'tcs': 'TCS.NS', 'infosys': 'INFY.NS',
            'hdfc bank': 'HDFCBANK.NS', 'icici bank': 'ICICIBANK.NS',
            'bharti airtel': 'BHARTIARTL.NS', 'itc': 'ITC.NS',
            'hindustan unilever': 'HINDUNILVR.NS', 'asian paints': 'ASIANPAINT.NS',
            'maruti suzuki': 'MARUTI.NS', 'bajaj finance': 'BAJFINANCE.NS',
            'wipro': 'WIPRO.NS', 'sbi': 'SBIN.NS', 'adani': 'ADANIENT.NS'
        }
        
        self.sector_etfs = {
            'technology': 'XLK', 'healthcare': 'XLV', 'finance': 'XLF',
            'energy': 'XLE', 'consumer': 'XLP', 'industrial': 'XLI',
            'materials': 'XLB', 'real estate': 'XLRE', 'utilities': 'XLU'
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
    
    def get_stock_data(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """Fetch stock data from yfinance"""
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period=period)
            
            if data.empty:
                return None
            
            return data
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def calculate_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators"""
        df = data.copy()
        
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        df['ATR'] = true_range.rolling(14).mean()
        
        return df
    
    def generate_signals(self, df: pd.DataFrame) -> dict:
        """Generate trading signals based on technical indicators"""
        latest = df.iloc[-1]
        
        signals = {
            'buy_signals': [],
            'sell_signals': [],
            'neutral_signals': []
        }
        
        if pd.notna(latest['SMA_20']) and pd.notna(latest['SMA_50']):
            if latest['Close'] > latest['SMA_20'] > latest['SMA_50']:
                signals['buy_signals'].append("Price above SMA20 and SMA50 (Bullish)")
            elif latest['Close'] < latest['SMA_20'] < latest['SMA_50']:
                signals['sell_signals'].append("Price below SMA20 and SMA50 (Bearish)")
        
        if pd.notna(latest['RSI']):
            if latest['RSI'] < 30:
                signals['buy_signals'].append(f"RSI oversold ({latest['RSI']:.1f})")
            elif latest['RSI'] > 70:
                signals['sell_signals'].append(f"RSI overbought ({latest['RSI']:.1f})")
            else:
                signals['neutral_signals'].append(f"RSI neutral ({latest['RSI']:.1f})")
        
        if pd.notna(latest['MACD']) and pd.notna(latest['Signal']):
            if latest['MACD'] > latest['Signal']:
                signals['buy_signals'].append("MACD above signal line (Bullish)")
            else:
                signals['sell_signals'].append("MACD below signal line (Bearish)")
        
        if pd.notna(latest['BB_Upper']) and pd.notna(latest['BB_Lower']):
            if latest['Close'] > latest['BB_Upper']:
                signals['sell_signals'].append("Price above upper Bollinger Band (Overbought)")
            elif latest['Close'] < latest['BB_Lower']:
                signals['buy_signals'].append("Price below lower Bollinger Band (Oversold)")
        
        return signals
    
    def analyze_stock(self, company_input: str) -> str:
        """Complete stock analysis with AI recommendations"""
        symbol = self.smart_symbol_lookup(company_input)
        
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            data = self.get_stock_data(symbol, period="1y")
            if data is None or data.empty:
                return f"❌ Unable to fetch data for {symbol}"
            
            df = self.calculate_technical_indicators(data)
            signals = self.generate_signals(df)
            
            current_price = df['Close'].iloc[-1]
            prev_close = df['Close'].iloc[-2] if len(df) > 1 else current_price
            change = current_price - prev_close
            change_pct = (change / prev_close) * 100
            
            year_high = df['High'].max()
            year_low = df['Low'].min()
            
            avg_volume = df['Volume'].mean()
            current_volume = df['Volume'].iloc[-1]
            
            volatility = df['Close'].pct_change().std() * np.sqrt(252) * 100
            
            buy_score = len(signals['buy_signals'])
            sell_score = len(signals['sell_signals'])
            
            if buy_score > sell_score:
                recommendation = "🟢 BUY"
                confidence = min(90, 50 + (buy_score * 10))
            elif sell_score > buy_score:
                recommendation = "🔴 SELL"
                confidence = min(90, 50 + (sell_score * 10))
            else:
                recommendation = "🟡 HOLD"
                confidence = 50
            
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
**Recommendation:** {recommendation}
**Confidence:** {confidence}%

### 📊 Technical Indicators
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**RSI (14):** {df['RSI'].iloc[-1]:.2f}
**MACD:** {df['MACD'].iloc[-1]:.2f}
**Signal Line:** {df['Signal'].iloc[-1]:.2f}
**SMA 20:** ${df['SMA_20'].iloc[-1]:.2f}
**SMA 50:** ${df['SMA_50'].iloc[-1]:.2f}
**Volatility:** {volatility:.2f}%

### 🎪 Trading Signals
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            
            if signals['buy_signals']:
                analysis += "\n**🟢 Buy Signals:**\n"
                for signal in signals['buy_signals']:
                    analysis += f"  • {signal}\n"
            
            if signals['sell_signals']:
                analysis += "\n**🔴 Sell Signals:**\n"
                for signal in signals['sell_signals']:
                    analysis += f"  • {signal}\n"
            
            if signals['neutral_signals']:
                analysis += "\n**🟡 Neutral Signals:**\n"
                for signal in signals['neutral_signals']:
                    analysis += f"  • {signal}\n"
            
            analysis += f"""
### 📉 Volume Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Current Volume:** {current_volume:,.0f}
**Average Volume:** {avg_volume:,.0f}
**Volume Ratio:** {(current_volume/avg_volume):.2f}x

### ℹ️ Company Information
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Sector:** {info.get('sector', 'N/A')}
**Industry:** {info.get('industry', 'N/A')}
**Market Cap:** ${info.get('marketCap', 0)/1e9:.2f}B
**P/E Ratio:** {info.get('trailingPE', 'N/A')}

---
*Analysis generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
            
            return analysis
            
        except Exception as e:
            return f"❌ Error analyzing {symbol}: {str(e)}"
    
    def get_current_price(self, symbol: str) -> float:
        """Get current stock price"""
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1d")
            if not data.empty:
                return data['Close'].iloc[-1]
            return 0.0
        except:
            return 0.0
