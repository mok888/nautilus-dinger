#!/usr/bin/env python3
"""
Test Rust adapter with paradex-py wrapper
Full trading loop test
"""
import os
import sys
import asyncio

# Set PYTHONPATH for paradex-py
sys.path.insert(0, '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages')
os.environ['PYTHONPATH'] = '/home/mok/projects/nautilus-dinger/.venv/lib/python3.12/site-packages'

from dotenv import load_dotenv
load_dotenv(".env.testnet")

async def test_rust_adapter():
    import paradex_adapter
    
    print("="*70)
    print("RUST ADAPTER WITH PARADEX-PY WRAPPER - FULL TEST")
    print("="*70)
    
    # Create config
    print("\n[1] Creating config...")
    config = paradex_adapter.PyParadexConfig(
        "testnet",
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_L2_ADDRESS"),
        os.getenv("PARADEX_SUBKEY_PRIVATE_KEY")
    )
    print("✅ Config created")
    
    # Create HTTP client
    print("\n[2] Creating HTTP client...")
    try:
        client = paradex_adapter.PyHttpClient(config)
        print("✅ HTTP client created (with paradex-py wrapper)")
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False
    
    # Test markets
    print("\n[3] Testing get_markets...")
    try:
        markets = await client.get_markets()
        import json
        markets_data = json.loads(markets)
        print(f"✅ Markets: {len(markets_data.get('results', []))} markets")
        btc = next((m for m in markets_data.get('results', []) if m.get('symbol') == 'BTC-USD-PERP'), None)
        if btc:
            print(f"   Found BTC-USD-PERP")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Test orderbook
    print("\n[4] Testing get_orderbook...")
    try:
        orderbook = await client.get_orderbook("BTC-USD-PERP")
        ob_data = json.loads(orderbook)
        print(f"✅ Orderbook:")
        print(f"   Bids: {len(ob_data.get('bids', []))} levels")
        print(f"   Asks: {len(ob_data.get('asks', []))} levels")
        if ob_data.get('asks'):
            print(f"   Best ask: ${ob_data['asks'][0][0]}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Test account
    print("\n[5] Testing get_account...")
    try:
        account = await client.get_account()
        acc_data = json.loads(account)
        print(f"✅ Account:")
        print(f"   Address: {acc_data.get('account', 'N/A')[:20]}...")
        print(f"   Status: {acc_data.get('status', 'N/A')}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Test positions
    print("\n[6] Testing get_positions...")
    try:
        positions = await client.get_positions()
        pos_data = json.loads(positions)
        print(f"✅ Positions: {len(pos_data.get('results', []))}")
        for pos in pos_data.get('results', [])[:3]:
            if float(pos.get('size', 0)) != 0:
                print(f"   {pos.get('market')}: {pos.get('size')}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Test open orders
    print("\n[7] Testing get_open_orders...")
    try:
        orders = await client.get_open_orders()
        orders_data = json.loads(orders)
        print(f"✅ Open orders: {len(orders_data.get('results', []))}")
        for order in orders_data.get('results', [])[:3]:
            print(f"   {order.get('market')}: {order.get('side')} {order.get('size')}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Test fills
    print("\n[8] Testing get_fills...")
    try:
        import time
        start_time = int(time.time() * 1000) - (24 * 60 * 60 * 1000)  # Last 24h
        fills = await client.get_fills(start_time)
        fills_data = json.loads(fills)
        print(f"✅ Fills: {len(fills_data.get('results', []))}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    print("\n" + "="*70)
    print("RUST ADAPTER TEST COMPLETE")
    print("="*70)
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_rust_adapter())
    sys.exit(0 if success else 1)
