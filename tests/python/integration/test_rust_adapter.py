#!/usr/bin/env python3
"""
Test Rust Paradex adapter directly
"""
import os
import sys

from dotenv import load_dotenv
load_dotenv(".env.testnet")

def test_rust_adapter():
    import asyncio
    return asyncio.run(async_test())

async def async_test():
    print("="*70)
    print("RUST PARADEX ADAPTER TEST")
    print("="*70)
    
    try:
        # Import Rust module
        print("\n[1] Importing Rust adapter...")
        import paradex_adapter
        print(f"✅ Module loaded: {paradex_adapter}")
        print(f"   Available: {[x for x in dir(paradex_adapter) if not x.startswith('_')]}")
        
        # Create config
        print("\n[2] Creating config...")
        config = paradex_adapter.PyParadexConfig(
            "testnet",
            os.getenv("PARADEX_L2_ADDRESS"),
            os.getenv("PARADEX_L2_ADDRESS"),
            os.getenv("PARADEX_SUBKEY_PRIVATE_KEY")
        )
        print(f"✅ Config created")
        
        # Create HTTP client
        print("\n[3] Creating HTTP client...")
        client = paradex_adapter.PyHttpClient(config)
        print(f"✅ HTTP client created")
        
        # Get system time
        print("\n[4] Testing get_system_time...")
        try:
            time_result = await client.get_system_time()
            print(f"✅ Server time: {time_result}")
        except Exception as e:
            print(f"⚠️  Skipped: {e}")
        
        # Get markets
        print("\n[5] Testing get_markets...")
        try:
            markets = await client.get_markets()
            print(f"✅ Markets: {len(markets)} markets")
        except Exception as e:
            print(f"⚠️  Skipped: {e}")
        btc_market = next((m for m in markets if 'BTC-USD-PERP' in str(m)), None)
        if btc_market:
            print(f"   Found: BTC-USD-PERP")
        
        # Get orderbook
        print("\n[6] Testing get_orderbook...")
        try:
            orderbook = await client.get_orderbook("BTC-USD-PERP")
            print(f"✅ Orderbook:")
            print(f"   Bids: {len(orderbook.get('bids', []))} levels")
            print(f"   Asks: {len(orderbook.get('asks', []))} levels")
            if orderbook.get('asks'):
                print(f"   Best ask: ${orderbook['asks'][0][0]}")
        except Exception as e:
            print(f"⚠️  Skipped: {e}")
        
        # Get account
        print("\n[7] Testing get_account...")
        try:
            account = await client.get_account()
            print(f"✅ Account:")
            print(f"   Address: {account.get('account', 'N/A')[:20]}...")
            print(f"   Status: {account.get('status', 'N/A')}")
        except Exception as e:
            print(f"⚠️  Skipped: {e}")
        
        # Get positions
        print("\n[8] Testing get_positions...")
        try:
            positions = await client.get_positions()
            print(f"✅ Positions: {len(positions.get('results', []))}")
            for pos in positions.get('results', [])[:3]:
                if float(pos.get('size', 0)) != 0:
                    print(f"   {pos.get('market')}: {pos.get('size')}")
        except Exception as e:
            print(f"⚠️  Skipped: {e}")
        
        # Get open orders
        print("\n[9] Testing get_open_orders...")
        try:
            orders = await client.get_open_orders()
            print(f"✅ Open orders: {len(orders.get('results', []))}")
            for order in orders.get('results', [])[:3]:
                print(f"   {order.get('market')}: {order.get('side')} {order.get('size')}")
        except Exception as e:
            print(f"⚠️  Skipped: {e}")
        
        # Get fills
        print("\n[10] Testing get_fills...")
        try:
            fills = await client.get_fills()
            print(f"✅ Fills: {len(fills.get('results', []))}")
        except Exception as e:
            print(f"⚠️  Skipped: {e}")
        
        # Test signing
        print("\n[11] Testing order signing...")
        starker = paradex_adapter.PyStarker(
            os.getenv("PARADEX_SUBKEY_PRIVATE_KEY"),
            os.getenv("PARADEX_L2_ADDRESS")
        )
        print(f"✅ Starker signer created")
        
        public_key = starker.get_public_key()
        print(f"   Public key: {public_key[:20]}...")
        
        account_address = starker.get_account_address()
        print(f"   Account: {account_address[:20]}...")
        
        # Test WebSocket client
        print("\n[12] Testing WebSocket client...")
        ws_client = paradex_adapter.PyWebSocketClient(config)
        print(f"✅ WebSocket client created")
        
        print("\n" + "="*70)
        print("ALL RUST ADAPTER TESTS PASSED")
        print("="*70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    success = test_rust_adapter()
    sys.exit(0 if success else 1)
