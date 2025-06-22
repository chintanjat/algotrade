"""
Strategy management and signal processing
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path

class StrategyManager:
    """Manages trading strategies and signal processing"""
    
    def __init__(self, config):
        self.config = config
        self.strategies_file = Path("data/strategies.json")
        self.signals_file = Path("data/signals.json")
        
        # Ensure data directory exists
        self.strategies_file.parent.mkdir(exist_ok=True)
        
        # Load existing data
        self.strategies = self._load_strategies()
        self.signals = self._load_signals()
        
        # Initialize default strategies
        self._initialize_default_strategies()
    
    def _load_strategies(self) -> List[Dict[str, Any]]:
        """Load strategies from file"""
        if self.strategies_file.exists():
            try:
                with open(self.strategies_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    def _save_strategies(self):
        """Save strategies to file"""
        with open(self.strategies_file, 'w') as f:
            json.dump(self.strategies, f, indent=2)
    
    def _load_signals(self) -> List[Dict[str, Any]]:
        """Load signals from file"""
        if self.signals_file.exists():
            try:
                with open(self.signals_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    def _save_signals(self):
        """Save signals to file"""
        with open(self.signals_file, 'w') as f:
            json.dump(self.signals, f, indent=2)
    
    def _initialize_default_strategies(self):
        """Initialize default strategies if none exist"""
        if not self.strategies:
            default_strategies = self._get_default_strategies()
            self.strategies = default_strategies
            self._save_strategies()
    
    def _get_default_strategies(self) -> List[Dict[str, Any]]:
        """Get default strategies"""
        return [
            {
                "id": "strat_ma_crossover_1",
                "name": "MA Crossover (NIFTY 50)",
                "description": "A simple moving average crossover strategy for large-cap stocks.",
                "symbols": ["RELIANCE", "HDFCBANK", "INFY", "TCS"],
                "signal_source": "manual",
                "enabled": True,
                "capital_allocation": 50000,
                "parameters": {
                    "fast_period": 10,
                    "slow_period": 30
                }
            },
            {
                "id": "strat_rsi_reversion_1",
                "name": "RSI Mean Reversion (Bank NIFTY)",
                "description": "A mean reversion strategy based on the RSI indicator for banking stocks.",
                "symbols": ["HDFCBANK", "ICICIBANK", "SBIN", "KOTAKBANK"],
                "signal_source": "manual",
                "enabled": False,
                "capital_allocation": 30000,
                "parameters": {
                    "rsi_period": 14,
                    "oversold_threshold": 30,
                    "overbought_threshold": 70
                }
            }
        ]
    
    def get_strategies(self) -> List[Dict[str, Any]]:
        """Get all strategies"""
        return self.strategies
    
    def get_strategy(self, strategy_id: str) -> Optional[Dict[str, Any]]:
        """Get specific strategy by ID"""
        for strategy in self.strategies:
            if strategy["id"] == strategy_id:
                return strategy
        return None
    
    def create_strategy(self, strategy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new strategy"""
        strategy_id = f"strategy_{len(self.strategies) + 1}"
        
        # Validate capital allocation
        capital_allocation = strategy_data.get("capital_allocation", 25000)
        if not isinstance(capital_allocation, (int, float)) or capital_allocation <= 0:
            capital_allocation = 25000  # Default value
        
        strategy = {
            "id": strategy_id,
            "name": strategy_data["name"],
            "description": strategy_data.get("description", ""),
            "enabled": strategy_data.get("enabled", False),
            "signal_source": strategy_data.get("signal_source", "manual"),
            "capital_allocation": capital_allocation,
            "symbols": strategy_data.get("symbols", []),
            "parameters": strategy_data.get("parameters", {}),
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
        self.strategies.append(strategy)
        self._save_strategies()
        
        return strategy
    
    def update_strategy(self, strategy_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing strategy"""
        strategy = self.get_strategy(strategy_id)
        if not strategy:
            return None
        
        # Update fields
        for key, value in updates.items():
            if key in strategy:
                strategy[key] = value
        
        strategy["last_updated"] = datetime.now().isoformat()
        self._save_strategies()
        
        return strategy
    
    def delete_strategy(self, strategy_id: str) -> bool:
        """Delete a strategy"""
        original_count = len(self.strategies)
        self.strategies = [s for s in self.strategies if s["id"] != strategy_id]
        
        if len(self.strategies) < original_count:
            self._save_strategies()
            return True
        return False
    
    def toggle_strategy(self, strategy_id: str) -> bool:
        """Toggle strategy enabled/disabled status"""
        strategy = self.get_strategy(strategy_id)
        if not strategy:
            return False
        
        strategy["enabled"] = not strategy["enabled"]
        strategy["last_updated"] = datetime.now().isoformat()
        self._save_strategies()
        
        return strategy["enabled"]
    
    def get_active_strategies(self) -> List[Dict[str, Any]]:
        """Get all enabled strategies"""
        return [s for s in self.strategies if s["enabled"]]
    
    def add_signal(self, signal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new trading signal"""
        signal = {
            "id": f"signal_{len(self.signals) + 1}",
            "strategy_id": signal_data["strategy_id"],
            "symbol": signal_data["symbol"],
            "side": signal_data["side"],
            "strength": signal_data.get("strength", 1.0),
            "price": signal_data.get("price", 0.0),
            "timestamp": datetime.now().isoformat(),
            "source": signal_data.get("source", "manual"),
            "status": "pending",
            "executed": False
        }
        
        self.signals.append(signal)
        self._save_signals()
        
        return signal
    
    def get_signals(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent signals"""
        return self.signals[-limit:] if limit else self.signals
    
    def get_pending_signals(self) -> List[Dict[str, Any]]:
        """Get pending signals that haven't been executed"""
        return [s for s in self.signals if s["status"] == "pending" and not s["executed"]]
    
    def mark_signal_executed(self, signal_id: str, order_id: Optional[str] = None):
        """Mark a signal as executed"""
        for signal in self.signals:
            if signal["id"] == signal_id:
                signal["executed"] = True
                signal["status"] = "executed"
                if order_id:
                    signal["order_id"] = order_id
                signal["executed_at"] = datetime.now().isoformat()
                break
        
        self._save_signals()
    
    def get_strategy_performance(self, strategy_id: str) -> Dict[str, Any]:
        """Get performance metrics for a strategy"""
        strategy_signals = [s for s in self.signals if s["strategy_id"] == strategy_id]
        executed_signals = [s for s in strategy_signals if s["executed"]]
        
        total_signals = len(strategy_signals)
        executed_count = len(executed_signals)
        
        return {
            "strategy_id": strategy_id,
            "total_signals": total_signals,
            "executed_signals": executed_count,
            "execution_rate": executed_count / total_signals if total_signals > 0 else 0,
            "last_signal": strategy_signals[-1]["timestamp"] if strategy_signals else None
        }
    
    def process_webhook_signal(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming webhook signal"""
        # Validate webhook data
        required_fields = ["strategy_id", "symbol", "side"]
        for field in required_fields:
            if field not in webhook_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Add signal
        signal = self.add_signal({
            "strategy_id": webhook_data["strategy_id"],
            "symbol": webhook_data["symbol"],
            "side": webhook_data["side"],
            "strength": webhook_data.get("strength", 1.0),
            "price": webhook_data.get("price", 0.0),
            "source": "webhook"
        })
        
        return signal
    
    def get_signal_sources(self) -> List[str]:
        """Get available signal sources"""
        return ["manual", "webhook", "tradingview", "custom_indicator"]
    
    def validate_strategy_config(self, strategy_data: Dict[str, Any]) -> bool:
        """Validate strategy configuration"""
        required_fields = ["name"]
        for field in required_fields:
            if field not in strategy_data:
                return False
        
        # Validate capital allocation
        capital_allocation = strategy_data.get("capital_allocation", 25000)
        if not isinstance(capital_allocation, (int, float)) or capital_allocation <= 0:
            return False
        
        return True
    
    def get_total_allocated_capital(self) -> float:
        """Get total capital allocated across all enabled strategies"""
        total = 0.0
        for strategy in self.strategies:
            if strategy.get("enabled", False):
                total += strategy.get("capital_allocation", 0)
        return total
    
    def get_strategy_capital_allocation(self, strategy_id: str) -> float:
        """Get capital allocation for a specific strategy"""
        strategy = self.get_strategy(strategy_id)
        if strategy:
            return strategy.get("capital_allocation", 0)
        return 0.0
    
    def update_strategy_capital(self, strategy_id: str, new_capital: float) -> bool:
        """Update capital allocation for a specific strategy"""
        if new_capital <= 0:
            return False
        
        strategy = self.get_strategy(strategy_id)
        if not strategy:
            return False
        
        strategy["capital_allocation"] = new_capital
        strategy["last_updated"] = datetime.now().isoformat()
        self._save_strategies()
        return True 