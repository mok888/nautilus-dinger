"""
HTTP Mock Server for Paradex API Testing.

Provides local mock endpoints for offline development and testing.
Supports basic CRUD operations for orders, fills, positions, markets.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import time
from typing import Any
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# In-memory storage for mock data
mock_data = {
    "orders": {},
    "fills": [],
    "positions": {},
    "markets": {},
    "instruments": {},
}

# Load test fixtures on startup
def load_fixtures():
    """Load test data from fixtures directory."""
    try:
        with open('fixtures/markets.json', 'r') as f:
            mock_data["markets"] = json.load(f)
        with open('fixtures/instruments.json', 'r') as f:
            mock_data["instruments"] = json.load(f)
        print("[MockServer] Loaded fixtures")
    except FileNotFoundError:
        print("[MockServer] No fixtures found, using empty state")

@app.route('/v1/system/time', methods=['GET'])
def get_system_time():
    """Mock system time endpoint."""
    return jsonify({"server_time": int(time.time() * 1000)})

@app.route('/v1/markets', methods=['GET'])
def get_markets():
    """Mock markets endpoint."""
    return jsonify({"results": list(mock_data["markets"].values())})

@app.route('/v1/instruments/<symbol>', methods=['GET'])
def get_instrument(symbol):
    """Mock instrument endpoint (requires auth in production)."""
    instrument = mock_data["instruments"].get(symbol)
    if instrument:
        return jsonify(instrument)
    return jsonify({"error": "NOT_FOUND", "message": f"Instrument {symbol} not found"}), 404

@app.route('/v1/orders/open', methods=['GET'])
def get_open_orders():
    """Mock open orders endpoint (requires auth)."""
    return jsonify({"results": list(mock_data["orders"].values())})

@app.route('/v1/orders', methods=['POST'])
def create_order():
    """Mock order creation (requires auth)."""
    order_data = request.json
    
    # Generate mock order ID
    order_id = f"order_{int(time.time())}"
    
    order = {
        "order_id": order_id,
        "status": "OPEN",
        **order_data,
        "timestamp": int(time.time() * 1000)
    }
    
    mock_data["orders"][order_id] = order
    return jsonify(order), 201

@app.route('/v1/orders/<order_id>', methods=['DELETE'])
def cancel_order(order_id):
    """Mock order cancellation (requires auth)."""
    if order_id in mock_data["orders"]:
        mock_data["orders"][order_id]["status"] = "CANCELED"
        return jsonify({"order_id": order_id, "status": "CANCELED"})
    return jsonify({"error": "NOT_FOUND", "message": f"Order {order_id} not found"}), 404

@app.route('/v1/orders', methods=['DELETE'])
def cancel_all_orders():
    """Mock cancel all orders (requires auth)."""
    count = len(mock_data["orders"])
    mock_data["orders"] = {}
    return jsonify({"cancelled_count": count})

@app.route('/v1/account/positions', methods=['GET'])
def get_positions():
    """Mock positions endpoint (requires auth)."""
    return jsonify({"results": list(mock_data["positions"].values())})

@app.route('/v1/account/fills', methods=['GET'])
def get_fills():
    """Mock fills endpoint (requires auth)."""
    return jsonify({"results": mock_data["fills"]})

@app.route('/v1/account', methods=['GET'])
def get_account():
    """Mock account summary endpoint (requires auth)."""
    return jsonify({
        "account": "0xmock_account_address",
        "account_value": "100000.00",
        "total_collateral": "95000.00",
        "initial_margin": "9500.00",
        "maintenance_margin": "9500.00",
        "total_margin": "19000.00",
        "free_collateral": "76000.00",
        "margin_fraction": "0.1",
        "status": "ACTIVE",
        "seq_no": 12345
    })

@app.route('/v1/config', methods=['GET'])
def get_config():
    """Mock config endpoint (requires auth)."""
    return jsonify({
        "environment": "testnet",
        "chain_id": "SEPOLIA",
        "paradex_contract": "0xmock_contract_address",
        "supported_order_types": ["LIMIT", "MARKET", "STOP", "TWAP", "TPSL"],
        "supported_time_in_force": ["GTC", "IOC", "FOK", "POST_ONLY"],
        "max_open_orders": 150,
        "position_limit": "200000",
        "maker_fee_rate": "0.0001",
        "taker_fee_rate": "0.0001"
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "paradex-mock"})

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "NOT_FOUND", "message": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "INTERNAL_ERROR", "message": "Internal server error"}), 500

if __name__ == '__main__':
    load_fixtures()
    print("[MockServer] Starting HTTP mock server on http://localhost:8080")
    print("[MockServer] Testnet mode enabled")
    print("[MockServer] Supported endpoints:")
    print("  - GET  /v1/system/time")
    print("  - GET  /v1/markets")
    print("  - GET  /v1/instruments/<symbol>")
    print("  - GET  /v1/orders/open")
    print("  - POST /v1/orders")
    print("  - DELETE /v1/orders/<order_id>")
    print("  - DELETE /v1/orders")
    print("  - GET  /v1/account/positions")
    print("  - GET  /v1/account/fills")
    print("  - GET  /v1/account")
    print("  - GET  /v1/config")
    print("  - GET  /health")
    app.run(host='0.0.0.0', port=8080, debug=True)
