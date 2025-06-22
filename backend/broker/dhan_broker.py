"""
Dhan Broker Integration
"""
import sys
import os

# Add the parent directory to the path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from dhanhq import dhanhq
except ImportError:
    print("Warning: dhanhq library not installed. Install with: pip install dhanhq")
    dhanhq = None

from typing import Dict, List, Any

class DhanBroker:
    """Handles all communication with Dhan API."""

    def __init__(self, config: Dict[str, Any]):
        self.client_id = config.get("client_id")
        self.access_token = config.get("access_token")
        
        if not self.client_id or not self.access_token or "YOUR_" in self.client_id:
            raise ValueError("Dhan client_id and access_token must be set in config.json")
        
        if dhanhq is None:
            raise ImportError("dhanhq library is not installed")
            
        self.api = dhanhq(self.client_id, self.access_token)

    def get_fund_limits(self) -> Dict[str, Any]:
        """Fetches fund limits from Dhan."""
        try:
            return self.api.get_fund_limits()
        except Exception as e:
            print(f"Error fetching Dhan fund limits: {e}")
            return {}

    def get_positions(self) -> List[Dict[str, Any]]:
        """Fetches open positions from Dhan."""
        try:
            result = self.api.get_positions()
            if isinstance(result, dict) and 'data' in result:
                data = result.get('data', [])
                if isinstance(data, list):
                    return data
            return []
        except Exception as e:
            print(f"Error fetching Dhan positions: {e}")
            return []

    def get_holdings(self) -> List[Dict[str, Any]]:
        """Fetches holdings from Dhan."""
        try:
            result = self.api.get_holdings()
            if isinstance(result, dict) and 'data' in result:
                data = result.get('data', [])
                if isinstance(data, list):
                    return data
            return []
        except Exception as e:
            print(f"Error fetching Dhan holdings: {e}")
            return []

    def place_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Places an order with Dhan."""
        try:
            # TODO: Map our order_data to Dhan's required format
            # This is a placeholder implementation
            dhan_order = {
                "security_id": order_data["security_id"],
                "exchange_segment": self.api.NSE, # Or map from order_data
                "transaction_type": self.api.BUY if order_data["side"].upper() == "BUY" else self.api.SELL,
                "quantity": order_data["quantity"],
                "order_type": self.api.MARKET, # Or map from order_data
                "product_type": self.api.INTRA, # Or map from order_data
                "price": 0,
            }
            return self.api.place_order(**dhan_order)
        except Exception as e:
            print(f"Error placing Dhan order: {e}")
            return {"status": "error", "reason": str(e)} 