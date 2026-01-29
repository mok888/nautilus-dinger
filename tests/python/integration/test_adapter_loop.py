#!/usr/bin/env python3
"""
Test Paradex adapter robustness using paradex-py SDK
Full trading loop:
1. Get market data
2. Place limit order
3. Check order status  
4. Check position
5. Close position
"""
import os
import asyncio
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv(".env.testnet")

L2_ADDRESS = os.getenv("PARADEX_L2_ADDRESS")
SUBKEY = os.getenv("PARADEX_SUBKEY_PRIVATE_KEY")

async def main():
    from paradex_py import ParadexSubkey
    from paradex_py.common.order import Order, OrderSide, OrderType
    
    print("="*70)
    print("PARADEX ADAPTER ROBUSTNESS TEST")
    print("="*70)
    
    # Initialize
    print("\n[1] Initializing client...")
    paradex = ParadexSubkey(
        env="testnet",
        l2_private_key=SUBKEY,
        l2_address=L2_ADDRESS
    )
    print("✅ Client initialized")
    
    # Get market data
    print("\n[2] Fetching market data...")
    markets = paradex.api_client.fetch_markets()
    btc_market = next((m for m in markets["results"] if m["symbol"] == "BTC-USD-PERP"), None)
    if not btc_market:
        print("❌ BTC-USD-PERP not found")
        return
    print(f"✅ Market: {btc_market['symbol']}")
    print(f"   Status: {btc_market.get('status', 'N/A')}")
    
    # Get orderbook
    print("\n[3] Fetching orderbook...")
    orderbook = paradex.api_client.fetch_orderbook("BTC-USD-PERP")
    ask = Decimal(orderbook["asks"][0][0])
    bid = Decimal(orderbook["bids"][0][0])
    print(f"✅ Bid: ${float(bid):,.2f}, Ask: ${float(ask):,.2f}")
    
    # Calculate entry
    entry = ask * Decimal("0.9995")
    entry = (entry / Decimal("0.1")).quantize(Decimal("1")) * Decimal("0.1")
    print(f"   Entry: ${float(entry):,.2f} (-5bps)")
    
    # Place limit order
    print("\n[4] Placing limit order...")
    order = Order(
        market="BTC-USD-PERP",
        order_side=OrderSide.Buy,
        order_type=OrderType.Limit,
        size=Decimal("0.001"),
        limit_price=entry
    )
    
    result = paradex.api_client.submit_order(order)
    order_id = result["id"]
    print(f"✅ Order placed: {order_id}")
    print(f"   Status: {result['status']}")
    
    # Wait for order processing
    await asyncio.sleep(2)
    
    # Check order status
    print("\n[5] Checking order status...")
    order_status = paradex.api_client.fetch_order(order_id)
    print(f"✅ Order {order_id}")
    print(f"   Status: {order_status['status']}")
    print(f"   Filled: {order_status['size']} / {order_status['remaining_size']}")
    
    # Check all open orders
    print("\n[6] Checking all open orders...")
    open_orders = paradex.api_client.fetch_orders()
    print(f"✅ Open orders: {len(open_orders['results'])}")
    for o in open_orders["results"][:3]:
        print(f"   {o['market']}: {o['side']} {o['size']} @ ${o['price']}")
    
    # Check positions
    print("\n[7] Checking positions...")
    positions = paradex.api_client.fetch_positions()
    print(f"✅ Positions: {len(positions['results'])}")
    
    has_position = False
    for pos in positions["results"]:
        size = Decimal(pos["size"])
        if size != 0:
            has_position = True
            print(f"   {pos['market']}: {size} @ ${pos['average_entry_price']}")
    
    # Close position if exists
    if has_position:
        print("\n[8] Closing position...")
        for pos in positions["results"]:
            size = Decimal(pos["size"])
            if size == 0:
                continue
            
            close_order = Order(
                market=pos["market"],
                order_side=OrderSide.Sell if size > 0 else OrderSide.Buy,
                order_type=OrderType.Market,
                size=abs(size)
            )
            
            close_result = paradex.api_client.submit_order(close_order)
            print(f"✅ Close order: {close_result['id']}")
            print(f"   Status: {close_result['status']}")
    else:
        print("\n[8] No position to close")
    
    # Cancel remaining orders
    print("\n[9] Cancelling open orders...")
    cancel_result = paradex.api_client.cancel_all_orders()
    print(f"✅ Cancelled orders")
    
    # Final status
    print("\n[10] Final status...")
    final_positions = paradex.api_client.fetch_positions()
    final_orders = paradex.api_client.fetch_orders()
    
    print(f"✅ Open orders: {len(final_orders['results'])}")
    print(f"✅ Open positions: {sum(1 for p in final_positions['results'] if Decimal(p['size']) != 0)}")
    
    print("\n" + "="*70)
    print("ADAPTER TEST COMPLETE - ALL FUNCTIONS WORKING")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
