#!/usr/bin/env python3
"""
20-trade robustness test using pure Rust adapter
Tests: Data -> Decision -> Order -> Feedback loop
"""
import os
import sys
import asyncio
import time
import json

sys.path.insert(0, '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages')
os.environ['PYTHONPATH'] = '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages'

from dotenv import load_dotenv
load_dotenv(".env.testnet")

import paradex_adapter


async def place_trade_via_rust(client, trade_num):
    """Single trade via Rust adapter"""
    print(f"\n{'='*70}")
    print(f"TRADE #{trade_num}/20")
    print(f"{'='*70}")
    
    # 1. Get market data
    print("[1] Fetching orderbook...")
    orderbook_json = await client.get_orderbook("BTC-USD-PERP")
    orderbook = json.loads(orderbook_json)
    
    best_bid = float(orderbook["bids"][0][0])
    best_ask = float(orderbook["asks"][0][0])
    mid = (best_bid + best_ask) / 2
    
    print(f"    Bid: ${best_bid:,.2f} | Ask: ${best_ask:,.2f}")
    
    # 2. Make decision
    entry = round(mid * 0.9995, 1)
    size = "0.001"
    side = "BUY" if trade_num % 2 == 1 else "SELL"
    
    if side == "SELL":
        entry = round(mid * 1.0005, 1)
    
    print(f"[2] Decision: {side} {size} @ ${entry}")
    
    # 3. Submit order
    print("[3] Submitting order...")
    order_json = await client.submit_order(
        "BTC-USD-PERP",
        side,
        "LIMIT",
        size,
        str(entry)
    )
    order = json.loads(order_json)
    order_id = order.get("id")
    
    print(f"    ✅ Order ID: {order_id}")
    print(f"    Status: {order.get('status')}")
    
    # 4. Get feedback
    await asyncio.sleep(2)
    print("[4] Getting feedback...")
    
    orders_json = await client.get_open_orders()
    orders = json.loads(orders_json)
    
    # Check if our order is still open
    our_order = next((o for o in orders.get("results", []) if o.get("id") == order_id), None)
    
    if our_order:
        print(f"    Status: {our_order.get('status')}")
        print(f"    Filled: {our_order.get('filled_qty', 0)} / {our_order.get('size')}")
    else:
        print(f"    Order closed/filled")
    
    return {
        "trade_num": trade_num,
        "order_id": order_id,
        "side": side,
        "price": entry,
        "status": order.get("status")
    }


async def main():
    print("="*70)
    print("RUST ADAPTER - 20 TRADE ROBUSTNESS TEST")
    print("Pure Rust: Data -> Decision -> Order -> Feedback")
    print("="*70)
    
    # Create Rust client
    print("\n[INIT] Creating Rust adapter client...")
    config = paradex_adapter.PyParadexConfig(
        "testnet",
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_SUBKEY_PRIVATE_KEY")
    )
    client = paradex_adapter.PyHttpClient(config)
    print("✅ Rust client ready")
    
    # Run 20 trades
    results = []
    start_time = time.time()
    
    for i in range(1, 21):
        try:
            result = await place_trade_via_rust(client, i)
            results.append(result)
            
            if i < 20:
                print(f"\n⏳ Waiting 10 seconds...")
                await asyncio.sleep(10)
                
        except Exception as e:
            print(f"❌ Trade {i} failed: {e}")
            results.append({
                "trade_num": i,
                "error": str(e)
            })
    
    # Summary
    elapsed = time.time() - start_time
    successful = len([r for r in results if "error" not in r])
    
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70)
    print(f"Total trades: 20")
    print(f"Successful: {successful}")
    print(f"Failed: {20 - successful}")
    print(f"Time elapsed: {elapsed:.1f}s")
    print(f"\nAll trades via Rust adapter:")
    for r in results[:5]:
        if "error" not in r:
            print(f"  #{r['trade_num']}: {r['side']} @ ${r['price']} - {r['status']}")
    if len(results) > 5:
        print(f"  ... and {len(results) - 5} more")


if __name__ == "__main__":
    asyncio.run(main())
