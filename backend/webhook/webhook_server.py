"""
Webhook server for external trading signals
"""

import json
import hmac
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

from utils.logger import LoggerMixin

class WebhookHandler(BaseHTTPRequestHandler, LoggerMixin):
    """HTTP request handler for webhook endpoints"""
    
    def __init__(self, *args, strategy_manager=None, secret=None, **kwargs):
        self.strategy_manager = strategy_manager
        self.secret = secret
        super().__init__(*args, **kwargs)
    
    def log_message(self, format, *args):
        """Override to use our logger"""
        self.log_info(f"{self.address_string()} - {format % args}")
    
    def do_POST(self):
        """Handle POST requests for webhook signals"""
        try:
            # Parse URL
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            
            if path == "/webhook/signal":
                self._handle_signal_webhook()
            elif path == "/webhook/health":
                self._handle_health_check()
            else:
                self._send_error_response(404, "Endpoint not found")
                
        except Exception as e:
            self.log_error(f"Error handling webhook: {e}")
            self._send_error_response(500, "Internal server error")
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == "/webhook/health":
            self._handle_health_check()
        else:
            self._send_error_response(404, "Endpoint not found")
    
    def _handle_signal_webhook(self):
        """Handle trading signal webhook"""
        try:
            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._send_error_response(400, "No content")
                return
            
            # Read request body
            post_data = self.rfile.read(content_length)
            
            # Verify signature if secret is configured
            if self.secret:
                if not self._verify_signature(post_data):
                    self._send_error_response(401, "Invalid signature")
                    return
            
            # Parse JSON data
            try:
                signal_data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                self._send_error_response(400, "Invalid JSON")
                return
            
            # Validate required fields
            required_fields = ["strategy_id", "symbol", "side"]
            for field in required_fields:
                if field not in signal_data:
                    self._send_error_response(400, f"Missing required field: {field}")
                    return
            
            # Process signal
            if self.strategy_manager:
                signal = self.strategy_manager.process_webhook_signal(signal_data)
                self.log_info(f"Processed webhook signal: {signal['id']}")
                
                response = {
                    "status": "success",
                    "message": "Signal processed successfully",
                    "signal_id": signal["id"],
                    "timestamp": datetime.now().isoformat()
                }
            else:
                self._send_error_response(500, "Strategy manager not available")
                return
            
            # Send response
            self._send_json_response(200, response)
            
        except Exception as e:
            self.log_error(f"Error processing signal webhook: {e}")
            self._send_error_response(500, "Internal server error")
    
    def _handle_health_check(self):
        """Handle health check endpoint"""
        response = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "algotrade-webhook"
        }
        self._send_json_response(200, response)
    
    def _verify_signature(self, data: bytes) -> bool:
        """Verify webhook signature"""
        if not self.secret:
            return True
        
        signature = self.headers.get('X-Signature')
        if not signature:
            return False
        
        # Calculate expected signature
        expected_signature = hmac.new(
            self.secret.encode('utf-8'),
            data,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    def _send_json_response(self, status_code: int, data: Dict[str, Any]):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Signature')
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

class WebhookServer(LoggerMixin):
    """Webhook server for external trading signals"""
    
    def __init__(self, config, strategy_manager):
        super().__init__()
        self.config = config
        self.strategy_manager = strategy_manager
        self.webhook_config = config.get_webhook_config()
        self.server = None
        self.server_thread = None
        self.running = False
        
        # Get configuration
        self.port = self.webhook_config.get("port", 8080)
        self.secret = self.webhook_config.get("secret", "")
    
    def start(self):
        """Start the webhook server"""
        if self.running:
            self.log_warning("Webhook server is already running")
            return
        
        try:
            # Create custom handler class
            handler_class = type(
                'CustomWebhookHandler',
                (WebhookHandler,),
                {
                    'strategy_manager': self.strategy_manager,
                    'secret': self.secret
                }
            )
            
            # Create server
            self.server = HTTPServer(('localhost', self.port), handler_class)
            self.running = True
            
            self.log_info(f"Starting webhook server on port {self.port}")
            
            # Start server in separate thread
            self.server_thread = threading.Thread(target=self._run_server)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            self.log_info("Webhook server started successfully")
            
        except Exception as e:
            self.log_error(f"Failed to start webhook server: {e}")
            raise
    
    def _run_server(self):
        """Run the server (called in separate thread)"""
        try:
            if self.server:
                self.server.serve_forever()
        except Exception as e:
            self.log_error(f"Webhook server error: {e}")
        finally:
            self.running = False
    
    def stop(self):
        """Stop the webhook server"""
        if not self.running:
            self.log_warning("Webhook server is not running")
            return
        
        try:
            self.log_info("Stopping webhook server...")
            self.running = False
            
            if self.server:
                self.server.shutdown()
                self.server.server_close()
            
            if self.server_thread and self.server_thread.is_alive():
                self.server_thread.join(timeout=5)
            
            self.log_info("Webhook server stopped")
            
        except Exception as e:
            self.log_error(f"Error stopping webhook server: {e}")
    
    def is_running(self) -> bool:
        """Check if server is running"""
        return self.running
    
    def get_status(self) -> Dict[str, Any]:
        """Get server status"""
        return {
            "running": self.running,
            "port": self.port,
            "secret_configured": bool(self.secret),
            "endpoints": [
                "POST /webhook/signal - Trading signal endpoint",
                "GET /webhook/health - Health check endpoint"
            ]
        } 