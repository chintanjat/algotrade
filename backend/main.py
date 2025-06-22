#!/usr/bin/env python3
"""
AlgoTrade - Main Entry Point
A modular pure Python algorithmic trading platform
"""

import argparse
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent))

from config import Config
from account_info import AccountInfo
from broker.broker_manager import BrokerManager
from strategies.strategy_manager import StrategyManager
from utils.logger import setup_logger
from webhook.webhook_server import WebhookServer
from http_bridge import start_http_bridge

def main():
    """Main CLI entry point for AlgoTrade"""
    parser = argparse.ArgumentParser(description='AlgoTrade - Algorithmic Trading Platform')
    parser.add_argument('--config', '-c', default='config.json', help='Configuration file path')
    parser.add_argument('--mode', '-m', choices=['cli', 'http', 'webhook'], default='cli', 
                       help='Operation mode')
    parser.add_argument('--port', '-p', type=int, default=5000, help='HTTP server port')
    parser.add_argument('--debug', '-d', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logger(debug=args.debug)
    logger.info("Starting AlgoTrade...")
    
    try:
        # Load configuration
        config = Config(args.config)
        
        # Initialize components
        account = AccountInfo(config)
        broker_manager = BrokerManager(config)
        strategy_manager = StrategyManager(config)
        
        if args.mode == 'http':
            # Start HTTP bridge for frontend communication
            logger.info(f"Starting HTTP bridge on port {args.port}")
            start_http_bridge(account, broker_manager, strategy_manager, port=args.port)
        elif args.mode == 'webhook':
            # Start webhook server for external signals
            webhook_server = WebhookServer(config, strategy_manager)
            webhook_server.start()
        else:
            # CLI mode
            run_cli_mode(account, broker_manager, strategy_manager)
            
    except Exception as e:
        logger.error(f"Failed to start AlgoTrade: {e}")
        sys.exit(1)

def run_cli_mode(account, broker_manager, strategy_manager):
    """Run AlgoTrade in CLI mode"""
    print("=== AlgoTrade CLI ===")
    print("Available commands:")
    print("1. status - Show account status")
    print("2. positions - Show open positions")
    print("3. strategies - List strategies")
    print("4. trades - Show recent trades")
    print("5. quit - Exit")
    
    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            
            if command == 'status':
                print(f"Account Balance: ${account.get_balance():,.2f}")
                print(f"Available Capital: ${account.get_available_capital():,.2f}")
                print(f"Allocated Capital: ${account.get_allocated_capital():,.2f}")
                
            elif command == 'positions':
                positions = broker_manager.get_open_positions()
                if positions:
                    for pos in positions:
                        print(f"{pos['symbol']}: {pos['quantity']} @ ${pos['avg_price']:.2f}")
                else:
                    print("No open positions")
                    
            elif command == 'strategies':
                strategies = strategy_manager.get_strategies()
                for strategy in strategies:
                    status = "ACTIVE" if strategy['enabled'] else "INACTIVE"
                    print(f"{strategy['name']}: {status}")
                    
            elif command == 'trades':
                trades = broker_manager.get_recent_trades(limit=10)
                for trade in trades:
                    print(f"{trade['timestamp']}: {trade['symbol']} {trade['side']} {trade['quantity']} @ ${trade['price']:.2f}")
                    
            elif command == 'quit':
                print("Goodbye!")
                break
                
            else:
                print("Unknown command. Type 'quit' to exit.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main() 