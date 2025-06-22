# AlgoTrade Backend

A modular pure Python algorithmic trading platform with CLI interface and optional HTTP bridge for frontend communication.

## 🏗️ Architecture

The backend is built with a modular design:

- **Core Modules**: Configuration, account management, broker integration
- **Strategy Engine**: Strategy management and signal processing
- **Webhook Server**: External signal integration
- **HTTP Bridge**: Frontend communication layer
- **Logging**: Centralized logging with rotation

## 📁 Project Structure

```
backend/
├── main.py                 # Main CLI entry point
├── config.py              # Configuration management
├── account_info.py        # Account and portfolio data
├── http_bridge.py         # HTTP server for frontend
├── broker/
│   └── broker_manager.py  # Trading operations
├── strategies/
│   └── strategy_manager.py # Strategy management
├── utils/
│   └── logger.py          # Logging utilities
├── webhook/
│   └── webhook_server.py  # External webhook server
├── logs/                  # Log files
└── data/                  # JSON data storage
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- No external dependencies (pure Python)

### Installation

1. Navigate to the backend directory:
```bash
cd backend
```

2. Run the main application:
```bash
python main.py
```

### Usage Modes

#### CLI Mode (Default)
```bash
python main.py --mode cli
```

#### HTTP Bridge Mode (for frontend)
```bash
python main.py --mode http --port 5000
```

#### Webhook Server Mode
```bash
python main.py --mode webhook --port 8080
```

#### Debug Mode
```bash
python main.py --debug
```

## ⚙️ Configuration

The system uses a JSON configuration file (`config.json`) that is automatically created on first run:

```json
{
  "broker": {
    "name": "alpaca",
    "api_key": "",
    "api_secret": "",
    "base_url": "https://paper-api.alpaca.markets",
    "paper_trading": true
  },
  "risk_management": {
    "max_position_size": 0.02,
    "max_portfolio_risk": 0.06,
    "stop_loss_pct": 0.05,
    "take_profit_pct": 0.10
  },
  "strategies": {
    "default_signal_source": "manual",
    "auto_execute": false,
    "confirmation_required": true
  },
  "logging": {
    "level": "INFO",
    "file": "logs/algotrade.log",
    "max_size": "10MB",
    "backup_count": 5
  },
  "webhook": {
    "enabled": true,
    "port": 8080,
    "secret": ""
  },
  "http_bridge": {
    "enabled": true,
    "port": 5000,
    "cors_origins": ["http://localhost:3000"]
  }
}
```

## 🔌 HTTP Bridge API

When running in HTTP mode, the following endpoints are available:

### Account & Portfolio

- `GET /api/account` - Get account summary
- `GET /api/positions` - Get open positions
- `GET /api/trades?limit=100` - Get recent trades
- `GET /api/performance` - Get performance metrics

### Strategies

- `GET /api/strategies` - Get all strategies
- `POST /api/strategy/toggle` - Toggle strategy enabled/disabled
- `POST /api/strategy/create` - Create new strategy
- `POST /api/strategy/update` - Update existing strategy

### Trading

- `POST /api/order` - Place new order
- `GET /api/signals?limit=100` - Get trading signals
- `POST /api/signal` - Create new signal

### System

- `GET /api/health` - Health check

### Example API Usage

```bash
# Get account information
curl http://localhost:5000/api/account

# Get open positions
curl http://localhost:5000/api/positions

# Toggle strategy
curl -X POST http://localhost:5000/api/strategy/toggle \
  -H "Content-Type: application/json" \
  -d '{"strategy_id": "strategy_1"}'

# Place order
curl -X POST http://localhost:5000/api/order \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "side": "buy",
    "quantity": 10,
    "type": "market"
  }'
```

## 🎯 Strategy Management

### Default Strategies

The system comes with three pre-configured strategies:

1. **Moving Average Crossover**
   - Symbols: AAPL, GOOGL, MSFT
   - Parameters: Fast period (10), Slow period (20)

2. **RSI Strategy**
   - Symbols: TSLA, NVDA, AMD
   - Parameters: RSI period (14), Oversold (30), Overbought (70)

3. **Breakout Strategy**
   - Symbols: SPY, QQQ, IWM
   - Parameters: Breakout period (20), Volume multiplier (1.5)

### Creating Custom Strategies

```python
strategy_data = {
    "name": "My Custom Strategy",
    "description": "Custom trading strategy",
    "enabled": False,
    "signal_source": "manual",
    "symbols": ["AAPL", "GOOGL"],
    "parameters": {
        "custom_param": 42,
        "risk_per_trade": 0.02
    }
}
```

## 🔗 Webhook Integration

The webhook server accepts external trading signals:

### Webhook Endpoints

- `POST /webhook/signal` - Submit trading signal
- `GET /webhook/health` - Health check

### Signal Format

```json
{
  "strategy_id": "strategy_1",
  "symbol": "AAPL",
  "side": "buy",
  "strength": 1.0,
  "price": 150.00
}
```

### Webhook Security

If a secret is configured, webhooks must include an `X-Signature` header:

```bash
curl -X POST http://localhost:8080/webhook/signal \
  -H "Content-Type: application/json" \
  -H "X-Signature: <calculated_signature>" \
  -d '{"strategy_id": "strategy_1", "symbol": "AAPL", "side": "buy"}'
```

## 📊 Data Storage

All data is stored in JSON files in the `data/` directory:

- `account_data.json` - Account and portfolio information
- `positions.json` - Current positions
- `trades.json` - Trade history
- `strategies.json` - Strategy configurations
- `signals.json` - Trading signals

## 🛠️ Development

### Adding New Brokers

1. Create a new broker class in `broker/`
2. Implement required methods:
   - `get_account_info()`
   - `get_open_positions()`
   - `place_order()`
   - `get_recent_trades()`

### Adding New Strategies

1. Create strategy configuration
2. Implement signal processing logic
3. Add to strategy manager

### Logging

The system uses a centralized logging system:

```python
from utils.logger import setup_logger

logger = setup_logger("my_module", debug=True)
logger.info("Application started")
logger.error("An error occurred")
```

## 🔧 CLI Commands

When running in CLI mode, the following commands are available:

- `status` - Show account status
- `positions` - Show open positions
- `strategies` - List strategies
- `trades` - Show recent trades
- `quit` - Exit

## 🚨 Error Handling

The system includes comprehensive error handling:

- Invalid configuration files
- Network connectivity issues
- Invalid order data
- Strategy validation errors

All errors are logged with appropriate context and stack traces in debug mode.

## 📝 License

This project is part of the AlgoTrade platform. 