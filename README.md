# 🚀 AI Stock Analyst with Blockchain Integration

<div align="center">

![Python](https://img.shields.io/badge/Python-3).


![Solidity](https://img.shields.io/badge/Solidity-0.8.28-363636?style=for-the-badge&logo=solidity&logoio/badge/Hardhat-2.22.0-FFF100?style=for-the-badge/badge/Ethereum-3C3C3D?style=forio/badge/Gradio-4.44.0-FF)







**A revolutionary financial analytics platform combining AI-powered stock analysis with blockchain-verified portfolio management**

[Features](#-key-features) -  [Demo](#-demo) -  [Installation](#-installation) -  [Usage](#-usage) -  [Architecture](#-architecture) -  [Contributing](#-contributing)

</div>

***

## 📖 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Project Architecture](#-project-architecture)
- [Installation Guide](#-installation-guide)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [Smart Contract Details](#-smart-contract-details)
- [API Reference](#-api-reference)
- [Security Considerations](#-security-considerations)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

***

## 🌟 Overview

The **AI Stock Analyst with Blockchain Integration** is a cutting-edge financial technology platform that bridges traditional stock market analysis with decentralized blockchain technology. Built for investors, traders, and financial analysts, this system provides:

- **Real-time stock analysis** powered by machine learning algorithms
- **Technical indicators** including RSI, MACD, Bollinger Bands, and ATR
- **Immutable portfolio tracking** on Ethereum blockchain
- **AI-driven buy/sell recommendations** with confidence scoring
- **Multi-market support** covering US and Indian stock exchanges
- **Beautiful web interface** built with Gradio for seamless user experience

### 🎯 Why This Project?

Traditional portfolio management systems are centralized, prone to data manipulation, and lack transparency. This project solves these problems by:

1. **Decentralization**: Investment records stored on blockchain cannot be altered or deleted
2. **Transparency**: All transactions are verifiable and auditable
3. **AI Intelligence**: Advanced algorithms provide data-driven investment insights
4. **Zero Trust**: No central authority controls your portfolio data
5. **Real-time Data**: Live stock prices and market data from Yahoo Finance API

***

## ✨ Key Features

### 🤖 AI-Powered Stock Analysis

- **Smart Symbol Lookup**: Fuzzy matching for company names (supports "Apple", "AAPL", etc.)
- **Technical Indicators**:
  - RSI (Relative Strength Index) - Identifies overbought/oversold conditions
  - MACD (Moving Average Convergence Divergence) - Trend momentum indicator
  - SMA (Simple Moving Averages) - 20, 50, 200 day averages
  - Bollinger Bands - Volatility and price level analysis
  - ATR (Average True Range) - Volatility measurement
- **AI Recommendation Engine**: Buy/Hold/Sell signals with confidence scores (0-100%)
- **Multi-factor Analysis**: Combines technical, fundamental, and sentiment analysis
- **Support for 80+ companies**: Major US stocks and Indian NSE stocks

### 💼 Portfolio Management

- **Local Storage**: Fast portfolio tracking with SQLite-like structure
- **Blockchain Verification**: Optional on-chain storage for immutable records
- **Real-time Valuation**: Live portfolio value updates using current market prices
- **Gain/Loss Tracking**: Detailed P&L calculations per investment
- **Multi-investment Support**: Track unlimited investments across different stocks
- **Purchase History**: Complete historical record with dates and prices

### 🔗 Blockchain Integration

- **Ethereum Smart Contract**: Solidity 0.8.28 with gas-optimized code
- **Web3.py Integration**: Seamless Python-Ethereum communication
- **Multi-network Support**:
  - Local Hardhat node (development)
  - Sepolia testnet (testing)
  - Ethereum mainnet (production)
- **Transaction Verification**: Real-time confirmation tracking
- **Gas Reporting**: Detailed gas usage analysis
- **20 Test Accounts**: Pre-funded accounts with 10,000 ETH each (local development)

### 📊 Advanced Analytics

- **Stock Comparison Tool**: Side-by-side analysis of multiple stocks
- **Market Overview Dashboard**: Real-time indices (S&P 500, NASDAQ, NIFTY 50, SENSEX)
- **Search Database**: Searchable database of 80+ companies
- **Volatility Analysis**: Historical volatility calculations
- **Volume Analysis**: Trading volume patterns and anomalies
- **Sector Performance**: Industry-wise market trends

### 🎨 User Interface

- **Gradio Framework**: Modern, responsive web interface
- **Tab-based Navigation**: Intuitive organization of features
- **Real-time Updates**: Auto-refreshing data displays
- **Mobile-responsive**: Works on all device sizes
- **Dark Mode Compatible**: Eye-friendly interface
- **Interactive Charts**: Visual representations of stock data

***

## 🛠️ Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.9+ | Core application logic |
| Gradio | 4.44.0 | Web UI framework |
| yfinance | 0.2.46 | Stock market data API |
| pandas | 2.2.3 | Data manipulation |
| numpy | 2.1.2 | Numerical computations |
| Web3.py | 7.4.0 | Ethereum blockchain interaction |
| eth-account | 0.13.4 | Wallet management |
| plotly | 5.24.1 | Interactive visualizations |
| matplotlib | 3.9.2 | Static plots |
| seaborn | 0.13.2 | Statistical visualizations |

### Blockchain

| Technology | Version | Purpose |
|------------|---------|---------|
| Solidity | 0.8.28 | Smart contract language |
| Hardhat | 2.22.0 | Development environment |
| Ethers.js | 6.13.0 | Ethereum library |
| Chai | 4.3.10 | Testing framework |
| Hardhat Toolbox | 5.0.0 | Essential Hardhat plugins |

### External Services

- **Yahoo Finance API**: Real-time stock data (free tier)
- **Alchemy/Infura**: Ethereum RPC providers (testnet/mainnet)
- **Etherscan API**: Contract verification (optional)

***

## 🏗️ Project Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    (Gradio Web Application)                     │
│                      http://localhost:7860                      │
└───────────────────────────┬─────────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
┌─────────────────────┐         ┌─────────────────────┐
│   Stock Advisor     │         │ Portfolio Manager   │
│   (stock_advisor.py)│         │(portfolio_manager.py)│
│                     │         │                     │
│ • Symbol lookup     │         │ • Local storage    │
│ • Data fetching     │         │ • Value calculation │
│ • Technical analysis│         │ • P&L tracking     │
│ • AI recommendations│         │ • Blockchain sync  │
└──────────┬──────────┘         └─────────┬───────────┘
           │                              │
           ▼                              ▼
┌──────────────────────┐      ┌──────────────────────┐
│  Yahoo Finance API   │      │ Blockchain Manager   │
│     (yfinance)       │      │(blockchain_integration)│
│                      │      │                      │
│ • Price data         │      │ • Web3 connection   │
│ • Company info       │      │ • Transaction signing│
│ • Historical data    │      │ • Contract calls    │
└──────────────────────┘      └──────────┬───────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │   Ethereum Network   │
                              │  (Local/Testnet/Main)│
                              │                      │
                              │ PortfolioTracker.sol │
                              │ • addInvestment()   │
                              │ • getInvestments()  │
                              │ • removeInvestment()│
                              └──────────────────────┘
```

### Directory Structure

```
ai-stock-analyst-blockchain/
│
├── backend/                          # Python application
│   ├── __init__.py                   # Package initialization
│   ├── app.py                        # Main Gradio application (500+ lines)
│   ├── blockchain_integration.py     # Web3 blockchain manager (350+ lines)
│   ├── portfolio_manager.py          # Portfolio logic (300+ lines)
│   ├── stock_advisor.py              # Stock analysis engine (400+ lines)
│   ├── requirements.txt              # Python dependencies
│   ├── .env                          # Backend configuration
│   ├── contract_abi.json             # Smart contract ABI (auto-generated)
│   └── contract_info.json            # Deployment info (auto-generated)
│
├── blockchain/                       # Smart contract project
│   ├── contracts/
│   │   └── PortfolioTracker.sol     # Main smart contract (250+ lines)
│   │
│   ├── scripts/
│   │   ├── deploy.js                # Deployment automation (150+ lines)
│   │   └── interact.js              # Contract testing script (200+ lines)
│   │
│   ├── test/
│   │   └── PortfolioTracker.test.js # 20+ test cases (300+ lines)
│   │
│   ├── deployments/                 # Deployment records (auto-generated)
│   ├── hardhat.config.js            # Hardhat configuration
│   ├── package.json                 # Node.js dependencies
│   └── .env                         # Blockchain configuration
│
├── artifacts/                        # Compiled contracts (auto-generated)
│   └── contracts/
│       └── PortfolioTracker.sol/
│           ├── PortfolioTracker.json     # Contract ABI + bytecode
│           └── PortfolioTracker.dbg.json # Debug information
│
├── .env                             # Root environment variables
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

**Total Lines of Code**: ~2,500+ lines across 15+ files

***

## 🚀 Installation Guide

### Prerequisites

Ensure you have these installed:

- **Node.js** 16.0.0 or higher ([Download](https://nodejs.org/))
- **Python** 3.9 or higher ([Download](https://python.org/))
- **npm** or **yarn** package manager
- **Git** for version control
- **MetaMask** browser extension (optional, for mainnet)

**Verify installations:**

```bash
node --version    # Should show v16.x.x or higher
python --version  # Should show Python 3.9.x or higher
npm --version     # Should show 8.x.x or higher
# OR
yarn --version    # Should show 1.x.x or 3.x.x
```

### Quick Start (5 minutes)

```bash
# 1. Clone or create project directory
mkdir ai-stock-analyst-blockchain && cd ai-stock-analyst-blockchain

# 2. Create folder structure
mkdir -p backend blockchain/contracts blockchain/scripts blockchain/test artifacts

# 3. Copy all provided code files into respective folders

# 4. Install blockchain dependencies
cd blockchain
npm install
# OR
yarn install

# 5. Install Python dependencies
cd ../backend
pip install -r requirements.txt

# 6. Configure environment variables (see Configuration section)

# 7. Start local blockchain (Terminal 1)
cd ../blockchain
npx hardhat node

# 8. Deploy smart contract (Terminal 2)
npx hardhat compile
npx hardhat run scripts/deploy.js --network localhost

# 9. Update backend/.env with contract address and private key

# 10. Run application (Terminal 3)
cd ../backend
python app.py

# 11. Open browser
# Navigate to http://localhost:7860
```

### Detailed Installation

#### Step 1: Project Setup

```bash
# Create main directory
mkdir ai-stock-analyst-blockchain
cd ai-stock-analyst-blockchain

# Create all subdirectories
mkdir -p backend blockchain/contracts blockchain/scripts blockchain/test artifacts/contracts/PortfolioTracker.sol
```

#### Step 2: Copy Source Files

Place the provided code files in their respective locations:

- Backend Python files → `backend/`
- Smart contracts → `blockchain/contracts/`
- Scripts → `blockchain/scripts/`
- Tests → `blockchain/test/`
- Configuration files → Root and respective folders

#### Step 3: Install Dependencies

**Blockchain (Node.js):**

```bash
cd blockchain

# Using npm
npm install

# OR using yarn
yarn install

# Verify installation
ls node_modules | wc -l
# Should show 200+ packages
```

**Backend (Python):**

```bash
cd ../backend

pip install -r requirements.txt

# Verify installation
pip list | grep -E "gradio|yfinance|web3"
# Should show all three packages
```

***

## ⚙️ Configuration

### Environment Variables

#### Root `.env`

```bash
PROJECT_NAME=ai-stock-analyst-blockchain
ENVIRONMENT=development

BLOCKCHAIN_ENABLED=True
CONTRACT_ADDRESS=                    # Filled after deployment
RPC_URL=http://127.0.0.1:8545       # Local node
NETWORK=localhost

GRADIO_PORT=7860
GRADIO_SHARE=False
DEBUG_MODE=True
```

#### `blockchain/.env`

```bash
# For testnet/mainnet deployment
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_KEY
MAINNET_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY
PRIVATE_KEY=your_private_key_here
ETHERSCAN_API_KEY=your_etherscan_key
REPORT_GAS=false
```

#### `backend/.env`

```bash
BLOCKCHAIN_ENABLED=True
CONTRACT_ADDRESS=0x5FbDB2315678afecb367f032d93F642f64180aa3  # From deployment
RPC_URL=http://127.0.0.1:8545
WALLET_PRIVATE_KEY=0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80  # Test account

GRADIO_PORT=7860
GRADIO_SHARE=False
DEBUG_MODE=True
```

### Network Configuration

| Network | RPC URL | Chain ID | Cost |
|---------|---------|----------|------|
| Hardhat (Local) | http://127.0.0.1:8545 | 1337 | Free |
| Sepolia Testnet | alchemy.com/sepolia | 11155111 | Free (testnet ETH) |
| Ethereum Mainnet | alchemy.com/mainnet | 1 | Real ETH required |

---

## 📚 Usage Guide

### Starting the Application

**Terminal 1: Blockchain Node**

```bash
cd blockchain
npx hardhat node
```

This provides 20 test accounts with 10,000 ETH each.

**Terminal 2: Deploy Contract**

```bash
cd blockchain
npx hardhat compile
npx hardhat run scripts/deploy.js --network localhost
```

Copy the contract address and Account #0 private key.

**Terminal 3: Run Application**

```bash
cd backend
python app.py
```

Open `http://localhost:7860` in your browser.

### Feature Walkthroughs

#### 1. Stock Analysis

**Steps:**
1. Navigate to **"Stock Analysis"** tab
2. Enter company name (e.g., "Apple", "Microsoft") or symbol (e.g., "AAPL", "MSFT")
3. Click **"Analyze Stock"** button
4. Wait 5-10 seconds for analysis

**Output includes:**
- Current price and daily change
- 52-week high/low
- AI recommendation (BUY/HOLD/SELL) with confidence score
- Technical indicators (RSI, MACD, Bollinger Bands)
- Buy/sell signals based on indicators
- Volume analysis
- Company information (sector, industry, market cap)

#### 2. Portfolio Management

**Add Investment:**
1. Go to **"Portfolio Management"** → **"Add Investment"** tab
2. Fill in details:
   - Company Name: `Apple`
   - Shares: `10`
   - Price: `175.50`
   - Date: `2025-10-28`
3. Click **"Add to Portfolio"**
4. If blockchain enabled: Transaction executes on-chain (~10-15 seconds)

**View Portfolio:**
1. Go to **"View Portfolio"** tab
2. Click **"Refresh Portfolio"**
3. See:
   - Total invested amount
   - Current portfolio value
   - Overall gain/loss percentage
   - Individual holdings with real-time prices
   - Blockchain verification badges (🔗) for on-chain investments

**Remove Investment:**
1. Go to **"Remove Investment"** tab
2. Copy investment ID from portfolio view
3. Paste ID and click **"Remove Investment"**

#### 3. Blockchain Operations

**Connect Wallet:**
1. Navigate to **"Blockchain"** → **"Connect Wallet"** tab
2. Enter:
   - Private Key: `0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80`
   - Contract Address: `0x5FbDB2315678afecb367f032d93F642f64180aa3`
3. Click **"Connect Blockchain"**
4. Confirmation shows wallet address, contract address, chain ID

**Sync from Blockchain:**
1. Go to **"Sync Portfolio"** tab
2. Click **"Sync from Blockchain"**
3. All on-chain investments load into local database

**View Statistics:**
1. Go to **"Blockchain Stats"** tab
2. Click **"Get Statistics"**
3. See:
   - Active investment count
   - Total invested amount (from blockchain)
   - Wallet and contract addresses

#### 4. Compare Stocks

1. Navigate to **"Compare Stocks"** tab
2. Enter two stock symbols (e.g., "AAPL" and "MSFT")
3. Click **"Compare Stocks"**
4. View side-by-side comparison table with:
   - Current prices
   - 6-month returns
   - Volatility comparison
   - Market caps
   - P/E ratios
   - Performance winner

#### 5. Market Overview

1. Go to **"Market Overview"** tab
2. Click **"Refresh Market Data"**
3. See real-time prices and changes for:
   - S&P 500
   - Dow Jones
   - NASDAQ
   - NIFTY 50
   - SENSEX

***

## 🔐 Smart Contract Details

### PortfolioTracker.sol

**Contract Address** (Local): `0x5FbDB2315678afecb367f032d93F642f64180aa3`

#### Data Structures

```solidity
struct Investment {
    string company;
    string symbol;
    uint256 shares;
    uint256 purchasePrice;
    uint256 timestamp;
    address investor;
    bool active;
}
```

#### Core Functions

| Function | Parameters | Returns | Gas Cost | Description |
|----------|-----------|---------|----------|-------------|
| `addInvestment` | company, symbol, shares, price | investmentId | ~245K | Adds new investment |
| `removeInvestment` | investmentId | - | ~45K | Marks investment inactive |
| `getInvestment` | investmentId | Investment details | View | Gets single investment |
| `getMyInvestmentIds` | - | uint256[] | View | Gets all user IDs |
| `getActiveInvestmentCount` | - | uint256 | View | Counts active investments |
| `getTotalInvested` | - | uint256 | View | Calculates total invested |
| `getAllMyInvestments` | - | Multiple arrays | View | Batch retrieval |

#### Events

```solidity
event InvestmentAdded(
    address indexed investor,
    uint256 indexed investmentId,
    string company,
    string symbol,
    uint256 shares,
    uint256 price,
    uint256 timestamp
);

event InvestmentRemoved(
    address indexed investor,
    uint256 indexed investmentId,
    uint256 timestamp
);
```

#### Security Features

- **Access Control**: Each user can only access their own investments
- **Input Validation**: Checks for empty strings and zero values
- **Gas Optimization**: Efficient storage patterns and minimal loops
- **Event Logging**: All state changes emit events for tracking
- **Reentrancy Protection**: No external calls in state-changing functions

***

## 🧪 Testing

### Smart Contract Tests

**Run all tests:**

```bash
cd blockchain
npx hardhat test
```

**Test Coverage:**

- ✅ Deployment verification (1 test)
- ✅ Investment addition (4 tests)
- ✅ Investment retrieval (2 tests)
- ✅ Investment removal (4 tests)
- ✅ Portfolio statistics (3 tests)
- ✅ Batch operations (2 tests)
- ✅ Multi-user isolation (1 test)

**Total: 20+ tests covering all contract functionality**

**Sample output:**

```
  PortfolioTracker
    Deployment
      ✔ Should deploy with investment counter at 0 (45ms)
    Adding Investments
      ✔ Should add investment successfully (67ms)
      ✔ Should emit InvestmentAdded event (54ms)
      ✔ Should revert with empty company name (31ms)
      ✔ Should revert with zero shares (28ms)
    ...

  20 passing (3.5s)
```

### Python Application Testing

```bash
cd backend
pytest
```

***

## 🚀 Deployment

### Local Development (Current Setup)

Already configured! Run:

```bash
# Terminal 1
npx hardhat node

# Terminal 2
npx hardhat run scripts/deploy.js --network localhost

# Terminal 3
python app.py
```

### Testnet Deployment (Sepolia)

**Step 1: Get Testnet ETH**

Visit [Sepolia Faucet](https://sepoliafaucet.com/) and request testnet ETH.

**Step 2: Configure Environment**

Update `blockchain/.env`:

```bash
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_ALCHEMY_KEY
PRIVATE_KEY=your_wallet_private_key
```

**Step 3: Deploy**

```bash
cd blockchain
npx hardhat run scripts/deploy.js --network sepolia
```

**Step 4: Verify on Etherscan**

```bash
npx hardhat verify --network sepolia CONTRACT_ADDRESS
```

**Step 5: Update Backend**

Update `backend/.env` with new contract address and Sepolia RPC URL.

### Mainnet Deployment (Production)

**⚠️ WARNING: Requires real ETH and thorough security audit!**

1. **Security Audit**: Have smart contract professionally audited
2. **Test Thoroughly**: Run extensive tests on testnet for weeks
3. **Update Configuration**: Use mainnet RPC URLs
4. **Deploy**: Use production private key (NEVER commit to Git)
5. **Verify**: Verify contract on Etherscan for transparency
6. **Monitor**: Set up monitoring for unusual activity

***

## 🔧 Troubleshooting

### Common Issues & Solutions

#### "Cannot connect to blockchain"

**Problem**: Python app can't reach Hardhat node

**Solution**:
```bash
# Ensure Hardhat node is running
cd blockchain
npx hardhat node

# Check if port 8545 is available
lsof -i :8545
```

#### "Contract not found"

**Problem**: Wrong contract address in `.env`

**Solution**:
```bash
# Redeploy contract
npx hardhat run scripts/deploy.js --network localhost

# Copy new contract address to backend/.env
```

#### "Insufficient funds"

**Problem**: Test account out of ETH (unlikely in local development)

**Solution**:
```bash
# Restart Hardhat node to reset balances
# Stop node (Ctrl+C) and restart
npx hardhat node
```

#### "Module not found"

**Problem**: Missing Python or Node packages

**Solution**:
```bash
# Reinstall Python dependencies
pip install -r backend/requirements.txt

# Reinstall Node dependencies
cd blockchain
npm install
```

#### "Transaction failed"

**Problem**: Smart contract execution error

**Solution**:
```bash
# Check Hardhat node terminal for error details
# Common causes:
# - Invalid parameters (empty strings, zero values)
# - Gas limit too low
# - Wrong network selected
```

***

## 🗺️ Roadmap

### Phase 1: Core Features ✅ (Current)
- [x] Stock analysis with technical indicators
- [x] Portfolio management (local + blockchain)
- [x] Smart contract deployment
- [x] Gradio web interface
- [x] Multi-network support

### Phase 2: Enhanced Analytics (Q1 2026)
- [ ] Advanced charting with Plotly
- [ ] Historical backtesting engine
- [ ] More technical indicators (Fibonacci, Ichimoku Cloud)
- [ ] Sentiment analysis from news articles
- [ ] Custom alert system

### Phase 3: Blockchain Expansion (Q2 2026)
- [ ] Multi-chain support (Polygon, BSC, Arbitrum)
- [ ] NFT certificates for investments
- [ ] DAO governance for platform decisions
- [ ] Token-based rewards system
- [ ] Layer 2 scaling solutions

### Phase 4: Social & Community (Q3 2026)
- [ ] Social trading features
- [ ] Portfolio sharing and comparison
- [ ] Community stock ratings
- [ ] Expert analyst integration
- [ ] Educational resources

### Phase 5: Mobile & API (Q4 2026)
- [ ] Mobile app (React Native)
- [ ] REST API for third-party integration
- [ ] Webhook notifications
- [ ] Desktop application
- [ ] Browser extension

***

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Workflow

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Code Standards

**Python:**
- Follow PEP 8 style guide
- Use type hints where possible
- Write docstrings for all functions
- Add unit tests for new features

**Solidity:**
- Follow Solidity style guide
- Use NatSpec comments
- Write comprehensive tests
- Gas optimization is priority

**JavaScript:**
- Use ES6+ features
- Follow Airbnb style guide
- Add JSDoc comments
- Test all scripts

### Testing Requirements

All PRs must:
- Pass all existing tests
- Include tests for new features
- Maintain or improve code coverage
- Pass linting checks

***

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

***

## 🙏 Acknowledgments

- **Yahoo Finance** for providing free stock market data API
- **Hardhat** team for excellent Ethereum development tools
- **Gradio** for the intuitive UI framework
- **OpenZeppelin** for secure smart contract patterns
- **Ethereum Foundation** for blockchain innovation
- **Community Contributors** for feedback and improvements

***

## 👨‍💻 Author

**TheHashiramaSenju**

- GitHub: [@TheHashiramaSenju](https://github.com/TheHashiramaSenju)
- Project: AI Stock Analyst with Blockchain Integration
- Version: 1.0.0
- Contact: Via GitHub Issues

***

## 📞 Support

For issues, questions, or suggestions:

- 📧 **Email**: Create a GitHub Issue
- 💬 **Discord**: Coming soon
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/TheHashiramaSenju/ai-stock-analyst-blockchain/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/TheHashiramaSenju/ai-stock-analyst-blockchain/discussions)

***

## 📊 Project Statistics

- **Total Lines of Code**: ~2,500+
- **Programming Languages**: Python, Solidity, JavaScript
- **Smart Contract Functions**: 9
- **Test Coverage**: 20+ tests
- **Supported Companies**: 80+
- **Supported Markets**: NYSE, NASDAQ, NSE (India)
- **Development Time**: Ongoing
- **Contributors**: Open for contributions!

***

## 🔒 Security

### Reporting Vulnerabilities

If you discover a security vulnerability, please:

1. **DO NOT** open a public issue
2. Email details to: [Create private security advisory on GitHub]
3. Include steps to reproduce
4. Allow time for fix before disclosure

### Security Best Practices

- ✅ Never commit `.env` files
- ✅ Use separate wallets for dev/test/prod
- ✅ Enable 2FA on all accounts
- ✅ Regular security audits for smart contracts
- ✅ Keep dependencies updated
- ✅ Use hardware wallets for mainnet
- ✅ Test extensively on testnet first

---

<div align="center">

**Built with ❤️ using Python, Solidity, and Blockchain Technology**

**⭐ Star this repo if you find it useful!**

[⬆ Back to Top](#-ai-stock-analyst-with-blockchain-integration)

---

*Last Updated: October 28, 2025*

</div>