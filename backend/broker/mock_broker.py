"""
Mock Broker for testing purposes
"""
from typing import Dict, List, Any

class MockBroker:
    """A mock broker that returns dummy data."""
    def __init__(self, config: Dict[str, Any]):
        print("Initializing MockBroker")

    def get_fund_limits(self) -> Dict[str, Any]:
        """Returns mock fund limits."""
        return {"status": "success", "data": {"avail_balance": 100000, "used_margin": 5000, "total_balance": 105000}}

    def get_positions(self) -> List[Dict[str, Any]]:
        """Returns mock positions."""
        return []

    def get_holdings(self) -> List[Dict[str, Any]]:
        """Returns mock holdings."""
        return []

    def place_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulates placing an order."""
        print(f"MockBroker: Placing order -> {order_data}")
        return {"status": "success", "order_id": "mock123"} 