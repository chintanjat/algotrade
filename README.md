# AlgoTrade - Algorithmic Trading Dashboard

A full-stack algorithmic trading platform built with Python backend and React frontend, specifically designed for the Indian market with Dhan broker integration.

## 🚀 Features

### Core Features
- **Real-time Trading Dashboard** - Monitor positions, PnL, and portfolio performance
- **Strategy Management** - Create, configure, and manage trading strategies
- **Capital Allocation** - Configure capital allocation per strategy with risk management
- **Dhan Broker Integration** - Direct integration with Dhan trading platform
- **Live Market Data** - Real-time market data and position tracking
- **Risk Management** - Built-in risk controls and position sizing

### Technical Features
- **Modern React Frontend** - Built with TypeScript, TailwindCSS, and Ant Design
- **Python Backend** - Modular architecture with HTTP bridge API
- **Real-time Updates** - WebSocket connections for live data
- **Responsive Design** - Works on desktop and mobile devices
- **Dark/Light Theme** - User-friendly interface with theme support

## 🏗️ Architecture

```
algotrade/
├── backend/                 # Python backend server
│   ├── broker/             # Broker integrations (Dhan, Mock)
│   ├── strategies/         # Strategy management
│   ├── utils/              # Utilities and logging
│   ├── webhook/            # Webhook server
│   └── http_bridge.py      # HTTP API server
├── frontend/               # React frontend application
│   └── algotrade-ui/       # React app with TypeScript
└── README.md
```

## 🛠️ Technology Stack

### Backend
- **Python 3.8+** - Core backend language
- **dhanhq** - Official Dhan API client
- **HTTP Server** - Custom HTTP bridge for API
- **JSON Storage** - File-based data persistence

### Frontend
- **React 18** - Frontend framework
- **TypeScript** - Type-safe development
- **TailwindCSS** - Utility-first CSS framework
- **Ant Design** - UI component library
- **Chart.js** - Data visualization

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **npm** or **yarn**
- **Dhan Trading Account** (for live trading)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/chintanjat/algotrade.git
cd algotrade
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Dhan Integration
Edit `backend/config.json`:
```json
{
  "broker": {
    "name": "dhan",
    "client_id": "YOUR_DHAN_CLIENT_ID",
    "access_token": "YOUR_DHAN_ACCESS_TOKEN"
  }
}
```

### 4. Frontend Setup
```bash
cd frontend/algotrade-ui
npm install
```

### 5. Start the Application

**Backend:**
```bash
cd backend
python start_server.py
```

**Frontend:**
```bash
cd frontend/algotrade-ui
npm start
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

## 📊 Dashboard Features

### Capital Summary
- Total portfolio value
- Available capital
- Allocated capital
- Real-time PnL tracking

### Strategy Management
- **ORB Scalper** - Opening Range Breakout strategy
- **Manual Trigger** - Manual signal-based trading
- **Momentum Trader** - Volume and price action strategy
- **Capital Allocation** - Per-strategy capital configuration

### Position Tracking
- Real-time position monitoring
- Unrealized PnL calculation
- Position sizing recommendations
- Risk exposure analysis

## 🔧 Configuration

### Strategy Configuration
Each strategy supports:
- **Capital Allocation** - Maximum capital per strategy (₹1,000 - ₹1,000,000)
- **Risk Parameters** - Stop loss, take profit, position sizing
- **Symbol Selection** - NSE/BSE symbols for Indian markets
- **Signal Sources** - Manual, TradingView, Webhook, Custom indicators

### Risk Management
- Maximum position size per strategy
- Portfolio risk limits
- Stop loss and take profit automation
- Capital allocation boundaries

## 🔌 API Endpoints

### Core Endpoints
- `GET /api/capital/summary` - Portfolio capital summary
- `GET /api/positions` - Current positions
- `GET /api/strategies` - Strategy list
- `POST /api/strategy/capital` - Update strategy capital allocation
- `GET /api/health` - Health check

### Strategy Management
- `GET /api/strategies` - List all strategies
- `POST /api/strategy/create` - Create new strategy
- `POST /api/strategy/update` - Update strategy
- `POST /api/strategy/toggle` - Enable/disable strategy

## 🛡️ Security

### Credential Management
- **Never commit** `config.json` with real credentials
- Use environment variables for production
- Rotate access tokens regularly
- Implement proper authentication for production

### Data Protection
- Local data storage (no cloud dependencies)
- Encrypted configuration files
- Secure API communication
- Input validation and sanitization

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd frontend/algotrade-ui
npm test
```

## 📈 Performance

### Optimizations
- Efficient data structures for real-time updates
- Minimal API calls with caching
- Optimized React rendering
- Background data synchronization

### Monitoring
- Real-time error tracking
- Performance metrics
- API response times
- Memory usage monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is for educational and research purposes. Trading involves substantial risk of loss and is not suitable for all investors. Past performance does not guarantee future results. Always consult with a financial advisor before making investment decisions.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the API endpoints

## 🔄 Roadmap

- [ ] Advanced strategy backtesting
- [ ] Multi-broker support
- [ ] Mobile application
- [ ] Advanced risk management
- [ ] Social trading features
- [ ] Machine learning integration

---

**Built with ❤️ for the Indian trading community** 