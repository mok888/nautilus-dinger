#!/usr/bin/env python3
"""
Test WebSocket with simple client
"""
import os
import sys
import asyncio
import json

sys.path.insert(0, '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages')
os.environ['PYTHONPATH'] = '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages'

from dotenv import load_dotenv
load_dotenv(".env.testnet")

import paradex_adapter


def on_orderbook_update(data_str):
    """Handle orderbook updates"""
    try:
        data = json.loads(data_str)
        if 'bids' in data and 'asks' in data:
            best_bid = float(data['bids'][0][0])
            best_ask = float(data['asks'][0][0])
            print(f"[WS] BID: ${best_bid:,.2f} | ASK: ${best_ask:,.2f}")
    except Exception as e:
        print(f"Error: {e}")


async def main():
    print("="*70)
    print("WEBSOCKET TEST - Simple Client")
    print("="*70)
    
    config = paradex_adapter.PyParadexConfig(
        "testnet",
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_SUBKEY_PRIVATE_KEY")
    )
    
    ws = paradex_adapter.PySimpleWebSocketClient(config)
    
    print("\n[1] Setting callback...")
    ws.on_orderbook(on_orderbook_update)
    
    print("[2] Connecting to WebSocket...")
    await ws.connect(["orderbook.BTC-USD-PERP"])
    
    print("\n✅ WebSocket test complete")


if __name__ == "__main__":
    asyncio.run(main())
