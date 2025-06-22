"""
HTTP Bridge for AlgoTrade Frontend Communication
"""

import json
import threading
from datetime import datetime
from typing import Dict, Any, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
from urllib.parse import urlparse, parse_qs
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.logger import LoggerMixin, get_logger

class BridgeHandler(BaseHTTPRequestHandler, LoggerMixin):
    """HTTP request handler for frontend bridge"""
    
    def __init__(self, *args, account_info=None, broker_manager=None, strategy_manager=None, **kwargs):
        self.account_info = account_info
        self.broker_manager = broker_manager
        self.strategy_manager = strategy_manager
        self.logger = get_logger("http_bridge")  # Ensure logger is initialized
        super().__init__(*args, **kwargs)
    
    def log_message(self, format, *args):
        """Override to use our logger"""
        self.logger.info(f"{self.address_string()} - {format % args}")
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            query_params = parse_qs(parsed_url.query)
            
            if path == "/api/account":
                self._handle_get_account()
            elif path == "/api/positions":
                self._handle_get_positions()
            elif path == "/api/trades":
                limit = int(query_params.get("limit", [100])[0])
                self._handle_get_trades(limit)
            elif path == "/api/strategies":
                self._handle_get_strategies()
            elif path == "/api/signals":
                limit = int(query_params.get("limit", [100])[0])
                self._handle_get_signals(limit)
            elif path == "/api/performance":
                self._handle_get_performance()
            elif path == "/api/capital/summary":
                self._handle_get_capital_summary()
            elif path == "/api/health":
                self._handle_health_check()
            elif path == "/health":
                self._handle_simple_health_check()
            else:
                self._send_error_response(404, "Endpoint not found")
                
        except Exception as e:
            self.logger.error(f"Error handling GET request: {e}")
            self._send_error_response(500, "Internal server error")
    
    def do_POST(self):
        """Handle POST requests"""
        try:
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            
            if path == "/api/order":
                self._handle_place_order()
            elif path == "/api/strategy/toggle":
                self._handle_toggle_strategy()
            elif path == "/api/strategy/create":
                self._handle_create_strategy()
            elif path == "/api/strategy/update":
                self._handle_update_strategy()
            elif path == "/api/strategy/capital":
                self._handle_update_strategy_capital()
            elif path == "/api/signal":
                self._handle_create_signal()
            else:
                self._send_error_response(404, "Endpoint not found")
                
        except Exception as e:
            self.logger.error(f"Error handling POST request: {e}")
            self._send_error_response(500, "Internal server error")
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
    
    def _handle_get_account(self):
        """Handle account information request"""
        if not self.broker_manager:
            self._send_error_response(500, "Broker manager not available")
            return
        
        try:
            account_data = {
                "account_id": "DHAN_ACCOUNT",
                "status": "ACTIVE",
                "currency": "INR",
                "capital_summary": self.broker_manager.get_capital_summary()
            }
            self._send_json_response(200, account_data)
        except Exception as e:
            self.logger.error(f"Error fetching account info: {e}", exc_info=True)
            self._send_error_response(500, "Failed to retrieve account information")
    
    def _handle_get_positions(self):
        """Handle positions request"""
        if not self.broker_manager:
            self._send_error_response(500, "Broker manager not available")
            return
        
        positions = self.broker_manager.get_open_positions()
        self._send_json_response(200, {"positions": positions})
    
    def _handle_get_trades(self, limit: int):
        """Handle trades request"""
        if not self.broker_manager:
            self._send_error_response(500, "Broker manager not available")
            return
        
        trades = self.broker_manager.get_recent_trades(limit)
        self._send_json_response(200, {"trades": trades})
    
    def _handle_get_strategies(self):
        """Handle strategies request"""
        if not self.strategy_manager:
            self._send_error_response(500, "Strategy manager not available")
            return
        
        strategies = self.strategy_manager.get_strategies()
        self._send_json_response(200, {"strategies": strategies})
    
    def _handle_get_signals(self, limit: int):
        """Handle signals request"""
        if not self.strategy_manager:
            self._send_error_response(500, "Strategy manager not available")
            return
        
        signals = self.strategy_manager.get_signals(limit)
        self._send_json_response(200, {"signals": signals})
    
    def _handle_get_performance(self):
        """Handle performance request"""
        if not self.account_info:
            self._send_error_response(500, "Account info not available")
            return
        
        performance = self.account_info.get_performance()
        risk_metrics = self.account_info.get_risk_metrics()
        
        response = {
            "performance": performance,
            "risk_metrics": risk_metrics,
            "timestamp": datetime.now().isoformat()
        }
        
        self._send_json_response(200, response)
    
    def _handle_get_capital_summary(self):
        """Handle capital summary request"""
        if not self.broker_manager:
            self._send_error_response(500, "Broker manager not available")
            return
        
        try:
            summary = self.broker_manager.get_capital_summary()
            self._send_json_response(200, summary)
        except Exception as e:
            self.logger.error(f"Error fetching capital summary: {e}", exc_info=True)
            self._send_error_response(500, "Failed to retrieve capital summary")
    
    def _handle_place_order(self):
        """Handle order placement request"""
        if not self.broker_manager:
            self._send_error_response(500, "Broker manager not available")
            return
        
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._send_error_response(400, "No content")
                return
            
            post_data = self.rfile.read(content_length)
            order_data = json.loads(post_data.decode('utf-8'))
            
            # Place order
            order = self.broker_manager.place_order(order_data)
            
            response = {
                "status": "success",
                "message": "Order placed successfully",
                "order": order
            }
            
            self._send_json_response(200, response)
            
        except json.JSONDecodeError:
            self._send_error_response(400, "Invalid JSON")
        except ValueError as e:
            self._send_error_response(400, str(e))
        except Exception as e:
            self._send_error_response(500, f"Order placement failed: {e}")
    
    def _handle_toggle_strategy(self):
        """Handle strategy toggle request"""
        if not self.strategy_manager:
            self._send_error_response(500, "Strategy manager not available")
            return
        
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._send_error_response(400, "No content")
                return
            
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            strategy_id = data.get("strategy_id")
            if not strategy_id:
                self._send_error_response(400, "Missing strategy_id")
                return
            
            enabled = self.strategy_manager.toggle_strategy(strategy_id)
            
            response = {
                "status": "success",
                "message": f"Strategy {'enabled' if enabled else 'disabled'}",
                "enabled": enabled
            }
            
            self._send_json_response(200, response)
            
        except json.JSONDecodeError:
            self._send_error_response(400, "Invalid JSON")
        except Exception as e:
            self._send_error_response(500, f"Strategy toggle failed: {e}")
    
    def _handle_create_strategy(self):
        """Handle strategy creation request"""
        if not self.strategy_manager:
            self._send_error_response(500, "Strategy manager not available")
            return
        
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._send_error_response(400, "No content")
                return
            
            post_data = self.rfile.read(content_length)
            strategy_data = json.loads(post_data.decode('utf-8'))
            
            # Validate strategy data
            if not self.strategy_manager.validate_strategy_config(strategy_data):
                self._send_error_response(400, "Invalid strategy configuration")
                return
            
            # Create strategy
            strategy = self.strategy_manager.create_strategy(strategy_data)
            
            response = {
                "status": "success",
                "message": "Strategy created successfully",
                "strategy": strategy
            }
            
            self._send_json_response(200, response)
            
        except json.JSONDecodeError:
            self._send_error_response(400, "Invalid JSON")
        except Exception as e:
            self._send_error_response(500, f"Strategy creation failed: {e}")
    
    def _handle_update_strategy(self):
        """Handle strategy update request"""
        if not self.strategy_manager:
            self._send_error_response(500, "Strategy manager not available")
            return
        
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._send_error_response(400, "No content")
                return
            
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            strategy_id = data.get("strategy_id")
            updates = data.get("updates", {})
            
            if not strategy_id:
                self._send_error_response(400, "Missing strategy_id")
                return
            
            # Update strategy
            strategy = self.strategy_manager.update_strategy(strategy_id, updates)
            
            if not strategy:
                self._send_error_response(404, "Strategy not found")
                return
            
            response = {
                "status": "success",
                "message": "Strategy updated successfully",
                "strategy": strategy
            }
            
            self._send_json_response(200, response)
            
        except json.JSONDecodeError:
            self._send_error_response(400, "Invalid JSON")
        except Exception as e:
            self._send_error_response(500, f"Strategy update failed: {e}")
    
    def _handle_update_strategy_capital(self):
        """Handle strategy capital update request"""
        if not self.strategy_manager:
            self._send_error_response(500, "Strategy manager not available")
            return
        
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._send_error_response(400, "No content")
                return
            
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            strategy_id = data.get("strategy_id")
            capital_allocation = data.get("capital_allocation")
            
            if not strategy_id:
                self._send_error_response(400, "Missing strategy_id")
                return
            
            if not capital_allocation:
                self._send_error_response(400, "Missing capital_allocation")
                return
            
            # Update strategy capital allocation
            success = self.strategy_manager.update_strategy_capital(strategy_id, capital_allocation)
            
            if not success:
                self._send_error_response(404, "Strategy not found or invalid capital amount")
                return
            
            # Get the updated strategy
            updated_strategy = self.strategy_manager.get_strategy(strategy_id)
            
            response = {
                "status": "success",
                "message": "Strategy capital allocation updated successfully",
                "strategy": updated_strategy
            }
            
            self._send_json_response(200, response)
            
        except json.JSONDecodeError:
            self._send_error_response(400, "Invalid JSON")
        except Exception as e:
            self._send_error_response(500, f"Strategy capital allocation update failed: {e}")
    
    def _handle_create_signal(self):
        """Handle signal creation request"""
        if not self.strategy_manager:
            self._send_error_response(500, "Strategy manager not available")
            return
        
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._send_error_response(400, "No content")
                return
            
            post_data = self.rfile.read(content_length)
            signal_data = json.loads(post_data.decode('utf-8'))
            
            # Create signal
            signal = self.strategy_manager.add_signal(signal_data)
            
            response = {
                "status": "success",
                "message": "Signal created successfully",
                "signal": signal
            }
            
            self._send_json_response(200, response)
            
        except json.JSONDecodeError:
            self._send_error_response(400, "Invalid JSON")
        except Exception as e:
            self._send_error_response(500, f"Signal creation failed: {e}")
    
    def _handle_health_check(self):
        """Handle health check request"""
        response = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "algotrade-http-bridge",
            "components": {
                "account_info": hasattr(self, 'account_info') and self.account_info is not None,
                "broker_manager": hasattr(self, 'broker_manager') and self.broker_manager is not None,
                "strategy_manager": hasattr(self, 'strategy_manager') and self.strategy_manager is not None
            }
        }
        self._send_json_response(200, response)
    
    def _handle_simple_health_check(self):
        """Handles simple health check for load balancers etc."""
        self._send_json_response(200, {"status": "ok"})
    
    def _send_cors_headers(self):
        """Send CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def _send_json_response(self, status_code: int, data: Dict[str, Any]):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self._send_cors_headers()
        self.end_headers()
        
        response_data = json.dumps(data, indent=2)
        self.wfile.write(response_data.encode('utf-8'))
    
    def _send_error_response(self, status_code: int, message: str):
        """Send error response"""
        error_data = {
            "error": message,
            "status_code": status_code,
            "timestamp": datetime.now().isoformat()
        }
        self._send_json_response(status_code, error_data)

def start_http_bridge(account_info, broker_manager, strategy_manager, port: int = 5000):
    """Start the HTTP bridge server"""

    class ThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
        allow_reuse_address = True
        daemon_threads = True

    try:
        # Create custom handler class
        handler_class = type(
            'CustomBridgeHandler',
            (BridgeHandler,),
            {
                'account_info': account_info,
                'broker_manager': broker_manager,
                'strategy_manager': strategy_manager
            }
        )
        
        # Create server
        server = ThreadingHTTPServer(('localhost', port), handler_class)
        
        print(f"HTTP Bridge started on http://localhost:{port}")
        print("Available endpoints:")
        print("  GET  /api/account - Account information")
        print("  GET  /api/positions - Open positions")
        print("  GET  /api/trades - Recent trades")
        print("  GET  /api/strategies - Trading strategies")
        print("  GET  /api/signals - Trading signals")
        print("  GET  /api/performance - Performance metrics")
        print("  GET  /api/capital/summary - Capital summary")
        print("  GET  /api/health - Health check")
        print("  GET  /health - Simple health check")
        print("  POST /api/order - Place order")
        print("  POST /api/strategy/toggle - Toggle strategy")
        print("  POST /api/strategy/create - Create strategy")
        print("  POST /api/strategy/update - Update strategy")
        print("  POST /api/strategy/capital - Update strategy capital")
        print("  POST /api/signal - Create signal")
        
        # Start server
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\nShutting down HTTP Bridge...")
        server.shutdown()
        server.server_close()
    except Exception as e:
        print(f"Error starting HTTP Bridge: {e}")
        raise 