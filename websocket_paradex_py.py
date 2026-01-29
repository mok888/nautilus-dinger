#!/usr/bin/env python3
"""
WebSocket using paradex-py SDK directly
"""
import os
import asyncio
from dotenv import load_dotenv
from paradex_py import ParadexSubkey

load_dotenv(".env.testnet")


async def main():
    print("="*70)
    print("WEBSOCKET - Using paradex-py SDK")
    print("="*70)
    
    paradex = ParadexSubkey(
        env="testnet",
        l2_private_key=os.getenv("PARADEX_SUBKEY_PRIVATE_KEY"),
        l2_address=os.getenv("PARADEX_L2_ADDRESS")
    )
    
    print("\n[1] Connecting to WebSocket...")
    
    # Subscribe to orderbook
    def on_orderbook(data):
        if 'bids' in data and 'asks' in data:
            best_bid = float(data['bids'][0][0])
            best_ask = float(data['asks'][0][0])
            mid = (best_bid + best_ask) / 2
            print(f"\r[WS] BID: ${best_bid:>9,.2f} | ASK: ${best_ask:>9,.2f} | MID: ${mid:>9,.2f}", end="", flush=True)
    
    # Start WebSocket
    await paradex.ws_client.subscribe_orderbook("BTC-USD-PERP", on_orderbook)
    
    print("\n[2] Receiving updates...")
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n\n✅ Stopped")


if __name__ == "__main__":
    asyncio.run(main())
