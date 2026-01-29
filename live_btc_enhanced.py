#!/usr/bin/env python3
"""
Live BTC price with detailed stats via Rust adapter
"""
import os
import sys
import asyncio
import json
import time
from datetime import datetime
from collections import deque

sys.path.insert(0, '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages')
os.environ['PYTHONPATH'] = '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages'

from dotenv import load_dotenv
load_dotenv(".env.testnet")

import paradex_adapter


async def display_live_price_enhanced():
    config = paradex_adapter.PyParadexConfig(
        "testnet",
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_SUBKEY_PRIVATE_KEY")
    )
    client = paradex_adapter.PyHttpClient(config)
    
    latencies = deque(maxlen=10)
    prices = deque(maxlen=10)
    
    print("\033[2J\033[H")  # Clear screen
    print("="*80)
    print("LIVE BTC-USD-PERP PRICE FEED (Rust Adapter)")
    print("="*80)
    
    while True:
        try:
            start = time.time()
            orderbook_json = await client.get_orderbook("BTC-USD-PERP")
            orderbook = json.loads(orderbook_json)
            latency_ms = (time.time() - start) * 1000
            
            best_bid = float(orderbook["bids"][0][0])
            best_ask = float(orderbook["asks"][0][0])
            spread = best_ask - best_bid
            mid = (best_bid + best_ask) / 2
            
            latencies.append(latency_ms)
            prices.append(mid)
            
            # Calculate stats
            avg_latency = sum(latencies) / len(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            
            price_change = prices[-1] - prices[0] if len(prices) > 1 else 0
            
            # Display
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            
            print(f"\033[4;0H")  # Move cursor
            print(f"Time:        {timestamp}")
            print(f"")
            print(f"BID:         ${best_bid:>10,.2f}")
            print(f"ASK:         ${best_ask:>10,.2f}")
            print(f"MID:         ${mid:>10,.2f}")
            print(f"SPREAD:      ${spread:>10.2f}")
            print(f"")
            print(f"LATENCY:     {latency_ms:>7.1f} ms")
            print(f"AVG (10):    {avg_latency:>7.1f} ms")
            print(f"MIN:         {min_latency:>7.1f} ms")
            print(f"MAX:         {max_latency:>7.1f} ms")
            print(f"")
            print(f"CHANGE (10s): ${price_change:>+9.2f}")
            print(f"")
            print(f"Updates: {len(prices)}")
            print(f"")
            print("Press Ctrl+C to stop")
            
            await asyncio.sleep(1)
            
        except KeyboardInterrupt:
            print("\n\n✅ Stopped")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(display_live_price_enhanced())
