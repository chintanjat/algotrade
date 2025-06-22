"""
Account and portfolio data management
"""

import json
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

class AccountInfo:
    """Manages account data, including portfolio and performance"""

    def __init__(self, config):
        self.config = config
        self.data_file = Path("data/account_data.json")
        self.data = self._load_account_data()

    def _load_account_data(self) -> Dict[str, Any]:
        """Load account data from file or create default"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        # Create default data if file doesn't exist or is invalid
        default_data = self._get_default_data()
        self._save_account_data(default_data)
        return default_data

    def _get_default_data(self) -> Dict[str, Any]:
        """Get default account data structure"""
        return {
            "account_id": "mock_account_in_123",
            "account_type": "paper",
            "currency": "INR",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "account_summary": {
                "total_portfolio_value": 500000.00,
                "cash": 200000.00,
                "available_capital": 200000.00,
                "allocated_capital": 300000.00,
                "total_pnl": 25000.00,
                "daily_pnl": 3500.00,
            },
            "positions": [
                {
                    "symbol": "RELIANCE",
                    "quantity": 50,
                    "avg_price": 2800.00,
                    "market_value": 142500.00,
                    "pnl": 2500.00
                }
            ],
            "performance_history": [],
            "risk_metrics": {
                "max_drawdown": 0.0,
                "sharpe_ratio": 0.0,
                "sortino_ratio": 0.0,
            }
        }

    def _save_account_data(self, data: Dict[str, Any]):
        """Save account data to file"""
        data["last_updated"] = datetime.now().isoformat()
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)

    # --- Data Getters ---
    
    def get_account_summary(self) -> Dict[str, Any]:
        """Get full account summary"""
        return self.data.get("account_summary", {})

    def get_total_value(self) -> float:
        """Get total portfolio value."""
        return self.get_account_summary().get("total_portfolio_value", 0)

    def get_available_capital(self) -> float:
        """Get available capital."""
        return self.get_account_summary().get("available_capital", 0)

    def get_allocated_capital(self) -> float:
        """Get allocated capital."""
        return self.get_account_summary().get("allocated_capital", 0)
        
    def get_total_pnl(self) -> float:
        """Get total P&L."""
        return self.get_account_summary().get("total_pnl", 0)

    def get_daily_pnl(self) -> float:
        """Get daily P&L."""
        return self.get_account_summary().get("daily_pnl", 0)

    def get_positions(self) -> List[Dict[str, Any]]:
        """Get current positions"""
        return self.data.get("positions", [])

    def get_performance_history(self) -> List[Dict[str, Any]]:
        """Get historical performance data"""
        return self.data.get("performance_history", [])

    def get_risk_metrics(self) -> Dict[str, Any]:
        """Get risk metrics"""
        return self.data.get("risk_metrics", {})
        
    # --- Data Updaters ---

    def update_positions(self, positions: List[Dict[str, Any]]):
        """Update current positions"""
        self.data["positions"] = positions
        self._save_account_data(self.data)

    def update_account_summary(self, summary: Dict[str, Any]):
        """Update account summary data"""
        self.data["account_summary"].update(summary)
        self._save_account_data(self.data)

    def add_performance_record(self, record: Dict[str, Any]):
        """Add a new performance record"""
        self.data["performance_history"].append(record)
        self._save_account_data(self.data) 