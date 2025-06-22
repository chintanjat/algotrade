#!/usr/bin/env python3
"""
Simple script to start the HTTP bridge server
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from broker.broker_manager import BrokerManager
from strategies.strategy_manager import StrategyManager
from http_bridge import start_http_bridge

def main():
    print("Starting AlgoTrade HTTP Bridge...")
    
    # Initialize components
    config = Config()
    broker_manager = BrokerManager(config)
    strategy_manager = StrategyManager(config)
    
    # Start HTTP bridge
    start_http_bridge(
        account_info=None,  # We're not using account_info anymore
        broker_manager=broker_manager,
        strategy_manager=strategy_manager,
        port=5000
    )

if __name__ == "__main__":
    main() 