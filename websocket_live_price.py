#!/usr/bin/env python3
"""
WebSocket live price feed with state management
"""
import os
import sys
import asyncio
import json
from datetime import datetime

sys.path.insert(0, '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages')
os.environ['PYTHONPATH'] = '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages'

from dotenv import load_dotenv
load_dotenv(".env.testnet")

import paradex_adapter


class LivePriceFeed:
    def __init__(self):
        self.best_bid = 0
        self.best_ask = 0
        self.last_update = None
        
    def on_orderbook(self, data):
        """Handle orderbook updates"""
        try:
            data_dict = json.loads(data) if isinstance(data, str) else data
            
            if 'bids' in data_dict and 'asks' in data_dict:
                self.best_bid = float(data_dict['bids'][0][0])
                self.best_ask = float(data_dict['asks'][0][0])
                self.last_update = datetime.now()
                
                mid = (self.best_bid + self.best_ask) / 2
                spread = self.best_ask - self.best_bid
                
                print(f"\r[{self.last_update.strftime('%H:%M:%S')}] "
                      f"BID: ${self.best_bid:>9,.2f} | "
                      f"ASK: ${self.best_ask:>9,.2f} | "
                      f"MID: ${mid:>9,.2f} | "
                      f"SPREAD: ${spread:>5.2f} | "
                      f"[WebSocket]",
                      end="", flush=True)
        except Exception as e:
            print(f"\nError: {e}")


async def main():
    print("="*70)
    print("WEBSOCKET LIVE PRICE FEED")
    print("="*70)
    print("Connecting...\n")
    
    config = paradex_adapter.PyParadexConfig(
        "testnet",
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_SUBKEY_PRIVATE_KEY")
    )
    
    ws = paradex_adapter.PyWebSocketClient(config)
    feed = LivePriceFeed()
    
    # Set callback
    ws.on_orderbook(feed.on_orderbook)
    
    # Subscribe
    await ws.subscribe_orderbook("BTC-USD-PERP")
    
    print("✅ Connected! Receiving real-time updates...\n")
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n\n✅ Stopped")


if __name__ == "__main__":
    asyncio.run(main())
