"""
Configuration management for AlgoTrade
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """Configuration manager for AlgoTrade"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Invalid JSON in {self.config_path}, using defaults")
                return self._get_default_config()
        else:
            # Create default config
            default_config = self._get_default_config()
            self._save_config(default_config)
            return default_config
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "broker": {
                "name": "dhan",
                "client_id": "YOUR_CLIENT_ID",
                "access_token": "YOUR_ACCESS_TOKEN",
            },
            "market_data": {
                "currency": "INR",
                "exchange": "NSE"
            },
            "risk_management": {
                "max_position_size": 0.02,  # 2% of portfolio per position
                "max_portfolio_risk": 0.06,  # 6% total portfolio risk
                "stop_loss_pct": 0.05,  # 5% stop loss
                "take_profit_pct": 0.10  # 10% take profit
            },
            "strategies": {
                "default_signal_source": "manual",
                "auto_execute": False,
                "confirmation_required": True
            },
            "logging": {
                "level": "INFO",
                "file": "logs/algotrade.log",
                "max_size": "10MB",
                "backup_count": 5
            },
            "webhook": {
                "enabled": True,
                "port": 8080,
                "secret": ""
            },
            "http_bridge": {
                "enabled": True,
                "port": 5000,
                "cors_origins": ["http://localhost:3000"]
            }
        }
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports nested keys with dots)"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value by key (supports nested keys with dots)"""
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        self._save_config(self.config)
    
    def get_broker_config(self) -> Dict[str, Any]:
        """Get broker configuration"""
        return self.get("broker", {})
    
    def get_risk_config(self) -> Dict[str, Any]:
        """Get risk management configuration"""
        return self.get("risk_management", {})
    
    def get_strategy_config(self) -> Dict[str, Any]:
        """Get strategy configuration"""
        return self.get("strategies", {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration"""
        return self.get("logging", {})
    
    def get_webhook_config(self) -> Dict[str, Any]:
        """Get webhook configuration"""
        return self.get("webhook", {})
    
    def get_http_bridge_config(self) -> Dict[str, Any]:
        """Get HTTP bridge configuration"""
        return self.get("http_bridge", {})
    
    def update_broker_credentials(self, api_key: str, api_secret: str):
        """Update broker API credentials"""
        self.set("broker.api_key", api_key)
        self.set("broker.api_secret", api_secret)
    
    def is_paper_trading(self) -> bool:
        """Check if paper trading is enabled"""
        return self.get("broker.paper_trading", True)
    
    def get_max_position_size(self) -> float:
        """Get maximum position size as percentage"""
        return self.get("risk_management.max_position_size", 0.02)
    
    def get_stop_loss_pct(self) -> float:
        """Get stop loss percentage"""
        return self.get("risk_management.stop_loss_pct", 0.05)
    
    def get_take_profit_pct(self) -> float:
        """Get take profit percentage"""
        return self.get("risk_management.take_profit_pct", 0.10) 