"""
Manages different broker integrations.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import sys
import os

# Add the parent directory to the path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from utils.logger import LoggerMixin
from broker.dhan_broker import DhanBroker
from broker.mock_broker import MockBroker

class BrokerManager(LoggerMixin):
    """
    Factory class to get the broker instance based on config.
    Delegates calls to the instantiated broker.
    """
    def __init__(self, config: Config):
        super().__init__('BrokerManager')
        self.config = config
        self.broker_config = config.get_broker_config()
        self.broker = self._get_broker()
        self.risk_config = config.get_risk_config()
        self.positions_file = Path("data/positions.json")
        self.trades_file = Path("data/trades.json")
        
        self.positions_file.parent.mkdir(exist_ok=True)
        self.trades_file.parent.mkdir(exist_ok=True)
        
        self.trades = self._load_trades()
        
        # Mock broker connection status
        self.connected = True
        self.last_heartbeat = datetime.now()
    
    def _get_broker(self):
        broker_name = self.broker_config.get("name")
        self.logger.info(f"Attempting to initialize broker: {broker_name}")

        try:
            if broker_name == "dhan":
                client_id = self.broker_config.get("client_id", "")
                access_token = self.broker_config.get("access_token", "")
                if "YOUR_" in client_id or not client_id or "YOUR_" in access_token or not access_token:
                    self.logger.warning("Dhan credentials are not set or are placeholders.")
                    raise ValueError("Invalid or placeholder credentials for Dhan")
                
                self.logger.info("Initializing DhanBroker...")
                return DhanBroker(self.broker_config)
        except (ValueError, ImportError, Exception) as e:
            self.logger.error(f"Failed to initialize live broker '{broker_name}': {e}")
            self.logger.warning("Falling back to MockBroker.")
        
        return MockBroker(self.broker_config)

    def _load_from_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Generic function to load JSON data from a file."""
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                self.logger.error(f"Could not decode JSON from {file_path}")
                return []
        return []

    def _save_to_file(self, data: List[Dict[str, Any]], file_path: Path):
        """Generic function to save JSON data to a file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def _load_trades(self) -> List[Dict[str, Any]]:
        return self._load_from_file(self.trades_file)
    
    def get_capital_summary(self) -> Dict[str, Any]:
        """Fetches capital summary from the broker."""
        try:
            if isinstance(self.broker, DhanBroker):
                fund_limits = self.broker.get_fund_limits()
                if fund_limits and fund_limits.get('status', 'error').lower() == 'success':
                    data = fund_limits.get('data', {})
                    return {
                        "total_capital": data.get('avail_balance', 0),
                        "pnl": 0, # Dhan API doesn't provide a direct PnL field in funds summary
                        "net_credit": data.get('opening_balance', 0),
                        "used_margin": data.get('used_margin', 0)
                    }
                else:
                    reason = fund_limits.get('remarks', 'Unknown error')
                    self.logger.error(f"Failed to get fund limits from Dhan: {reason}")
                    return {"total_capital": 0, "pnl": 0, "net_credit": 0, "used_margin": 0}
            
            # Fallback to MockBroker's implementation
            mock_data = self.broker.get_fund_limits().get('data', {})
            return {
                "total_capital": mock_data.get('total_balance', 100000),
                "pnl": 500.50, # Mock PnL
                "net_credit": mock_data.get('avail_balance', 100000),
                "used_margin": mock_data.get('used_margin', 5000)
            }
        except Exception as e:
            self.logger.error(f"Error in get_capital_summary: {e}")
            return {"total_capital": 0, "pnl": 0, "net_credit": 0, "used_margin": 0}

    def get_open_positions(self) -> List[Dict[str, Any]]:
        """Get all open positions from the broker."""
        try:
            return self.broker.get_positions()
        except Exception as e:
            self.logger.error(f"Could not fetch positions from broker: {e}. Falling back to local file.")
            return self._load_from_file(self.positions_file)

    def get_holdings(self) -> List[Dict[str, Any]]:
        """Get all holdings from the broker."""
        try:
            return self.broker.get_holdings()
        except Exception as e:
            self.logger.error(f"Could not fetch holdings from broker: {e}")
            return [] # Mock holdings if needed

    def place_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Place a new order via the broker."""
        try:
            result = self.broker.place_order(order_data)
            # You might want to log the trade if it's successful
            if result.get('status', 'error').lower() == 'success':
                self.trades.append({**order_data, **result, "timestamp": datetime.now().isoformat()})
                self._save_to_file(self.trades, self.trades_file)
            return result
        except Exception as e:
            self.logger.error(f"Error placing order via broker: {e}")
            return {"status": "error", "reason": str(e)}

    def get_recent_trades(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent trades from local log."""
        return self.trades[-limit:] if limit else self.trades
    
    def is_connected(self) -> bool:
        """Check if broker is connected"""
        return self.connected and (datetime.now() - self.last_heartbeat).seconds < 60
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information from broker"""
        return {
            "account_id": "DEMO_ACCOUNT",
            "status": "ACTIVE",
            "currency": "USD",
            "buying_power": 50000.00,
            "cash": 50000.00,
            "portfolio_value": 100000.00,
            "pattern_day_trader": False,
            "trading_blocked": False,
            "transfers_blocked": False,
            "account_blocked": False,
            "created_at": "2024-01-01T00:00:00Z",
            "trade_suspended_by_user": False,
            "multiplier": "1"
        }
    
    def get_position(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get specific position by symbol"""
        for position in self.get_open_positions():
            if position["symbol"] == symbol:
                return position
        return None
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        # Mock implementation - in real broker, this would cancel the order
        return True
    
    def get_order_status(self, order_id: str) -> Dict[str, Any]:
        """Get order status"""
        for trade in self.trades:
            if trade["id"] == order_id:
                return {
                    "id": trade["id"],
                    "status": trade["status"],
                    "filled_at": trade["filled_at"],
                    "filled_price": trade["filled_price"]
                }
        return {"error": "Order not found"}
    
    def get_market_data(self, symbol: str) -> Dict[str, Any]:
        """Get current market data for symbol"""
        # Mock market data
        return {
            "symbol": symbol,
            "price": 100.00,
            "bid": 99.95,
            "ask": 100.05,
            "volume": 1000000,
            "timestamp": datetime.now().isoformat()
        }
    
    def calculate_position_size(self, symbol: str, risk_amount: float) -> int:
        """Calculate position size based on risk management rules"""
        max_position_size = self.config.get_max_position_size()
        account_value = 100000.00  # Mock account value
        
        # Calculate maximum position value
        max_position_value = account_value * max_position_size
        
        # Get current price
        market_data = self.get_market_data(symbol)
        current_price = market_data["price"]
        
        # Calculate quantity
        quantity = int(max_position_value / current_price)
        
        return max(1, quantity)  # Minimum 1 share
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get portfolio summary"""
        total_value = 100000.00  # Mock total value
        positions_value = sum(pos["market_value"] for pos in self.get_open_positions())
        cash = total_value - positions_value
        
        return {
            "total_value": total_value,
            "cash": cash,
            "positions_value": positions_value,
            "unrealized_pl": sum(pos["unrealized_pl"] for pos in self.get_open_positions()),
            "position_count": len(self.get_open_positions())
        } 