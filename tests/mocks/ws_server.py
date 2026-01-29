"""
WebSocket Mock Server for Paradex API Testing.

Provides local mock WebSocket for offline development and testing.
Supports JSON-RPC 2.0 protocol and simulates Paradex behavior.
"""

import asyncio
import websockets
import json
import logging
from typing import Set

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store active subscriptions
active_subscriptions: Set[str] = set()

# Mock data generators
async def generate_trade_update(symbol: str):
    """Generate mock trade update."""
    return {
        "jsonrpc": "2.0",
        "method": "data",
        "params": {
            "channel": f"trades.{symbol}",
            "data": {
                "trade_id": f"trade_{asyncio.get_event_loop().time()}",
                "price": "95000" + str(asyncio.get_event_loop().time() % 100),
                "size": "0.001",
                "side": "BUY",
                "timestamp": int(asyncio.get_event_loop().time() * 1000)
            }
        },
        "id": 1
    }

async def generate_orderbook_update(symbol: str):
    """Generate mock order book update."""
    return {
        "jsonrpc": "2.0",
        "method": "data",
        "params": {
            "channel": f"orderbook.{symbol}",
            "data": {
                "bids": [
                    {"price": "95000", "size": "0.5"},
                    {"price": "94999", "size": "0.3"}
                ],
                "asks": [
                    {"price": "95001", "size": "0.3"},
                    {"price": "95002", "size": "0.5"}
                ]
            }
        },
        "id": 2
    }

async def generate_order_update(order_id: str, status: str):
    """Generate mock order status update."""
    return {
        "jsonrpc": "2.0",
        "method": "data",
        "params": {
            "channel": f"orders.{order_id.split('_')[0]}",
            "data": {
                "order_id": order_id,
                "status": status,
                "timestamp": int(asyncio.get_event_loop().time() * 1000)
            }
        },
        "id": 3
    }

async def handle_connection(websocket: websockets.WebSocketServerProtocol, path: str):
    """Handle new WebSocket connection."""
    logger.info(f"[WebSocket] New connection from {path}")
    
    try:
        async for message in websocket:
            data = json.loads(message)
            logger.debug(f"[WebSocket] Received: {data}")
            
            # Handle auth method
            if data.get("method") == "auth":
                bearer = data.get("params", {}).get("bearer")
                if bearer == "valid_mock_token":
                    await websocket.send(json.dumps({
                        "jsonrpc": "2.0",
                        "result": {
                            "status": "authenticated",
                            "expiresAt": int(asyncio.get_event_loop().time()) + 300000
                        },
                        "id": data.get("id")
                    }))
                else:
                    await websocket.send(json.dumps({
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32000,
                            "message": "Unauthorized"
                        },
                        "id": data.get("id")
                    }))
            
            # Handle subscription requests
            elif data.get("method") == "subscribe":
                channel = data.get("params", {}).get("channel")
                active_subscriptions.add(channel)
                logger.info(f"[WebSocket] Subscribed to {channel}")
                
                await websocket.send(json.dumps({
                    "jsonrpc": "2.0",
                    "result": {
                        "channel": channel,
                        "subscribed": True
                    },
                    "id": data.get("id")
                }))
            
            # Handle unsubscribe requests
            elif data.get("method") == "unsubscribe":
                channel = data.get("params", {}).get("channel")
                if channel in active_subscriptions:
                    active_subscriptions.remove(channel)
                    logger.info(f"[WebSocket] Unsubscribed from {channel}")
                
                await websocket.send(json.dumps({
                    "jsonrpc": "2.0",
                    "result": {
                        "channel": channel,
                        "unsubscribed": True
                    },
                    "id": data.get("id")
                }))
            
            else:
                logger.warning(f"[WebSocket] Unknown method: {data.get('method')}")
                await websocket.send(json.dumps({
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32602,
                        "message": "Invalid params"
                    },
                    "id": data.get("id")
                }))
    
    except Exception as e:
        logger.error(f"[WebSocket] Error handling message: {e}")

async def start_broadcasts(websocket: websockets.WebSocketServerProtocol):
    """Start broadcasting mock data for active subscriptions."""
    while True:
        await asyncio.sleep(1)  # Send updates every second
        
        for channel in active_subscriptions:
            try:
                # Parse channel name
                if channel.startswith("trades."):
                    symbol = channel.split(".")[1]
                    message = await generate_trade_update(symbol)
                elif channel.startswith("orderbook."):
                    symbol = channel.split(".")[1]
                    message = await generate_orderbook_update(symbol)
                elif channel.startswith("orders."):
                    # Generate mock order updates
                    if "BTC-USD-PERP" in channel:
                        message = await generate_order_update("order_123", "OPEN")
                        message = await generate_order_update("order_456", "FILLED")
                else:
                    continue  # Skip unknown channels
                
                await websocket.send(json.dumps(message))
            except Exception as e:
                logger.error(f"[WebSocket] Error broadcasting: {e}")

async def handler(websocket, path):
    """WebSocket connection handler."""
    logger.info(f"[WebSocket] Handler called for path: {path}")
    
    # Send initial connection confirmation
    await websocket.send(json.dumps({
        "jsonrpc": "2.0",
        "result": {
            "status": "connected",
            "server": "paradex-mock"
        },
        "id": 0
    }))
    
    # Start broadcasting
    broadcast_task = asyncio.create_task(start_broadcasts(websocket))
    
    try:
        # Handle messages
        await handle_connection(websocket, path)
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"[WebSocket] Connection closed: {path}")
        if path in active_subscriptions:
            active_subscriptions.remove(path)
    except Exception as e:
        logger.error(f"[WebSocket] Error: {e}")
    finally:
        if not broadcast_task.done():
            broadcast_task.cancel()

async def main():
    """Start WebSocket mock server."""
    host = "localhost"
    port = 8081
    
    logger.info(f"[WebSocket] Starting mock server on ws://{host}:{port}")
    logger.info(f"[WebSocket] Supported channels:")
    logger.info("  - trades.{symbol}")
    logger.info("  - orderbook.{symbol}")
    logger.info("  - orders.{symbol}")
    logger.info("  - fills.{symbol}")
    logger.info("  - positions")
    
    async with websockets.serve(handler, host, port) as server:
        logger.info(f"[WebSocket] Server started on ws://{host}:{port}")
        logger.info("[WebSocket] Waiting for connections...")
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("[WebSocket] Server shutdown requested")
    except Exception as e:
        logger.error(f"[WebSocket] Fatal error: {e}")
