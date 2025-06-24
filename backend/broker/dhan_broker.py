"""
Dhan Broker Integration
"""
import sys
import os
import json
import traceback

# Add the parent directory to the path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from dhanhq import dhanhq
except ImportError:
    # This print is okay as it's at module load time before logger might be set up
    print("Warning: dhanhq library not installed. Install with: pip install dhanhq")
    dhanhq = None

from typing import Dict, List, Any
from backend.utils.logger import LoggerMixin # Import LoggerMixin

class DhanBroker(LoggerMixin): # Inherit from LoggerMixin
    """Handles all communication with Dhan API."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__() # Initialize LoggerMixin (sets up self.logger)
        self.client_id = config.get("client_id")
        self.access_token = config.get("access_token")
        
        if not self.client_id or not self.access_token or "YOUR_" in self.client_id:
            self.logger.error("Dhan client_id and access_token must be set in config.json and not be placeholders.")
            raise ValueError("Dhan client_id and access_token must be set in config.json")
        
        if dhanhq is None:
            self.logger.error("dhanhq library is not installed. Cannot initialize DhanBroker.")
            raise ImportError("dhanhq library is not installed")
            
        self.api = dhanhq(self.client_id, self.access_token)
        self.logger.info("DhanBroker initialized successfully.")

    def get_fund_limits(self) -> Dict[str, Any]:
        """Fetches fund limits from Dhan."""
        try:
            response = self.api.get_fund_limits()
            self.logger.debug(f"get_fund_limits raw response: {json.dumps(response)}") # Debug for potentially large responses
            return response
        except Exception as e:
            self.logger.error(f"Error fetching Dhan fund limits: {e}", exc_info=True) # exc_info=True for traceback
            return {}

    def _parse_data_list_response(self, response: Any, context: str) -> List[Dict[str, Any]]:
        """Helper to parse responses expected to contain a list in 'data' or be a list itself."""
        if isinstance(response, dict):
            if 'data' in response:
                data_content = response['data']
                if isinstance(data_content, list):
                    self.logger.info(f"Successfully parsed {context} from response['data']. Items: {len(data_content)}")
                    return data_content
                else:
                    self.logger.warning(f"For {context}, 'data' field found but is not a list. Type: {type(data_content)}. Content: {str(data_content)[:200]}")
                    return []
            else:
                self.logger.warning(f"For {context}, response is a dict but no 'data' key found. Keys: {list(response.keys())}. Response: {str(response)[:200]}")
                return []
        elif isinstance(response, list):
            self.logger.info(f"For {context}, response itself is a list. Assuming this is the data. Items: {len(response)}")
            return response
        else:
            self.logger.warning(f"For {context}, unexpected response type: {type(response)}. Response: {str(response)[:200]}")
            return []

    def get_positions(self) -> List[Dict[str, Any]]:
        """Fetches open positions from Dhan."""
        try:
            result = self.api.get_positions()
            self.logger.debug(f"get_positions raw response: {json.dumps(result if isinstance(result, (dict, list)) else str(result))}")
            return self._parse_data_list_response(result, "positions")
        except Exception as e:
            self.logger.error(f"Error fetching Dhan positions: {e}", exc_info=True)
            return []

    def get_holdings(self) -> List[Dict[str, Any]]:
        """Fetches holdings from Dhan."""
        try:
            result = self.api.get_holdings()
            self.logger.debug(f"get_holdings raw response: {json.dumps(result if isinstance(result, (dict, list)) else str(result))}")
            return self._parse_data_list_response(result, "holdings")
        except Exception as e:
            self.logger.error(f"Error fetching Dhan holdings: {e}", exc_info=True)
            return []

    def place_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Places an order with Dhan."""
        try:
            # TODO: Map our order_data to Dhan's required format
            dhan_order = {
                "security_id": order_data["security_id"],
                "exchange_segment": self.api.NSE, # Or map from order_data
                "transaction_type": self.api.BUY if order_data["side"].upper() == "BUY" else self.api.SELL,
                "quantity": order_data["quantity"],
                "order_type": self.api.MARKET, # Or map from order_data
                "product_type": self.api.INTRA, # Or map from order_data
                "price": 0, # Market order price is 0
            }
            self.logger.info(f"Placing order with data: {json.dumps(dhan_order)}")
            response = self.api.place_order(**dhan_order)
            self.logger.info(f"place_order response: {json.dumps(response)}")
            return response
        except Exception as e:
            self.logger.error(f"Error placing Dhan order: {e}", exc_info=True)
            return {"status": "error", "reason": str(e), "dhan_broker_error": True}