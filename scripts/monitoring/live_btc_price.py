#!/usr/bin/env python3
"""
Live BTC price display via Rust adapter with latency
"""
import os
import sys
import asyncio
import json
import time
from datetime import datetime

sys.path.insert(0, '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages')
os.environ['PYTHONPATH'] = '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages'

from dotenv import load_dotenv
load_dotenv(".env.testnet")

import paradex_adapter


async def display_live_price():
    # Initialize Rust client
    config = paradex_adapter.PyParadexConfig(
        "testnet",
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_SUBKEY_PRIVATE_KEY")
    )
    client = paradex_adapter.PyHttpClient(config)
    
    print("="*70)
    print("LIVE BTC-USD-PERP PRICE (via Rust Adapter)")
    print("="*70)
    print("Press Ctrl+C to stop\n")
    
    while True:
        try:
            # Measure latency
            start = time.time()
            
            # Fetch orderbook via Rust
            orderbook_json = await client.get_orderbook("BTC-USD-PERP")
            orderbook = json.loads(orderbook_json)
            
            latency_ms = (time.time() - start) * 1000
            
            # Parse data
            best_bid = float(orderbook["bids"][0][0])
            best_ask = float(orderbook["asks"][0][0])
            spread = best_ask - best_bid
            mid = (best_bid + best_ask) / 2
            
            # Display
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            print(f"\r[{timestamp}] "
                  f"BID: ${best_bid:>9,.2f} | "
                  f"ASK: ${best_ask:>9,.2f} | "
                  f"MID: ${mid:>9,.2f} | "
                  f"SPREAD: ${spread:>5.2f} | "
                  f"LATENCY: {latency_ms:>6.1f}ms", 
                  end="", flush=True)
            
            await asyncio.sleep(1)
            
        except KeyboardInterrupt:
            print("\n\n✅ Stopped")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(display_live_price())
