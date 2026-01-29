#!/usr/bin/env python3
"""Test single trade via Rust adapter"""
import os
import sys
import asyncio
import json

sys.path.insert(0, '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages')
os.environ['PYTHONPATH'] = '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages'

from dotenv import load_dotenv
load_dotenv(".env.testnet")

import paradex_adapter


async def main():
    print("Testing single trade via Rust adapter...")
    
    config = paradex_adapter.PyParadexConfig(
        "testnet",
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_SUBKEY_PRIVATE_KEY")
    )
    client = paradex_adapter.PyHttpClient(config)
    
    # Get orderbook
    print("\n[1] Fetching orderbook...")
    orderbook_json = await client.get_orderbook("BTC-USD-PERP")
    orderbook = json.loads(orderbook_json)
    best_ask = float(orderbook["asks"][0][0])
    print(f"    Best ask: ${best_ask}")
    
    # Submit order
    print("\n[2] Submitting order...")
    entry = round(best_ask * 0.9995, 1)
    
    order_json = await client.submit_order(
        "BTC-USD-PERP",
        "BUY",
        "LIMIT",
        "0.001",
        str(entry)
    )
    order = json.loads(order_json)
    
    print(f"    ✅ Order ID: {order.get('id')}")
    print(f"    Status: {order.get('status')}")
    
    print("\n✅ Single trade test passed!")


if __name__ == "__main__":
    asyncio.run(main())
